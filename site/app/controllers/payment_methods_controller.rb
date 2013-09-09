class PaymentMethodsController < ConsoleController
  include BillingAware
  include PaymentMethodsHelper

  before_filter :authenticate_user!
  before_filter :user_can_upgrade_plan!

  def edit
    @billing_info = current_aria_user.billing_info
    @payment_method = current_aria_user.payment_method
    @balance = current_aria_user.forwarded_balance

    @previous_payment_method = @payment_method.dup

    update_errors(@payment_method.errors, (params[:payment_method] || {})[:errors] || {})

    @payment_method.cc_no = nil
    @payment_method.mode = Aria::DirectPost.get_or_create(post_name, url_for(:action => :direct_update))
    @payment_method.session_id = current_aria_user.create_session
  end

  def direct_update
    if serve_direct?
      render :notify_parent, :layout => 'bare'
    else
      redirect_to next_path and return if @errors.empty?
      redirect_to url_for(:action => :edit, :payment_method => {:errors => @errors})
    end
  end

  def delete
  end

  def destroy
  end

  protected
    # Allow subclasses to override edit redirection behavior
    def next_path
      account_path
    end
    def post_name
      'account'
    end

    def serve_direct?
      logger.debug params.inspect
      
      @errors = (params[:error_messages] || {}).values.inject({}) do |h, v|
        key = v['error_field']
        if key == 'server_error'
          (h[:base] ||= []) << "#{v['error_key']},#{v['error_code']}"
        else
          (h[key] ||= []) << v['error_key']
        end
        h
      end
      @user = current_aria_user

      # Always clear when returning from direct_post
      # Updating payment method can change status, mark invoices paid, process payments, etc
      @user.clear_cache!

      if not @user.has_valid_payment_method? and @errors.empty?
        (@errors[:base] ||= []).unshift :unknown
      end
      params[:params] && params[:params][:params] == 'serve_direct'
    end

    # Convert these Aria errors to more generic versions
    REPLACE_ERRORS = {
      :servercardmustbe16digits => :server_card_contents,
      :servercardmustbe15digits => :server_card_contents,
      :serverlengthofccnumber   => :server_card_contents,
      :serverccnumnumeric       => :server_card_contents,
      :servercvvmissing         => :server_card_cvv,
      :servercvvmustbenumeric   => :server_card_cvv,
      :servercvvhowmanydigits   => :server_card_cvv,
    }

    def update_errors(model, errors)
      unknown_error = I18n.t(:unknown, :scope => [:aria, :direct_post])
      errors.each_pair do |attr,keys|
        logger.debug "Found keys #{keys.inspect} for #{attr}"
        Array(keys).each do |key|
          (key,code) = key.split(",")
          error_code_str = code.present? ? " (Error ##{code.to_i})" : ""
          model.add(attr, I18n.t(REPLACE_ERRORS[key.to_sym] || key, :scope => [:aria, :direct_post], :default => unknown_error) + error_code_str)
        end
      end
    end

    def active_tab
      :account
    end

    def text
      TextHelper.instance
    end
    class TextHelper
      include Singleton
      include ActionView::Helpers::TextHelper
    end
end