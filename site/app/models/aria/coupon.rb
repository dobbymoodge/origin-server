module Aria
  class Coupon < Base
    define_attribute_method :coupon_code

    def messages
      @messages ||= []
    end

    def blank?
      coupon_code.blank?
    end

    # Applies a coupon named "external<coupon_code>" to the user's account
    # Returns true if the coupon was already applied, or is successfully applied. Result messages are available in the coupon.messages array
    # Returns false with errors attached to the coupon_code field if the coupon wasn't applied
    def apply_to_acct(user_or_acct_no)
      messages.clear
      acct_no = user_or_acct_no.respond_to?(:acct_no) ? user_or_acct_no.acct_no : user_or_acct_no
      coupon_message = Aria.apply_coupon_to_acct(acct_no, "external-#{coupon_code}".downcase).user_success_msg
      messages.push("The coupon was successfully applied.")
      messages.push(coupon_message) if coupon_message.present?
      true
    rescue Aria::CouponExists => e
      messages.push("The coupon was already applied to your account.")
      true
    rescue Aria::CouponDoesNotExist
      errors.add(:coupon_code, "Invalid coupon code")
      false
    rescue Exception => e
      Rails.logger.error "Error applying coupon: #{e}\n#{e.backtrace.join("\n  ")}"
      errors.add(:coupon_code, "The coupon could not be applied")
      false
    end
  end
end