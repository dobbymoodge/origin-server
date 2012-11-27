Broker::Application.configure do
  # Settings specified here will take precedence over those in config/application.rb

  # In the development environment your application's code is reloaded on
  # every request. This slows down response time but is perfect for development
  # since you don't have to restart the web server when you make code changes.
  config.cache_classes = true

  # Log error messages when you accidentally call methods on nil.
  config.whiny_nils = true

  # Show full error reports and enable caching
  config.consider_all_requests_local       = true
  config.action_controller.perform_caching = true

  # Don't care if the mailer can't send
  config.action_mailer.raise_delivery_errors = false

  # Print deprecation notices to the Rails logger
  config.active_support.deprecation = :log

  # Only use best-standards-support built into browsers
  config.action_dispatch.best_standards_support = :builtin
  
  # Log the query plan for queries taking more than this (works
  # with SQLite, MySQL, and PostgreSQL)
  #config.active_record.auto_explain_threshold_in_seconds = 0.5

  # Disable assets
  config.assets.enabled = false

  # Do not compress assets
  config.assets.compress = false

  # Expands the lines which load the assets
  config.assets.debug = true
  
  # Set the log level
  config.log_level = :debug

  ############################################
  # OpenShift Configuration Below this point #
  ############################################
  conf = OpenShift::Config.new(File.join(OpenShift::Config::CONF_DIR, 'broker-dev.conf'))
  replica_sets = conf.get_bool("MONGO_REPLICA_SETS", "true")
  hp = conf.get("MONGO_HOST_PORT", "localhost:27017")
  if !hp
    raise "Broker is missing Mongo configuration."
  elsif replica_sets
    host_port = hp.split.map do |x|
      (h,p) = x.split(":")
      [h, p.to_i]
    end
  else
    (h,p) = hp.split(":")
    host_port = [h, p.to_i]
  end
  
  config.datastore = {
    :replica_set => replica_sets,
    :host_port => host_port,
  
    :user => conf.get("MONGO_USER", ""),
    :password => conf.get("MONGO_PASSWORD", ""),
    :db => conf.get("MONGO_DB", "openshift_broker_dev"),
    :collections => {:user => "user",
                     :district => "district",
                     :application_template => "template",
                     :distributed_lock => "distributed_lock"}
  }

  config.usage_tracking = {
    :datastore_enabled => conf.get_bool("ENABLE_USAGE_TRACKING_DATASTORE", "true"),
    :syslog_enabled => conf.get_bool("ENABLE_USAGE_TRACKING_SYSLOG", "false")
  }
  
  config.analytics = {
    :enabled => conf.get_bool("ENABLE_ANALYTICS", "false"), # global flag for whether any analytics should be enabled
  }
  
  config.user_action_logging = {
    :logging_enabled => conf.get_bool("ENABLE_USER_ACTION_LOG", "true"),
    :log_filepath => conf.get("USER_ACTION_LOG_FILE", "/var/log/openshift/user_action.log")
  }
  
  config.openshift = {
    :domain_suffix => conf.get("CLOUD_DOMAIN", "dev.rhcloud.com"),
    :default_max_gears => (conf.get("DEFAULT_MAX_GEARS", "3")).to_i,
    :default_gear_size => conf.get("DEFAULT_GEAR_SIZE", "small"),
    :gear_sizes => conf.get("VALID_GEAR_SIZES", "small,medium,c9").split(","),
    :community_quickstarts_url => conf.get('COMMUNITY_QUICKSTARTS_URL'),
  }
  
  config.auth = {
    # formerly the broker_auth_secret
    :salt => conf.get("AUTH_SALT", ""),
    :privkeypass => conf.get("AUTH_PRIV_KEY_PASS", ""),
    :privkeyfile => conf.get("AUTH_PRIV_KEY_FILE", ""),
    :pubkeyfile  => conf.get("AUTH_PUB_KEY_FILE", ""),
    :rsync_keyfile => conf.get("AUTH_RSYNC_KEY_FILE", ""),
  }

  config.analytics = {
    :enabled => conf.get_bool("ENABLE_ANALYTICS", "false"),
    :nurture => {
      :enabled => conf.get_bool("ENABLE_NURTURE", "false"),
      :username => conf.get("NURTURE_USERNAME", ""),
      :password => conf.get("NURTURE_PASSWORD", ""),
      :url => conf.get("NURTURE_URL", ""),
    }
  }

  config.billing = {
    :aria => {
      :config => {
        :url => "https://streamline-proxy1.ops.rhcloud.com/api/ws/api_ws_class_dispatcher.php",
        :auth_key => "sRvjFqjSadu3AFB8jRAR3tqeH5Qf6XjW",
        :client_no => 3754655
      },
      :usage_type => {
        :gear => {:small => 10014123,
                  :medium => 10014125,
                  :large => 10014127,
                  :xlarge => 10014151},
        :storage => {:gigabyte_hour => 10037755}
      },
      :default_plan => :freeshift,
      :plans => {
        :freeshift => {
          :plan_no => 10044929,
          :name => "FreeShift",
          :capabilities => {
            'max_gears' => 3,
            'gear_sizes' => ["small"]
          }
        },
        :megashift => {
          :plan_no => 10044931,
          :name => "MegaShift",
          :capabilities => {
            'max_gears' => 16,
            'gear_sizes' => ["small", "medium"],
            'max_storage_per_gear' => 30 # 30GB
          }
        }
      },
      :supp_plans => {}
    }
  }

  # Profiler config
  # See ruby-prof documentation for more info
  # :type     Type of report file: flat (default), graph, graph_html, call_tree, call_stack
  # :measure  Measured property: proc (default), wall, cpu, alloc, mem, gc_runs, gc_time
  # :sqash_threads  Only profile the current thread (def: true)
  # :squash_runtime Don't report common library calls (def: true)
  # :min_percent    Only report calls above this percentage (def: 0)
#  config.profiler = {
#    :type => 'call_tree',
#    :measure => 'wall',
#    :min_percent => 0,
#    :squash_threads => true,
#    :squash_runtime => true
#  }


end
