require 'openshift/exception.rb'
require 'openshift/config.rb'
require 'openshift/helper.rb'
require 'openshift/server.rb'
require 'openshift/user.rb'
require 'openshift/nurture.rb'
require 'openshift/util.rb'

module Libra

  def self.client_debug(str)
    debugIO = Thread.current[:debugIO]
    if debugIO
      debugIO.puts str
    else
      puts str
    end
  end
  
  def self.client_message(str)
    messageIO = Thread.current[:messageIO]
    if messageIO
      messageIO.puts str
    else
      puts str
    end
  end

  def self.client_result(str)
    resultIO = Thread.current[:resultIO]
    if resultIO
      resultIO.puts str
    else
      puts str
    end
  end

  def self.logger_debug(str)
    if defined? Rails
      Rails.logger.debug str
    else
      puts str
    end
  end

  def self.execute(framework, action, app_name, rhlogin)
    # get user
    user = User.find(rhlogin)
    if not user
      raise UserException.new(254), "User '#{rhlogin}' not found", caller[0..5]
    end

    # process actions

    case action
    when 'configure'
      # create a new app.  Don't expect it to exist
      configure_app(framework, app_name, user)

    when 'deconfigure'
      # destroy an app.  It must exists, but won't at the end
      # get the app object
      # get the server
      # send the command to the server
      # remove the app object from persistant storage
      deconfigure_app(framework, app_name, user)

    else
      # send a command to an app.  It must exist and will afterwards
      # get the app object
      # get the server
      # send the command
      app_info = user.app_info(app_name)
      if not app_info
        raise UserException.new(101), "An application named '#{app_name}' does not exist", caller[0..5]
      end

      server = Server.new(app_info['server_identity'])
      if not server
        raise NodeException.new(142), "The application #{app_name} is registered to an invalid node.  If the problem persists please contact Red Hat support.", caller[0..5]
      end

      Libra.logger_debug "DEBUG: Performing action '#{action}' on node: #{server.name} - #{server.repos} repos" if Libra.c[:rpc_opts][:verbose]
      server_execute_direct(framework, action, app_name, user, server, app_info)
    end
  end


  def self.configure_app(framework, app_name, user)
    raise UserException.new(100), "An application named '#{app_name}' already exists", caller[0..5] if user.app_info(app_name)
    # Find the next available server
    server = Server.find_available

    Libra.logger_debug "DEBUG: Performing configure on node: #{server.name} - #{server.repos} repos" if Libra.c[:rpc_opts][:verbose]

    user.validate_app_limit # TODO there is a race condition here if two users get past here before creating the app and updating s3
    # Create S3 app entry on configure (one of the first things)
    app_info  = user.create_app(app_name, framework, server)

    begin
      # Configure the user on this server if necessary
      server.create_user(user, app_info) # not cleaned up on failure

      server_execute_direct(framework, 'configure', app_name, user, server, app_info)
      begin
        # update DNS
        public_ip = server.get_fact_direct('public_ip')
        Libra.logger_debug "DEBUG: Public ip being configured '#{public_ip}' to namespace '#{user.namespace}'"
        sshfp = server.get_fact_direct('sshfp').split[-1]
        Server.create_app_dns_entries(app_name, user.namespace, public_ip, sshfp)
      rescue Exception => e
        begin
          Libra.logger_debug "DEBUG: Failed to register dns entry for app '#{app_name}' and user '#{user.rhlogin}' on node '#{server.name}'"
          Libra.client_debug "Failed to register dns entry for: '#{app_name}'"
          server_execute_direct(framework, 'deconfigure', app_name, user, server, app_info)
        ensure
          raise
        end
      end
    rescue Exception => e
      begin
        Libra.logger_debug "DEBUG: Failed to create application '#{app_name}' for user '#{user.rhlogin}' on node '#{server.name}'"
        Libra.client_debug "Failed to create application: '#{app_name}'"
        server_execute_direct(framework, 'deconfigure', app_name, user, server, app_info)        
      ensure
        raise
      end
    end
  end

  # remove an application from server and persistant storage
  def self.deconfigure_app(framework, app_name, user)
    # get the application details
    app_info = user.app_info(app_name)
    if not app_info
      raise UserException.new(101), "An application named '#{app_name}' does not exist", caller[0..5]
    end
    
    # Remove the application and account from the server
    server = Server.new(app_info['server_identity'])    
    if server
      
      # first, remove the application
      Libra.logger_debug "DEBUG: deconfiguring app #{app_name} on node: #{server.name} - #{server.repos} repos" if Libra.c[:rpc_opts][:verbose]
      begin
        server_execute_direct(framework, 'deconfigure', app_name, user, server, app_info)
      rescue
        if server.has_app?(app_info, app_name)
          raise
        else
          Libra.logger_debug "Application '#{app_name}' not found on node #{server.name}.  Continuing with deconfigure."
          Libra.logger_debug "Error from cartridge on deconfigure: #{e.message}"
        end
      end

      # then remove the account

      # remove the node account from the server node.
      begin
        Libra.logger_debug "Removing app account from server node: #{app_info}"
        server.delete_account(app_info['uuid'])
      rescue
        # check if the user account is still there
      end
    else # NO SERVER
      Libra.client_debug "Application is registered to an invalid node, still attempting to remove everything else..."
      Libra.logger_debug "DEBUG: Application '#{app_name}' is registered by user '#{rhlogin}(#{app_info['uuid']})' to an invalid node '#{app_info.server_identity}', application will be destroyed but some space may still be consumed for app on the node..."
    end

    # remove the DNS entries
    Libra.logger_debug "DEBUG: Public ip being deconfigured from namespace '#{user.namespace}'"
    Server.delete_app_dns_entries(app_name, user.namespace)

    # remove the app record from the user object
    # Remove S3 app on deconfigure (one of the last things)
    Libra.logger_debug "Removing app info from persistant storage: #{app_name}"
    user.delete_app(app_name)

  end

  def self.server_execute_direct(framework, action, app_name, user, server, app_info)
    # Execute the action on the server using a framework cartridge
    Nurture.application(user.rhlogin, user.uuid, app_name, user.namespace, framework, action, app_info['uuid'])
    result = server.execute_direct(framework, action, "#{app_name} #{user.namespace} #{app_info['uuid']}")[0]
    if (result && defined? result.results)
      output = result.results[:data][:output]
      exitcode = result.results[:data][:exitcode]
      if action == 'status'
        if exitcode == 0
          Libra.client_result output
        else
          Libra.client_result "Application '#{app_name}' is either stopped or inaccessible"
        end
      elsif exitcode != 0
        Libra.client_debug "Cartridge return code: " + exitcode.to_s
        Libra.client_debug "Cartridge output: " + output
        Libra.logger_debug "DEBUG: execute_direct results: " + output
        raise NodeException.new(143), "Node execution failure (invalid exit code from execute direct).  If the problem persists please contact Red Hat support.", caller[0..5]
      end
    else
      raise NodeException.new(143), "Node execution failure (error getting result from execute direct).  If the problem persists please contact Red Hat support.", caller[0..5]
    end
  end

  #
  # Adjusts the capacity of the Libra cluster if
  # necessary
  #
  def self.adjust_capacity
    # Get the initial capacity
    current_servers = Server.find_all
    current_servers.each do |server|
      # If any server is below the threshold,
      # don't add a new server
      if server.repos < c[:repo_threshold]
        return
      end
    end

    # Add the additional server if needed
    result = Server.create
    Libra.logger_debug "DEBUG: Added EC2 instance #{result[0]}"
  end
end
