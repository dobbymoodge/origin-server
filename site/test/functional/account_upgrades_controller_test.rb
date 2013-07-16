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

  with_aria

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

  test "should validate vat before upgrading streamline" do
    with_confirmed_user

    # Try to save a valid IE VAT with a DE address
    Aria::UserContext.any_instance.expects(:create_account).never
    Streamline::FullUser.any_instance.expects(:promote).never

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
          :country => 'DE',
          :address1 => '10 Adelgatan',
          :zip => '223309',
          :taxpayer_id => 'IE6388047V',
        }
      }

    # Make sure we got the right error
    assert_response :success
    assert_template :edit
    assert full_user = assigns[:full_user]
    assert billing_info = assigns[:billing_info]
    assert_equal 1, billing_info.errors[:taxpayer_id].length, billing_info.errors.inspect
  end

  test "should validate vat and upgrade streamline" do
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
          :country => 'IE',
          :address1 => '10 Adelgatan',
          :zip => '223309',
          :taxpayer_id => 'IE6388047V',
        }
      }

    aria_user = Aria::UserContext.new(@user)
    assert aria_user.has_valid_account?
    assert aria_user.has_complete_account?
    assert aria_user.billing_info.persisted?
    assert_equal 'eur', aria_user.currency_cd
    assert_equal 'IE6388047V', aria_user.account_details.taxpayer_id
    assert aria_user.tax_exempt?

    assert_equal :full, session[:streamline_type]
    assert_redirected_to account_plan_upgrade_payment_method_path
  end  

  test "should upgrade a full user in streamline" do
    with_confirmed_user
    test_country = 'SE'
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
          :country => test_country,
          :address1 => '10 Adelgatan',
          :zip => '223309',
        }
      }

    assert full_user = assigns[:full_user]
    assert_not_nil full_user.state
    assert billing_info = assigns[:billing_info]
    assert !billing_info.persisted? # Existing behavior

    aria_user = Aria::UserContext.new(@user)
    assert aria_user.has_valid_account?
    assert aria_user.has_complete_account?
    assert aria_user.billing_info.persisted?
    assert_equal 'eur', aria_user.currency_cd
    assert_equal @user.email_address, aria_user.account_details.alt_email
    assert_equal @user.email_address, aria_user.account_details.billing_email

    assert config_collections_group_id = Rails.configuration.collections_group_id_by_country[test_country]
    assert config_functional_group_no = Rails.configuration.functional_group_no_by_country[test_country].to_i
    assert_equal config_functional_group_no, aria_user.account_details.seq_func_group_no
    assert aria_acct_groups = Aria.get_acct_groups_by_acct(aria_user.acct_no)
    assert aria_coll_groups = aria_acct_groups.select{ |g| g.group_type == 'C' }
    assert aria_func_groups = aria_acct_groups.select{ |g| g.group_type == 'F' }
    assert_equal 2, aria_acct_groups.count
    assert_equal 1, aria_coll_groups.count
    assert_equal 1, aria_func_groups.count
    assert_equal config_collections_group_id, aria_acct_groups[0].client_acct_group_id
    assert_equal config_functional_group_no, aria_func_groups[0].group_no.to_i

    assert_equal :full, session[:streamline_type]
    assert_redirected_to account_plan_upgrade_payment_method_path
  end

  test "should redirect if the user lacks capabilities" do
    user = with_user(full)
    OnlineCapabilities.any_instance.expects(:plan_upgrade_enabled?).returns(false)
    get :new, :plan_id => 'free'
    assert_redirected_to account_path
  end

  test "should redirect users with terminated aria accounts" do
    user = with_user(full)
    Aria::UserContext.any_instance.expects(:has_account?).at_least_once.returns(true)
    Aria::UserContext.any_instance.expects(:account_status).at_least_once.returns(:terminated)
    get :new, :plan_id => 'free'
    assert_redirected_to account_path
    get :show, plan
    assert_redirected_to account_path
    get :edit
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
    Aria::UserContext.any_instance.expects(:has_account?).at_least_once.returns(false)

    get :new, :plan_id => 'free'
    assert_template :no_upgrade
  end

  test "should prevent users from seeing :create if their RHN account is in an unsupported country" do
    user = with_user(full)
    Aria::ContactInfo.any_instance.expects(:country).at_least_once.returns('JP')
    Aria::UserContext.any_instance.expects(:has_account?).at_least_once.returns(false)

    get :create
    assert_template :no_upgrade
  end

  test "should prevent users from seeing :edit if their RHN account is in an unsupported country" do
    user = with_user(full)
    Aria::ContactInfo.any_instance.expects(:country).at_least_once.returns('JP')
    Aria::UserContext.any_instance.expects(:has_account?).at_least_once.returns(false)

    get :edit
    assert_template :no_upgrade
  end

  test "should always allow users to work with their plan if they already have an Aria account" do
    user = with_user(full)
    Aria::ContactInfo.any_instance.expects(:country).at_least_once.returns('JP')
    Aria::UserContext.any_instance.expects(:has_account?).at_least_once.returns(false)

    get :new, :plan_id => 'free'
    assert_template :no_upgrade

    Aria::UserContext.any_instance.expects(:has_account?).at_least_once.returns(true)

    get :new, :plan_id => 'free'
    assert_template :change
  end
end
