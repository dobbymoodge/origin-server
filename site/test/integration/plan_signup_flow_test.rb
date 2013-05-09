# encoding: UTF-8

require File.expand_path('../../test_helper', __FILE__)

class PlanSignupFlowTest < ActionDispatch::IntegrationTest

  def setup
    omit_if_aria_is_unavailable
    WebMock.allow_net_connect!
    https!
    open_session
  end

  def credit_card_params
    {
      'cvv' => '111',
      'cc_no' => '4111 1111 1111 1111',
      'cc_exp_yyyy' => '2015',
      'cc_exp_mm' => '12',
    }
  end

  def user_params
    { :streamline_full_user => {
        :greeting =>"Mr.",
        :first_name =>"Joe",
        :last_name =>"Somebody",
        :title => "Stuntman",
        :company => "Red Hat, Inc.",
        :phone_number => "9191111111",
        :email_subscribe => false,
        :password => "f00b4r",
        :password_confirmation =>"f00b4r"
      },
      :aria_billing_info => billing_params,
    }
  end

  def billing_params
    { :first_name =>"Joe",
      :middle_initial =>"",
      :last_name =>"Somebody",
      :address1 =>"12345 Happy Street",
      :address2 =>"",
      :address3 =>"",
      :city => "Lund",
      :region =>"Scania",
      :zip => "223397",
      :country => "SE",
    }
  end

  def simple_user
    @simple_user ||= {:web_user => {:rhlogin => uuid, :password => 'password'}}
  end

  def login_simple_user
    post '/login', simple_user
    assert_response :redirect, @response.inspect
    simple_user
  end

  test 'anonymous without prev signin redirected to signup' do
    get '/account/plans'
    assert_response :redirect

    get '/account/plan'
    assert_response :redirect

    get '/account/plans/silver/upgrade'
    assert_redirected_to new_account_path(:then => account_plan_upgrade_path('silver'))
  end

  test 'anonymous with signin redirected to login' do
    cookies[:prev_login] = true

    get '/account/plans'
    assert_response :redirect

    get '/account/plan'
    assert_response :redirect

    get '/account/plans/silver/upgrade'
    assert_redirected_to login_path(:then => account_plan_upgrade_path('silver'))
  end

  test 'user can signup' do
    Rails.configuration.expects(:aria_direct_post_name).at_least_once.returns(nil)

    user = new_streamline_user
    omit_on_register unless user.register('/email_confirm')
    assert user.confirm_email
    post '/login', {:web_user => {:rhlogin => user.email_address, :password => user.password}}

    get '/account/plans'
    assert_response :redirect

    get '/account/plan'
    assert_response :success
    assert_select ".plan h4 span:content(?)", /\$/, true, "Prices should be in USD by default"

    get '/account/plans/silver/upgrade'
    assert_redirected_to '/account/plans/silver/upgrade/edit'

    get '/account/plans/silver/upgrade/edit'
    assert_response :success

    put '/account/plans/silver/upgrade/edit', :streamline_full_user => user_params
    assert_redirected_to '/account/plans/silver/upgrade/payment_method'

    omit_if_aria_is_unavailable
    get '/account/plans/silver/upgrade/payment_method'
    assert_redirected_to '/account/plans/silver/upgrade/payment_method/new'

    get '/account/plans/silver/upgrade/payment_method/new'
    assert_response :success

    res = submit_form('form#payment_method', credit_card_params)
    assert Net::HTTPRedirection === res, res.inspect
    redirect = res['Location']
    assert redirect.starts_with?(direct_create_account_plan_upgrade_payment_method_url('silver')), redirect

    get redirect
    assert_redirected_to '/account/plans/silver/upgrade'

    # Do some direct checking here just to validate
    omit_if_aria_is_unavailable
    aria_user = Aria::UserContext.new(WebUser.new(:rhlogin => user.rhlogin))
    assert_equal 'eur', aria_user.currency_cd
    assert_equal user.email_address, aria_user.account_details.alt_email

    assert config_collections_group_id = Rails.configuration.collections_group_id_by_country[aria_user.account_details.country]
    assert config_functional_group_no = Rails.configuration.functional_group_no_by_country[aria_user.account_details.country].to_i
    assert_equal config_functional_group_no, aria_user.account_details.seq_func_group_no
    assert aria_acct_groups = Aria.get_acct_groups_by_acct(aria_user.acct_no)
    assert aria_coll_groups = aria_acct_groups.select{ |g| g.group_type == 'C' }
    assert aria_func_groups = aria_acct_groups.select{ |g| g.group_type == 'F' }
    assert_equal 2, aria_acct_groups.count
    assert_equal 1, aria_coll_groups.count
    assert_equal 1, aria_func_groups.count
    assert_equal config_collections_group_id, aria_acct_groups[0].client_acct_group_id
    assert_equal config_functional_group_no, aria_func_groups[0].group_no.to_i

    assert aria_user.has_valid_payment_method?
    assert payment_method = aria_user.payment_method
    assert payment_method.persisted?
    assert payment_method.cc_no.ends_with?(credit_card_params['cc_no'][-4..-1])
    assert_equal credit_card_params['cc_exp_yyyy'].to_i, payment_method.cc_exp_yyyy
    assert_equal credit_card_params['cc_exp_mm'].to_i, payment_method.cc_exp_mm

    rest_user = User.find :one, :as => user
    plan = rest_user.plan
    assert plan
    assert_equal "free", plan.id, "The user plan is not free prior to upgrade\n#{rest_user.inspect}\n#{user.inspect}\n#{plan.inspect}"

    get '/account/plans/silver/upgrade/new'
    assert_response :success
    assert_select ".plan-pricing td:content(?)", /€/, true, "Prices should be in EUR once selected during account creation"
    assert_select ".plan-pricing td:content(?)", /\$/, false, "Prices should not be in USD once EUR is selected during account creation"

    post '/account/plans/silver/upgrade', {:plan_id => 'silver'}
    assert_response :success
    assert_select 'h1', 'You have upgraded to the Silver plan!'
    assert_template :upgraded

    assert_equal 'silver', User.find(:one, :as => user).plan_id

    get '/account/plan'
    assert_response :success
  end
end
