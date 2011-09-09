class ExpressDomainController < ApplicationController
  before_filter :require_login

  def create
    # Get only relevant parameters
    domain_params = params[:express_domain]
    # check for which domain action we should call
    @dom_action = domain_params.delete :dom_action
    Rails.logger.debug "dom_action: #{@dom_action}"
    domain_params[:rhlogin] = session[:login]
    domain_params[:ticket] = cookies[:rh_sso]
    domain_params[:password] = ''
    @domain = ExpressDomain.new(domain_params)
    if @domain.valid?
      begin
        if @dom_action == 'create'
          Rails.logger.debug 'creating domain'
          @domain.create do |json_response|
            process_response json_response
          end
        elsif @dom_action == 'update'
          @domain.update do |json_response|
            process_response json_response
          end
        end #end if action
      rescue Exception
        # Exception messages are recorded in the error hash in ExpressApi
        @message = @domain.errors.full_messages.join("; ")
        @message_type = :error
      end
    else
      # display validation errors
      @message = @domain.errors.full_messages.join("; ")
      @message_type = :error
      Rails.logger.error "Validation error: #{@message}"
    end
    
    @userinfo = ExpressUserinfo.new :rhlogin => session[:login],
                                    :ticket => session[:ticket]
    @userinfo.establish
    Rails.logger.debug "Updated userinfo: #{@userinfo.inspect}"
    # respond based on requested format
    respond_to do |format|
      format.html {flash[@message_type] = @message; redirect_to :controller => 'control_panel'}
      format.js
    end
  end
  
  def process_response(json_response)
    Rails.logger.debug "Domain api result: #{json_response.inspect}"
    # check that we have expected result
    unless json_response["exit_code"] > 0
      @message = I18n.t("express_api.messages.domain_#{@dom_action}")
      @message_type = :success
    else
      # broker error
      @message = json_response["result"].empty? ? I18n.t(:unknown) : json_response["result"]
      @message_type = :error
    end
  end
end
