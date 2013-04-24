module Aria
  module Methods

    # Helper methods that force certain arguments on Aria methods and
    # unwrap output.  These methods should not catch exceptions or
    # perform complicated logic - they only exist to enforce certain 
    # call behaviors.

    def client_no
      Rails.application.config.aria_client_no
    end

    def default_plan_no
      Rails.application.config.aria_default_plan_no
    end

    def set_session(*args)
      super.session_id
    end

    def userid_exists(user_id)
      super(:user_id => user_id)
    end

    def get_client_plans_basic
      super.plans_basic
    end

    def get_client_plans_all
      super.all_client_plans
    end

    def get_client_plan_services(plan_no)
      super(:plan_no => plan_no).plan_services
    end

    def get_acct_no_from_user_id(user_id)
      super(:user_id => user_id).acct_no
    end

    def get_acct_groups_by_client
      Array(super.acct_groups)
    end

    def get_acct_groups_by_acct(acct_no)
      Array(super(:acct_no => acct_no).acct_groups)
    end

    def create_acct_complete(params)
      super encode_supplemental(params)
    end

    def update_acct_complete(acct_no, params)
      params[:acct_no] = acct_no
      super encode_supplemental(params, true)
    end

    def get_acct_details_all(acct_no)
      super(:acct_no => acct_no)
    end

    def get_acct_plans_all(acct_no)
      super(:acct_no => acct_no).all_acct_plans
    end

    def get_supp_field_values(acct_no, field_name)
      super(:acct_no => acct_no, :field_name => field_name).supp_field_values || []
    end
    def get_supp_field_value(acct_no, field_name)
      get_supp_field_values(acct_no, field_name).first
    end

    def get_reg_uss_config_params(set)
      (super(:set_name => set)['out_reg_uss_config_params'] || []).inject({}) do |h, r|
        h[r.param_name] = r.param_val
        h
      end
    end

    def clear_reg_uss_config_params(set)
      super(:set_name => set)
    end

    def set_reg_uss_config_params(set, *args)
      opts = args.extract_options!
      if args.length == 2
        super(:set_name => set, :param_name => args[0], :param_val => args[1])
      else
        names = []
        values = []
        opts.each_pair do |k,v|
          set_reg_uss_config_params(set, k, v) and next if k.to_s.include? '|' or v.to_s.include? '|'
          names << k
          values << v
        end
        super(:set_name => set, :param_name => names.join('|'), :param_val => values.join('|'))
      end
    end

    def get_usage_history(acct_no, opts)
      opts[:acct_no] = acct_no
      Array(super(opts).usage_history_records)
    rescue Aria::NoLineItemsProvided
      []
    end

    def get_acct_invoice_history(acct_no)
      Array(super(:acct_no => acct_no).invoice_history)
    end

    def get_invoice_details(acct_no, src_transaction_id)
      Array(super({:acct_no => acct_no, :src_transaction_id => src_transaction_id}).invoice_line_items)
    end

    def get_payments_on_invoice(acct_no, src_transaction_id)
      Array(super({:acct_no => acct_no, :src_transaction_id => src_transaction_id}).invoice_payments)
    rescue Aria::NoLineItemsProvided
      []
    end

    def get_acct_statement_history(acct_no, opts={})
      opts[:acct_no] = acct_no
      Array(super(opts).statement_history)
    end

    def get_acct_trans_history(acct_no, opts={})
      opts[:account_no] = acct_no
      Array(super(opts).history)
    end

    def get_client_plan_service_rates(plan_no, service_no)
      Array(super(:plan_no => plan_no, :service_no => service_no).plan_service_rates)
    end

    def get_unbilled_usage_summary(acct_no)
      super(:acct_no => acct_no)
    end

    def get_queued_service_plans(acct_no)
      Array(super(:account_number => acct_no).queued_plans)
    end

    def record_usage(acct_no, usage_type, usage_units, opts={})
      opts[:acct_no] = acct_no
      opts[:usage_type] = usage_type
      opts[:usage_units] = usage_units
      super(opts).usage_rec_no
    end

    def advance_virtual_datetime(hours)
      if Rails.env.production?
        raise "advance_virtual_datetime not allowed in production environments"
      elsif !ENV['ARIA_ADVANCE_VIRTUAL_DATETIME_ALLOWED']
        raise "ARIA_ADVANCE_VIRTUAL_DATETIME_ALLOWED is not set"
      else
        super({:offset_hours => hours})
      end
    end

    private
      def encode_supplemental(params, update=false)
        if supplemental = params.delete(:supplemental)
          names, values = [], []
          supplemental.keys.sort.each do |k|
            v = supplemental[k]
            next if k.nil? || v.nil?
            names << k.to_s.gsub(/\|/,'_')
            values << v.to_s.gsub(/\|/,'_')
          end
          params[:supp_field_names] = names.join('|')
          params[:supp_field_values] = values.join('|')
          params[:supp_field_directives] = ([2] * values.length).join('|') if update
        end
        params
      end
  end
end
