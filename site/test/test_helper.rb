ENV["RAILS_ENV"] = "test"
$:.unshift(File.dirname(__FILE__) + '/../../server-common')
require File.expand_path('../../config/environment', __FILE__)
require 'rails/test_help'
require 'mocha'
require 'openshift'
require 'streamline'

class ActiveSupport::TestCase
  # Setup all fixtures in test/fixtures/*.(yml|csv) for all tests in alphabetical order.
  #
  # Note: You'll currently still have to declare fixtures explicitly in integration tests
  # -- they do not yet inherit this setting
  #fixtures :all
  
  def setup_session(role='')
    session[:login] = 'tester'
    session[:user] = WebUser.new
    session[:ticket] = '123'
    @request.cookies['rh_sso'] = '123'
    @request.env['HTTPS'] = 'on'
    session[:user].roles.push(role) unless role.empty?
  end

  def expects_integrated
    flunk 'Test requires integrated Streamline authentication' unless Rails.configuration.integrated
  end
end

