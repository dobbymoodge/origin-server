ENV["TEST_NAME"] = "usage_integration_plan_api_test"
require 'test_helper'
require 'openshift-origin-controller'
require 'mocha/setup'

class PlansApiTest < ActionDispatch::IntegrationTest

  PLANS_COLLECTION_URL = "/broker/rest/plans"
  def setup
    @random = gen_uuid[0..9]
    @login = "test_user#{@random}"

    # Headers for testing authenticated requests
    @headers = {}
    @headers["HTTP_AUTHORIZATION"] = "Basic " + Base64.encode64("#{@login}:password")
    @headers["HTTP_ACCEPT"] = "application/json"

    # Headers for testing unauthenticated requests
    # (these are permitted)
    @unauthenticated_headers = {}
    @unauthenticated_headers["HTTP_ACCEPT"] = "application/json"

    https!
  end

  def teardown

  end

  def test_plan_show
    [@headers, @unauthenticated_headers].each do |header_list|
      request_via_redirect(:get, PLANS_COLLECTION_URL + "/#{:free}", {}, header_list)
      assert_response :ok
      body = JSON.parse(@response.body)
      plan = body["data"]
      assert_equal(plan["id"], "free", "Plan id #{plan["id"]} expected free")
      assert_equal(plan["name"], "Free", "Plan name #{plan["name"]} expected Free")
      assert_not_nil(plan["plan_no"])

      request_via_redirect(:get, PLANS_COLLECTION_URL + "/#{:silver}", {}, header_list)
      assert_response :ok
      body = JSON.parse(@response.body)
      plan = body["data"]
      assert_equal(plan["id"], "silver", "Plan id #{plan["id"]} expected silver")
      assert_equal(plan["name"], "Silver", "Plan name #{plan["name"]} expected Silver")
      assert_not_nil(plan["plan_no"])
    end
  end

  def test_plan_index
    [@headers, @unauthenticated_headers].each do |header_list|
      request_via_redirect(:get, PLANS_COLLECTION_URL, {}, header_list)
      assert_response :ok
      body = JSON.parse(@response.body)
      plans = body["data"]
      assert(plans.length > 1)
      plans.each do |plan|
        assert_not_nil(plan["id"], "Id for plan is nil")
        assert_not_nil(plan["name"], "Name for plan #{plan["id"]} is nil")
        assert_not_nil(plan["plan_no"], "Plan no for plan #{plan["id"]} is nil")
      end
    end
  end

end