class AccountUpgradesController < ConsoleController
  include BillingAware

  before_filter :authenticate_user!, :except => :show
  before_filter :authenticate_user_for_upgrade!, :only => :show
  before_filter :user_can_upgrade_plan!
  before_filter :aria_account_is_not_terminated!
  before_filter :account_in_supported_country!, :only => [:new, :create, :edit]

  rescue_from Aria::Error do |e|
    @message = case e
      when Aria::UserIdCollision; "Your account encountered a problem during the create account step.  Please contact technical support about the error: IDCOLLISION."
      when Aria::UserNoRHLogin; "Your account is not properly configured.  Please contact technical support about the error: MISSING_RHLOGIN(#{current_user.rhlogin})."
      when Aria::AuthenticationError; "Unable to authenticate to the Aria service."
      end
    render :error
  end

  def new
    @billing_info = current_aria_user.billing_info
    @payment_method = current_aria_user.payment_method
    @plan = Aria::MasterPlan.cached.find(params[:plan_id])
    @user = User.find :one, :as => current_user
    @current_plan = @user.plan

    render :unchanged and return if @plan == @current_plan
    render :downgrade and return if @plan.basic?
    render :change and return unless @current_plan.basic?
  end

  def create
    @billing_info = current_aria_user.billing_info
    @payment_method = current_aria_user.payment_method
    @plan = Aria::MasterPlan.cached.find(params[:plan_id])
    @user = User.find :one, :as => current_user
    @current_plan = @user.plan

    @user.plan_id = params[:plan_id]

    unless @payment_method.persisted? and @billing_info.persisted?
      @user.errors[:base] = "You must provide a method of payment and billing address for this account."
      render :new and return
    end

    if @user.save
      current_aria_user.clear_cache!
      if @current_plan.basic? and !@plan.basic?
        @google_conversion_label = "VerYCLiZ3gQQqKqa4AM"
        render :upgraded and return
      end
      redirect_to account_path, ({:flash => {:info => "Plan changed to #{@plan.name}"}} if @plan.id != @current_plan.id) || {}
    else
      render :unchanged and return if @plan == @current_plan
      render :downgrade and return if @plan.basic?
      render :change and return unless @current_plan.basic?
      render :new
    end
  end

  def show
    user = current_user
    user.streamline_type!

    redirect_to edit_account_plan_upgrade_path and return unless current_aria_user.full_user? && current_aria_user.has_complete_account?
    redirect_to account_plan_upgrade_payment_method_path and return unless current_aria_user.has_valid_payment_method?
    redirect_to new_account_plan_upgrade_path
  end

  def edit
    @billing_info = current_aria_user.billing_info
    @payment_method = current_aria_user.payment_method
    @full_user = current_aria_user.full_user
    @full_user = Streamline::FullUser.test if !@full_user.persisted? && Rails.env.development?

    if @full_user.persisted?
      @show_vat = Aria::ContactInfo.from_full_user(@full_user).vies_country.present?
    else
      @show_vat = Rails.configuration.vies_countries.present? ? :dynamic : false
    end

    copy_user_to_billing(@full_user, @billing_info) unless @billing_info.persisted?
  end

  def update
    user_params = params[:streamline_full_user]
    email = current_aria_user.email_address || current_aria_user.load_email_address
    @billing_info = Aria::BillingInfo.new(user_params[:aria_billing_info], current_aria_user.has_account?)
    @billing_info.email = email

    user = current_user
    @full_user = user.full_user

    # Attempt to promote the streamline user to a full streamline user
    # if they aren't already
    if @full_user.persisted?
      @contact_info = Aria::ContactInfo.from_full_user(@full_user)
      @contact_info.email = email
      # Tell the billing info how to validate the taxpayer id
      @billing_info.vies_country = @contact_info.vies_country
      # Set in case we show :edit again
      @show_vat = @contact_info.vies_country.present?
    else
      @contact_info = Aria::ContactInfo.from_billing_info(@billing_info)
      @contact_info.email = email
      # Tell the billing info how to validate the taxpayer id
      @billing_info.vies_country = @contact_info.vies_country
      # Set in case we show :edit again
      @show_vat = Rails.configuration.vies_countries.present? ? :dynamic : false

      @full_user = Streamline::FullUser.new(
        {:postal_code => user_params[:aria_billing_info][:zip], :state => user_params[:aria_billing_info][:region]}.
        merge!(user_params[:streamline_full_user]).
        merge!(user_params[:aria_billing_info].slice(:address1, :address2, :address3, :city, :country))
      )

      # Validate first before promoting, so we don't lock bad values in streamline
      render :edit and return unless @billing_info.valid? and @contact_info.valid?

      render :edit and return unless @full_user.promote(user)
    end

    current_user_changed!
    
    if current_aria_user.has_account?
      # This is definitely an update scenario
      render :edit and return unless current_aria_user.update_account(:billing_info => @billing_info)
    else
      # This may or may not be an update scenario; try creating first.
      begin
        render :edit and return unless current_aria_user.create_account(:billing_info => @billing_info, :contact_info => @contact_info)
      rescue Aria::AccountExists
        render :edit and return unless current_aria_user.update_account(:billing_info => @billing_info)
      end
    end

    redirect_to account_plan_upgrade_payment_method_path and return unless current_aria_user.has_valid_payment_method?
    redirect_to new_account_plan_upgrade_path
  end

  protected
    def authenticate_user_for_upgrade!
      redirect_to login_or_signup_path(account_plan_upgrade_path) unless user_signed_in?
    end

    def account_in_supported_country!
      # If the user already has an Aria account, we do not prevent their access to billing
      return if current_aria_user.has_account?

      @full_user = current_aria_user.full_user
      if @full_user.persisted?
        @contact_info = Aria::ContactInfo.from_full_user(@full_user)
        render :no_upgrade and return false if @contact_info.country.blank? or not Rails.configuration.allowed_countries.include?(@contact_info.country.to_sym)
      end
    end

    def copy_user_to_billing(full_user, billing)
      # Here we must also transform between postal_code (FullUser) and zip (Aria)
      [:first_name, :last_name,
       :address1, :address2, :address3,
       :city, :state, :country, :postal_code
      ].each do |s|
        attr = case s
               when :postal_code
                 :zip
               when :state
                 :region
               else
                 s
               end
        billing.send(:"#{attr}=", full_user.send(s))
      end
      billing
    end

    def active_tab
      :account
    end
end
