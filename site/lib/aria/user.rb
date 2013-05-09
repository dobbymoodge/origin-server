
require 'delegate'

module Aria
  module User
    # mixins for Aria user integration

    def acct_no
      @acct_no ||= Aria.cached.get_acct_no_from_user_id(user_id)
    end

    def has_account?
      if @has_account.nil?
        @has_account = begin
          acct_no.present?
        rescue AccountDoesNotExist
          false
        end
      end
      @has_account
    end

    def create_session
      @session_id ||= Aria.set_session(:user_id => user_id)
    end

    def destroy_session
      Aria.kill_session(:session_id => @session_id) if @session_id
      @session_id = nil
    rescue InvalidSession
      nil
    end

    def has_valid_account?
      values = Aria.cached.get_supp_field_values(acct_no, :rhlogin)
      raise Aria::UserNoRHLogin, acct_no if values.empty?
      raise Aria::UserIdCollision, acct_no unless values.include?(login)
      true
    rescue AccountDoesNotExist
      false
    end

    def has_complete_account?
      return false unless has_valid_account?
      billing_info.valid?
    rescue AccountDoesNotExist
      false
    end

    def account_details
      @account_details ||= begin
        Aria.cached.get_acct_details_all(acct_no)
      end
    end

    def currency_cd
      account_details.currency_cd
    end

    def billing_info
      @billing_info ||= begin
        Aria::BillingInfo.from_account_details(account_details)
      rescue AccountDoesNotExist
        Aria::BillingInfo.new
      end
    end

    def contact_info
      @contact_info ||= begin
        Aria::ContactInfo.from_account_details(account_details)
      rescue AccountDoesNotExist
        Aria::ContactInfo.new
      end
    end

    # A pay_method of 0 is "Other/None", 1 is "Credit Card"
    # This may need to be changed if we accept other payment methods
    def has_valid_payment_method?
      account_details.pay_method.to_i != 0
    end

    def payment_method
      @payment_method ||= begin
        Aria::PaymentMethod.from_account_details(account_details)
      rescue AccountDoesNotExist
        Aria::PaymentMethod.new
      end
    end

    def tax_exempt
      # replace with call to get_tax_acct_status
      #@tax_exempt ||= (Aria.get_supp_field_value(acct_no, :tax_exempt) || 0).to_i
    end
    def tax_exempt?
      # tax_exempt > 0
      false
    end

    def test_user?
      account_details.is_test_acct == 'Y'
    end

    def bill_dates
      invoices_with_amounts.map(&:bill_date).uniq.sort.reverse!
    end

    def bill_for(invoice)
      return nil unless invoice
      Aria::Bill.new(
        :recurring_bill_from => aria_datetime(invoice.recurring_bill_from),
        :recurring_bill_thru => aria_datetime(invoice.recurring_bill_thru),
        :usage_bill_from => aria_datetime(invoice.usage_bill_from),
        :usage_bill_thru => aria_datetime(invoice.usage_bill_thru),
        :due_date => aria_datetime(invoice.bill_date),
        :invoice_line_items => invoice.line_items,
        :invoice_payments => invoice.payments,
        :forwarded_balance => forwarded_balance(invoice)
      )
    end

    def next_bill
      if @next_bill.nil?
        default_plan = Rails.configuration.aria_default_plan_no.to_s
        @next_bill =
          if plan_no == default_plan && next_plan_no == default_plan
            false
          else
            usage_bill_from = aria_datetime(current_period_start_date)
            Aria::Bill.new(
              :usage_bill_from => usage_bill_from,
              :usage_bill_thru => aria_datetime(current_period_end_date),
              :due_date => aria_datetime(account_details.next_bill_date),
              :day => (Aria::DateTime.today - usage_bill_from).to_i + 1,
              :invoice_line_items => next_plan_recurring_line_items,
              :unbilled_usage_line_items => unbilled_usage_line_items,
              :unbilled_usage_balance => unbilled_usage_balance,
              :forwarded_balance => forwarded_balance
            )
          end
      end
      @next_bill
    end

    def current_period_start_date
      if account_details.last_arrears_bill_thru_date
        (account_details.last_arrears_bill_thru_date.to_date + 1.day).to_s
      else
        account_details.created
      end
    end

    def current_period_end_date
      (account_details.next_bill_date.to_date - 1.day).to_s
    end

    def unbilled_usage_line_items
      @unbilled_usage_line_items ||=
        Aria::UsageLineItem.for_usage(Aria.cached.get_usage_history(acct_no, :date_range_start => current_period_start_date), plan_no).sort_by(&Aria::LineItem.plan_sort)
    end

    def unbilled_usage_balance
      @unbilled_usage_balance ||=
        Aria.cached.get_unbilled_usage_summary(acct_no).ptd_balance_amount.to_f
    end

    def unpaid_invoices
      invoices.reject{ |i| i.paid_date }
    end

    def paid_invoices
      invoices.select{ |i| i.paid_date.nil? }
    end

    def invoices_with_amounts
      invoices.select {|i| i.debit != 0 || i.credit != 0 }
    end

    def usage_invoices
      invoices.select(&:usage_bill_from)
    end

    def invoices
      @invoices ||= Aria.cached.get_acct_invoice_history(acct_no).map {|i| Aria::Invoice.new(i, acct_no) }.sort.reverse!
    end

    def transactions
      @transactions ||= Aria.cached.get_acct_trans_history(acct_no).sort_by(&:transaction_create_date)
    end

    def statements
      @statements ||= Aria.cached.get_acct_statement_history(acct_no)
    end

    def forwarded_balance(invoice=nil)
      if invoice
        transaction = transactions.find {|t| t.transaction_type == 1 && t.transaction_source_id == invoice.invoice_no }
        statement = statements.find {|s| s.statement_no == transaction.statement_no } if transaction
        return statement.balance_forward_amount if statement
        return 0
      else
        unpaid_invoices.inject(0) {|balance, i| balance + i.debit - i.credit}
      end
    end

    def past_usage_line_items(periods=3)
      Hash[
        usage_invoices.slice(0, periods).inject([]) { |a, i| 
          arr = [ i.usage_period_name, i.line_items.select(&:usage?) ]
          a << arr if arr.last.present?
          a
        }
      ]
    end

    def plan_no
      account_details.plan_no
    end

    def next_plan_no
      if plan = queued_plans.last
        plan.new_plan_no.to_s
      else
        plan_no
      end
    end

    def default_plan_pending?
      next_plan_no == Rails.configuration.aria_default_plan_no.to_s && 
        plan_no != Rails.configuration.aria_default_plan_no.to_s
    end

    def next_plan_recurring_line_items
      @next_plan_recurring_line_items ||= begin
          if plan = queued_plans.last
            Aria::RecurringLineItem.find_all_by_plan_no(plan.new_plan_no.to_s)
          else
            Aria::RecurringLineItem.find_all_by_current_plan(acct_no)
          end
        end
    end

    def queued_plans
      @queued_plans ||= Aria.cached.get_queued_service_plans(acct_no)
    end

    def create_account(opts=nil)
      params = default_account_params
      validates = true
      opts.each_pair do |k,v|
        if v.respond_to? :to_aria_attributes
          params.merge!(v.to_aria_attributes)
        else
          params[k] = v
        end
        validates &= v.valid? if v.respond_to? :valid?
      end if opts
      return false unless validates

      # Set the invoice template ID
      # Try the account country first, which is coming from Streamline if the
      # user has a pre-existing RHN account, then fall back to the billing country
      template_id = invoice_template_id(params['country'],params['bill_country'])
      params['alt_msg_template_no'] = template_id unless template_id.nil?

      # Set the account currency based on the billing country
      params['currency_cd'] = Aria::User.account_currency_cd(params['bill_country'])

      # Set the collection group; always keyed to billing country
      params['client_coll_acct_group_ids'] = Aria::User.collections_acct_group_id(params['bill_country'])

      # Set the functional group and sequence group
      # Try the account country first, which is coming from Streamline if the
      # user has a pre-existing RHN account, then fall back to the billing country
      params['functional_acct_groups'] = params['seq_func_group_no'] = Aria::User.functional_acct_group_no(params['country'],params['bill_country'])

      begin
        Aria.create_acct_complete(params)
        true
      ensure
        clear_cache!
      end
    rescue Aria::AccountExists
      raise
    rescue Aria::Error => e
      errors.add(:base, e.to_s)
      false
    end

    def update_account(opts)
      params = HashWithIndifferentAccess.new
      validates = true
      opts.each_pair do |k,v|
        if v.respond_to? :to_aria_attributes
          params.merge!(v.to_aria_attributes('update'))
        else
          params[k] = v
        end
        validates &= v.valid? if v.respond_to? :valid?
      end
      return false unless validates

      Aria.update_acct_complete(acct_no, params)
      clear_cache!
      true
    rescue Aria::Error => e
      errors.add(:base, e.to_s)
      false
    end

    def cancel_queued_service_plan
      @queued_plans = nil
      Aria.cancel_queued_service_plan :account_number => acct_no
    end

    def set_session_redirect(url)
      set_reg_uss_params('redirecturl', url)
    end

    def clear_cache!
      (instance_variables - [:@delegate_sd_obj, :@mocha, :@acct_no]).each{ |s| remove_instance_variable(s) }
    ensure
      Rails.cache.delete([Aria::User.name, "acct_no", acct_no]) if has_account? rescue nil
    end

    def self.cache_key(acct_no)
      Rails.cache.fetch([Aria::User.name, "acct_no", acct_no]) { [acct_no, Time.now.strftime("%Y-%m-%d %H:%M:%S.%N") ] }
    end

    private
      def user_id
        Digest::MD5::hexdigest(login)
      end
      def random_password
        ::SecureRandom.base64(16)[0..12].gsub(/[^a-zA-Z0-9]/,'_') # Max allowed Aria limit
      end

      def set_reg_uss_params(name, value)
        Aria.set_reg_uss_params({
          :session_id => create_session,
          :param_name => name,
          :param_val => value,
        })
      end

      def default_account_params
        HashWithIndifferentAccess.new({
          :userid => user_id,
          :status_cd => 0,
          :master_plan_no => Aria.default_plan_no,
          :password => random_password,
          :alt_bill_day => 1,
          :test_acct_ind => Rails.application.config.aria_force_test_users ? 1 : 0,
          :supplemental => {:rhlogin => login},
        })
      end

      def invoice_template_id(country, bill_country)
        country_code = country.blank? ? bill_country : country
        Rails.configuration.aria_invoice_template_id_map[country_code]
      end

      def self.account_currency_cd(bill_country)
        return Rails.configuration.default_currency.to_s if bill_country.blank?
        Rails.configuration.currency_cd_by_country[bill_country]
      end

      def self.collections_acct_group_id(bill_country)
        Rails.configuration.collections_group_id_by_country[bill_country]
      end

      def self.functional_acct_group_no(country, bill_country)
        country_code = country.blank? ? bill_country : country
        Rails.configuration.functional_group_no_by_country[country_code]
      end

      def aria_datetime(s)
        Date.strptime(s, '%Y-%m-%d').to_datetime if s
      end
  end

  class UserContext < SimpleDelegator
    include Aria::User
  end
end
