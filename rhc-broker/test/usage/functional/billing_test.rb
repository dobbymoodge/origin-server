ENV["TEST_NAME"] = "usage_funtional_billing_test"
require 'test_helper'

class BillingTest < ActiveSupport::TestCase
  def setup
    # Create user locally first
    @user = CloudUser.new(login: "aria_testuser_#{gen_uuid[0..9]}")
    @user.save
    @user_id = Digest::MD5::hexdigest(@user.login)
    super
  end

  test "get account no from user id" do
    api = Express::AriaBilling::Api.instance
    acct_no = api.create_fake_acct(@user_id, :freeshift)
    assert_not_nil(acct_no, "account number is nil")
    acct_no_from_id = api.get_acct_no_from_user_id(@user_id)
    assert_equal(acct_no, acct_no_from_id, "Account no #{acct_no_from_id} expected #{acct_no}")
  end
  
  test "get account info" do
    api = Express::AriaBilling::Api.instance
    acct_no = api.create_fake_acct(@user_id, :freeshift)
    acct_info = api.get_acct_details_all(acct_no)
    assert_equal(acct_info["status_cd"], "1", "Account status #{acct_info["status_cd"]} expected 1")
    assert_equal(acct_info["userid"], @user_id, "Account userid #{acct_info["userid"]} expected #{@user_id}")
  end
  
  test "get plans" do
    api = Express::AriaBilling::Api.instance
    acct_no = api.create_fake_acct(@user_id, :freeshift)
    plans = api.get_acct_plans_all(acct_no)
    assert(plans.length == 1)
    current_plan = plans[0]
    assert_equal(current_plan["plan_name"], "FreeShift", "Current plan name #{current_plan["plan_name"]} expected FreeShift")
    assert_not_nil(current_plan["plan_no"], "plan_no is nil")
  end
  
  test "update account status" do
    api = Express::AriaBilling::Api.instance
    acct_no = api.create_fake_acct(@user_id, :freeshift)
    acct_info = api.get_acct_details_all(acct_no)
    assert_equal(acct_info["status_cd"], "1", "Account status #{acct_info["status_cd"]} expected 1")
    api.update_acct_status(acct_no, 0)
    acct_info = api.get_acct_details_all(acct_no)
    assert_equal(acct_info["status_cd"], "0", "Account status #{acct_info["status_cd"]} expected 0")
  end
  
  test "update master plan" do
    api = Express::AriaBilling::Api.instance
    acct_no = api.create_fake_acct(@user_id, :freeshift)
    plans = api.get_acct_plans_all(acct_no)
    assert(plans.length == 1)
    current_plan = plans[0]
    assert_equal(current_plan["plan_name"], "FreeShift", "Current plan name #{current_plan["plan_name"]} expected FreeShift")
    
    api.update_master_plan(acct_no, :megashift)
    
    plans = api.get_acct_plans_all(acct_no)
    assert(plans.length == 1)
    current_plan = plans[0]
    assert_equal(current_plan["plan_name"], "MegaShift", "Current plan name #{current_plan["plan_name"]} expected MegaShift")
  end
  
test "update master plan and then revert to previous" do
    api = Express::AriaBilling::Api.instance
    acct_no = api.create_fake_acct(@user_id, :freeshift)
    plans = api.get_acct_plans_all(acct_no)
    assert(plans.length == 1)
    current_plan = plans[0]
    assert_equal(current_plan["plan_name"], "FreeShift", "Current plan name #{current_plan["plan_name"]} expected FreeShift")
      
    api.update_master_plan(acct_no, :megashift)
      
    plans = api.get_acct_plans_all(acct_no)
    assert(plans.length == 1)
    current_plan = plans[0]
    assert_equal(current_plan["plan_name"], "MegaShift", "Current plan name #{current_plan["plan_name"]} expected MegaShift")
      
    api.update_master_plan(acct_no, :freeshift)
      
    plans = api.get_acct_plans_all(acct_no)
    assert(plans.length == 1)
    current_plan = plans[0]
    assert_equal(current_plan["plan_name"], "FreeShift", "Current plan name #{current_plan["plan_name"]} expected FreeShift")
  end
  
  test "update master plan to same plan" do
    api = Express::AriaBilling::Api.instance
    acct_no = api.create_fake_acct(@user_id, :megashift)
    plans = api.get_acct_plans_all(acct_no)
    assert(plans.length == 1)
    current_plan = plans[0]
    assert_equal(current_plan["plan_name"], "MegaShift", "Current plan name #{current_plan["plan_name"]} expected MegaShift")
      
    api.update_master_plan(acct_no, :megashift)
      
    plans = api.get_acct_plans_all(acct_no)
    assert(plans.length == 1)
    current_plan = plans[0]
    assert_equal(current_plan["plan_name"], "MegaShift", "Current plan name #{current_plan["plan_name"]} expected MegaShift")
  end

  def teardown
    @user.force_delete
  end
end
