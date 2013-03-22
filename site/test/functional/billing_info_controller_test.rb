require File.expand_path('../../test_helper', __FILE__)

class BillingInfoControllerTest < ActionController::TestCase
  test "should provide billing info on edit" do
    omit_if_aria_is_unavailable
    with_account_holder
    get :edit
    assert_response :success
    assert_not_nil assigns(:billing_info)
  end

  test "update should return to account page if no validation errors" do
    omit_if_aria_is_unavailable
    with_account_holder
    aria_billing_info = Aria::BillingInfo.test.attributes
    Aria::UserContext.any_instance.expects(:update_account).returns(true)
    post :update, :aria_billing_info => aria_billing_info
    assert_redirected_to account_path
  end

  test "update should return to edit page if validation errors" do
    omit_if_aria_is_unavailable
    with_account_holder
    aria_billing_info = Aria::BillingInfo.test.attributes
    Aria::UserContext.any_instance.expects(:update_account).returns(false)
    post :update, :aria_billing_info => aria_billing_info
    assert_template :edit
  end

  test "update should return to edit page if length validation errors" do
    omit_if_aria_is_unavailable
    with_account_holder
    aria_billing_info = Aria::BillingInfo.test.attributes
    aria_billing_info['middle_initial'] = 'ABC'
    Aria.expects(:update_acct_complete).never()
    post :update, :aria_billing_info => aria_billing_info
    assert assigns(:billing_info)
    assert assigns(:billing_info).errors[:middle_initial].length > 0
    assert_template :edit
  end

  test "should provide account path" do
    assert_equal account_path, @controller.next_path
    assert_equal account_path, @controller.previous_path
  end
end
