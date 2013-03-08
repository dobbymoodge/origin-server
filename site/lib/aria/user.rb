require 'delegate'

module Aria
  module User
    # mixins for Aria user integration

    def acct_no
      @acct_no ||= Aria.cached.get_acct_no_from_user_id(user_id)
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

    def billing_info
      @billing_info ||= begin
        Aria::BillingInfo.from_account_details(account_details)
      rescue AccountDoesNotExist
        Aria::BillingInfo.new
      end
    end

    def has_valid_payment_method?
      account_details.status_cd.to_i > 0
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

    def unbilled_usage_line_items
      @unbilled_usage_line_items ||=
        Aria::UsageLineItem.for_usage(Aria.get_usage_history(acct_no, :date_range_start => account_details.last_bill_date), account_details.plan_no)
    end

    def unbilled_balance
      @unbilled_balance ||=
        Aria.get_unbilled_usage_summary(acct_no)
    end

    def unpaid_invoices
      invoices.select{ |i| i.paid_date.blank? }
    end

    #
    # In order of bill date
    #
    def paid_invoices
      invoices.select{ |i| i.paid_date.present? }
    end

    def invoices
      @invoices ||= Aria.get_acct_invoice_history(acct_no)
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
          params.merge!(v.to_aria_attributes)
        else
          params[k] = v
        end
        validates &= v.valid? if v.respond_to? :valid?
      end
      return false unless validates

      Aria.update_acct_complete(acct_no, params)
      @billing_info = nil
      @account_details = nil
      #@tax_exempt = nil
      true
    rescue Aria::Error => e
      errors.add(:base, e.to_s)
      false
    end

    def set_session_redirect(url)
      set_reg_uss_params('redirecturl', url)
    end

    private
      def user_id
        Digest::MD5::hexdigest(login)
      end
      def random_password
        ::SecureRandom.base64(16)[0..12].gsub(/[^a-zA-Z0-9]/,'_') # Max allowed Aria limit
      end

      # Checks whether the basic Aria account exists, but not whether
      # it is valid.
      def has_account?
        Aria.userid_exists user_id
        true
      rescue AccountDoesNotExist
        false
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
          :test_acct_ind => Rails.application.config.aria_force_test_users ? 1 : 0,
          :supplemental => {:rhlogin => login},
        })
      end
  end

  class UserContext < SimpleDelegator
    include Aria::User
  end
end
