# encoding: UTF-8

require File.expand_path('../../test_helper', __FILE__)

require 'aria'

#
# Mock tests only - should verify functionality of ActiveResource extensions
# and simple server/client interactions via HttpMock
#
class AriaUnitTest < ActiveSupport::TestCase
  uses_http_mock
  setup { WebMock.disable_net_connect! }
  setup{ Rails.cache.clear }
  teardown { WebMock.allow_net_connect! }

  def query_for(method, query=nil)
    config = Rails.application.config
    {
      :auth_key => config.aria_auth_key,
      :client_no => config.aria_client_no.to_s,
      :rest_call => method.nil? ? nil : method.to_s,
    }.merge(query || {})
  end

  def stub_aria(method=nil, params=nil, partial=false)
    r = stub_request(:post, Rails.application.config.aria_uri)
    q = query_for(method)
    q = hash_including(q) if partial
    r.with(:query => q, :body => params).with do |request|
      request.headers['User-Agent'] == Rails.configuration.user_agent
    end
  end
  def error_wddx(code, message, body={})
    {'error_code' => code, 'error_msg' => message}.merge(body).to_wddx
  end
  def ok_wddx(body={})
    error_wddx(0, 'Ok', body)
  end
  def resp(*args)
    opts = args.extract_options!
    {:status => 200, :body => args[0] || ok_wddx}.merge!(opts).merge!(:headers => {'Content-Type' => 'text/html;charset=UTF-8'}.merge(opts[:headers] || {}))
  end

  def stub_acct_details(acct_no, values)
    stub_aria(:get_acct_details_all, {
      :acct_no => acct_no.to_s
    }).to_return(resp(ok_wddx(values)))
  end

  def stub_queued_plans(acct_no, plans)
    stub_aria(:get_queued_service_plans, {
      :account_number => acct_no.to_s
    }).to_return(resp(ok_wddx({
      :queued_plans => plans,
    })))
  end

  def stub_acct_invoice_history(acct_no, invoices)
    stub_aria(:get_acct_invoice_history, {
      :acct_no => acct_no.to_s
    }).to_return(resp(ok_wddx({
      :invoice_history => invoices,
    })))
  end

  def stub_acct_plans_all(acct_no, plans)
    stub_aria(:get_acct_plans_all, {
      :acct_no => acct_no.to_s
    }).to_return(resp(ok_wddx({
      :all_acct_plans => plans,
    })))
  end

  def stub_client_plans_all(plans)
    stub_aria(:get_client_plans_all, {
    }).to_return(resp(ok_wddx({
      :all_client_plans => plans,
    })))
  end

  def stub_client_plans_basic(plans)
    stub_aria(:get_client_plans_basic, {
    }).to_return(resp(ok_wddx({
      :plans_basic => plans,
    })))
  end

  def stub_client_plan_services(plan_no, services)
    stub_aria(:get_client_plan_services, {
      :plan_no => plan_no.to_s
    }).to_return(resp(ok_wddx({
      :plan_services => services,
    })))
  end

  test 'should not respond to object or module methods on Aria' do
    Aria.expects(:client).never
    assert Aria.respond_to? :public_instance_methods
    assert Aria.to_s
  end

  test 'should not respond to object methods on client' do
    Aria::Client.expects(:post).never
    c = Aria::Client.new
    assert !c.respond_to?(:before_remove_const)
    assert c.respond_to?(:to_s)
    assert c.to_s
  end

  test 'should support indifferent access' do
    s = Aria::WDDX::Struct.new('foo' => 1, 'other' => nil)

    assert s.respond_to?('foo')
    assert s.respond_to?(:foo)
    assert s.respond_to?('other')
    assert s.respond_to?(:other)
    assert !s.respond_to?(:bar)
    assert !s.respond_to?('bar')
    assert s.respond_to?(:[])
    assert s.respond_to?(:[]=)

    assert_equal 1, s[:foo]
    assert_equal 1, s['foo']
    assert_equal 1, s.foo

    assert_nil s[:other]
    assert_nil s['other']
    assert_nil s.other

    assert_equal 2, (s[:foo] = 2)
    assert_equal 2, s.foo
    assert_equal 3, (s['foo'] = 3)
    assert_equal 3, s.foo
    assert_equal 4, (s.foo = 4)
    assert_equal 4, s.foo

    assert_equal 1, (s[:other] = 1)
    assert_equal 1, s.other
    assert_nil s[:other] = nil
    assert_nil s.other

    assert_equal 1, (s['other'] = 1)
    assert_equal 1, s.other
    s[:other] = nil

    assert_equal 1, (s.other = 1)
    assert_equal 1, s.other
    s[:other] = nil

    assert_raise(NoMethodError){ s.bar }
    assert_nil s['bar']
    assert_nil s[:bar]

    assert_raise(NoMethodError){ s.bar = 2 }
    assert_equal 2, (s['bar'] = 2)
    assert_nil s.send(:[]=, 'bar', 2)
    assert_nil s['bar']
    assert_equal 2, (s[:bar] = 2)
    assert_nil s.send(:[]=, :bar, 2)
    assert_nil s[:bar]
  end

  test 'should form a simple request' do
    stub_aria(:get_test).to_return(resp)

    assert !Aria.respond_to?(:get_test)

    assert r = Aria.get_test
    assert_equal 0, r['error_code']
    assert_equal 0, r.error_code
    assert_equal 'Ok', r['error_msg']
    assert_equal 'Ok', r.error_msg
  end

  test 'should query raw requests' do
    stub_aria(:get_test).to_return(resp)

    a = Aria
    a.expects(:get_test).never

    assert !a.respond_to?(:get_test_raw)
    assert r = a.get_test_raw
    assert_equal 200, r.code
    assert_equal 0, r.data['error_code']
    assert_equal 0, r.data.error_code
    assert_equal 'Ok', r.data['error_msg']
    assert_equal 'Ok', r.data.error_msg
  end

  test 'should yield response' do
    stub_aria(:get_test).to_return(resp)
    y = Aria.get_test do |data, r|
      assert data
      assert_equal 0, data.error_code
      assert_equal 200, r.code
      -3
    end
    assert_equal -3, y
  end

  test 'should raise generic' do
    stub_aria(:get_test).to_return(resp(error_wddx(1000,'Unknown')))
    e = assert_raise(Aria::Error){ Aria.get_test }
    assert_equal 'Unknown', e.data['error_msg']
    assert_equal 'Unknown', e.data[:error_msg]
    assert_equal 'Unknown', e.data.error_msg
    assert_equal 1000, e.code
    assert e.to_s =~ /\(1000\)/
  end

  test 'should have default_plan_no' do
    assert Aria.default_plan_no.is_a? Fixnum
    assert Aria.default_plan_no > 0
  end

  test 'should have client_no' do
    assert Aria.client_no.is_a? Fixnum
    assert Aria.client_no > 0
  end

  test 'should raise ParameterMissing' do
    stub_aria(:get_test).to_return(resp(error_wddx(1010,'Missing required parameter')))
    e = assert_raise(Aria::MissingRequiredParameter){ Aria.get_test }
    assert_equal 1010, e.code
    assert_equal 'Missing required parameter (1010)', e.to_s
  end

  test 'should raise unavailable on 503' do
    stub_aria(:get_test).to_return(:status => 503)
    e = assert_raise(Aria::NotAvailable){ Aria.get_test }
    assert_equal 503, e.response.code
  end

  test 'should raise unavailable on 404' do
    stub_aria(:get_test).to_return(:status => 404, :body => ' ')
    e = assert_raise(Aria::NotAvailable){ Aria.get_test }
    assert_equal 404, e.response.code
  end

  test 'should raise invalid method on 404' do
    stub_aria(:get_test).to_return(resp(error_wddx(-1, 'Not attempted'), :status => 404 ))
    e = assert_raise(Aria::InvalidMethod){ Aria.get_test }
  end

  class TestUser
    include ActiveModel::Validations
    include Aria::User
  end

  test 'should return false on create_account error' do
    user = TestUser.new
    user.expects(:login).returns('foo').at_least_once
    Aria.expects(:create_acct_complete).raises(Aria::AuthenticationError)
    assert billing_info = Aria::BillingInfo.test
    assert contact_info = Aria::ContactInfo.from_billing_info(billing_info)
    assert !user.create_account( :billing_info => billing_info, :contact_info => contact_info )
    assert user.errors.size == 1
    assert user.errors[:base][0] =~ /AuthenticationError/, user.errors.inspect
  end

  test 'should invoke create_acct_complete' do
    assert billing_info = Aria::BillingInfo.test
    assert contact_info = Aria::ContactInfo.from_billing_info(billing_info)

    api_args = {
      :supp_field_values => 'foo',
      :supp_field_names => 'rhlogin',
      :password => 'passw0rd',
      :alt_bill_day => 1.to_s,
      :test_acct_ind => 1.to_s,
      :status_cd => 0.to_s,
      :master_plan_no => Rails.application.config.aria_default_plan_no.to_s,
      :userid => Digest::MD5::hexdigest('foo'),
      :alt_msg_template_no => '111',
      :currency_cd => 'usd'
    }
    api_args.merge!(billing_info.to_aria_attributes)
    api_args.merge!(contact_info.to_aria_attributes)
    api_args[:client_coll_acct_group_ids] = Rails.application.config.collections_group_id_by_country[api_args['country']]
    stub_aria(:create_acct_complete, api_args).to_return(resp(ok_wddx))

    stub_aria(:get_acct_no_from_user_id, {
      :user_id => Digest::MD5::hexdigest('foo'),
    }).to_return(resp(ok_wddx({:acct_no => 123.to_s})))

    user = TestUser.new
    user.expects(:random_password).returns('passw0rd')
    user.expects(:login).returns('foo').at_least_once
    assert user.create_account( :billing_info => billing_info, :contact_info => contact_info )
    assert user.errors.empty?
  end

  # Temporary test case to accomodate Streamline bug. This should be removed when the
  # ContactInfo models is updated for correct enforcement.
  test 'should enable creation of ContactInfo without country' do
    full_user = Streamline::FullUser.test
    full_user.country = nil
    assert contact_info = Aria::ContactInfo.from_full_user(full_user)
    assert_equal nil, contact_info.country
    full_user.country = ''
    assert contact_info = Aria::ContactInfo.from_full_user(full_user)
    assert_equal '', contact_info.country
  end

  test 'get_acct_no_from_user_id is cacheable' do
    Aria::Client.any_instance.expects(:invoke).once.
      with(:get_acct_no_from_user_id, {:user_id => 'foo'}).
      returns(Aria::WDDX::Struct.new({'acct_no' => '1'}))
    assert_equal '1', Aria.cached.get_acct_no_from_user_id('foo')
    assert_equal '1', Aria.cached.get_acct_no_from_user_id('foo')
  end

  def mock_plans
    ActiveResource::HttpMock.respond_to do |mock|
      mock.get '/broker/rest/plans/free.json', anonymous_json_header, {:id => 'free', :plan_no => '1'}.to_json
      mock.get '/broker/rest/plans/silver.json', anonymous_json_header, {:id => 'silver', :plan_no => '2'}.to_json
    end
    Aria::Client.any_instance.expects(:invoke).once.
      with(:get_client_plans_basic).
      returns(Aria::WDDX::Struct.new({
        'plans_basic' => [
          Aria::WDDX::Struct.new({
            'plan_no' => '1',
            'plan_name' => 'Free',
            'plan_desc' => 'Free plan description'
          }),
          Aria::WDDX::Struct.new({
            'plan_no' => '2',
            'plan_name' => 'Silver',
            'plan_desc' => 'Silver plan description'
          })
        ]
      }))
  end

  test 'Aria::MasterPlan.find is cacheable' do
    mock_plans
    assert Aria.cached.get_client_plans_basic
    assert_equal 2, Aria.cached.get_client_plans_basic.length
    assert_equal 'Free', Aria::MasterPlan.cached.find('free').name
    assert_equal 'Free', Aria::MasterPlan.cached.find('free').name

    assert_equal 'Silver', Aria::MasterPlan.cached.find('silver').name
  end

  test 'Aria::MasterPlan can lazy load aria_plan with cache' do
    mock_plans
    base_plan = Aria::MasterPlan.cached.find('free')
    cached_plan = Aria::MasterPlan.cached.find('free')
    assert_equal 'Free', cached_plan.name
  end

  test 'should throw when non hash passed' do
    assert_raise(ArgumentError){ Aria.get_test 'hello' }
  end

  test 'billing info should init from billing details' do
    attr = Aria::WDDX::Struct.new({'billing' => 'a', 'billing_city' => 'Houston', 'billing_address1' => '1 test', 'other' => '2', 'billing_country' => 'US', 'billing_state' => 'TX', 'billing_locality' => 'Invalid'})
    assert info = Aria::BillingInfo.from_account_details(attr)
    assert info.persisted?
    assert_equal 'Houston', info.city
    assert_equal 'TX', info.region
    assert_equal({'city' => 'Houston', 'address1' => '1 test', 'region' => 'TX', 'country' => 'US'}, info.attributes)
    assert_equal({'bill_city' => 'Houston', 'bill_address1' => '1 test', 'bill_state_prov' => 'TX', 'bill_country' => 'US'}, info.to_aria_attributes)
    assert_equal({'bill_city' => 'Houston', 'bill_address1' => '1 test', 'bill_state_prov' => 'TX', 'bill_country' => 'US', 'bill_locality' => '~'}, info.to_aria_attributes('update'))

    info.address2 = ""
    assert_equal({'bill_city' => 'Houston', 'bill_address1' => '1 test', 'bill_state_prov' => 'TX', 'bill_country' => 'US', 'bill_address2' => ''}, info.to_aria_attributes)
    assert_equal({'bill_city' => 'Houston', 'bill_address1' => '1 test', 'bill_state_prov' => 'TX', 'bill_country' => 'US', 'bill_address2' => '~', 'bill_locality' => '~'}, info.to_aria_attributes('update'))
  end

  test 'billing info should serialize supplemental fields' do
    #info = Aria::BillingInfo.new
    #info.tax_exempt = 1
    #assert_equal({:supplemental => {'tax_exempt' => 1}}, info.to_aria_attributes)
  end

  test 'create_acct_complete should serialize supplemental fields' do
    base = Class.new(Object){ def create_acct_complete(*args) has(*args) end }
    a = Class.new(base){ include Aria::Methods }.new
    a.expects(:has).with({
      :supp_field_names => 'tax_exempt',
      :supp_field_values => '1',
    },nil)
    a.create_acct_complete({:supplemental => {'tax_exempt' => 1}})
  end

  test 'update_acct_complete should serialize supplemental fields' do
    base = Class.new(Object){ def update_acct_complete(*args) has(*args) end }
    a = Class.new(base){ include Aria::Methods }.new
    a.expects(:has).with({
      :acct_no => 1,
      :supp_field_names => 'tax_exempt',
      :supp_field_values => '1',
      :supp_field_directives => '2',
    },nil)
    a.update_acct_complete(1, {:supplemental => {'tax_exempt' => 1}})
  end

  test 'direct_post should not generate names when not configured' do
    Rails.configuration.expects(:aria_direct_post_name).at_least_once.returns(nil)
    assert_nil Aria::DirectPost.get_configured
    assert_nil Aria::DirectPost.get_configured('bar')
  end

  test 'direct_post should generate names when configured' do
    Rails.configuration.expects(:aria_direct_post_name).at_least_once.returns('foo')
    assert_equal 'foo', Aria::DirectPost.get_configured
    assert_equal 'foo_bar', Aria::DirectPost.get_configured('bar')
  end

  test 'payment_method should initialize from account details' do
    assert p = Aria::PaymentMethod.from_account_details(stub(
      :pay_method => '1',
      :attributes => {
        :cc_expire_mm => '10',
        :cc_expire_yyyy => '2015',
        :cc_suffix => '1111'
      }
    ))
    assert_equal '1111', p.cc_no
    assert_equal '10', p.cc_exp_mm
    assert_equal '2015', p.cc_exp_yyyy
    assert p.persisted?
  end

  test 'validates values for create account' do
    user = TestUser.new
    user.expects(:login).at_least_once.returns('foo')
    assert billing_info = Aria::BillingInfo.new
    assert contact_info = Aria::ContactInfo.from_billing_info(billing_info)
    assert !user.create_account( :billing_info => billing_info, :contact_info => contact_info )
    assert user.errors.empty?
    assert !billing_info.errors.empty?
  end

  test 'validates values for update account' do
    user = TestUser.new
    billing_info = Aria::BillingInfo.new
    assert !user.update_account(:billing_info => billing_info)
    assert user.errors.empty?
    assert !billing_info.errors.empty?
  end

  test 'payment_method is only persisted when account_details pay_method is 1' do
    assert p = Aria::PaymentMethod.from_account_details(stub(
      :pay_method => '0',
      :attributes => {
        :cc_expire_mm => '10',
        :cc_expire_yyyy => '2015',
        :cc_suffix => '1111'
      }
    ))
    assert !p.persisted?
  end

  test 'master plan adds aria plan details to broker plans' do
    Aria::Client.any_instance.expects(:invoke).once.
      with(:get_client_plans_basic).
      returns(Aria::WDDX::Struct.new({
        'plans_basic' => [
          Aria::WDDX::Struct.new({
            'plan_no' => '1',
            'plan_name' => 'Free',
            'plan_desc' => 'Free description'
          }),
          Aria::WDDX::Struct.new({
            'plan_no' => '2',
            'plan_name' => 'Silver',
            'plan_desc' => 'Silver description'
          })
        ]
      }))

    assert plan = Aria::MasterPlan.new(
      :plan_no => '1',
      :capabilities => { :max_gears => 3, :gear_sizes => ['small'] }
    )
    assert_equal 'Free', plan.name
    assert_equal 'Free description', plan.description
    assert_equal 3, plan.max_gears
    assert_equal ['small'], plan.gear_sizes

    # The aria plan object should be protected.
    assert_raise(NoMethodError) { plan.aria_plan }
  end

  test 'master plan parses complex aria description text into plan features' do
    Aria::Client.any_instance.expects(:invoke).once.
      with(:get_client_plans_basic).
      returns(Aria::WDDX::Struct.new({
        'plans_basic' => [
          Aria::WDDX::Struct.new({
            'plan_no' => '3',
            'plan_name' => 'MockShift',
            'plan_desc' => "This is the MockShift plan.\n\nFeatures:\n\n* Free Gears: 3\n* Support: Red Hat 24x7x365\n* Scaling: Included\n* Additional Storage: 1 Meellion Gigabytes\n* SSL: Custom domain support\n* Java EE6 Full Profile & CDI: Bazinga"
          })
        ]
      }))

    assert plan = Aria::MasterPlan.new(
      :plan_no => '3',
      :capabilities => { :max_gears => 16, :gear_sizes => ['small','medium'] }
    )

    assert_equal 'This is the MockShift plan.', plan.description
    assert features = plan.features
    assert_equal 'Red Hat 24x7x365', features.each.select{ |feat| feat.name == 'Support' }[0].value
    assert_equal 3, plan.feature('Free Gears').count
    assert_equal nil, plan.feature('NotAFeature').count
    assert_equal true, plan.feature('NotAFeature').not_available?
  end

  test 'master plan parses complex aria description text into currency specific plan features' do
    Aria::Client.any_instance.expects(:invoke).once.
      with(:get_client_plans_basic).
      returns(Aria::WDDX::Struct.new({
        'plans_basic' => [
          Aria::WDDX::Struct.new({
            'plan_no' => '3',
            'plan_name' => 'MockShift',
            'plan_desc' => """This is the MockShift plan.

Features:
* Price: €33/Month (EUR) *
* Price: C$43.05/Month (CAD) *
* Price: $42/Month (USD) *
* Free Gears: 3
* Support: By Red Hat
* Scaling: 3 Included
* Additional Storage: €1/GB per month (EUR) *
* Additional Storage: C$1/GB per month (CAD) *
* Additional Storage: $1/GB per month (USD) *
* SSL: For custom domains *
* Java EE6 Full Profile & CDI: 3 gears free; €0.02/hr per additional gear (EUR) *
* Java EE6 Full Profile & CDI: 3 gears free; $0.03/hr per additional gear (USD) *
* Java EE6 Full Profile & CDI: 3 gears free; C$0.03/hr per additional gear (CAD) *
"""
          })
        ]
      }))

    assert plan = Aria::MasterPlan.new(
      :plan_no => '3',
      :capabilities => { :max_gears => 16, :gear_sizes => ['small','medium'] }
    )

    assert_equal 'This is the MockShift plan.', plan.description
    assert features = plan.features

    assert_equal "By Red Hat", plan.feature("Support").value
    assert_nil plan.feature("Support").currency_cd

    assert_equal "$42/Month", plan.feature("Price").value
    assert_equal "usd", plan.feature("Price").currency_cd

    assert_equal "$42/Month", plan.feature("Price", "usd").value
    assert_equal "usd", plan.feature("Price", "usd").currency_cd

    assert_equal "C$43.05/Month", plan.feature("Price", "cad").value
    assert_equal "cad", plan.feature("Price", "cad").currency_cd

    assert_equal "€33/Month", plan.feature("Price", "eur").value
    assert_equal "eur", plan.feature("Price", "eur").currency_cd
  end

  test 'should raise an error when an aria description can not be parsed into plan features' do
    Aria::Client.any_instance.expects(:invoke).once.
      with(:get_client_plans_basic).
      returns(Aria::WDDX::Struct.new({
        'plans_basic' => [
          Aria::WDDX::Struct.new({
            'plan_no' => '3',
            'plan_name' => 'MockShift',
            'plan_desc' => "This is the MockShift plan.\n\nFeatures:\n\n* : 3\n* Support: Red Hat 24x7x365\n* Scaling: Included\n* Additional Storage: 1 Meellion Gigabytes\n* SSL: Custom domain support\n* Java EE6 Full Profile & CDI: Bazinga"
          })
        ]
      }))

    assert plan = Aria::MasterPlan.new(
      :plan_no => '3',
      :capabilities => { :max_gears => 16, :gear_sizes => ['small','medium'] }
    )

    assert_raise(Aria::MasterPlanFeature::MalformedFeatureError) {features = plan.features}
  end

  test 'should be able to sort master plans by price then gear size options' do
    Aria::Client.any_instance.expects(:invoke).once.
      with(:get_client_plans_basic).
      returns(Aria::WDDX::Struct.new({
        'plans_basic' => [
          Aria::WDDX::Struct.new({
            'plan_no' => '3',
            'plan_name' => 'MockShift',
            'plan_desc' => "This is the MockShift plan.\n\nFeatures:\n\n* Price: Free"
          }),
          Aria::WDDX::Struct.new({
            'plan_no' => '4',
            'plan_name' => 'SuperMockShift',
            'plan_desc' => "This is the SuperMockShift plan.\n\nFeatures:\n\n* Price: $42/month *"
          }),
          Aria::WDDX::Struct.new({
            'plan_no' => '5',
            'plan_name' => 'MegaMockShift',
            'plan_desc' => "This is the MegaMockShift plan.\n\nFeatures:\n\n* Price: $42/month *"
          })
        ]
      }))

    assert plan = Aria::MasterPlan.new(
      :plan_no => '3',
      :capabilities => { :max_gears => 16, :gear_sizes => ['small'] }
    )
    assert plan2 = Aria::MasterPlan.new(
      :plan_no => '4',
      :capabilities => { :max_gears => 32, :gear_sizes => ['small','medium'] }
    )
    assert plan3 = Aria::MasterPlan.new(
      :plan_no => '5',
      :capabilities => { :max_gears => 32, :gear_sizes => ['small','medium','large'] }
    )

    assert_equal [plan, plan2], [plan2, plan].sort
    assert_equal [plan2, plan3], [plan3, plan2].sort
  end

  test 'should be able to sort master plan features from different plans' do
    Aria::Client.any_instance.expects(:invoke).once.
      with(:get_client_plans_basic).
      returns(Aria::WDDX::Struct.new({
        'plans_basic' => [
          Aria::WDDX::Struct.new({
            'plan_no' => '3',
            'plan_name' => 'MockShift',
            'plan_desc' => "This is the MockShift plan.\n\nFeatures:\n\n* Free Gears: 3\n* Support: Red Hat 24x7x365\n* Scaling: Included\n* Additional Storage: 1 Meellion Gigabytes\n* SSL: Custom domain support\n* Java EE6 Full Profile & CDI: Bazinga"
          }),
          Aria::WDDX::Struct.new({
            'plan_no' => '4',
            'plan_name' => 'SuperMockShift',
            'plan_desc' => "This is the SuperMockShift plan.\n\nFeatures:\n\n* Free Gears: 5\n* Support: Red Hat 24x7x365\n* Scaling: Unlimited **\n* Additional Storage: 1 Meellion Gigabytes\n* SSL: Custom domain support\n* Java EE6 Full Profile & CDI: Bazinga"
          })
        ]
      }))

    assert plan = Aria::MasterPlan.new(
      :plan_no => '3',
      :capabilities => { :max_gears => 16, :gear_sizes => ['small','medium'] }
    )
    assert plan2 = Aria::MasterPlan.new(
      :plan_no => '4',
      :capabilities => { :max_gears => 32, :gear_sizes => ['small','medium','large'] }
    )

    # These are numeric but have no ranking
    assert plan1_gears = plan.feature('Free Gears')
    assert plan2_gears = plan2.feature('Free Gears')
    assert_equal [plan1_gears, plan2_gears], [plan2_gears, plan1_gears].sort

    # These have ranking and are non-numeric
    assert plan1_scale = plan.feature('Scaling')
    assert plan2_scale = plan2.feature('Scaling')
    assert_equal [plan1_scale, plan2_scale], [plan2_scale, plan1_scale].sort

    # These have no ranking and are non-numeric
    assert_equal plan.feature('SSL').rank, plan2.feature('SSL').rank

    # Different features can't be sorted together
    assert_raise(Aria::MasterPlanFeature::ComparisonError) {[plan2_scale, plan1_gears].sort}
  end

  def test_bill_should_be_blank
    assert Aria::Bill.new(nil, nil, nil, nil, nil, [], [], 0).blank?
    assert Aria::Bill.new(nil, nil, nil, nil, nil, [], [], 0, 0).blank?
    assert Aria::Bill.new(nil, nil, nil, nil, nil, [], [], 0.01).present?
    assert Aria::Bill.new(nil, nil, nil, nil, nil, [], [], 0.01, 0.01).present?
    assert Aria::Bill.new(nil, nil, nil, nil, nil, [], [], 0.01, -0.01).present?
    assert Aria::Bill.new(nil, nil, nil, nil, nil, [Aria::RecurringLineItem.new({'amount' => 0.01}, 1)], [], 0).present?
    assert Aria::Bill.new(nil, nil, nil, nil, nil, [Aria::RecurringLineItem.new({'amount' => 0.00}, 1)], [], 0).present?

  end

  def test_bill_shows_payment_details_correctly
    payment1 = Aria::Payment.new(Aria::WDDX::Struct.new({
      "transaction_id"=>1,
      "transaction_type"=>3,
      "description"=>"Credit Card",
      "amount"=>100.00,
      "applied_amount"=>100.00,
      "currency_code"=>"usd",
      "transaction_date"=>"2010-01-01",
      "is_voided"=>"false",
      "statement_no"=>0,
      "payment_type"=>"1",
      "payment_src_description"=>"Credit Card",
      "payment_src_suffix"=>"1111",
      "client_receipt_id"=>nil
    }))

    payment2 = Aria::Payment.new(Aria::WDDX::Struct.new({
      "transaction_id"=>1,
      "transaction_type"=>3,
      "description"=>"Credit Card",
      "amount"=>100.00,
      "applied_amount"=>50.00,
      "currency_code"=>"usd",
      "transaction_date"=>"2010-01-01",
      "is_voided"=>"false",
      "statement_no"=>0,
      "payment_type"=>"1",
      "payment_src_description"=>"Credit Card",
      "payment_src_suffix"=>"1111",
      "client_receipt_id"=>nil
    }))

    assert Aria::Bill.new(nil, nil, nil, nil, nil, [], [], 0).show_payment_amounts
    assert Aria::Bill.new(nil, nil, nil, nil, nil, [payment1], [], 0).show_payment_amounts, "A payment that doesn't match the balance should show the amount"
    assert Aria::Bill.new(nil, nil, nil, nil, nil, [payment2], [], 50).show_payment_amounts, "A payment that is partially applied should show the amount"
    assert Aria::Bill.new(nil, nil, nil, nil, nil, [payment2], [], 100).show_payment_amounts, "A payment that is partially applied should show the amount"
    assert Aria::Bill.new(nil, nil, nil, nil, nil, [payment1, payment2], [], 100).show_payment_amounts, "When there are multiple payments, they should show their amounts"
    
    assert !Aria::Bill.new(nil, nil, nil, nil, nil, [payment1], [], 100).show_payment_amounts, "A payment that is fully applied and matches the balance due shouldn't show its amount"
  end

  def test_line_item_prorated
    assert !Aria::RecurringLineItem.new({'units' => 1.0}, 1).prorated?
    assert  Aria::RecurringLineItem.new({'units' => 0.1}, 1).prorated?
  end

  def test_sort_line_items
    rec = Aria::RecurringLineItem.new({'amount' => 0.00, 'rate_per_unit' => 1.0, 'service_name' => 'Recurring'}, 1)
    assert !rec.tax?
    assert rec.recurring?
    tx1 = Aria::RecurringLineItem.new({'amount' => 1.00, 'rate_per_unit' => nil, 'service_name' => 'State Taxes'}, 1)
    assert tx1.tax?
    tx2 = Aria::RecurringLineItem.new({'amount' => 2.00, 'rate_per_unit' => 1.0, 'service_name' => 'Taxes'}, 1)
    assert tx2.tax?
    use = Aria::UsageLineItem.new({'units' => 1, 'rate' => 1.0}, 1)
    assert_equal [rec,use,tx2,tx1], [use,tx1,tx2,rec].sort_by(&Aria::LineItem.plan_sort)
  end

  def test_get_recurring_line_items
    stub_client_plans_all([stub_plan_free, stub_plan_pay])

    assert items = Aria::RecurringLineItem.find_all_by_plan_no(stub_plan_free['plan_no'])
    assert items.length == 0

    assert items = Aria::RecurringLineItem.find_all_by_plan_no(stub_plan_pay['plan_no'])
    assert items.length == 1
  end

  def test_tolerate_missing_plans
    stub_client_plans_all([])
    assert items = Aria::RecurringLineItem.find_all_by_plan_no(1)
    assert_equal 0, items.length

    stub_acct_plans_all(1, [])
    assert items = Aria::RecurringLineItem.find_all_by_current_plan(1)
    assert_equal 0, items.length
  end

  def test_collapse_identical_usage_line_items
    usage = [
      Aria::WDDX::Struct.new({'usage_type_no' => 1, 'rate_per_unit' => 1, 'units' => 1}),
      Aria::WDDX::Struct.new({'usage_type_no' => 1, 'rate_per_unit' => 1, 'units' => 2}),
      Aria::WDDX::Struct.new({'usage_type_no' => 2, 'rate_per_unit' => 1, 'units' => 4}),
      Aria::WDDX::Struct.new({'usage_type_no' => 2, 'rate_per_unit' => 1, 'units' => 8})
    ]
    assert line_items = Aria::UsageLineItem.for_usage(usage, 1)
    assert_equal 2, line_items.length

    assert_equal 1, line_items.first.usage_type_no
    assert_equal 3, line_items.first.total_cost

    assert_equal 2, line_items.last.usage_type_no
    assert_equal 12, line_items.last.total_cost
  end

  def test_collapse_close_rate_usage_line_items
    # Invoice line items use rate_per_unit'
    # Unbilled usage items use 'pre_rated_rate'
    usage = [
      Aria::WDDX::Struct.new({'usage_type_no' => 1, 'rate_per_unit' => 1, 'units' => 1}),
      Aria::WDDX::Struct.new({'usage_type_no' => 1, 'pre_rated_rate' => 1.001, 'units' => 2}),
      Aria::WDDX::Struct.new({'usage_type_no' => 1, 'rate_per_unit' => 2, 'units' => 4}),
      Aria::WDDX::Struct.new({'usage_type_no' => 1, 'pre_rated_rate' => 2.001, 'units' => 8})
    ]
    assert line_items = Aria::UsageLineItem.for_usage(usage, 1)
    assert_equal 2, line_items.length

    assert_equal 1, line_items.first.usage_type_no
    assert_equal 3.002, line_items.first.total_cost

    assert_equal 1, line_items.last.usage_type_no
    assert_equal 24.008, line_items.last.total_cost
  end


  def test_user_should_not_have_next_bill
    u = TestUser.new
    u.expects(:acct_no).at_least_once.returns('1')
    stub_acct_details(1, {
      :plan_no => Rails.configuration.aria_default_plan_no.to_s
    })
    stub_queued_plans(1, [])
    assert_equal false, u.next_bill
  end

  def test_user_should_have_next_bill
    u = TestUser.new
    u.expects(:acct_no).at_least_once.returns('1')
    stub_next_bill :plan_no => '2'
    assert bill = u.next_bill
    assert bill.present?
    assert bill.line_items.present?
    assert_equal 'Plan: SuperMockShift', bill.line_items.first.name
  end

  def test_user_should_have_bill_today_when_billed_through_yesterday
    u = TestUser.new
    u.expects(:acct_no).at_least_once.returns(1.to_s)
    stub_next_bill(
      :plan_no => '2',
      :next_bill_date => (Date.today + 1.days).to_s,
      :last_arrears_bill_thru_date => (Date.today - 1.day).to_s,
    )
    assert bill = u.next_bill
    assert bill.present?
    assert_equal 1, bill.day
    assert_equal Date.today, bill.start_date
    assert_equal Date.today, bill.end_date
  end

  def test_user_should_have_bill_when_created_today
    u = TestUser.new
    u.expects(:acct_no).at_least_once.returns(1.to_s)
    stub_next_bill(
      :plan_no => '2',
      :next_bill_date => (Date.today + 1.days).to_s,
      :last_arrears_bill_thru_date => nil,
      :created => Date.today.to_s
    )
    assert bill = u.next_bill
    assert bill.present?
    assert_equal 1, bill.day
    assert_equal Date.today, bill.start_date
    assert_equal Date.today, bill.end_date
  end

  def test_new_user_current_period
    u = TestUser.new
    u.expects(:acct_no).at_least_once.returns('1')
    
    # Created and upgraded on 1/5
    stub_acct_details(1, {
      :bill_day => "1",
      :created => "2010-01-05",
      :date_to_expire => nil,
      :date_to_suspend => nil,
      :last_arrears_bill_thru_date => nil,
      :last_bill_date => nil,
      :last_bill_thru_date => "2010-01-31",
      :next_bill_date => "2010-02-01",
      :plan_date => "2010-01-05",
      :status_date => "2010-01-05"
    })
    assert_equal '2010-01-05', u.current_period_start_date
    assert_equal '2010-01-31', u.current_period_end_date
  end

  def test_upgraded_user_current_period_start_date
    u = TestUser.new
    u.expects(:acct_no).at_least_once.returns('1')
    
    # Created on 1/5, added payment info on 1/10, upgraded on 1/15
    stub_acct_details(1, {
      :bill_day => "1",
      :created => "2010-01-05",
      :date_to_expire => nil,
      :date_to_suspend => nil,
      :last_arrears_bill_thru_date => nil,
      :last_bill_date => nil,
      :last_bill_thru_date => "2010-01-31",
      :next_bill_date => "2010-02-01",
      :plan_date => "2010-01-15",
      :status_date => "2010-01-10"
    })
    assert_equal '2010-01-05', u.current_period_start_date
    assert_equal '2010-01-31', u.current_period_end_date
  end

  def test_existing_user_current_period_start_date
    u = TestUser.new
    u.expects(:acct_no).at_least_once.returns('1')
    
    # Created on 1/5, added payment info on 1/10, upgraded on 1/15, last billed on 2/1
    stub_acct_details(1, {
      :bill_day => "1",
      :created => "2010-01-05",
      :date_to_expire => nil,
      :date_to_suspend => nil,
      :last_arrears_bill_thru_date => "2010-01-31",
      :last_bill_date => "2010-02-01",
      :last_bill_thru_date => "2010-02-28",
      :next_bill_date => "2010-03-01",
      :plan_date => "2010-01-15",
      :status_date => "2010-01-10"
    })
    assert_equal '2010-02-01', u.current_period_start_date
    assert_equal '2010-02-28', u.current_period_end_date
  end

  def test_user_should_have_empty_bill_if_downgraded
    u = TestUser.new
    u.expects(:acct_no).at_least_once.returns(1.to_s)
    stub_next_bill(
      :plan_no => '2',
      :queued_plans => [{
        'new_plan_no' => Rails.configuration.aria_default_plan_no,
      }]
    )
    assert bill = u.next_bill
    assert bill.empty?
  end

  def test_user_should_have_nonempty_bill_if_downgraded
    u = TestUser.new
    u.expects(:acct_no).at_least_once.returns(1.to_s)
    stub_next_bill(
      :plan_no => '2',
      :unbilled_usage_balance_ptd => 1.0,
      :queued_plans => [{
        'new_plan_no' => Rails.configuration.aria_default_plan_no,
      }]
    )
    assert bill = u.next_bill
    assert !bill.empty?
    assert_equal 1.0, bill.balance
  end

  def test_usage_line_item_should_have_partial_rate
    plan = stub_plan_pay
    plan['plan_services'].last['plan_service_rates'] = [
      {
        'rate_per_unit' => 0.00001,
        'to_unit' => 1,
      },
      {
        'rate_per_unit' => 0.0,
        'to_unit' => 0,
      },
      {
        'rate_per_unit' => 1.0,
        'to_unit' => 0,
      },
      {
        'rate_per_unit' => 0.0,
        'to_unit' => 10,
      },
    ]
    stub_client_plans_all([plan])
    li = Aria::UsageLineItem.new({'usage_type_no' => 10}, 2)
    assert_equal 10, li.free_units
  end

  def stub_next_bill(opts={})
    acct_no = 1 || opts[:acct_no]
    opts.reverse_merge!({
      :next_bill_date => (Date.today + 2.days).to_s,
      :last_arrears_bill_thru_date => (Date.today - 1.day).to_s,
    })
    plan_no = opts[:plan_no] || Rails.application.aria_default_plan_no

    stub_aria(:get_virtual_datetime, {
    }).to_return(resp(ok_wddx({
      :current_offset_hours => 0,
    })))
    stub_acct_details(acct_no, {:plan_no => plan_no}.merge(opts.slice(:next_bill_date, :last_arrears_bill_thru_date, :created)))
    stub_queued_plans(acct_no, opts[:queued_plans] || [])
    stub_acct_invoice_history(acct_no, opts[:invoice_history] || [])
    stub_aria(:get_usage_history, {
      :acct_no => acct_no.to_s,
      :date_range_start => Date.today.to_s,
    }).to_return(resp(ok_wddx({
      :usage_history_records => opts[:usage_history] || [],
    })))
    stub_aria(:get_unbilled_usage_summary, {:acct_no => acct_no.to_s}).to_return(resp(ok_wddx({
      :ptd_balance_amount => opts[:unbilled_usage_balance_ptd] || 0.0,
    })))
    acct_plan = 
      if opts[:acct_plan]
        opts[:acct_plan]
      elsif plan_no != Rails.configuration.aria_default_plan_no
        [stub_plan_pay]
      else
        [stub_plan_free]
      end
    stub_acct_plans_all(acct_no, acct_plan)
    stub_client_plans_all([stub_plan_free, stub_plan_pay])
  end

  def stub_plan_pay
    {
      'plan_no' => '2',
      'plan_name' => 'SuperMockShift',
      'plan_services' => [
        {
          'service_desc' => 'Recurring',
          'is_recurring_ind' => 1,
          'usage_type' => nil,
          'is_usage_based_ind' => 0,
          'plan_service_rates' => [
            {
              'monthly_fee' => 41,
            }
          ]
        },
        {
          'service_desc' => 'State Tax',
          'is_recurring_ind' => 0,
          'usage_type' => nil,
          'is_usage_based_ind' => 0,
          'plan_service_rates' => [],
        },
        {
          'service_desc' => 'Usage',
          'usage_type' => 10,
          'is_recurring_ind' => 0,
          'is_usage_based_ind' => 1,
          'plan_service_rates' => [],
        },
      ]
    }
  end
  def stub_plan_free
    {
      'plan_no' => Rails.configuration.aria_default_plan_no,
      'plan_name' => 'FreeMockShift',
      'plan_services' => [
        {
          'service_desc' => 'Recurring',
          'is_recurring_ind' => 1,
          'usage_type' => nil,
          'is_usage_based_ind' => 0,
          'plan_service_rates' => [
            {
              'monthly_fee' => 0.0,
            }
          ]
        },
        {
          'service_desc' => 'State Tax',
          'is_recurring_ind' => 0,
          'usage_type' => nil,
          'is_usage_based_ind' => 0,
          'plan_service_rates' => [],
        },
        {
          'service_desc' => 'Usage',
          'usage_type' => 10,
          'is_recurring_ind' => 0,
          'is_usage_based_ind' => 1,
          'plan_service_rates' => [],
        },
      ]
    }
  end


end
