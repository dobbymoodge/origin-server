ENV["TEST_NAME"] = "unit_streamline_auth_test"
require 'test_helper'
require 'mocha'

module Rails
  def self.logger
    l = Mocha::Mock.new("logger")
    l.stubs(:debug)
    l.stubs(:info)
    l.stubs(:add)
    l
  end
end

class StreamlineAuthTest < ActiveSupport::TestCase
  test "authentication with cache" do
    mock_request = mock("Request")
    mock_request.expects(:headers).returns({"User-Agent" => ""})
    mock_request.expects(:cookies).returns({"rh_sso" => nil}) #{"rh_sso" => "abcde"})

    Rails.configuration.auth[:integrated] = true
    Rails.configuration.action_controller.perform_caching = true

    TestAuthService.new.authenticate(mock_request, 'login', 'pwd')

    # The cookie should be written to the Rails cache
    cookie = Rails.cache.read("abcde")
    assert cookie.nil? == false
  end

  test "authentication without cache" do
    mock_request = mock("Request")
    mock_request.expects(:headers).returns({"User-Agent" => ""})
    mock_request.expects(:cookies).returns({"rh_sso" => "abcde"})

    Rails.configuration.auth[:integrated] = true
    Rails.configuration.action_controller.perform_caching = true

    begin
      TestCachedAuthService.new.authenticate(mock_request, 'login', 'pwd')
    rescue Exception => e
      assert false, e.message
    end

    # The cookie should still be present in the Rails cache
    cookie = Rails.cache.read("abcde")
    assert cookie.nil? == false
  end

  def teardown
    Rails.configuration.auth[:integrated] = false
    Rails.configuration.action_controller.perform_caching = false
    Mocha::Mockery.instance.stubba.unstub_all
  end
end

class TestAuthService < OpenShift::StreamlineAuthService
  def http_post(url, args={}, ticket=nil)
    ticket = "abcde" unless ticket
    return {"username" => "login", "roles" => ["cloud_access_1"]}, ticket
  end
end

class TestCachedAuthService < OpenShift::StreamlineAuthService
  def http_post(url, args={}, ticket=nil)
    # If the authentication ticket is cached, this method should not be called
    raise "If the authentication ticket is cached, auth service should not be called"
  end
end

