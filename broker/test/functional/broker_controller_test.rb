require 'test_helper'

class BrokerControllerTest < ActionController::TestCase
=begin
  test "cart list" do
    # setup cache
    Rails.cache.clear
    Rails.application.config.action_controller.perform_caching = true

    # should be a cache miss
    resp = post(:cart_list_post, {:json_data => '{"cart_type" : "standalone"}'})
    assert_equal 200, resp.status
    body1 = resp.body

    # should be a cache hit
    resp = post(:cart_list_post, {:json_data => '{"cart_type" : "standalone"}'})
    assert_equal 200, resp.status
    body2 = resp.body

    assert body1 == body2
  end

  test "embedded cart list" do
    # setup cache
    Rails.cache.clear
    Rails.application.config.action_controller.perform_caching = true

    # should be a cache miss
    resp = post(:cart_list_post, {:json_data => '{"cart_type" : "embedded"}'})
    assert_equal 200, resp.status
    body1 = resp.body

    # should be a cache hit
    resp = post(:cart_list_post, {:json_data => '{"cart_type" : "embedded"}'})
    assert_equal 200, resp.status
    body2 = resp.body

    assert body1 == body2
  end
=end
end

