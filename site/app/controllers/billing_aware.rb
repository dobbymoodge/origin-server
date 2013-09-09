module BillingAware
  extend ActiveSupport::Concern

  included do
    include CapabilityAware
    helper_method :current_aria_user, :user_currency_cd, :user_can_upgrade_plan?, :user_on_basic_plan?
  end

  def current_aria_user
    @current_aria_user ||= Aria::UserContext.new(current_user)
  end

  # Must be public for use in application_helper.rb
  def user_currency_cd
    if session[:currency_cd].blank? and user_can_upgrade_plan?
      session[:currency_cd] = current_aria_user.has_account? ? current_aria_user.currency_cd : Rails.configuration.default_currency.to_s
    end
    session[:currency_cd] || Rails.configuration.default_currency.to_s
  end

  protected

    #
    # Is the current user authorized to upgrade their plan?  Will lazily
    # load and cache the capabilities for the user.
    #
    # This is unrelated to the user's payment method, status_cd, etc
    # It is only used as a gatekeeper to hide upgrade function prior to general release
    #
    def user_can_upgrade_plan?
      Rails.configuration.aria_enabled && current_user && user_capabilities.plan_upgrade_enabled?
    rescue => e
      logger.error "Unable to check plan: #{e.message}\n  #{e.backtrace.join("\n  ")}"
      false
    end

    def aria_account_is_not_terminated?
      user = current_aria_user
      user.has_account? ? user.account_status != :terminated : true
    end

    #
    # Is the user on the lowest plan tier?
    #
    def user_on_basic_plan?
      user_capabilities.plan_id == 'free'
    end

    #
    # Only users who can upgrade their plan can see the account upgrade flow
    #
    def user_can_upgrade_plan!
      redirect_to account_path unless user_can_upgrade_plan?
    end

    #
    # Users with terminated Aria accounts cannot see the account upgrade flow
    #
    def aria_account_is_not_terminated!
      redirect_to account_path unless aria_account_is_not_terminated?
    end

    #
    # Return the login path if the user has previously_signed_in? or the
    # new account path if not.
    #
    def login_or_signup_path(path)
      if previously_signed_in?
        login_path(:then => path)
      else
        new_account_path(:then => path)
      end
    end
end