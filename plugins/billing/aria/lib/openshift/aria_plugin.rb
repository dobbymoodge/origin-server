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
          created_at = usage["qualifier_2"]
          sync_time = usage["qualifier_3"]
          if (urec['sync_time'].to_i == sync_time.to_i) &&
             (urec['gear_id'].to_s == gear_id) && (urec['created_at'].to_i == created_at.to_i)
            found = true
            break
          end
        end
        if found
          print_warning "Usage already posted to billing vendor but not removed from mongo datastore."\
                        "Resetting begin_time to previous sync_time.", urec
          urec['time'] = urec['sync_time']
        end
      end
      total_time = 0
      if urec['end_time'] > urec['time']
        total_time = (urec['end_time'] - urec['time']) / 3600 #hours
      end
      total_time
    end

    def preprocess_user_srecs(user_srecs)
      new_srecs = []
      user_srecs.each do |srec|
        billing_usage_type = get_billing_usage_type(srec)
        next unless billing_usage_type
        srec['billing_usage_type'] = billing_usage_type
        if srec['time'].month != srec['end_time'].month
          month_begin_time = Time.new(srec['end_time'].year, srec['end_time'].month)
          new_srec = srec.dup
          srec['end_time'] = month_begin_time
          srec['usage_date'] = srec['time'].strftime("%Y-%m-%d %H:%M:%S")
          srec['usage'] = get_usage_time(srec)

          new_srec['time'] = month_begin_time
          new_srec['usage_date'] = new_srec['end_time'].strftime("%Y-%m-%d %H:%M:%S")
          new_srec['created_at'] += 1 # Make it different from orig. rec
          new_srec['no_update'] = true
          new_srec['usage'] = get_usage_time(new_srec)
          new_srecs << new_srec
        else
          srec['usage_date'] = srec['end_time'].strftime("%Y-%m-%d %H:%M:%S")
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
      created_times = []
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
        usage_dates << srec['usage_date']
        gear_ids << srec['gear_id'].to_s
        created_times << srec['created_at'].to_i
      end
      # Send usage in bulk to billing vendor
      update_query = {"$set" => {event: UsageRecord::EVENTS[:continue], time: sync_time, sync_time: nil}}
      if (acct_nos.size == 0) or bulk_record_usage(acct_nos, usage_types, usage_units, gear_ids, created_times, sync_time, usage_dates)
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
                          srec['created_at'].to_i, sync_time, srec['usage_date'])
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

    def update_master_plan(*args)
      begin
        get_response(@ah.update_master_plan(*args), __method__)
      rescue OpenShift::AriaErrorCodeException => e
        raise if e.error_code.to_s != "1034"
      end
      return true
    end
  
    def get_queued_service_plans(*args)
      result = get_response(@ah.get_queued_service_plans(*args), __method__)
      result.data['queued_plans']
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

    private

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
