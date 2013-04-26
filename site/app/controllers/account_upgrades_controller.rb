class AccountUpgradesController < ConsoleController
  include BillingAware

  before_filter :authenticate_user!, :except => :show
  before_filter :authenticate_user_for_upgrade!, :only => :show
  before_filter :user_can_upgrade_plan!

  # These filters set the user, aria, plan, etc instance variables
  before_filter :streamline_type, :only => :show
  before_filter :aria_user, :only => [:new, :create, :edit, :update]
  before_filter :plan, :only => [:new, :create]
  before_filter :billing_info, :only => [:new, :create, :edit]
  before_filter :payment_method, :only => [:new, :create, :edit]
  before_filter :process_async

  before_filter :streamline_account_in_supported_country!, :only => [:new, :create, :edit]

  rescue_from Aria::Error do |e|
    @message = case e
      when Aria::UserIdCollision; "Your account encountered a problem during the create account step.  Please contact technical support about the error: IDCOLLISION."
      when Aria::UserNoRHLogin; "Your account is not properly configured.  Please contact technical support about the error: MISSING_RHLOGIN(#{current_user.rhlogin})."
      when Aria::AuthenticationError; "Unable to authenticate to the Aria service."
      end
    render :error
  end

  def new
    render :unchanged and return if @plan == @current_plan
    render :downgrade and return if @plan.basic?
    render :change and return unless @current_plan.basic?
  end

  def create
    @user.plan_id = params[:plan_id]

    unless @payment_method.persisted? and @billing_info.persisted?
      @user.errors[:base] = "You must provide a method of payment and billing address for this account."
      render :new and return
    end

    if @user.save
      render :upgraded and return if (@current_plan.basic? and !@plan.basic?)
      redirect_to account_path, ({:flash => {:info => "Plan changed to #{@plan.name}"}} if @plan.id != @current_plan.id)
    else
      render :unchanged and return if @plan == @current_plan
      render :downgrade and return if @plan.basic?
      render :change and return unless @current_plan.basic?
      render :new
    end
  end

  def show
    redirect_to edit_account_plan_upgrade_path and return unless @aria_user.full_user? && @aria_user.has_complete_account?
    redirect_to account_plan_upgrade_payment_method_path and return unless @aria_user.has_valid_payment_method?
    redirect_to new_account_plan_upgrade_path
  end

  def edit
    @full_user = @aria_user.full_user
    @full_user = Streamline::FullUser.test if !@full_user.persisted? && Rails.env.development?

    copy_user_to_billing(@full_user, @billing_info) unless @billing_info.persisted?
  end

  def update
    user_params = params[:streamline_full_user]
    @billing_info = Aria::BillingInfo.new(user_params[:aria_billing_info], @aria_user.has_account?)
    user = current_user
    @full_user = user.full_user

    # Attempt to promote the streamline user to a full streamline user
    # if they aren't already
    if @full_user.persisted?
      @contact_info = Aria::ContactInfo.from_full_user(@full_user)
    else
      @contact_info = Aria::ContactInfo.from_billing_info(@billing_info)

      @full_user = Streamline::FullUser.new(
        {:postal_code => user_params[:aria_billing_info][:zip]}.
        merge!(user_params[:streamline_full_user]).
        merge!(user_params[:aria_billing_info].slice(:address1, :address2, :address3, :city, :region, :country))
      )

      render :edit and return unless @full_user.promote(user)
    end

    current_user_changed!
    process_async(:aria_user => current_user)

    email = begin
      current_user.email_address || current_user.load_email_address
    rescue
    end

    begin
      render :edit and return unless @aria_user.create_account(:billing_info => @billing_info, :contact_info => @contact_info, :email => email, :bill_email => email )
    rescue Aria::AccountExists
      render :edit and return unless @aria_user.update_account(:billing_info => @billing_info)
    end

    redirect_to account_plan_upgrade_payment_method_path and return unless @aria_user.has_valid_payment_method?
    redirect_to new_account_plan_upgrade_path
  end

  protected
    def authenticate_user_for_upgrade!
      redirect_to login_or_signup_path(account_plan_upgrade_path) unless user_signed_in?
    end

    def streamline_account_in_supported_country!
      @full_user = @aria_user.full_user
      if @full_user.persisted?
        @contact_info = Aria::ContactInfo.from_full_user(@full_user)
        render :no_upgrade and return false unless @contact_info.country.nil? or @contact_info.country.blank? or Rails.configuration.allowed_countries.include?(@contact_info.country.to_sym)
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
