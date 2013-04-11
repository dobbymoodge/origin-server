require File.expand_path('../../test_helper', __FILE__)

class AccountUpgradePaymentMethodControllerTest < ActionController::TestCase

  setup { omit_if_aria_is_unavailable }

  test "should display payment method errors when creating" do
    with_account_holder
    get :new, :plan_id => :silver, :payment_method => {:errors => {:base => 'foo', :cvv => 'servercvvmustbenumeric'}}
    assert_response :success
    assert_select ".alert.alert-error", /payment information could not be processed/
    assert_select "#aria_payment_method_cvv_input.error .help-inline", /security code is a three or four digit/
  end

  test "should display payment method errors on edit" do
    with_account_holder
    get :edit, :plan_id => :silver, :payment_method => {:errors => {:base => 'foo', :cvv => 'servercvvmustbenumeric'}}
    assert_response :success
    assert_select ".alert.alert-error", /payment information could not be processed/
    assert_select "#aria_payment_method_cvv_input.error .help-inline", /security code is a three or four digit/
  end

  test "should redirect when aria reports success" do
    with_account_holder
    Aria::UserContext.any_instance.expects(:has_valid_payment_method?).returns(true)
    get :direct_update, :plan_id => :silver
    assert_redirected_to account_plan_upgrade_path
  end

  test "should redirect when aria reports an error" do
    with_account_holder
    Aria::UserContext.any_instance.expects(:has_valid_payment_method?).returns(true)
    get(:direct_create, {:plan_id => :silver, :error_messages => {
      0 => {
        :error_field => 'server_error',
        :error_key => 'serveraccountdetails'
      },
      1 => {
        :error_field => 'cc_no',
        :error_key => 'servercardnumnumeric'
      }
    }})
    assert_redirected_to new_account_plan_upgrade_payment_method_path({:payment_method => {:errors => {:base => ['serveraccountdetails'], :cc_no => ['servercardnumnumeric']}}})
  end
end
