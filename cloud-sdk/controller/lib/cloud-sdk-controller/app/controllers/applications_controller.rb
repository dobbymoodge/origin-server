class ApplicationsController < BaseController
  respond_to :xml, :json
  before_filter :authenticate
  include LegacyBrokerHelper
  
  # GET /domains/[domain id]/applications
  def index
    domain_id = params[:domain_id]
    cloud_user = CloudUser.find(@login)
    applications = Application.find_all(cloud_user)
    
    if applications.nil? 
      @reply = RestReply.new(:not_found)
      message = Message.new(:error, "No applications found for user #{@login}.")
      @reply.messages.push(message)
      respond_with @reply, :status => @reply.status
    else
      apps = Array.new
      applications.each do |application|
        app = RestApplication.new(application, domain_id)
        apps.push(app)
      end
      @reply = RestReply.new(:ok, "applications", apps)
      respond_with @reply, :status => @reply.status
    end
  end
  
  # GET /domains/[domain_id]/applications/<id>
  def show
    domain_id = params[:domain_id]
    id = params[:id]
    
    cloud_user = CloudUser.find(@login)
    application = Application.find(cloud_user,id)
    
    if application.nil?
      @reply = RestReply.new(:not_found)
      message = Message.new(:error, "Application #{id} not found.")
      @reply.messages.push(message)
      respond_with @reply, :status => @reply.status
    else
      app = RestApplication.new(application, domain_id)
      @reply = RestReply.new(:ok, "application", app)
      respond_with @reply, :status => @reply.status
    end
  end
  
  # POST /domains/[domain_id]/applications
  def create
    application = validate_create_params
    create_and_configure_application(application)
  end
  
  # DELELTE domains/[domain_id]/applications/[id]
  def destroy
    domain_id = params[:domain_id]
    id = params[:id]
    cloud_user = CloudUser.find(@login)
    application = Application.find(cloud_user,id)
    if application.nil?
      @reply = RestReply.new(:not_found)
      message = Message.new(:error, "Application #{id} not found.")
      @reply.messages.push(message)
      respond_with(@reply) do |format|
         format.xml { render :xml => @reply, :status => @reply.status }
         format.json { render :json => @reply, :status => @reply.status }
      end
      return
    end
    
    begin
      Rails.logger.debug "Deleting application #{id}"
      application.cleanup_and_delete()
    rescue Exception => e
      Rails.logger.error "Failed to Delete application #{id}: #{e.message}"
      @reply = RestReply.new(:internal_server_error)
      message = Message.new(:error, "Failed to delete application #{app_name} due to:#{e.message}") 
      @reply.messages.push(message)
      respond_with(@reply) do |format|
         format.xml { render :xml => @reply, :status => @reply.status }
         format.json { render :json => @reply, :status => @reply.status }
      end
      return
    end
 
    @reply = RestReply.new(:no_content)
    message = Message.new(:info, "Application #{id} is deleted.")
    @reply.messages.push(message)
    respond_with(@reply) do |format|
      format.xml { render :xml => @reply, :status => @reply.status }
      format.json { render :json => @reply, :status => @reply.status }
    end
  end
  
  protected
  
  def validate_create_params
    domain_id = params[:domain_id]
    user = CloudUser.find(@login)
    app_name = params[:name]
    cartridge = params[:cartridge]
    scale = params[:scale]
    scale = false if scale.nil? or scale=="false"
    scale = true if scale=="true"
    if app_name.nil? 
      @reply = RestReply.new( :bad_request)
      message = Message.new(:error, "Missing required parameter name.") 
      @reply.messages.push(message)
      respond_with @reply, :status => @reply.status
      return nil
    end
    application = Application.find(user,app_name)
    if not application.nil?
      @reply = RestReply.new(:conflict)
      message = Message.new(:error, "The supplied application name '#{app_name}' already exists") 
      @reply.messages.push(message)
      respond_with @reply, :status => @reply.status
      return nil
    end
    Rails.logger.debug "Checking to see if application name is black listed"
    if Cloud::Sdk::ApplicationContainerProxy.blacklisted? app_name
      @reply = RestReply.new(:forbidden)
      message = Message.new(:error, "The supplied application name '#{app_name}' is not allowed") 
      @reply.messages.push(message)
      respond_with @reply, :status => @reply.status
      return nil
    end
    if cartridge.nil? or not CartridgeCache.cartridge_names('standalone').include?(cartridge)
      @reply = RestReply.new( :bad_request)
      carts = get_cached("cart_list_standalone", :expires_in => 21600.seconds) {Application.get_available_cartridges("standalone")}
      message = Message.new(:error, "Invalid cartridge #{cartridge}.  Valid values are (#{carts.join(', ')})") 
      @reply.messages.push(message)
      respond_with @reply, :status => @reply.status
      return nil
    end
    Rails.logger.debug "Checking to see if user limit for number of apps has been reached"
    if (user.consumed_gears >= user.max_gears)
      @reply = RestReply.new(:forbidden)
      message = Message.new(:error, "#{@login} has already reached the application limit of #{user.max_gears}")
      @reply.messages.push(message)
      respond_with @reply, :status => @reply.status
      return nil
    end
    Rails.logger.debug "Validating application"
    return Application.new(user, app_name, nil, nil, cartridge, scale)   
  end
  
  def create_and_configure_application(application)
    if application.valid?
      begin
        Rails.logger.debug "Creating application #{application.name}"
        application.create
        Rails.logger.debug "Configuring dependencies #{application.name}"
        application.configure_dependencies
        Rails.logger.debug "Adding system ssh keys #{application.name}"
        application.add_system_ssh_keys
        Rails.logger.debug "Adding ssh keys #{application.name}"
        application.add_ssh_keys
        Rails.logger.debug "Adding system environment vars #{application.name}"
        application.add_system_env_vars
        begin
          Rails.logger.debug "Creating dns"
          application.create_dns
        rescue Exception => e
            Rails.logger.error e
            application.destroy_dns
            @reply = RestReply.new(:internal_server_error)
            message = Message.new(:error, "Failed to create dns for application #{application.name} due to:#{e.message}") 
            @reply.messages.push(message)
            respond_with @reply, :status => @reply.status
            return
        end
      rescue Exception => e
        if application.persisted?
          Rails.logger.debug e.message
          Rails.logger.debug e.backtrace.inspect
          application.deconfigure_dependencies
          application.destroy
          application.delete
        end

        @reply = RestReply.new(:internal_server_error)
        message = Message.new(:error, "Failed to create application #{application.name} due to:#{e.message}") 
        @reply.messages.push(message)
        respond_with @reply, :status => @reply.status
        return
      end
      app = RestApplication.new(application, application.domain)
      @reply = RestReply.new( :created, "application", app)
      message = Message.new(:info, "Application #{application.name} was created.")
      @reply.messages.push(message)
      respond_with @reply, :status => @reply.status
    else
      @reply = RestReply.new( :bad_request)
      message = Message.new(:error, "Failed to create application #{application.name}") 
      @reply.messages.push(message)
      message = Message.new(:error, application.errors.first[1][:message]) 
      @reply.messages.push(message)
      respond_with @reply, :status => @reply.status
    end
  end
end
