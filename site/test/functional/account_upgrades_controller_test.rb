require File.expand_path('../../test_helper', __FILE__)

class AccountUpgradesControllerTest < ActionController::TestCase

  def plan
    {:plan_id => :silver}
  end
  def with_user(user)
    @user ||= begin
      @controller.expects(:current_user).at_least_once.returns(user)
      set_user(user)
    end
  end
  def simple
    WebUser.new :rhlogin => 'outside_user@gmail.com', :email_address => 'outside_user@gmail.com', :streamline_type => :full
  end
  def full
    WebUser.new :rhlogin => 'rhnuser', :email_address => 'rhnuser@redhat.com', :streamline_type => :full
  end

  setup { omit_if_aria_is_unavailable }

  test "should show an unchanged plan when the current plan matches the new one" do
    user = with_user(full)
    get :new, :plan_id => 'free'
    assert_not_nil assigns[:user]
    assert_not_nil assigns[:plan]
    assert_not_nil assigns[:current_plan]
    assert_not_nil assigns[:payment_method]
    assert_not_nil assigns[:billing_info]
    assert_template :unchanged
  end

  test "should upgrade a full user in streamline" do
    with_confirmed_user
    put :update,
      :plan_id => 'silver',
      :streamline_full_user => {
        :streamline_full_user => {
          :first_name => 'Bob',
          :last_name => 'Smith',
          :email_subscribe => false,
          :phone_number => '9191110000',
          :greeting => 'Mr.',
          :title => 'Engineer',
          :company => 'Red Hat Test',
          :password => 'aoeuaoeu',
          :password_confirmation => 'aoeuaoeu',
        },
        :aria_billing_info => {
          :first_name => 'Bob',
          :last_name => 'Smith',
          :city => 'Lund',
          :region => 'Scania',
          :country => 'SE',
          :address1 => '10 Adelgatan',
          :zip => '223309',
        }
      }

    assert full_user = assigns[:full_user]
    assert billing_info = assigns[:billing_info]
    assert !billing_info.persisted? # Existing behavior

    aria_user = Aria::UserContext.new(@user)
    assert aria_user.has_valid_account?
    assert aria_user.has_complete_account?
    assert aria_user.billing_info.persisted?
    assert_equal 'eur', aria_user.currency_cd

    assert_equal :full, session[:streamline_type]
    assert_redirected_to account_plan_upgrade_payment_method_path
  end

  test "should redirect if the user lacks capabilities" do
    user = with_user(full)
    OnlineCapabilities.any_instance.expects(:plan_upgrade_enabled?).returns(false)
    get :new, :plan_id => 'free'
    assert_redirected_to account_path
  end

  test "should raise on invalid user" do
    user = with_user(full)
    Aria::UserContext.any_instance.expects(:has_complete_account?).raises(Aria::UserIdCollision.new(1))
    get :show, plan
    assert_response :success
    assert m = assigns(:message)
    assert m =~ /IDCOLLISION/, "Message was '#{m}'"
  end

  test "should make a copy of billing info for editing" do
    user = with_confirmed_user
    # We are testing #edit; calling #new forces necessary before_filter calls to run
    get :new, :plan_id => 'free'
    @controller.edit
    assert_not_nil assigns[:full_user]
    assert_not_nil assigns[:billing_info]
  end

  test "should prevent users from seeing :new if their RHN account is in an unsupported country" do
    user = with_user(full)
    Aria::ContactInfo.any_instance.expects(:country).at_least_once.returns('JP')

    get :new, :plan_id => 'free'
    assert_template :no_upgrade
  end

  test "should prevent users from seeing :create if their RHN account is in an unsupported country" do
    user = with_user(full)
    Aria::ContactInfo.any_instance.expects(:country).at_least_once.returns('JP')

    get :create
    assert_template :no_upgrade
  end

  test "should prevent users from seeing :edit if their RHN account is in an unsupported country" do
    user = with_user(full)
    Aria::ContactInfo.any_instance.expects(:country).at_least_once.returns('JP')

    get :edit
    assert_template :no_upgrade
  end
end
