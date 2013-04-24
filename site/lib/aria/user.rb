
require 'delegate'

module Aria
  module User
    # mixins for Aria user integration

    def acct_no
      @acct_no ||= Aria.cached.get_acct_no_from_user_id(user_id)
    end

    def has_account?
      acct_no.present?
    rescue AccountDoesNotExist
      false
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
        Aria.get_acct_details_all(acct_no)
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
      start_date = aria_datetime(invoice.recurring_bill_from)
      end_date = aria_datetime(invoice.recurring_bill_thru)
      due_date = aria_datetime(invoice.bill_date)
      Aria::Bill.new(
        start_date,
        end_date,
        due_date,
        nil,
        invoice.line_items,
        invoice.payments,
        [],
        0,
        forwarded_balance(invoice)
      )
    end

    def next_bill
      if @next_bill.nil?
        default_plan = Rails.configuration.aria_default_plan_no.to_s
        @next_bill =
          if plan_no == default_plan && next_plan_no == default_plan
            false
          else
            start_date = aria_datetime(current_period_start_date)
            end_date = aria_datetime(current_period_end_date)
            next_bill_date = aria_datetime(account_details.next_bill_date)
            Aria::Bill.new(
              start_date,
              end_date,
              next_bill_date,
              (Aria::DateTime.today - start_date).to_i + 1,
              next_plan_recurring_line_items,
              [],
              unbilled_usage_line_items,
              unbilled_usage_balance,
              forwarded_balance
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
        Aria::UsageLineItem.for_usage(Aria.get_usage_history(acct_no, :date_range_start => current_period_start_date), plan_no).sort_by(&Aria::LineItem.plan_sort)
    end

    def unbilled_usage_balance
      @unbilled_usage_balance ||=
        Aria.get_unbilled_usage_summary(acct_no).ptd_balance_amount.to_f
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
      @invoices ||= Aria.get_acct_invoice_history(acct_no).map {|i| Aria::Invoice.new(i, acct_no) }.sort_by(&:bill_date).reverse!
    end

    def transactions
      @transactions ||= Aria.get_acct_trans_history(acct_no).sort_by(&:transaction_create_date)
    end

    def statements
      @statements ||= Aria.get_acct_statement_history(acct_no)
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
          arr = [ i.period_name, i.line_items.select(&:usage?) ]
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
      @queued_plans ||= Aria.get_queued_service_plans(acct_no)
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

      # Set the invoice template ID based on the country
      template_id = invoice_template_id(params['country'],params['bill_country'])
      params['alt_msg_template_no'] = template_id unless template_id.nil?

      # Set the account currency CD based on the billing country
      params['currency_cd'] = Aria::User.account_currency_cd(params['bill_country'])

      # Set the collection group
      params['client_coll_acct_group_ids'] = Aria::User.collections_acct_group_id(params['country'],params['bill_country'])

      Aria.create_acct_complete(params)
      true
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
      (instance_variables - [:@delegate_sd_obj, :@acct_no]).each{ |s| remove_instance_variable(s) }
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

      def self.collections_acct_group_id(country, bill_country)
        country_code = country.blank? ? bill_country : country
        Rails.configuration.collections_group_id_by_country[country_code]
      end

      def aria_datetime(s)
        Date.strptime(s, '%Y-%m-%d').to_datetime
      end
  end

  class UserContext < SimpleDelegator
    include Aria::User
  end
end
