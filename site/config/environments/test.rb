RedHatCloud::Application.configure do
  # Settings specified here will take precedence over those in config/application.rb

  # The test environment is used exclusively to run your application's
  # test suite.  You never need to work with it otherwise.  Remember that
  # your test database is "scratch space" for the test suite and is wiped
  # and recreated between test runs.  Don't rely on the data there!
  config.cache_classes = true

  # Log error messages when you accidentally call methods on nil.
  config.whiny_nils = true

  # Show full error reports and disable caching
  config.consider_all_requests_local       = true
  config.action_controller.perform_caching = false

  # Raise exceptions instead of rendering exception templates
  config.action_dispatch.show_exceptions = false

  # Disable request forgery protection in test environment
  config.action_controller.allow_forgery_protection    = false

  # Tell Action Mailer not to deliver emails to the real world.
  # The :test delivery method accumulates sent emails in the
  # ActionMailer::Base.deliveries array.
  config.action_mailer.delivery_method = :test

  # Use SQL instead of Active Record's schema dumper when creating the test database.
  # This is necessary if your schema can't be completely dumped by the schema dumper,
  # like if you have constraints or database-specific column types
  # config.active_record.schema_format = :sql

  # Print deprecation notices to the stderr
  config.active_support.deprecation = :stderr

  ############################################
  # OpenShift Configuration Below this point #
  ############################################
  config.app_scope = "app"
  config.integrated = false
  config.login = "/app/login"
  config.streamline = {
    :host => 'https://localhost',
    :base_url => '',
    :email_confirm_url => '/confirm.html',
    :lost_password_url => '/lostPassword.html',
    :login_url => '',
    :secret => 'c0ldW1n3'
  }
  config.captcha_secret = 'secret'
  
  # Maximum number of apps
  config.express_max_apps = 5
  
  # Express API base url
  config.express_api_url = 'https://localhost'
  
  ## AWS configuration
  #config.aws_key = "AKIAJMZR4X6F46UMXV6Q"
  #config.aws_secret = "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"
  #config.aws_keypair = "libra"
  #config.aws_name = "libra-node"
  #config.aws_environment = "demo"
  #config.aws_ami = "N/A"
  #config.repo_threshold = 100
  #config.s3_bucket = "libra-dev"

  ## DDNS configuration
  #config.libra_domain = "rhcloud.com"
  #config.resolver = "209.132.178.9"
  #config.secret = "hmac-md5:dhcpupdate:fzAvGcKPZWiFgmF8qmNUaA=="

  ## Broker configuration
  #config.per_user_app_limit = 1
end
