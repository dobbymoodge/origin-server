module OpenShift
  class AriaEvent

    EVENTS = {
      "105" => "Account Status Changed",
      "106" => "Account Status Queued for Change",
      "118" => "Account Supplemental Field Value Added",
      "119" => "Account Supplemental Field Value Modified"
    }
    PLAN_STATE_UPDATE_RETRIES = 3
    PLAN_STATE_UPDATE_RETRY_TIME = 3

    def self.handle_event(h)
      aria_config = Rails.application.config.billing[:config]
      h['event_id'].each do |ev|
        case ev.to_i
        when 105, 106
          # "-1" => "Suspended", "-2" => "Cancelled", "-3" => "Terminated"
          if h['status_cd'] < "0"
            mark_acct_canceled(h)
            if ev.to_i == 106
              h['effective_date'] = get_end_of_month(h)
            else
              h['effective_date'] = h['created']
            end
            h['old_plan_name'] = h['plan_name']
            h['plan_name'] = nil
            send_entitlements(h)
          end
        when 118, 119
          supp_field_info = get_supplemental_fields(h)
          if supp_field_info
            h['effective_date'] = h['created']
            subject = "Openshift Notification - Account Info Modified"
            body = populate_contact_info(h, supp_field_info)
            email_to = aria_config[:event_acct_modif_email]
            OpenShift::AriaNotification.report_event(subject, body, email_to)
          end
        else
          Rails.logger.error "Invalid Event, id: #{ev}"
        end
      end
    end
   
    def self.send_entitlements(h)
      billing_config = Rails.application.config.billing
      aria_config = billing_config[:config]
      aria_plans = billing_config[:plans]
      default_plan = billing_config[:default_plan]

      if h['old_plan_name'] and (aria_plans[default_plan][:name] != h['old_plan_name'])
        subject = "Openshift Notification - Revoke Entitlements"
        email_to = aria_config[:event_plan_revoke_email]
        body = populate_plan_info(h, h['old_plan_name'])
        OpenShift::AriaNotification.report_event(subject, body, email_to)
      end
      if h['plan_name'] and (aria_plans[default_plan][:name] != h['plan_name'])
        subject = "Openshift Notification - Assign Entitlements"
        email_to = aria_config[:event_plan_assign_email]
        body = populate_plan_info(h, h['plan_name'])
        OpenShift::AriaNotification.report_event(subject, body, email_to)
      end
    end

    private

    def self.get_end_of_month(h)
      year, month, skip = h['created'].split('-').map { |x| x.to_i }
      day = (Date.new(year, 12, 31) << (12-month)).day
      "#{year}-#{month}-#{day}"
    end

    def self.get_login(h)
      unless h['login']
        begin
          user = CloudUser.find_by(usage_account_id: h['acct_no'])
          h['login'] = user.login if user
        rescue
          #Ignore
        end
      end
      h['login']
    end

    def self.get_account_data(h, plan_name, base_info=false)
      base_data = <<MSG
Operating Unit: #{h['operating_unit']}

Account Data
-----------------------------------
RHLogin: #{get_login(h)}
Aria Client#: #{h['acct_no']}
Aria PO#: #{h['transaction_id']}
MSG
      if base_info
        data = ""
      else
        billing_config = Rails.application.config.billing
        aria_plans = billing_config[:plans]
        sku = ""
        aria_plans.values.each do |plan|
          if plan[:name] == plan_name
            sku = plan[:sku] if plan[:sku]
            break
          end
        end
        sku += " (#{plan_name})"
        data = <<MSG

Sku: #{sku}
Qty: #{h['plan_units']}
Effective: #{h['effective_date']}
MSG
      end
      base_data + data
    end

    def self.get_account_contact(h)
      user_info = nil
      auth_service = OpenShift::AuthService.instance
      if auth_service.respond_to?('get_user_info')
        user_info = auth_service.get_user_info(get_login(h))
      end
      return if user_info.nil? or user_info.empty?
      
      billing_config = Rails.application.config.billing
      billing_config[:config][:gss_operating_units].each do |ou_name, ou_values|
        if ou_values.include?(user_info['country'])
          h['operating_unit'] = ou_name.to_s
          break
        end
      end
      data = <<MSG
End User Contact
-----------------------------------
First Name: #{user_info['firstName']}
Last Name: #{user_info['lastName']}
Company Name: #{user_info['company']}
Address1: #{user_info['address1']}
Address2: #{user_info['address2']}
City: #{user_info['city']}
State/Province: #{user_info['state']}
Postal Code: #{user_info['postalCode']}
Country: #{user_info['country']}
Phone: #{user_info['phoneNumber']}
Email: #{user_info['emailAddress']}
MSG
    end

    def self.get_billing_data
      data = <<MSG
Billing Data
-----------------------------------
Company Name: Aria Systems
MSG
    end

    def self.get_supplemental_fields(h)
      supp_fields = ""
      begin
        for i in 0..h['supp_field_name'].length-1 do
          next if h['supp_field_name'][i] == 'RHLogin'  # skip RHLogin, already listed in Account Data section
          supp_fields += "#{h['supp_field_name'][i]}: #{h['supp_field_value'][i]}\n"
        end 
      rescue
        # Ignore
      end  
      return if supp_fields.empty?
      data = <<MSG
Supplemental Fields
-----------------------------------
#{supp_fields}
MSG
    end

    def self.populate_contact_info(h, supp_field_info)
      acct_contact = get_account_contact(h)
      acct_data = get_account_data(h, nil, true)
      body = <<MSG
#{acct_data}
#{acct_contact}
#{supp_field_info}
MSG
    end
   
    def self.populate_plan_info(h, plan_name)
      supp_field_info = get_supplemental_fields(h)
      acct_contact = get_account_contact(h)
      acct_data = get_account_data(h, plan_name)
      body = <<MSG
#{acct_data}
#{acct_contact}
MSG
      body + supp_field_info.to_s + get_billing_data
    end

    def self.mark_acct_canceled(h)
      begin
        login = get_login(h)
        Rails.logger.error "Unable to find 'RHLogin' field for the event: #{h}" if login.empty?
        filter = {:login => login, :pending_plan_id => nil, :pending_plan_uptime => nil}
        update = {"$set" => {:pending_plan_id => :free, :pending_plan_uptime => Time.now.utc, :plan_state => CloudUser::PLAN_STATES['canceled']}}
        user = nil
        OpenShift::AriaEvent::PLAN_STATE_UPDATE_RETRIES.times do 
          user = CloudUser.with(consistency: :strong).where(filter).find_and_modify(update, {:new => true})
          break if user
          sleep OpenShift::AriaEvent::PLAN_STATE_UPDATE_RETRY_TIME
        end
        Rails.logger.error "Failed to change plan state to 'canceled' for user '#{login}'. Event: #{h}" unless user
      rescue Exception => e
        Rails.logger.error e.message
        Rails.logger.error e.backtrace.inspect
      end 
    end
  end
end
