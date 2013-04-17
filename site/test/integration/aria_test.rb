require File.expand_path('../../test_helper', __FILE__)

class AriaIntegrationTest < ActionDispatch::IntegrationTest

  setup { omit_if_aria_is_unavailable }

  test 'should correctly handle sessions' do
    user = Aria::UserContext.new(WebUser.new :rhlogin => new_uuid)

    assert_nil user.destroy_session

    assert_raise(Aria::AuthenticationError){ user.create_session }
    assert_nil user.destroy_session

    assert billing_info = Aria::BillingInfo.test
    assert contact_info = Aria::ContactInfo.from_billing_info(billing_info)
    assert user.create_account( :billing_info => billing_info, :contact_info => contact_info )

    assert s = user.create_session
    assert s.length > 0

    assert_nil user.destroy_session
    assert_nil user.destroy_session
  end

  test 'should correctly create and validate a simple user' do
    user = Aria::UserContext.new(WebUser.new :rhlogin => new_uuid)

    assert !user.has_valid_account?
    assert !user.send(:has_account?)

    assert billing_info = Aria::BillingInfo.test
    assert contact_info = Aria::ContactInfo.from_billing_info(billing_info)
    assert user.create_account( :billing_info => billing_info, :contact_info => contact_info )
    assert user.errors.empty?

    assert_equal 'Y', Aria.get_acct_details_all(user.acct_no).is_test_acct
    assert_equal user.rhlogin, Aria.get_supp_field_value(user.acct_no, :rhlogin)

    assert user.has_valid_account?
    assert user.send(:has_account?)
  end

  test 'should set bill day correctly' do
    user = Aria::UserContext.new(WebUser.new :rhlogin => new_uuid)
    assert billing_info = Aria::BillingInfo.test
    assert contact_info = Aria::ContactInfo.from_billing_info(billing_info)
    assert user.create_account( :billing_info => billing_info, :contact_info => contact_info )
    assert user.errors.empty?
    assert_equal '1', user.account_details.bill_day, "A new user's bill_day is not 1. Make sure 'Perform Prorated Initial Invoicing Upon Account Creation' is set to false in Aria"
  end

  test 'should set and update billing info' do
    user = Aria::UserContext.new(WebUser.new :rhlogin => new_uuid)
    user_eur = Aria::UserContext.new(WebUser.new :rhlogin => new_uuid)
    user_cad = Aria::UserContext.new(WebUser.new :rhlogin => new_uuid)

    methods = Aria::BillingInfo.generated_attribute_methods.instance_methods

    info = Aria::BillingInfo.new

    #
    # user
    #
    # create US account
    methods.each {|m| info.send(m, ::SecureRandom.base64(5)) if m.to_s.ends_with?('=') }
    info.country = 'US'
    info.zip = 12345.to_s
    info.region = 'TX'
    info.middle_initial = 'P'

    assert contact_info = Aria::ContactInfo.from_billing_info(info)
    assert user.create_account(:billing_info => info, :contact_info => contact_info), user.errors.inspect
    assert_equal info.attributes, user.billing_info.attributes
    assert_equal 'usd', user.currency_cd
    assert_equal Rails.configuration.aria_invoice_template_id_map['US'], user.account_details.alt_msg_template_no.to_s

    # update to Canadian address
    info.country = 'CA'
    info.zip = 'K1A0B1'
    info.region = 'ON'
    info.middle_initial = 'M'
    assert user.update_account(:billing_info => info), user.errors.inspect
    assert_equal info.attributes, user.billing_info.attributes
    assert_equal 'usd', user.currency_cd
    assert_equal Rails.configuration.aria_invoice_template_id_map['US'], user.account_details.alt_msg_template_no.to_s

    # update to French address, unset some optional fields
    info.country = 'FR'
    info.zip = 54321.to_s
    info.region = 'Loraine'
    info.middle_initial = info.address2 = "" # Unset some fields using an empty string
    expected_attributes = Hash[info.attributes.map {|(k,v)| [k, v == "" ? nil : v] }]
    info.address3 = nil # Set some fields to nil, meaning "preserve existing value"
    assert user.update_account(:billing_info => info), user.errors.inspect
    # Ensure all unset fields go to nil in Aria
    info.middle_initial = info.address2 = nil
    assert_equal expected_attributes, user.billing_info.attributes
    assert_equal 'usd', user.currency_cd
    assert_equal Rails.configuration.aria_invoice_template_id_map['US'], user.account_details.alt_msg_template_no.to_s

    #
    # user_eur
    #
    # create new French account
    methods.each {|m| info.send(m, ::SecureRandom.base64(5)) if m.to_s.ends_with?('=') }
    info.country = 'FR'
    info.zip = 54321.to_s
    info.region = 'Loraine'
    info.middle_initial = 'P'
    assert contact_info = Aria::ContactInfo.from_billing_info(info)
    assert user_eur.create_account(:billing_info => info, :contact_info => contact_info), user_eur.errors.inspect
    assert_equal info.attributes, user_eur.billing_info.attributes
    assert_equal 'eur', user_eur.currency_cd
    assert_equal Rails.configuration.aria_invoice_template_id_map['FR'], user_eur.account_details.alt_msg_template_no.to_s

    #
    # user_cad
    #
    # create new French account
    methods.each {|m| info.send(m, ::SecureRandom.base64(5)) if m.to_s.ends_with?('=') }
    info.country = 'CA'
    info.zip = 'K1A0B1'
    info.region = 'ON'
    info.middle_initial = 'P'
    assert contact_info = Aria::ContactInfo.from_billing_info(info)
    assert user_cad.create_account(:billing_info => info, :contact_info => contact_info), user_cad.errors.inspect
    assert_equal info.attributes, user_cad.billing_info.attributes
    assert_equal 'cad', user_cad.currency_cd
    assert_equal Rails.configuration.aria_invoice_template_id_map['CA'], user_cad.account_details.alt_msg_template_no.to_s
  end

  test 'should set direct post settings' do
    set = Aria::DirectPost.create('testplan', "https://example.com")

    params = Aria.get_reg_uss_config_params("direct_post_#{set}")
    assert_equal({
      'redirecturl' => 'https://example.com',
      'do_cc_auth' => '1',
      'min_auth_threshold' => '0',
      'change_status_on_cc_auth_success' => '1',
      'status_on_cc_auth_success' => '1',
      'change_status_on_cc_auth_failure' => '1',
      'status_on_cc_auth_failure' => '-1',
    }, params)

    Aria::DirectPost.destroy(set)

    assert Aria.get_reg_uss_config_params("direct_post_#{set}").empty?
  end

  test 'should get plan details' do
    assert plans = Aria.get_client_plans_basic
    assert plans.length > 0
    assert plan = plans[0]
    assert plan.plan_no.is_a? Fixnum
    assert plan.plan_name
    assert_raise(NoMethodError){ plan.not_an_attribute }

    assert r = Aria.get_client_plans_basic_raw
    assert r.data
    assert r.data.plans_basic.length > 0

    assert p = plans.find{ |p| p.plan_no == Aria.default_plan_no }
    assert p['plan_name'] =~ /free/i, p.inspect
  end

  test 'should raise when missing parameter' do
    assert_raise(Aria::MissingRequiredParameter){ Aria.get_acct_comments }
  end

  test 'should raise when method does not exist' do
    assert_raise(Aria::InvalidMethod){ Aria.get_not_a_real_method }
  end

  test 'should provide combined master plans' do
    assert plans = Aria::MasterPlan.all
    assert plans.length > 0
    assert plan = plans[0]
    assert plan.description.is_a? String
    assert plan.max_gears.is_a? Fixnum
    assert plan.gear_sizes.kind_of? Array
    assert plan.gear_sizes.length > 0
  end

  test "should have an anniversary date of day 1" do
    u = with_account_holder
    assert_equal u.account_details.bill_day, "1"
  end

  test "should record usage" do
    u = with_account_holder
    assert_difference 'Aria.get_usage_history(u.acct_no, :date_range_start => u.account_details.last_arrears_bill_thru_date).count', 2 do
      record_usage_for_user(u)
    end
    assert usage = Aria.get_unbilled_usage_summary(u.acct_no)
    assert usage.ptd_balance_amount > 0
    assert_equal 'usd', usage.currency_cd

    assert u.unbilled_usage_line_items.present?
    assert_equal usage.ptd_balance_amount, u.unbilled_usage_balance
    assert_equal u.unbilled_usage_balance.round(2), u.unbilled_usage_line_items.map(&:total_cost).sum.round(2)
  end

  #
  # 'aaa' is a user with an unpaid invoice that has usage records.
  #
  test "should calculate total cost for usage record from an unpaid invoice" do
    user = Aria::UserContext.new(WebUser.new :rhlogin => 'aaa')
    assert user.next_bill.line_items.map(&:total_cost), "The user 'aaa' must have an unbilled line item"
  end

  test "should get past invoices" do
    u = record_usage_for_user(with_account_holder)
    assert invoices = u.invoices
    assert invoices.length > 0
  end

  test "should get past invoice line items" do
    u = record_usage_for_user(with_account_holder)
    assert invoices = u.invoices
    assert invoices.length > 0
    assert line_items = invoices.first.line_items
    assert line_items.length > 0
  end

  test "should get a next bill" do
    u = record_usage_for_user(with_account_holder)
    assert bill = u.next_bill
    assert bill.due_date > bill.end_date
    assert bill.start_date <= Aria::DateTime.today.to_datetime
    assert bill.line_items.present?
    assert bill.line_items.select(&:recurring?).present?
    assert bill.line_items.select(&:usage?).present?
    assert bill.balance > 0
    assert bill.estimated_balance > 0
  end

  test "should get recurring line items from plans" do
    assert items = Aria::RecurringLineItem.find_all_by_plan_no(Aria::MasterPlan.find('silver').plan_no)
    assert items.length == 1
    assert_equal "Plan: Silver", items[0].name
    assert_equal 42, items[0].amount
    assert_equal 42, items[0].total_cost
    assert !items[0].prorated?
    assert_equal 1.0, items[0].units

    assert items = Aria::RecurringLineItem.find_all_by_plan_no(Aria::MasterPlan.find('free').plan_no)
    assert items.empty?
  end
end
