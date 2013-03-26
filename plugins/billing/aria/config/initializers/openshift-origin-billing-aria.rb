require 'openshift-origin-common'

Broker::Application.configure do
  conf_file = File.join(OpenShift::Config::PLUGINS_DIR, File.basename(__FILE__, '.rb') + '.conf')
  if Rails.env.development? or Rails.env.test?
    dev_conf_file = File.join(OpenShift::Config::PLUGINS_DIR, File.basename(__FILE__, '.rb') + '-dev.conf')
    if File.exist? dev_conf_file
      conf_file = dev_conf_file
    else
      Rails.logger.info "Development configuration for #{File.basename(__FILE__, '.rb')} not found. Using production configuration."
    end
  end
  conf = OpenShift::Config.new(conf_file)

  aria_billing_info = {
    :config => {
      :url =>       conf.get("BILLING_PROVIDER_URL"),
      :auth_key =>  conf.get("BILLING_PROVIDER_AUTH_KEY"),
      :client_no => conf.get("BILLING_PROVIDER_CLIENT_NO").to_i,
      :enable_event_notification => conf.get_bool("BILLING_PROVIDER_EVENT_NOTIFICATION", "false"),
      :event_remote_ipaddr_begin => conf.get("BILLING_PROVIDER_EVENT_REMOTE_IPADDR_BEGIN", ""),
      :event_remote_ipaddr_end   => conf.get("BILLING_PROVIDER_EVENT_REMOTE_IPADDR_END", ""),
      :event_orders_team_email   => conf.get("BILLING_PROVIDER_EVENT_ORDERS_TEAM_EMAIL", ""),
      :event_peoples_team_email  => conf.get("BILLING_PROVIDER_EVENT_PEOPLES_TEAM_EMAIL", "")
    },
    :usage_type => {
      :gear => {
        :small    => conf.get("BILLING_PROVIDER_USAGE_TYPE_GEAR_SMALL").to_i,
        :medium   => conf.get("BILLING_PROVIDER_USAGE_TYPE_GEAR_MEDIUM").to_i,
        :large    => conf.get("BILLING_PROVIDER_USAGE_TYPE_GEAR_LARGE").to_i,
        :xlarge   => conf.get("BILLING_PROVIDER_USAGE_TYPE_GEAR_XLARGE").to_i,
      },
      :storage => {
        :gigabyte => conf.get("BILLING_PROVIDER_USAGE_TYPE_STORAGE_GEAR").to_i,
      },
      :cartridge => {
        :"jbosseap-6.0" => conf.get("BILLING_PROVIDER_USAGE_TYPE_GEAR_JBOSS_EAP").to_i,
      }
    },
    :default_plan => :free,
    # Maintain the order of plans from lowest to the highest
    # Upgrade or Downgrade is decided based on this order.
    :plans => {
      :free => {
        :plan_no => conf.get("BILLING_PROVIDER_FREE_PLAN_NO").to_i,
        :name => "Free",
        :capabilities => {
          'subaccounts' => false,
          'max_gears' => 3,
          'gear_sizes' => ["small"],
          'plan_upgrade_enabled' => true
        }
      },
      :silver => {
        :plan_no => conf.get("BILLING_PROVIDER_SILVER_PLAN_NO").to_i,
        :name => "Silver",
        :capabilities => {
          'subaccounts' => false,
          'max_gears' => 16,
          'gear_sizes' => ["small", "medium"],
          'max_storage_per_gear' => 30, # 30GB
          'plan_upgrade_enabled' => true,
          'private_ssl_certificates' => true
        },
        :usage_rates => {
          :gear => { 
                    :small => { 
                               :usd => 0.05, #$/hr
                               :duration => :hour
                              },
                    :medium => {
                                :usd => 0.12, #$/hr
                                :duration => :hour
                               }
                   },
          :storage => {
                       :gigabyte => {
                                     :usd => 1.00, #$/month
                                     :duration => :month
                                    }
                      },
          :cartridge => {
                         :'jbosseap-6.0' => {
                                             :usd => 0.03, #$/hr
                                             :duration => :hour
                                            }
                        }
        }
      }
    }
  }
  config.billing = aria_billing_info
end