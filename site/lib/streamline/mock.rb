require 'base64'
#
# This mixin module mocks the calls that are used
# for the streamline interface
#
module Streamline
  module Mock

    #
    # Establish the user state based on the current ticket
    #
    # Returns the login
    #
    def establish
      self.rhlogin ||= Base64.decode64(ticket) || "openshift@redhat.com"

      set_fake_roles unless instance_variable_get(:@roles)
      self
    end

    def terms
      @terms ||= establish_terms
    end

    def roles!
      establish
      roles
    end

    #
    # Get the user's email address
    #
    def load_email_address
      @email_address = if rhlogin.present? && !rhlogin.index('@')
          @email_address = "#{rhlogin}@rhn.com"
        else
          @email_address = rhlogin
        end
    end

    def establish_terms
      if @rhlogin == nil || @rhlogin == 'terms+test@redhat.com'
        @terms = [{"termId"=>1046, "termUrl"=>"http://openshift.redhat.com/app/legal/pdf/services_agreement.pdf", "termTitle"=>"OpenShift Online Site Terms"},
                  {"termId"=>1, "termUrl"=>"http://www.redhat.com/legal/legal_statement.html", "termTitle"=>"Red Hat Site Terms"},
                  {"termId"=>1010, "termUrl"=>"https://access.redhat.com/help/terms_conditions.html", "termTitle"=>"Red Hat Portals Terms of Use"}]
      else
        @terms = []
      end
    end

    def accept_terms
      @terms = []
    end

    def refresh_roles(force=false)
    end

    def change_password(args=nil)
      if args.nil?
        if valid? :change_password
          return true
        else
          if @old_password == 'invalid_old_password'
            errors.add :old_password, "Your old password is not valid"
          end
          return false
        end
      end
      return {'errors' => ['password_invalid']} unless args['newPassword'] == args['newPasswordConfirmation']
      return {'errors' => ['password_incorrect']} if args['oldPassword'] == 'invalid_old_password'
      return {}
    end

    def request_password_reset(args)
      Rails.logger.debug "Requesting password reset"
      if args.is_a? String
        valid? :reset_password
      else
        {}
      end
    end

    def reset_password(args=nil)
      if args.nil?
        valid? :change_password
      else
        {}
      end
    end

    def complete_reset_password(token)
      raise Streamline::TokenExpired if token.blank? || token == 'expired'
      true
    end

    def authenticate!(login, password)
      self.rhlogin = login
      self.ticket = nil
      Rails.logger.debug "Authenticating user #{login}"

      if login.present? and password.present?
        @ticket = Base64.strict_encode64(login)
        @rhlogin = login
        set_fake_roles
      else
        raise Streamline::StreamlineException, "Bad stuff"
      end
      self
    end

    def logout
    end

    #
    # Register a new streamline user
    #
    def register(confirm_url, promo_code=nil)
      Rails.logger.warn("Non integrated environment - passing through #{promo_code}")
    end

    def confirm_email(key, email=@email_address)
      raise "No email address provided" unless email
      true
    end

    #
    # Request access to a cloud solution
    #
    def request_access(solution)
      @roles << CloudAccess.auth_role(solution)
    end

    #
    # Whether the user is authorized for a given cloud solution
    #
    def has_access?(solution)
      if @rhlogin == 'allaccess+test@redhat.com'
        true
      else
        !@roles.index(CloudAccess.auth_role(solution)).nil?
      end
    end

    #
    # Whether the user has already requested access for a given cloud solution
    #
    def has_requested?(solution)
      if @rhlogin == 'allaccess+test@redhat.com'
        false
      else
        !@roles.index(CloudAccess.req_role(solution)).nil?
      end
    end

    def entitled?
      return true if @rhlogin == 'allaccess+test@redhat.com'

      return true if roles.include?('cloud_access_1')
      if roles.include?('cloud_access_request_1')
        false
      else
        refresh_roles(true)
        true
      end
    end

    def waiting_for_entitle?
      if @rhlogin == 'allaccess+test@redhat.com'
        true
      else
        not roles.include?('cloud_access_1') and roles.include?('cloud_access_request_1')
      end
    end

    def user_info!
      if full_user?
        {"last_name"=>"Test",
         "greeting"=>"Mr.",
         "state"=>"TX",
         "address1"=>"123 Address",
         "address2"=>nil,
         "address3"=>nil,
         "city"=>"SOMEWHERE",
         "country"=>"US",
         "title"=>"Software",
         "postal_code"=>"12345",
         "phone_number"=>"000-000-0000",
         "company"=>"Red Hat",
         "login"=>login,
         "first_name"=>"User"}
      else
        {
          "login"=>login,
        }
      end
    end

    def promote(*args)
      @streamline_type = :full
      @roles = ['authenticated']
      true
    end

    def streamline_type!
    end

    private
      def set_fake_roles
        @roles, @email_address = if @rhlogin.index '@'
          @streamline_type = :simple
          [["simple_authenticated"], @rhlogin]
        else
          @streamline_type = :full
          [["authenticated"], "#{@rhlogin}@rhn.com"]
        end
      end
  end

  class MockContext < SimpleDelegator
    include Streamline::Mock
  end
end
