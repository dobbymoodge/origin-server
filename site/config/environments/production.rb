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
  config.captcha_types = [:recaptcha,:picatcha]

  # Aria API information
  config.aria_enabled = true
  config.aria_uri = "https://secure.current.stage.ariasystems.net/api/ws/api_ws_class_dispatcher.php"
  config.aria_direct_post_uri = "https://secure.current.stage.ariasystems.net/api/direct_post.php"
  config.aria_auth_key = "sRvjFqjSadu3AFB8jRAR3tqeH5Qf6XjW"
  config.aria_client_no = 3754655
  config.aria_default_plan_no = 10044929
  config.aria_force_test_users = false
  config.aria_max_parallel_requests = 5
  # Aria direct post configuration
  config.aria_direct_post_uri = "https://secure.current.stage.ariasystems.net/api/direct_post.php"
  config.aria_direct_post_name = 'website_new_payment'
  config.aria_direct_post_redirect_base = 'https://openshift.redhat.com/app'

  # Currency
  # Specify allowed currencies here, use ISO4217 format
  config.allowed_currencies = [:usd, :cad, :eur]
  config.default_currency = :usd

  # Specify allowed countries
  # Add a corresponding value in config/countries.yml if the country uses something other than:
  #  - 'State' for the locality
  #  - 'Postcode' for the postal code
  config.allowed_countries = %w(AT BE CA CH DE DK ES FI FR GB IE IS IT LU NL NO PT SE US).map(&:to_sym)
  # Preferred countries will show up first in the countries list
  config.preferred_countries = [:US]

  # Specify accepted cards here. Keys can be found in config/credit_cards.yml
  config.accepted_cards = [:visa,:mastercard,:amex]
  # Disable extended credit card validation rules
  #config.disable_cc_validation = true
  # Disable JS based address form updates
  #config.disable_dynamic_country_form = true

  # Promo code Email notification setup
  config.email_from = 'OpenShift <noreply@openshift.redhat.com>'
  config.marketing_mailing_list = ['Marketing Mailing List <jgurrero@redhat.com>', 'mthompso@redhat.com']

  # Twitter API information
  config.twitter_api_site = 'https://api.twitter.com'
  config.twitter_api_prefix = '/1.1/statuses/'
  config.twitter_oauth_consumer_key = 'kRJ1Hjo3uNd2M8zKCCF0bw'
  config.twitter_oauth_consumer_secret = 'psNvYg3IOAhWtngxBobajkYWKlus53xkNBQxWz3MU'
  config.twitter_oauth_token = '17620820-rm2UBzOWYrETRh2Ut4rjkGISqmkfdlVKSYcmmAOGt'
  config.twitter_oauth_token_secret = 'aFfOPRBJBckWarMxlWYg3MljK6EgoaKUW9CjFSsaG8'

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
                                 jquery.payment.js
                                 site/home.js
                                 site/tracking.js
                                 site/omniture.js
                                 site/s_code.js
                                 site/picatcha.js
                                 common.css
                                 console.css
                                 site.css
                                 overpass.css
                                 picatcha.css
                                )

  # Account Support contact
  config.acct_help_mail_to = 'os.accounts@redhat.com'

  Console.configure(ENV['CONSOLE_CONFIG_FILE'] || '/etc/openshift/console.conf')
end
