require 'openshift/helper'
require 'aws'
require 'json'
require 'resolv'
require 'pp'

module Libra
  class Server
    # Cartridge definitions
    @@C_CONTROLLER = 'li-controller'
    @@USE_CNAME = false

    attr_reader :name, :repos, :carts, :embedcarts

    def initialize(name, repos=nil, carts=nil, embedcarts=nil)
      @name = name
      @repos = repos.to_i if repos
      @carts = carts if carts
      @embedcarts = embedcarts if embedcarts
    end

    def self.create(opts={})
      # Set defaults
      opts[:aws_name] ||= Libra.c[:aws_name]
      opts[:key_name] ||= Libra.c[:aws_keypair]
      opts[:image_id] ||= Libra.c[:aws_ami]
      opts[:max_count] ||= 1
      opts[:instance_type] ||= "m1.large"

      # Create the instances in EC2, returning
      # an array of the image id's
      instances = Helper.ec2.launch_instances(opts[:image_id],
                      :max_count => opts[:max_count],
                      :key_name => opts[:key_name],
                      :instance_type => opts[:instance_type]).collect do |server|
        server[:aws_instance_id]
      end

      # Tag the instance(s) if necessary
      if opts[:aws_name]
        instances.each {|i| Helper.ec2.create_tag(i, 'Name', opts[:aws_name])}
      end

      instances
    end

    #
    # Returns the preferred available server.
    # Currently this is defined by the server that
    # has the least number of git repos on it.
    #
    def self.find_available
      # Defaults
      current_server, current_repos = rpc_find_available
      if !current_server
        current_server, current_repos = rpc_find_available(true)
      end
      raise NodeException.new(140), "No nodes available.  If the problem persists please contact Red Hat support.", caller[0..5] unless current_server
      Libra.logger_debug "DEBUG: server.rb:find_available #{current_server}: #{current_repos}"
      new(current_server, current_repos)
    end

    def self.rpc_find_available(forceRediscovery=false)
      current_server, current_repos = nil, 100000000
      Helper.rpc_get_fact('git_repos', nil, forceRediscovery) do |server, repos|
        num_repos = repos.to_i
        if num_repos < current_repos
          current_server = server
          current_repos = num_repos
        end
      end
      return current_server, current_repos
    end

    #
    # Returns a list of all the servers that respond
    #
    def self.find_all
      servers = []

      Helper.rpc_get_fact('git_repos') do |server, repos|
        servers << new(server, repos)
      end

      servers
    end

    #
    # Get a DNS txt entry
    #
    def self.has_dns_txt?(namespace)
      dns = Resolv::DNS.new
      resp = dns.getresources("#{namespace}.#{Libra.c[:libra_domain]}", Resolv::DNS::Resource::IN::TXT)
      return resp.length > 0
    end

    def self.dyn_login(retries=0)
      # Set your customer name, username, and password on the command line
      # Set up our HTTP object with the required host and path
      url = URI.parse("#{Libra.c[:dynect_url]}/REST/Session/")
      headers = { "Content-Type" => 'application/json' }
      # Login and get an authentication token that will be used for all subsequent requests.
      session_data = { :customer_name => Libra.c[:dynect_customer_name], :user_name => Libra.c[:dynect_user_name], :password => Libra.c[:dynect_password] }
      auth_token = nil
      dyn_do('dyn_login', retries) do
        http = Net::HTTP.new(url.host, url.port)
        #http.set_debug_output $stderr
        http.use_ssl = true
        begin
          Libra.logger_debug "DEBUG: DYNECT Login with path: #{url.path}"
          resp, data = http.post(url.path, JSON.generate(session_data), headers)
          case resp
          when Net::HTTPSuccess
            raise_dns_exception(nil, resp) unless dyn_success?(data)
            result = JSON.parse(data)
            auth_token = result['data']['token']         
          else
            raise_dns_exception(nil, resp)
          end
        rescue DNSException => e
          raise
        rescue Exception => e
          raise_dns_exception(e)
        end
      end
      # Is the session still alive?
      #headers = { "Content-Type" => 'application/json', 'Auth-Token' => auth_token }
      #resp, data = http.get(url.path, headers)
      #Libra.logger_debug 'GET Session Response: ', data, '\n'
      return auth_token
    end

    def self.raise_dns_exception(e=nil, resp=nil)
      if e
        Libra.logger_debug "DEBUG: Exception caught from DNS request: #{e.message}"
        Libra.logger_debug e.backtrace        
      end
      if resp
        Libra.logger_debug "DEBUG: Response code: #{resp.code}"
        Libra.logger_debug "DEBUG: Response body: #{resp.body}"
      end
      raise DNSException.new(145), "Error communicating with DNS system.  If the problem persists please contact Red Hat support.", caller[0..5]
    end
    
    def delete_app_dns_entries(app_name, namespace, retries=2)
      auth_token = Server.dyn_login(retries)
      if @@USE_CNAME
        dyn_delete_cname_record(app_name, namespace, auth_token, retries)
      else
        dyn_delete_sshfp_record(app_name, namespace, auth_token, retries)
        dyn_delete_a_record(app_name, namespace, auth_token, retries)
      end
      Server.dyn_publish(auth_token, retries)
      Server.dyn_logout(auth_token, retries)
    end

    def create_app_dns_entries(app_name, namespace, retries=2)
      auth_token = Server.dyn_login(retries)
      if @@USE_CNAME
        dyn_create_cname_record(app_name, namespace, auth_token, retries)
      else
        dyn_create_a_record(app_name, namespace, auth_token, retries)
        dyn_create_sshfp_record(app_name, namespace, auth_token, retries)
      end
      Server.dyn_publish(auth_token, retries)
      Server.dyn_logout(auth_token, retries)
    end

    def recreate_app_dns_entries(app_name, old_namespace, new_namespace, auth_token, retries=2)
      if @@USE_CNAME
        dyn_delete_cname_record(app_name, old_namespace, auth_token, retries)
        dyn_create_cname_record(app_name, new_namespace, auth_token, retries)
      else
        dyn_delete_sshfp_record(app_name, old_namespace, auth_token, retries)
        dyn_delete_a_record(app_name, old_namespace, auth_token, retries)
        dyn_create_a_record(app_name, new_namespace, auth_token, retries)
        dyn_create_sshfp_record(app_name, new_namespace, auth_token, retries)
      end
    end

    def self.dyn_do(method, retries=2)
      i = 0
      while true
        begin
          yield
          break
        rescue DNSException => e
          raise if i >= retries
          Libra.logger_debug "DEBUG: Retrying #{method} after exception caught from DNS request: #{e.message}"
          i += 1
        end
      end
    end

    def self.dyn_logout(auth_token, retries=0)
      # Logout
      resp, data = dyn_delete("Session/", auth_token, retries)
    end

    def dyn_create_a_record(application, namespace, auth_token, retries=0)
      public_ip = get_fact_direct('public_ip')
      Libra.logger_debug "DEBUG: Public ip being configured '#{public_ip}' to app '#{application}'"
      fqdn = "#{application}-#{namespace}.#{Libra.c[:libra_domain]}"
      # Create the A record
      path = "ARecord/#{Libra.c[:libra_zone]}/#{fqdn}/"
      record_data = { :rdata => { :address => public_ip }, :ttl => "60" }
      resp, data = Server.dyn_post(path, record_data, auth_token, retries)
    end
    
    def dyn_create_cname_record(application, namespace, auth_token, retries=0)
      public_hostname = get_fact_direct('public_hostname')
      Libra.logger_debug "DEBUG: Public ip being configured '#{public_hostname}' to app '#{application}'"
      fqdn = "#{application}-#{namespace}.#{Libra.c[:libra_domain]}"
      # Create the CNAME record
      path = "CNAMERecord/#{Libra.c[:libra_zone]}/#{fqdn}/"
      record_data = { :rdata => { :cname => public_hostname }, :ttl => "60" }
      resp, data = Server.dyn_post(path, record_data, auth_token, retries)
    end
    
    def dyn_create_sshfp_record(application, namespace, auth_token, retries=0)
      sshfp = get_fact_direct('sshfp').split[-1]
      fqdn = "#{application}-#{namespace}.#{Libra.c[:libra_domain]}"
      # Create the SSHFP record
      path = "SSHFPRecord/#{Libra.c[:libra_zone]}/#{fqdn}/"
      record_data = { :rdata => { :algorithm => '1',  :fptype => '1', :fingerprint => sshfp}, :ttl => "60" }
      resp, data = Server.dyn_post(path, record_data, auth_token, retries)
    end

    def dyn_delete_a_record(application, namespace, auth_token, retries=0)
      fqdn = "#{application}-#{namespace}.#{Libra.c[:libra_domain]}"
      # Delete the A record
      path = "ARecord/#{Libra.c[:libra_zone]}/#{fqdn}/"
      resp, data = Server.dyn_delete(path, auth_token, retries)
    end
    
    def dyn_delete_cname_record(application, namespace, auth_token, retries=0)
      fqdn = "#{application}-#{namespace}.#{Libra.c[:libra_domain]}"
      # Delete the A record
      path = "CNAMERecord/#{Libra.c[:libra_zone]}/#{fqdn}/"
      resp, data = Server.dyn_delete(path, auth_token, retries)
    end
    
    def dyn_delete_sshfp_record(application, namespace, auth_token, retries=0)
      fqdn = "#{application}-#{namespace}.#{Libra.c[:libra_domain]}"
      # Delete the SSHFP record
      path = "SSHFPRecord/#{Libra.c[:libra_zone]}/#{fqdn}/"
      resp, data = Server.dyn_delete(path, auth_token, retries)
    end

    def self.dyn_create_txt_record(namespace, auth_token, retries=0)
      fqdn = "#{namespace}.#{Libra.c[:libra_domain]}"
      # Create the TXT record
      path = "TXTRecord/#{Libra.c[:libra_zone]}/#{fqdn}/"
      record_data = { :rdata => { :txtdata => "Text record for #{namespace}"}, :ttl => "60" }
      resp, data = dyn_post(path, record_data, auth_token, retries)
    end

    def self.dyn_delete_txt_record(namespace, auth_token, retries=0)
      fqdn = "#{namespace}.#{Libra.c[:libra_domain]}"
      # Delete the TXT record
      path = "TXTRecord/#{Libra.c[:libra_zone]}/#{fqdn}/"
      resp, data = dyn_delete(path, auth_token, retries)
    end

    def self.dyn_publish(auth_token, retries=0)
      # Publish the changes
      path = "Zone/#{Libra.c[:libra_zone]}/"
      publish_data = { "publish" => "true" }
      resp, data = dyn_put(path, publish_data, auth_token, retries)
    end

    def self.dyn_has_txt_record?(namespace, auth_token, raise_exception_on_exists=false)
      fqdn = "#{namespace}.#{Libra.c[:libra_domain]}"
      path = "TXTRecord/#{Libra.c[:libra_zone]}/#{fqdn}/"      
      dyn_has = dyn_has?(path, auth_token)
      if dyn_has && raise_exception_on_exists
        raise UserException.new(103), "A namespace with name '#{namespace}' already exists", caller[0..5]
      else
        return dyn_has
      end
    end
    
    def self.handle_temp_redirect(resp, auth_token)
      if resp.body =~ /^\/REST\//
        headers = { "Content-Type" => 'application/json', 'Auth-Token' => auth_token }
        url = URI.parse("#{Libra.c[:dynect_url]}#{resp.body}")
        http = Net::HTTP.new(url.host, url.port)
        #http.set_debug_output $stderr
        http.use_ssl = true
        sleep_time = 2
        success = false
        retries = 0
        while !success && retries < 5
          retries += 1
          begin
            Libra.logger_debug "DEBUG: DYNECT handle temp redirect with path: #{url.path} and headers: #{headers.pretty_inspect} attempt: #{retries} sleep_time: #{sleep_time}"
            resp, data = http.get(url.path, headers)
            case resp
            when Net::HTTPSuccess, Net::HTTPTemporaryRedirect
              data = JSON.parse(data)
              if data && data['status']
                Libra.logger_debug "DEBUG: DYNECT Response data: #{data['data']}"
                status = data['status']
                if status == 'success'
                  success = true
                elsif status == 'incomplete'
                  sleep sleep_time
                  sleep_time *= 2
                else #if status == 'failure'                  
                  Libra.logger_debug "DEBUG: DYNECT Response status: #{data['status']}"
                  raise_dns_exception(nil, resp)
                end
              end
            else
              raise_dns_exception(nil, resp)
            end
          rescue DNSException => e
            raise
          rescue Exception => e
            raise_dns_exception(e)
          end
        end
        if !success
          raise_dns_exception(nil, resp)
        end
      else
        raise_dns_exception(nil, resp)
      end
    end

    def self.dyn_has?(path, auth_token)
      headers = { "Content-Type" => 'application/json', 'Auth-Token' => auth_token }
      url = URI.parse("#{Libra.c[:dynect_url]}/REST/#{path}")
      http = Net::HTTP.new(url.host, url.port)
      #http.set_debug_output $stderr
      http.use_ssl = true
      has = false
      begin
        Libra.logger_debug "DEBUG: DYNECT has? with path: #{url.path} and headers: #{headers.pretty_inspect}"
        resp, data = http.get(url.path, headers)
        case resp
        when Net::HTTPSuccess
          has = dyn_success?(data)
        when Net::HTTPNotFound
          Libra.logger_debug "DEBUG: DYNECT returned 404 for: #{url.path}"
        else
          raise_dns_exception(nil, resp)
        end
      rescue DNSException => e
        raise
      rescue Exception => e
        raise_dns_exception(e)
      end
      return has
    end

    def self.dyn_put(path, put_data, auth_token, retries=0)
      return dyn_put_post(path, put_data, auth_token, true, retries)
    end

    def self.dyn_post(path, post_data, auth_token, retries=0)
      return dyn_put_post(path, post_data, auth_token, false, retries)
    end

    def self.dyn_put_post(path, post_data, auth_token, put=false, retries=0)
      url = URI.parse("#{Libra.c[:dynect_url]}/REST/#{path}")
      headers = { "Content-Type" => 'application/json', 'Auth-Token' => auth_token }
      resp, data = nil, nil
      dyn_do('dyn_put_post', retries) do
        http = Net::HTTP.new(url.host, url.port)
        #http.set_debug_output $stderr
        http.use_ssl = true
        json_data = JSON.generate(post_data);
        begin
          Libra.logger_debug "DEBUG: DYNECT put/post with path: #{url.path} json data: #{json_data} and headers: #{headers.pretty_inspect}"
          if put
            resp, data = http.put(url.path, json_data, headers)
          else
            resp, data = http.post(url.path, json_data, headers)
          end
          case resp
          when Net::HTTPSuccess
            raise_dns_exception(nil, resp) unless dyn_success?(data)
          when Net::HTTPTemporaryRedirect
            handle_temp_redirect(resp, auth_token)
          else
            raise_dns_exception(nil, resp)
          end
        rescue DNSException => e
          raise
        rescue Exception => e
          raise_dns_exception(e)
        end
      end
      return resp, data
    end
    
    def self.dyn_success?(data)
      Libra.logger_debug "DEBUG: DYNECT Response: #{data}"
      success = false
      if data
        data = JSON.parse(data)
        if data && data['status'] && data['status'] == 'failure'
          Libra.logger_debug "DEBUG: DYNECT Response status: #{data['status']}"
        elsif data && data['status'] == 'success'
          Libra.logger_debug "DEBUG: DYNECT Response data: #{data['data']}"
          #has = data['data'][0].length > 0
          success = true
        end
      end
      success
    end

    def self.dyn_delete(path, auth_token, retries=0)
      headers = { "Content-Type" => 'application/json', 'Auth-Token' => auth_token }
      url = URI.parse("#{Libra.c[:dynect_url]}/REST/#{path}")
      resp, data = nil, nil
      dyn_do('dyn_delete', retries) do
        http = Net::HTTP.new(url.host, url.port)
        #http.set_debug_output $stderr
        http.use_ssl = true
        begin
          Libra.logger_debug "DEBUG: DYNECT delete with path: #{url.path} and headers: #{headers.pretty_inspect}"
          resp, data = http.delete(url.path, headers)
          case resp
          when Net::HTTPSuccess
            raise_dns_exception(nil, resp) unless dyn_success?(data)
          when Net::HTTPNotFound
            Libra.logger_debug "DEBUG: DYNECT: Could not find #{url.path} to delete"
          when Net::HTTPTemporaryRedirect
            handle_temp_redirect(resp, auth_token)
          else
            raise_dns_exception(nil, resp)
          end
        rescue DNSException => e
          raise
        rescue Exception => e
          raise_dns_exception(e)
        end
      end
      return resp, data
    end

    #
    # Configures the user on this server
    #
    def create_account(user, app_info)
      # Make the call to configure the user
      #execute_internal(@@C_CONTROLLER, 'configure', "-c #{user.uuid} -e #{user.rhlogin} -s #{user.ssh}")
      result = execute_direct(@@C_CONTROLLER, 'configure', "-c #{app_info['uuid']} -e #{user.rhlogin} -s #{user.ssh}")
      handle_controller_result(result)
    end

    def delete_account(app_uuid)
      # Make the call to configure the user
      result = execute_direct(@@C_CONTROLLER, 'deconfigure', "-c #{app_uuid}")
      handle_controller_result(result)
    end
    
    def handle_controller_result(result)
      result = result[0]
      if (result && defined? result.results)
        output = result.results[:data][:output]
        exitcode = result.results[:data][:exitcode]
        log_result_output(output, exitcode)
        if exitcode != 0
          Libra.client_debug "Controller return code: " + exitcode.to_s
          raise NodeException.new(143), "Node execution failure (invalid exit code from node controller).  If the problem persists please contact Red Hat support.", caller[0..5]
        end
      else
        raise NodeException.new(143), "Node execution failure (error getting result from node controller).  If the problem persists please contact Red Hat support.", caller[0..5]
      end
    end

    #
    # Returns whether this server has the specified app
    #
    def has_app?(app, app_name)
      Helper.rpc_exec('libra', @name) do |client|
        client.has_app(:uuid => app['uuid'],
                       :application => app_name) do |response|
          output = response[:body][:data][:output]
          return output == true
        end
      end
    end

    
    #
    # Returns the server identity of the specified app
    #    
    def self.find_app(app, app_name)
      server_identity = nil
      Helper.rpc_exec('libra') do |client|
        client.has_app(:uuid => app['uuid'],
                       :application => app_name) do |response|
          output = response[:body][:data][:output]
          if output == true
            server_identity = response[:senderid]
          end
        end
      end
      return server_identity
    end
    
    #
    # Returns whether this server has the specified embedded app
    #
    def has_embedded_app?(app, embedded_type)
      Helper.rpc_exec('libra', @name) do |client|
        client.has_embedded_app(:uuid => app['uuid'],
                       :embedded_type => embedded_type) do |response|
          output = response[:body][:data][:output]
          return output == true
        end
      end
    end

    #
    # Configures the application for this user on this server
    #
    def execute(framework, action, app_name, user)
      # Make the call to configure the application
      Libra.client_debug "Executing framework:#{framework} action:#{action} app_name:#{app_name} user:#{user}" if Libra.c[:rpc_opts][:verbose]
      execute_internal(framework, action, "#{app_name} #{user.namespace} #{user.uuid}")
    end

    #
    # Execute cartridge directly on a node
    #
    def execute_direct(cartridge, action, args)
        mc_args = { :cartridge => cartridge,
                    :action => action,
                    :args => args }
        rpc_client = Helper.rpc_exec_direct('libra')
        result = nil
        begin
          result = rpc_client.custom_request('cartridge_do', mc_args, self.name, {'identity' => self.name})
        ensure
          rpc_client.disconnect
        end
        Libra.logger_debug result
        result
    end
    
    #
    # Logs result output
    #
    def log_result_output(output, exitcode, user=nil)
      if output && !output.empty?
        output.each_line do |line|
          if line =~ /^CLIENT_(MESSAGE|RESULT|DEBUG): /
            if line =~ /^CLIENT_MESSAGE: /
              Libra.client_message line['CLIENT_MESSAGE: '.length..-1]
            elsif line =~ /^CLIENT_RESULT: /
              Libra.client_result line['CLIENT_RESULT: '.length..-1]
            else
              Libra.client_debug line['CLIENT_DEBUG: '.length..-1]
            end
          elsif user && line =~ /^SSH_KEY_(ADD|REMOVE): /
            if line =~ /^SSH_KEY_ADD: /
              key = line['SSH_KEY_ADD: '.length..-1].chomp
              user.set_system_ssh_key(key)
            else
              key = line['SSH_KEY_REMOVE: '.length..-1].chomp
              user.remove_system_ssh_key()
            end
          elsif exitcode != 0
            Libra.client_debug line
            Libra.logger_debug "DEBUG: server results: " + line
          end
        end
      end
    end

    #
    # Execute the cartridge and action on this server
    #
    def execute_internal(cartridge, action, args)
      Helper.rpc_exec('libra', name) do |client|
        cartridge_do(client, cartridge, action, args)
      end
    end

    #
    # Execute an action on all nodes
    #
    def self.execute_all(cartridge, action, args)
        Helper.rpc_exec('libra') do |client|
          cartridge_do(client, cartridge, action, args)
        end
    end

    def self.cartridge_do(client, cartridge, action, args)
      client.cartridge_do(:cartridge => cartridge,
                          :action => action,
                          :args => args) do |response|
        return_code = response[:body][:data][:exitcode]
        output = response[:body][:data][:output]
        if return_code != 0
          Libra.logger_debug "DEBUG: Non-zero exit code detected for cartridge: #{cartridge} action: #{action} args: #{args} with response:"
          Libra.logger_debug response.pretty_inspect
          if Libra.c[:rpc_opts][:verbose]
            Libra.client_debug "Cartridge return code: #{return_code}"
            Libra.client_debug "Cartridge node: #{response[:senderid]}"
            Libra.client_debug "Cartridge output: #{output}"
          end
          raise CartridgeException.new(141), output, caller[0..5]
        else
          if output && !output.empty?
            Libra.client_debug "Cartridge output: #{output}" if Libra.c[:rpc_opts][:verbose]
          end
        end
      end
    end

    #
    # Returns the list of cartridges that the server has (sep w/ |)
    # looking it up as needed. This returns the full list, including
    # cartridges we may wish to keep private!
    #
    def carts
      Helper.rpc_get_fact('cart_list', name) do |server, carts|
          @carts = carts
      end unless @carts
      @carts
    end

    #
    # Returns the list of embed cartridges that the server has (sep w/ |)
    # looking it up as needed. This returns the full list, including
    # cartridges we may wish to keep private!
    #
    def embedcarts
      Helper.rpc_get_fact('embed_cart_list', name) do |server, embedcarts|
          @embedcarts = embedcarts
      end unless @embedcarts
      @embedcarts
    end


    #
    # Returns the number of repos that the server has
    # looking it up if needed
    #
    def repos
      # Only call out to MCollective if the value isn't set
      Helper.rpc_get_fact('git_repos', name) do |server, repos|
        @repos = repos
      end unless @repos

      @repos
    end

    #
    # Returns the requested fact
    #
    def get_fact_direct(fact)
        Helper.rpc_get_fact_direct(fact, self.name)
    end

    #
    # Clears out any cached data
    #
    def reload
      @repos = nil
    end

    #
    # Base equality on the server name
    #
    def ==(another_server)
      self.name == another_server.name
    end

    #
    # Base sorting on the server name
    #
    def <=>(another_server)
      self.name <=> another_server.name
    end
  end
end
