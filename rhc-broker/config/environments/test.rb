Broker::Application.configure do
  # Settings specified here will take precedence over those in config/application.rb

  # The test environment is used exclusively to run your application's
  # test suite. You never need to work with it otherwise. Remember that
  # your test database is "scratch space" for the test suite and is wiped
  # and recreated between test runs. Don't rely on the data there!
  config.cache_classes = true

  # Disable Rails's static asset server (Apache or nginx will already do this)
  #config.serve_static_assets = false

  # Log error messages when you accidentally call methods on nil
  config.whiny_nils = true

  # Show full error reports and enable caching
  config.consider_all_requests_local       = true
  config.action_controller.perform_caching = true

  # Raise exceptions instead of rendering exception templates
  config.action_dispatch.show_exceptions = false

  # Disable request forgery protection in test environment
  config.action_controller.allow_forgery_protection    = false

  # Tell Action Mailer not to deliver emails to the real world.
  # The :test delivery method accumulates sent emails in the
  # ActionMailer::Base.deliveries array.
  config.action_mailer.delivery_method = :test

  # Raise exception on mass assignment protection for Active Record models
  #config.active_record.mass_assignment_sanitizer = :strict

  # Print deprecation notices to the stderr
  config.active_support.deprecation = :stderr

  # Set the log level
  config.log_level = :debug

  ############################################
  # OpenShift Configuration Below this point #
  ############################################
  config.dns = {
    :zone => "dev.rhcloud.com",
    :dynect_customer_name => "redhat",
    :dynect_user_name => "oo-dev-user",
    :dynect_password => "vo8zaijoN7Aecoo",
    :dynect_url => "https://api2.dynect.net"
  }

  config.auth = {
    :integrated => false,
    # formerly the broker_auth_secret
    :salt => "EIvWT6u3lsvSRNRGZhhW8YcWMh5mUAlc32nZlRJPdJM=",
    # formerly the broker_auth_rsa_secret
    :privkeypass => "SJDIkdfhuISe3wrulhjvcKHJFDUeoi8gfcdnu8299dhc",
    :privkeyfile => "config/keys/private.pem",
    :pubkeyfile  => "/var/www/openshift/broker/config/keys/public.pem",
    :rsync_keyfile => "/var/www/openshift/broker/config/keys/rsync_id_rsa",
    :token_login_key => :rhlogin,
    :auth_service => {
      :host => "https://streamline-proxy1.ops.rhcloud.com",
      :base_url => "/wapps/streamline"
    }
  }

  config.usage_tracking = {
    :datastore_enabled => true,
    :audit_log_enabled => true,
    :audit_log_filepath => "/var/log/openshift/broker/usage.log"
  }

  config.analytics = {
    :enabled => false, # global flag for whether any analytics should be enabled
    :nurture => {
      :enabled => false,
      :username => "admin",
      :password => "password",
      :url => "http://69.164.192.124:4500/"
    }
  }

  config.datastore = {
    :host_port => "localhost:27017",
    :user => "openshift",
    :password => "mooo",
    :db => "openshift_broker_test",
    :ssl => false
  }

  config.user_action_logging = {
    :logging_enabled => true,
    :log_filepath => "/var/log/openshift/broker/user_action.log"
  }

  config.maintenance = {
    :enabled => false,
    :outage_msg_filepath => "/etc/openshift/outage_notification.txt"
  }

  # OpenShift Config
  config.openshift = {
    :domain_suffix => "dev.rhcloud.com",
    :default_max_gears => 3,
    :default_gear_size => "small",
    :default_gear_capabilities => ["small"],
    :gear_sizes => ["small", "medium", "c9"],
    :scopes => ['Scope::Session', 'Scope::Read', 'Scope::Application', 'Scope::Userinfo'],
    :default_scope => 'userinfo',
    :scope_expirations => OpenShift::Controller::Configuration.parse_expiration("session=1.days|2.days", 1.month),
    :download_cartridges_enabled => true,
  }

  # Profiler config
#  config.profiler = {
#    :type => 'call_tree',
#    :measure => 'wall',
#    :min_percent => 0,
#    :squash_threads => true,
#    :squash_runtime => true
#  }

  # mcollective configuration
  config.msg_broker = {
    :rpc_options => {
        :disctimeout => 2,
        :timeout => 180,
        :verbose => false,
        :progress_bar => false,
        :filter => {"identity" => [], "fact" => [], "agent" => [], "cf_class" => [], "compound" => []},
        :config => "/etc/mcollective/client.cfg"
    },
    :districts => {
        :enabled => true,
        :require_for_app_create => false,
        :max_capacity => 6000, # Only used with district create.  Modify capacity through oo-admin-ctl-district.
        :first_uid => 1000 # Can not modify after district is created.  Only affects new districts.
    },
    :node_profile_enabled => false
  }

  config.downloaded_cartridges = {
    :max_downloaded_carts_per_app => 5,
    :max_download_redirects => 2,
    :max_cart_size => 20480,
    :max_download_time => 10
  }

end
