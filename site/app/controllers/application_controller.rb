class ApplicationController < ActionController::Base
  include Console::Rescue
  include Console::CommunityAware
  include Secured
  include AsyncAware
  include BillingAware

  protect_from_forgery

  rescue_from AccessDeniedException, :with => :access_denied
  rescue_from 'Aria::ResourceNotFound', :with => :resource_not_found
  rescue_from 'Streamline::Error',
              'Aria::Error', 'Aria::NotAvailable',
              :with => :generic_error
  rescue_from :with => :generic_error

  helper_method :account_settings_redirect, :active_tab

  protected
    def handle_unverified_request
      raise Console::AccessDenied, "Request authenticity token does not match session #{session.inspect}"
    end

    def set_no_cache
      response.headers["Cache-Control"] = "no-cache, no-store, max-age=0, must-revalidate"
      response.headers["Pragma"] = "no-cache"
      response.headers["Expires"] = "Fri, 01 Jan 1990 00:00:00 GMT"
    end

    def terms_redirect
      redirect = session[:terms_redirect]
      session[:terms_redirect] = nil
      redirect || default_after_login_redirect
    end

    def terms_redirect=(redirect)
      session[:terms_redirect] = redirect
    end

    def remote_request?(referrer)
      referrer.present? && referrer.host && (
        (request.host != referrer.host) || !referrer.path.start_with?('/app')
      )
    end

    def server_relative_uri(s)
      return nil unless s.present?
      uri = URI.parse(s).normalize
      uri.path = nil if uri.path[0] != '/'
      uri.query = nil if uri.query == '?'
      return nil unless uri.path.present? || uri.query.present?
      scheme, host, port = uri.scheme, uri.host, uri.port if request.host == uri.host && uri.port == 8118 && ['http', 'https'].include?(uri.scheme)
      URI::Generic.build([scheme, nil, host, port, nil, uri.path, nil, uri.query.presence, nil]).to_s
    rescue
      nil
    end

    def sauce_testing?
      retval = false
      if Rails.env.development?
        logger.debug "------"
        logger.debug "Checking for Sauce testing credentials"
        logger.debug request.cookies.to_yaml

        key = 'sauce_testing'
        logger.debug "cookie: #{request.cookies[key]}"
        retval = true if (request.cookies[key] == 'true')

        logger.debug "------"
      end

      logger.debug "========== TESTING ===========" if retval
      retval
    end

    def generic_error(e=nil, message=nil, alternatives=nil)
      @reference_id = request.uuid
      logger.error "Unhandled exception reference ##{@reference_id}: #{e.message}\n#{e.backtrace.join("\n  ")}"
      @message, @alternatives = message, alternatives
      render 'console/error', :layout => 'console'
    end

    def access_denied(e)
      logger.debug "Access denied: #{e}"
      redirect_to logout_path :cause => e.message, :then => account_path
    end
    def console_access_denied(e)
      access_denied(e)
    end

    def account_settings_redirect
      settings_account_path
    end

    def active_tab
      nil
    end
end
