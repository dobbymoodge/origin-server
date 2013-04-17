class ActiveSupport::TestCase
  def with_account_holder
    @@account_holder ||= begin
      Aria::UserContext.new(WebUser.new({
        :email_address=> "openshift_test_account_perm_1",
        :rhlogin=>       "openshift_test_account_perm_1",
        :ticket => '1'
      })).tap do |u|
        begin
          create_silver_user(u)
          record_usage_for_user(u)
        rescue Aria::AccountExists
        end
        u.account_details
      end
    end
    set_user(@@account_holder.dup)
  end

  def omit_if_aria_is_unavailable
    omit("Aria not available; omitting test.") unless Aria.available?
  end

  def create_silver_user(u)
    billing_info = Aria::BillingInfo.test
    contact_info = Aria::ContactInfo.from_billing_info(billing_info)
    assert u.create_account :billing_info => billing_info,
                            :contact_info => contact_info,
                            :payment_method => Aria::PaymentMethod.test,
                            :test_acct_ind => 0,
                            :status_cd => 1
    User.find(:one, :as => u).tap{ |a| a.plan_id = :silver; assert a.save }
  end

  def record_usage_for_user(u, small_usage=10, medium_usage=5, usage_date=nil)
    p = Aria::MasterPlan.find 'silver'
    assert s = Aria.get_client_plan_services(p.plan_no).find{ |s| s.client_coa_code == 'usage_gear_small' }
    assert m = Aria.get_client_plan_services(p.plan_no).find{ |s| s.client_coa_code == 'usage_gear_medium' }
    Aria.record_usage(u.acct_no, s.usage_type, small_usage, {:comments => "Test small gear hours usage", :usage_date => usage_date})
    Aria.record_usage(u.acct_no, m.usage_type, medium_usage, {:comments => "Test medium gear hours usage", :usage_date => usage_date})
    u.clear_cache!
    u
  end

  def create_user_id(tag, prefix="jtl-")
    id = "#{prefix}#{tag.gsub(/[^a-z0-9]+/i, '-')}-#{Time.now.strftime("%Y%m%d-%H%M%S")}"
    puts id
    id
  end
end
