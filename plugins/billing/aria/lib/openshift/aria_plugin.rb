require 'rubygems'

module OpenShift
  class AriaPlugin < OpenShift::BillingService
    attr_accessor :ah, :url, :usage_type

    def initialize(access_info=nil)
      super()
      if access_info != nil
        # no-op
      elsif defined? Rails
        access_info = Rails.application.config.billing
      else
        raise Exception.new("Aria Billing Api service is not initialized")
      end
      @url = access_info[:config][:url]
      @usage_type = access_info[:usage_type]
      @ah = OpenShift::AriaApiHelper.instance(access_info)
      @plans = access_info[:plans]
    end

    def self.instance
      OpenShift::AriaPlugin.new
    end

    def self.get_provider_name
      "Aria"
    end

    def get_billing_usage_type(urec)
      billing_usage_type = nil
      err_msg = "Billing usage type NOT supported for '#{urec['usage_type']}'."
      case urec['usage_type']
      when UsageRecord::USAGE_TYPES[:gear_usage]
        if @usage_type[:gear][urec['gear_size'].to_sym]
          billing_usage_type = @usage_type[:gear][urec['gear_size'].to_sym]
        elsif Rails.configuration.openshift[:gear_sizes].include?(urec['gear_size'])
          return billing_usage_type
        else
          print_error(err_msg, urec)
          return billing_usage_type
        end 
      when UsageRecord::USAGE_TYPES[:addtl_fs_gb]
        billing_usage_type = @usage_type[:storage][:gigabyte]
      when UsageRecord::USAGE_TYPES[:premium_cart]
        billing_usage_type = @usage_type[:cartridge][urec['cart_name'].to_sym]
      end
      raise Exception.new err_msg unless billing_usage_type
      billing_usage_type
    end

    # Compute Usage time, if needed query aria to get partial synced usage
    def get_usage_time(urec)
      billing_usage_type = get_billing_usage_type(urec)
      if urec['acct_no'] and billing_usage_type and urec['sync_time']
        found = false
        usages = get_usage_history(urec['acct_no'], billing_usage_type)
        usages.each do |usage|
          gear_id = usage["qualifier_1"]
          app_name = usage["qualifier_2"]
          sync_time = usage["qualifier_3"]
          sync_identifier = usage["qualifier_4"]
          if (urec['sync_time'].to_i == sync_time.to_i) && (urec['app_name'] == app_name) &&
             (urec['gear_id'].to_s == gear_id.to_s) && (urec['time'].to_i == sync_identifier.to_i)
            found = true
            break
          end
        end
        if found
          print_warning "Usage already posted to billing vendor but not removed from mongo datastore."\
                        "Resetting begin_time to previous sync_time.", urec
          urec['time'] = adjust_to_aria_time(urec['sync_time'])
        end
      end
      total_time = 0
      if urec['end_time'] > urec['time']
        total_time = (urec['end_time'] - urec['time']) / 3600 #hours
      end
      total_time
    end

    def get_usage_date(srec)
      mid_time_epoch = (srec['time'].to_i + srec['end_time'].to_i)/2
      Time.at(mid_time_epoch).strftime("%Y-%m-%d %H:%M:%S")
    end

    def preprocess_user_srecs(user_srecs)
      new_srecs = []
      # Split usage between plan changes
      user_srecs.each do |srec|
        billing_usage_type = get_billing_usage_type(srec)
        next unless billing_usage_type
        srec['billing_usage_type'] = billing_usage_type
        srec['time'] = adjust_to_aria_time(srec['time'])
        srec['end_time'] = adjust_to_aria_time(srec['end_time'])

        if srec['plan_history'] and !srec['plan_history'].empty?
          begin_time = srec['time']
          set_no_update = false
          # Sort plan history: Plan history can be out of order due to downgrades where end time will be end of month.
          sorted_plan_history = srec['plan_history'].sort_by { |plan| plan['end_time'] }

          sorted_plan_history.each do |old_plan|
            old_plan_end_time = adjust_to_aria_time(old_plan['end_time'])

            if (begin_time < old_plan_end_time) and (srec['end_time'] >= old_plan_end_time)
              new_srec = srec.dup
              new_srec['time'] = begin_time
              new_srec['end_time'] = old_plan_end_time
              new_srec['usage'] = get_usage_time(new_srec)
              set_no_update ? (new_srec['no_update'] = true) : (set_no_update = true)
              new_srecs << new_srec
              begin_time = old_plan_end_time
            end
          end
          new_srec = srec.dup
          new_srec['time'] = begin_time
          new_srec['usage'] = get_usage_time(new_srec)
          if set_no_update
            new_srec['no_update'] = true
          end
          new_srecs << new_srec
        else
          new_srecs << srec
        end
      end

      user_srecs = new_srecs
      new_srecs = []
      # Split usage between months
      user_srecs.each do |srec|
        if srec['time'].month != srec['end_time'].month
          month_begin_time = Time.new(srec['end_time'].year, srec['end_time'].month)
          new_srec = srec.dup
          srec['end_time'] = month_begin_time
          srec['usage'] = get_usage_time(srec)

          new_srec['time'] = month_begin_time
          new_srec['usage'] = get_usage_time(new_srec)
          new_srec['no_update'] = true
          new_srecs << new_srec
        end
        new_srecs << srec
      end
      new_srecs
    end

    def sync_usage(session, user_srecs, sync_time)
      return if user_srecs.empty?
    
      user_srecs = preprocess_user_srecs(user_srecs)
      return if user_srecs.empty?

      # Saving sync time before sending usage data to billing vendor
      user_ids = user_srecs.map { |rec| rec['_id'] unless rec['no_update']}
      session.with(safe:true)[:usage_records].find({_id: {"$in" => user_ids}}).update_all({"$set" => {sync_time: sync_time}})

      # Prepare for bulk usage reporting
      acct_nos = []
      usage_types = []
      usage_units = []
      usage_dates = []
      gear_ids = []
      app_names = []
      sync_identifiers = []
      continue_user_ids = []
      ended_srecs = []
      user_srecs.each do |srec|
        if srec['no_update']
          # Ignore
        elsif !srec['ended']
          continue_user_ids << srec['_id']
        else
          ended_srecs << srec
        end
        next if srec['usage'] == 0
        acct_nos << srec['acct_no']
        usage_types << srec['billing_usage_type']
        usage_units << srec['usage']
        usage_dates << get_usage_date(srec)
        gear_ids << srec['gear_id'].to_s
        app_names << srec['app_name']
        sync_identifiers << srec['time'].to_i
      end
      # Send usage in bulk to billing vendor
      update_query = {"$set" => {event: UsageRecord::EVENTS[:continue], time: sync_time, sync_time: nil}}
      if (acct_nos.size == 0) or bulk_record_usage(acct_nos, usage_types, usage_units, gear_ids, app_names, sync_time, sync_identifiers, usage_dates)
        # For non-ended usage records: set event to 'continue'
        session.with(safe:true)[:usage_records].find({_id: {"$in" => continue_user_ids}}).update_all(update_query) unless continue_user_ids.empty?
        # For ended usage records: delete from mongo
        delete_ended_urecs(session, ended_srecs)
      else 
        # Bulk reporting failed. bulk_record_usage api doesn't tell which accounts/records failed to report.
        # Try to sync the failed ones one at a time and unset sync_time only for sucessful reported records.
        print_warning "Bulk usage reporting failed for accounts:[#{acct_nos.join(',')}], trying one at a time"
        continue_user_ids = []
        ended_srecs = []
        ignore_srecs = []
        # Recalculate usage
        user_srecs.each do |srec|
          if srec['usage'] != 0
            begin
              srec['usage'] = get_usage_time(srec)
            rescue Exception => e
              print_error(e.message, srec)
              Rails.logger.error e.backtrace.inspect
              # Ignore processing this record this time
              ignore_srecs << srec
              next
            end
          end
        end
        user_srecs -= ignore_srecs

        user_srecs.each do |srec|
          if (srec['usage'] == 0) or
             record_usage(srec['acct_no'], srec['billing_usage_type'], srec['usage'], srec['gear_id'].to_s,
                          srec['app_name'], sync_time, srec['time'].to_i, get_usage_date(srec))
            if srec['no_update']
              # Ignore
            elsif !srec['ended']
              continue_user_ids << srec['_id']
            else
              ended_srecs << srec
            end
          else
            print_error "Usage reporting to billing vendor failed.", srec
          end
        end
        # For non-ended usage records: set event to 'continue'
        session.with(safe:true)[:usage_records].find({_id: {"$in" => continue_user_ids}}).update_all(update_query) unless continue_user_ids.empty?
        # For ended usage records: delete from mongo        
        delete_ended_urecs(session, ended_srecs)
      end
    end

    def send_entitlements(login, acct_no, old_plan_name, new_plan_name, effective_time, tid)
      return unless Rails.application.config.billing[:config][:enable_event_notification]
      hash = {}
      hash['login'] = login
      hash['acct_no'] = acct_no
      hash['old_plan_name'] = old_plan_name
      hash['plan_name'] = new_plan_name
      hash['plan_units'] = 1
      hash['effective_date'] = effective_time.strftime("%Y-%m-%d")
      hash['transaction_id'] = tid
      OpenShift::AriaEvent.send_entitlements(hash) 
    end

    ######################## ARIA API methods #######################

    def get_plans
      @plans
    end

    def valid_plan(plan_id)
      @plans.keys.include?(plan_id.to_sym)
    end

    def get_plan_id_from_plan_no(plan_no)
      @plans.each do |k, v|
        return k if v[:plan_no] == plan_no
      end
      return nil
    end

    # NOTE: This method is only used for *Testing*
    def create_fake_acct(*args)
      result = get_response(@ah.create_fake_acct(*args), __method__)
      result.acct_no
    end

    # NOTE: This method is only used for *Testing*
    def update_acct_contact(*args)
      get_response_status(@ah.update_acct_contact(*args), __method__)
    end

    def update_acct_status(*args)
      get_response_status(@ah.update_acct_status(*args), __method__)
    end

    def userid_exists(*args)
      get_response_status(@ah.userid_exists(*args), __method__)
    end

    def get_user_id_from_acct_no(*args)
      result = get_response(@ah.get_user_id_from_acct_no(*args), __method__)
      result.user_id
    end

    def get_acct_no_from_user_id(*args)
      result = get_response(@ah.get_acct_no_from_user_id(*args), __method__)
      result.acct_no
    end

    def record_usage(*args) 
      get_response_status(@ah.record_usage(*args), __method__)
    end

    def bulk_record_usage(*args) 
      get_response_status(@ah.bulk_record_usage(*args), __method__)
    end

    def get_usage_history(*args)
      usage_history = []
      begin
        result = get_response(@ah.get_usage_history(*args), __method__)
        usage_history = result.data["usage_history_records"]
      rescue OpenShift::AriaErrorCodeException => e
        return usage_history if e.error_code.to_s == "1008"
        Rails.logger.error e.message
        Rails.logger.error e.backtrace.inspect
        raise
      end
      usage_history
    end

    def get_acct_plans_all(*args)
      result = get_response(@ah.get_acct_plans_all(*args), __method__)
      result.data["all_acct_plans"]
    end
    
    def get_acct_details_all(*args)
      result = get_response(@ah.get_acct_details_all(*args), __method__)   
      result.data
    end

    def update_master_plan(acct_no, plan_name, is_upgrade=false, num_plan_units=1)
      begin
        get_response(@ah.update_master_plan(acct_no, plan_name, is_upgrade, num_plan_units), __method__)
        if is_upgrade
          cancel_queued_service_plan(acct_no)
        end
      rescue OpenShift::AriaErrorCodeException => e
        raise if e.error_code.to_s != "1034"
      end
      return true
    end
 
    def write_acct_comment(*args)
      get_response_status(@ah.write_acct_comment(*args), __method__)
    end
 
    def get_queued_service_plans(*args)
      result = get_response(@ah.get_queued_service_plans(*args), __method__)
      result.data['queued_plans']
    end

    def cancel_queued_service_plan(*args)
      get_response(@ah.cancel_queued_service_plan(*args), __method__)
    end

    def assign_supp_plan(*args)
      get_response_status(@ah.assign_supp_plan(*args), __method__)
    end

    def modify_supp_plan(*args)
      get_response_status(@ah.modify_supp_plan(*args), __method__)
    end

    def cancel_supp_plan(*args)
      get_response_status(@ah.cancel_supp_plan(*args), __method__)
    end

    def update_acct_supp_fields(*args)
      get_response_status(@ah.update_acct_supp_fields(*args), __method__)
    end

    def get_virtual_datetime_offset
      return 0 if Rails.env.production?
      @virtual_datetime_offset ||= get_virtual_datetime().current_offset_hours
    end

    def get_virtual_datetime(*args)
      get_response(@ah.get_virtual_datetime(*args), __method__)
    end

    private

    def adjust_to_aria_time(time)
      if time
        time + get_virtual_datetime_offset.hours
      else
        time
      end
    end

    def send(request)
      begin
        return request.execute
      rescue RestClient::RequestTimeout, RestClient::ServerBrokeConnection, RestClient::SSLCertificateNotVerified => e
        raise OpenShift::AriaException.new "Failed to access resource: #{e.message}"
      rescue RestClient::ExceptionWithResponse => e
        raise OpenShift::AriaException.new "Exception: #{e.response}, #{e.message}"
      rescue Exception => e
        raise OpenShift::AriaException.new "Failed to access resource: #{e.message}"
      end
      return nil
    end

    def convert_to_get_params(hash)
      raise OpenShift::AriaException.new "Param input is NOT a hash" unless hash.kind_of?(Hash)
      param_str = ""
      hash.each do |k, v|
        param_str += "&" if param_str != ""
        v = URI.escape(v.to_s, Regexp.new("[^#{URI::PATTERN::UNRESERVED}]"))
        param_str += "#{k}=#{v}"
      end
      param_str
    end

    def get_response(hash, method_name, ret_output=true)
      end_point = @url + '?' + convert_to_get_params(hash)
      Rails.logger.debug "Aria Billing api request: #{end_point}"
      request = RestClient::Request.new(:url => end_point, :method => :get)
      wddx_response = send(request)
      response = WDDX.load(wddx_response)
      Rails.logger.debug "Aria Billing api response: #{response.inspect}"
      if response.error_code != 0 && ret_output
        raise OpenShift::AriaErrorCodeException.new("#{method_name} failed with error message: #{response.error_msg}", response.error_code)
      end
      if ret_output
        return response
      else
        return response.error_code == 0
      end
    end

    def get_response_status(hash, method_name)
      get_response(hash, method_name, false)
    end
  end
end
