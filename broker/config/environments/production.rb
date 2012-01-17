Broker::Application.configure do
  # Settings specified here will take precedence over those in config/application.rb

  # The production environment is meant for finished, "live" apps.
  # Code is not reloaded between requests
  config.cache_classes = true

  # Full error reports are disabled and caching is turned on
  config.consider_all_requests_local       = false
  config.action_controller.perform_caching = true

  # Specifies the header that your server uses for sending files
  config.action_dispatch.x_sendfile_header = "X-Sendfile"

  # For nginx:
  # config.action_dispatch.x_sendfile_header = 'X-Accel-Redirect'

  # If you have no front-end server that supports something like X-Sendfile,
  # just comment this out and Rails will serve the files

  # See everything in the log (default is :info)
  config.log_level = :debug

  # Use a different logger for distributed setups
  # config.logger = SyslogLogger.new

  # Use a different cache store in production
  # config.cache_store = :mem_cache_store

  # Disable Rails's static asset server
  # In production, Apache or nginx will already do this
  config.serve_static_assets = false

  # Enable serving of images, stylesheets, and javascripts from an asset server
  # config.action_controller.asset_host = "http://assets.example.com"

  # Disable delivery errors, bad email addresses will be ignored
  # config.action_mailer.raise_delivery_errors = false

  # Enable threaded mode
  # config.threadsafe!

  # Enable locale fallbacks for I18n (makes lookups for any locale fall back to
  # the I18n.default_locale when a translation can not be found)
  config.i18n.fallbacks = true

  # Send deprecation notices to registered listeners
  config.active_support.deprecation = :notify

  ############################################
  # OpenShift Configuration Below this point #
  ############################################
  config.app_scope = ""
  
  config.districts = {
    :enabled => true,
    :district => nil,
    :max_capacity => 6000,
    :first_uid => 1000
  }
  
  config.dns = {
    :zone => "rhcloud.com",
    :dynect_customer_name => "demo-redhat",
    :dynect_user_name => "390XFV-dev-user",
    :dynect_password => "Mei5aeru6yahchee",
    :dynect_url => "https://api2.dynect.net"
  }
  
  config.auth = {
    :integrated => true,
    :broker_auth_secret => "EIvWT6u3lsvSRNRGZhhW8YcWMh5mUAlc32nZlRJPdJM=",
    :broker_auth_rsa_secret => "SJDIkdfhuISe3wrulhjvcKHJFDUeoi8gfcdnu8299dhc",
    :auth_service => {
      :host => "https://www.redhat.com",
      :base_url => "/wapps/streamline"
    }
  }
  
  config.rpc_opts = {
    :disctimeout => 3,
    :timeout     => 30,
    :verbose     => false,
    :progress_bar=> false,
    :filter      => {"identity"=>[], "fact"=>[], "agent"=>[], "cf_class"=>[]},
    :config      => "/etc/mcollective/client.cfg"
  }
  
  config.datastore = {
    :aws_key => "KEY_HERE",
    :aws_secret => "SECRET_HERE",
    :s3_bucket => "BUCKET_HERE"
  }
  
  config.analytics = {
    :nurture_enabled => true,
    :nurture_username => "admin",
    :nurture_password => "password",
    :nurture_url => "http://69.164.192.124:4500/",
    
    :apptegic_enabled => true,
    :apptegic_url => "https://redhat.apptegic.com/httpreceiver",
    :apptegic_key => "redhat",
    :apptegic_secret => "4DC5A0AA-48AE-9287-5F66-9A73E14B6E31",
    :apptegic_dataset => "test"
  }
  
  # CDK Config
  config.cdk = {
    :domain_suffix => "rhcloud.com",
    :per_user_app_limit => 5
  }

end
