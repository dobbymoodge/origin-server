require 'mocha'
require 'openshift'
require 'streamline'

require 'webmock/test_unit'
WebMock.allow_net_connect!

class ActiveSupport::TestCase

  setup { $VERBOSE = nil }
  teardown { $VERBOSE = false }

  def setup_user(unique=false)
    @user = user_to_session(WebUser.new :email_address=>"app_test1#{unique ? uuid : ''}@test1.com", :rhlogin=>"app_test1#{unique ? uuid : ''}@test1.com")
  end

  def user_to_session(user)
    session[:login] = user.login
    session[:user] = user
    session[:ticket] = user.ticket || '123'
    session[:streamline_type] = user.streamline_type
    @request.cookies['rh_sso'] = session[:ticket]
    @request.env['HTTPS'] = 'on'
    user
  end

  def expects_integrated
    flunk 'Test requires integrated Streamline authentication' unless Rails.configuration.integrated
  end

  def gen_small_uuid()
    %x[/usr/bin/uuidgen].gsub('-', '').strip
  end

  @@name = 0
  def unique_name_format
    'name%i'
  end
  def unique_name(format=nil)
    (format || unique_name_format) % self.class.next
  end
  def self.next
    @@name += 1
  end

  @@once = []
  def once(symbol, &block)
    unless @@once.include? symbol
      @@once << symbol
      exit_block = yield block
      at_exit do
        exit_block.call if exit_block
      end
    end
  end
end

