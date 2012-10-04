RedHatCloud::Application.configure do
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


  # Enable serving of images, stylesheets, and javascripts from an asset server
  # config.action_controller.asset_host = "http://assets.example.com"

  # Disable delivery errors, bad email addresses will be ignored
  # config.action_mailer.raise_delivery_errors = false

  # Enable threaded mode
  config.threadsafe!
  # Workaround for Rails 3.2.x and threadsafe!
  config.dependency_loading = true if $rails_rake_task

  # Enable locale fallbacks for I18n (makes lookups for any locale fall back to
  # the I18n.default_locale when a translation can not be found)
  config.i18n.fallbacks = true

  # Send deprecation notices to registered listeners
  config.active_support.deprecation = :notify

  ############################################
  # OpenShift Configuration Below this point #
  ############################################
  config.integrated = false# true
  config.streamline = {
    :host => 'https://www.redhat.com',
    :base_url => '/wapps/streamline',
    :register_secret => 'c0ldW1n3',
    :user_info_secret => 'sw33tl1Qu0r',
    :cookie_domain => 'redhat.com',
    :timeout => 5
  }
  config.captcha_secret = 'zvw5LiixMB0I4mjk06aR'
  config.sso_verify_interval = 60

  # Aria API information
  config.aria_enabled = false
  config.aria_uri = "https://secure.current.stage.ariasystems.net/api/ws/api_ws_class_dispatcher.php"
  config.aria_direct_post_uri = "https://secure.current.stage.ariasystems.net/api/direct_post.php"
  config.aria_auth_key = "sRvjFqjSadu3AFB8jRAR3tqeH5Qf6XjW"
  config.aria_client_no = 3754655
  config.aria_default_plan_no = 10044929
  config.aria_force_test_users = false
  # Aria direct post configuration
  config.aria_direct_post_uri = "https://secure.current.stage.ariasystems.net/api/direct_post.php"
  config.aria_direct_post_name = 'website_new_payment'
  config.aria_direct_post_redirect_base = 'https://openshift.redhat.com'

  # Promo code Email notification setup
  config.email_from = 'OpenShift <noreply@openshift.redhat.com>'
  config.marketing_mailing_list = ['Marketing Mailing List <jgurrero@redhat.com>', 'mthompso@redhat.com']

  # Disable Rails's static asset server
  # In production, Apache or nginx will already do this
  config.serve_static_assets = true#false

  config.assets.compile = false
  config.assets.initialize_on_precompile = false
  config.assets.compress = true
  # Digest is disabled so we serve the same resources
  #config.assets.digest = true
  config.assets.js_compressor = :uglifier
  config.assets.precompile += %w(application.js
                                 console.js
                                 modernizr.min.js
                                 site/home.js
                                 site/tracking.js
                                 site/omniture.js
                                 site/s_code.js
                                 common.css
                                 console.css
                                 site.css
                                 overpass.css
                                )

  if config.respond_to? :sass
    config.sass.style = :compressed
    config.sass.line_comments = false
    config.sass.relative_assets = true
  end

  Console.configure do |c|
    c.api = :local
  end
end
