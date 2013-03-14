class BillingInfoController < ConsoleController
  include BillingAware

  before_filter :authenticate_user!
  before_filter :user_can_upgrade_plan!

  def edit
    @billing_info = Aria::UserContext.new(current_user).billing_info
  end

  def update
    user = Aria::UserContext.new(current_user)
    @billing_info = Aria::BillingInfo.new params[:aria_billing_info]
    render :edit and return unless user.update_account(:billing_info => @billing_info)
    redirect_to next_path
  end

  def next_path
    account_path
  end
  def previous_path
    next_path
  end

  protected
    def active_tab
      :account
    end
end
