require 'net/http'
require 'net/https'
require 'json'
require 'cgi'

class EmailConfirmController < ApplicationController

  @@ERRORS = {'user_failed_confirmation' => "Email confirmation failed",
            'user_email_failed_confirmation' => "Email confirmation failed",
            :unknown => "An unknown error has occurred"
  }
  
  def confirm_flex
    confirm(flex_path)
  end
  
  def confirm_express
    confirm(express_path)
  end
  
  def confirm_external
    registration_referrer = params[:registration_referrer]
    if registration_referrer
      path = url_for(:action => 'show',
                     :controller => 'getting_started_external',
                     :only_path => true,
                     :registration_referrer => registration_referrer)
      confirm(path)
    else
      confirm
    end
  end

  def confirm(redirect_path=express_path)
    key = params[:key]
    email = params[:emailAddress]

    @errors = {}
    if key == nil
      @errors[:invalidConfirmLinkMissingKey] = 'The confirmation link used is missing the key parameter.  Please check your link or try registering again.'
    end
    if email == nil
      @errors[:invalidConfirmLinkMissingEmail] = 'The confirmation link used is missing the emailAddress parameter.  Please check your link or try registering again.'
    end
    
    # Run validations
    valid = @errors.length == 0

    # Stop if you have a validation error
    render :error and return unless valid

    begin
      url = URI.parse(Rails.configuration.streamline + Rails.configuration.streamline_service_base_url + '/confirm.html?key=' + key + '&emailAddress=' + CGI::escape(email))
      req = Net::HTTP::Get.new(url.path + '?' + url.query)
      http = Net::HTTP.new(url.host, url.port)
      if url.scheme == "https"
        http.use_ssl = true
        http.verify_mode = OpenSSL::SSL::VERIFY_NONE
      end
      response = http.start {|http| http.request(req)}
      case response
      when Net::HTTPSuccess
        logger.debug "HTTP response from server is:"
        logger.debug "Response body: #{response.body}"

        begin
          result = JSON.parse(response.body)
          if (result['errors'])
            errors = result['errors']
            if errors[0] == 'user_already_registered'
              #success
            else
              errors.each { |error|
                if (@@ERRORS[error])
                  @errors[error] = @@ERRORS[error]
                else
                  @errors[:unknown] = @@ERRORS[:unknown]
                end
              }
            end
          elsif result['emailAddress']
            #success
          else
            @errors[:unknown] = @@ERRORS[:unknown]
          end
        rescue Exception => e
          logger.error e
          @errors[:unknown] = @@ERRORS[:unknown]
        end
      else
        logger.error "Problem with server. Response code was #{response.code}"
        logger.error "HTTP response from server is #{response.body}"
        @errors[:unknown] = @@ERRORS[:unknown]
      end

    rescue Exception => e
      logger.error e
      @errors[:unknown] = @@ERRORS[:unknown]
    ensure
      if (@errors.length > 0)
        render :error and return
      else
        reset_sso
        reset_session
        session[:confirm_flow] = true
        session[:confirm_login] = email
        redirect_to redirect_path
      end
    end
  end
end
