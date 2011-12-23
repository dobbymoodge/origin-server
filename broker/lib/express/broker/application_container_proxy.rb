require 'mcollective'
include MCollective::RPC
module Express
  module Broker
    class ApplicationContainerProxy
      @@C_CONTROLLER = 'li-controller'
      attr_accessor :id, :current_capacity
      
      def initialize(id, current_capacity=nil)
        @id = id
        @current_capacity = current_capacity
      end
      
      def self.find_available_impl(node_profile=nil)       
        current_server, current_capacity = rpc_find_available(node_profile)
        Rails.logger.debug "CURRENT SERVER: #{current_server}"
        if !current_server
          current_server, current_capacity = rpc_find_available(node_profile, true)
          Rails.logger.debug "CURRENT SERVER: #{current_server}"
        end
        raise Cloud::Sdk::NodeException.new("No nodes available.  If the problem persists please contact Red Hat support.", 140) unless current_server
        Rails.logger.debug "DEBUG: server.rb:find_available #{current_server}: #{current_capacity}"
        
        ApplicationContainerProxy.new(current_server, current_capacity)
      end
      
      IGNORE_CARTS = %w(abstract abstract-httpd li-controller embedded)
      def get_available_cartridges(cart_type)
        cartridges = []
        
        case cart_type
        when 'standalone'
          ApplicationContainerProxy.rpc_get_fact('cart_list', @id) do |server, carts|
            cartridges = carts.split('|')
          end
        when 'embedded'
          ApplicationContainerProxy.rpc_get_fact('embed_cart_list', @id) do |server, embedcarts|
            cartridges = embedcarts.split('|')
          end
        end
        cartridges.delete_if {|cart| IGNORE_CARTS.include?(cart)}
        
        cartridges
      end
      
      def create(app)
        result = execute_direct(@@C_CONTROLLER, 'configure', "-c '#{app.uuid}' -s '#{app.user.ssh}'")
        parse_result(result)
      end
    
      def destroy(app)
        result = execute_direct(@@C_CONTROLLER, 'deconfigure', "-c '#{app.uuid}'")
        parse_result(result)
      end
      
      def add_authorized_ssh_key(app, ssh_key)
        result = execute_direct(@@C_CONTROLLER, 'add-authorized-ssh-key', "-c '#{app.uuid}' -s '#{ssh_key}'")
        parse_result(result)
      end
      
      def remove_authorized_ssh_key(app, ssh_key)
        result = execute_direct(@@C_CONTROLLER, 'add-authorized-ssh-key', "-c '#{app.uuid}' -s '#{ssh_key}'")
        parse_result(result)
      end
    
      def add_env_var(app, key, value)
        result = execute_direct(@@C_CONTROLLER, 'add-env-var', "-c '#{app.uuid}' -k '#{key}' -v '#{value}'")
        parse_result(result)
      end
      
      def remove_env_var(app, key)
        result = execute_direct(@@C_CONTROLLER, 'remove-env-var', "-c '#{app.uuid}' -k '#{key}'")
        parse_result(result)    
      end
    
      def add_broker_auth_key(app, iv, token)
        result = execute_direct(@@C_CONTROLLER, 'add-broker-auth-key', "-c '#{app.uuid}' -i '#{iv}' -t '#{token}'")
        parse_result(result)
      end
    
      def remove_broker_auth_key(app)
        result = execute_direct(@@C_CONTROLLER, 'remove-broker-auth-key', "-c '#{app.uuid}'")
        handle_controller_result(result)
      end
      
      def preconfigure_cartridge(app, cart)
        run_cartridge_command(cart, app, "preconfigure")
      end
      
      def configure_cartridge(app, cart)
        run_cartridge_command(cart, app, "configure")
      end
      
      def deconfigure_cartridge(app, cart)
        run_cartridge_command(cart, app, "deconfigure")
      end
      
      def get_public_hostname
        rpc_get_fact_direct('public_hostname')
      end
      
      def get_ip_address
        rpc_get_fact_direct('ipaddress')
      end
      
      def start(app, cart)
        run_cartridge_command(cart, app, "start")
      end
      
      def stop(app, cart)
        run_cartridge_command(cart, app, "stop")
      end
      
      def force_stop(app, cart)
        run_cartridge_command(cart, app, "force-stop")
      end
      
      def restart(app, cart)
        run_cartridge_command(cart, app, "restart")
      end
      
      def reload(app, cart)
        run_cartridge_command(cart, app, "reload")
      end
      
      def status(app, cart)
        run_cartridge_command(cart, app, "status")
      end
      
      def tidy(app, cart)
        run_cartridge_command(cart, app, "tidy")
      end
      
      def threaddump(app, cart)
        run_cartridge_command(cart, app, "threaddump")
      end
      
      def add_alias(app, cart, server_alias)
        run_cartridge_command(cart, app, "add-alias", server_alias)
      end
      
      def remove_alias(app, cart, server_alias)
        run_cartridge_command(cart, app, "remove-alias", server_alias)
      end
      
      def add_component(app, component)
        reply = ResultIO.new
        begin
          reply.append run_cartridge_command('embedded/' + component, app, 'configure')
        rescue Exception => e
          begin
            Rails.logger.debug "DEBUG: Failed to embed '#{component}' in '#{app.name}' for user '#{app.user.rhlogin}'"
            reply.debugIO << "Failed to embed '#{component} in '#{app.name}'"
            reply.append run_cartridge_command('embedded/' + component, app, 'deconfigure')
          ensure
            raise
          end
        end
        
        component_details = reply.appInfoIO.string.empty? ? '' : reply.appInfoIO.string
        reply.debugIO << "Embedded app details: #{component_details}"
        [reply, component_details]
      end
      
      def remove_component(app, component)
        begin
          Rails.logger.debug "DEBUG: Deconfiguring embedded application '#{component}' in application '#{app.name}' on node '#{@id}'"
          return run_cartridge_command('embedded/' + component, app, 'deconfigure')
        rescue Exception => e
          #if still present
            #raise
          #else
            Rails.logger.debug "DEBUG: Embedded application '#{component}' not found in application '#{app.name}' on node '#{@id}'.  Continuing with deconfigure."
            Rails.logger.debug "DEBUG: Error from cartridge on deconfigure: #{e.message}"
          #end
        end
      end
      
      def start_component(app, component)
        run_cartridge_command('embedded/' + component, app, "start")
      end
      
      def stop_component(app, component)
        run_cartridge_command('embedded/' + component, app, "stop")
      end
      
      def restart_component(app, component)
        run_cartridge_command('embedded/' + component, app, "restart")    
      end
      
      def reload_component(app, component)
        run_cartridge_command('embedded/' + component, app, "reload")    
      end
      
      def component_status(app, component)
        run_cartridge_command('embedded/' + component, app, "status")    
      end
      
      def move_app(app, destination_container_proxy)
        source_container = app.container
        
        unless app.embedded.nil?
          raise Cloud::Sdk::UserException.new("Cannot move app '#{app.name}' with mysql embedded",1) if app.embedded.has_key?('mysql-5.1') 
          raise Cloud::Sdk::UserException.new("Cannot move app '#{app.name}' with mongo embedded",1) if app.embedded.has_key?('mongodb-2.0')           
        end

        if destination_container_proxy.nil?
          destination_container_proxy = Cloud::Sdk::ApplicationContainerProxy.find_available(app.node_profile)
        end

        if source_container.id == destination_container_proxy.id
          raise Cloud::Sdk::UserException.new("Error moving app.  Old and new servers are the same: #{source_container.id}", 1)
        end

        Rails.logger.debug "DEBUG: Moving app '#{app.name}' with uuid #{app.uuid} from #{source_container.id} to #{destination_container_proxy.id}"

        num_tries = 2
        reply = ResultIO.new
        begin
          Rails.logger.debug "DEBUG: Stopping existing app '#{app.name}' before moving"
          (1..num_tries).each do |i|
            begin
              reply.append source_container.stop(app, app.framework)
              break
            rescue Exception => e
              Rails.logger.debug "DEBUG: Error stopping existing app on try #{i}: #{e.message}"
              raise if i == num_tries
            end
          end

          begin
            Rails.logger.debug "DEBUG: Creating new account for app '#{app.name}' on #{destination_container_proxy.id}"
            reply.append destination_container_proxy.create(app)

            Rails.logger.debug "DEBUG: Moving content for app '#{app.name}' to #{destination_container_proxy.id}"
            Rails.logger.debug `eval \`ssh-agent\`; ssh-add /var/www/libra/broker/config/keys/rsync_id_rsa; ssh -o StrictHostKeyChecking=no -A root@#{source_container.get_ip_address} "rsync -a -e 'ssh -o StrictHostKeyChecking=no' /var/lib/libra/#{app.uuid}/ root@#{destination_container_proxy.get_ip_address}:/var/lib/libra/#{app.uuid}/"`
            if $?.exitstatus != 0
              raise Cloud::Sdk::NodeException.new("Error moving app '#{app.name}' from #{source_container.id} to #{destination_container_proxy.id}", 143)
            end

            begin
              Rails.logger.debug "DEBUG: Performing cartridge level move for '#{app.name}' on #{destination_container_proxy.id}"
              reply.append destination_container_proxy.send(:run_cartridge_command, app.framework, app, "move")
              unless app.embedded.nil?
                app.embedded.each do |cart, cart_info|
                  Rails.logger.debug "DEBUG: Performing cartridge level move for embedded #{cart} for '#{app.name}' on #{destination_container_proxy.id}"
                  reply.append destination_container_proxy.send(:run_cartridge_command, "embedded/" + cart, app, "move")
                end
              end
              
              unless app.aliases.nil?
                app.aliases.each do |server_alias|
                  destination_container_proxy.add_alias(app, app.framework, server_alias)
                end
              end
            rescue Exception => e
              reply.append destination_container_proxy.send(:run_cartridge_command, app.framework, app, "remove_httpd_proxy")              
              raise
            end

            Rails.logger.debug "DEBUG: Starting '#{app.name}' after move on #{destination_container_proxy.id}"
            (1..num_tries).each do |i|
              begin
                reply.append destination_container_proxy.start(app, app.framework)
                break
              rescue Exception => e
                Rails.logger.debug "DEBUG: Error starting after move on try #{i}: #{e.message}"
                raise if i == num_tries
              end
            end

            Rails.logger.debug "DEBUG: Fixing DNS and s3 for app '#{app.name}' after move"
            Rails.logger.debug "DEBUG: Changing server identity of '#{app.name}' from '#{source_container.id}' to '#{destination_container_proxy.id}'"
            app.server_identity = destination_container_proxy.id
            app.container = destination_container_proxy
            reply.append app.destroy_dns
            reply.append app.create_dns
            app.save
          rescue Exception => e
            reply.append destination_container_proxy.destroy(app)
            raise
          end
        rescue Exception => e
          reply.append source_container.start(app, app.framework)
          raise
        ensure
          Rails.logger.debug "URL: http://#{app.name}-#{app.user.namespace}.#{Rails.application.config.cdk[:domain_suffix]}"
        end

        Rails.logger.debug "DEBUG: Deconfiguring old app '#{app.name}' on #{source_container.id} after move"
        (1..num_tries).each do |i|
          begin
            reply.append source_container.destroy(app)
            break
          rescue Exception => e
            Rails.logger.debug "DEBUG: Error deconfiguring old app on try #{i}: #{e.message}"
            raise if i == num_tries
          end
        end
        Rails.logger.debug "Successfully moved '#{app.name}' with uuid #{app.uuid} from #{source_container.id} to #{destination_container_proxy.id}"
        reply
      end
      
      def update_namespace(app, cart, new_ns, old_ns)
        begin
          mcoll_reply = execute_direct(cart, 'update_namespace', "#{app.name} #{new_ns} #{old_ns} #{app.uuid}")
          result = parse_result(mcoll_reply)
          return result.exitcode == 0
        rescue Exception => e
          Rails.logger.debug "Exception caught updating namespace #{e.message}"
          Rails.logger.debug "DEBUG: Exception caught updating namespace #{e.message}"
          Rails.logger.debug e.backtrace
        end
        return false
      end
      
      #
      # Execute an RPC call for the specified agent.
      # If a server is supplied, only execute for that server.
      #
      def self.rpc_exec(agent, server=nil, forceRediscovery=false, options = rpc_options)
        if server
          Rails.logger.debug("DEBUG: rpc_exec: Filtering rpc_exec to server #{server}")
          # Filter to the specified server
          options[:filter]["identity"] = server
          options[:mcollective_limit_targets] = "1"
        end
      
        # Setup the rpc client
        rpc_client = rpcclient(agent, :options => options)
        if forceRediscovery
          rpc_client.reset
        end
        Rails.logger.debug("DEBUG: rpc_exec: rpc_client=#{rpc_client}")
      
        # Execute a block and make sure we disconnect the client
        begin
          result = yield rpc_client
        ensure
          rpc_client.disconnect
        end
      
        result
      end
      
      private
      
      def execute_direct(cartridge, action, args)
          mc_args = { :cartridge => cartridge,
                      :action => action,
                      :args => args }
          rpc_client = rpc_exec_direct('libra')
          result = nil
          begin
            Rails.logger.debug "DEBUG: rpc_client.custom_request('cartridge_do', #{mc_args.inspect}, #{@id}, {'identity' => #{@id}})"
            result = rpc_client.custom_request('cartridge_do', mc_args, @id, {'identity' => @id})
            Rails.logger.debug "DEBUG: #{result.inspect}"
          ensure
            rpc_client.disconnect
          end
          Rails.logger.debug result.inspect
          result
      end
      
      def parse_result(mcoll_reply, app=nil, command=nil)
        result = ResultIO.new
        
        mcoll_result = mcoll_reply[0]
        output = nil
        if (mcoll_result && defined? mcoll_result.results && mcoll_result.results.has_key?(:data))
          output = mcoll_result.results[:data][:output]
          result.exitcode = mcoll_result.results[:data][:exitcode]
          if command == "status" && app
            if result.exitcode == 0
              result.resultIO << output
            else
              result.exitcode = 0
              result.resultIO << "Application '#{app.name}' is either stopped or inaccessible"
            end
          else
            #Rails.logger.debug "--output--\n\n#{output}\n\n"
          end
        else
          raise Cloud::Sdk::NodeException.new("Node execution failure (error getting result from node).  If the problem persists please contact Red Hat support.", 143)
        end
        
        if output && !output.empty?
          output.each_line do |line|
            if line =~ /^CLIENT_(MESSAGE|RESULT|DEBUG|ERROR): /
              if line =~ /^CLIENT_MESSAGE: /
                result.messageIO << line['CLIENT_MESSAGE: '.length..-1]
              elsif line =~ /^CLIENT_RESULT: /
                result.resultIO << line['CLIENT_RESULT: '.length..-1]
              elsif line =~ /^CLIENT_DEBUG: /
                result.debugIO << line['CLIENT_DEBUG: '.length..-1]
              else
                result.errorIO << line['CLIENT_ERROR: '.length..-1]
              end
            elsif line =~ /^APP_INFO: /
              result.appInfoIO << line['APP_INFO: '.length..-1]
            elsif result.exitcode == 0
              if line =~ /^SSH_KEY_(ADD|REMOVE): /
                if line =~ /^SSH_KEY_ADD: /
                  key = line['SSH_KEY_ADD: '.length..-1].chomp
                  result.cart_commands.push({:command => "SYSTEM_SSH_KEY_ADD", :args => [key]})
                else
                  result.cart_commands.push({:command => "SYSTEM_SSH_KEY_REMOVE", :args => []})
                end
              elsif line =~ /^ENV_VAR_(ADD|REMOVE): /
                if line =~ /^ENV_VAR_ADD: /
                  env_var = line['ENV_VAR_ADD: '.length..-1].chomp.split('=')
                  result.cart_commands.push({:command => "ENV_VAR_ADD", :args => [env_var[0], env_var[1]]})
                else
                  key = line['ENV_VAR_REMOVE: '.length..-1].chomp
                  result.cart_commands.push({:command => "ENV_VAR_REMOVE", :args => [key]})
                end
              elsif line =~ /^BROKER_AUTH_KEY_(ADD|REMOVE): /
                if line =~ /^BROKER_AUTH_KEY_ADD: /
                  result.cart_commands.push({:command => "BROKER_KEY_ADD", :args => []})
                else
                  result.cart_commands.push({:command => "BROKER_KEY_REMOVE", :args => []})
                end
              else
                result.debugIO << line
              end
            else # exitcode != 0
              #result.debugIO << line
              Rails.logger.debug "DEBUG: server results: " + line
            end
          end
        end
        result
      end
      
      def run_cartridge_command(framework, app, command, arg=nil)
        arguments = "'#{app.name}' '#{app.user.namespace}' '#{app.uuid}'"
        arguments += " '#{arg}'" if arg
        
        result = execute_direct(framework, command, arguments)
        resultIO = parse_result(result, app, command)
        if resultIO.exitcode != 0
          resultIO.debugIO << "Cartridge return code: " + resultIO.exitcode.to_s
          raise Cloud::Sdk::NodeException.new("Node execution failure (invalid exit code from node).  If the problem persists please contact Red Hat support.", 143, resultIO)
        end
        resultIO
      end
      
      def self.rpc_find_available(node_profile=nil, forceRediscovery=false)
        current_server, current_capacity = nil, nil
        additional_filters = [
          {:fact => "capacity",
           :value => "100",
           :operator => "<"
          }
        ]
        if node_profile
          additional_filters.push({:fact => "node_profile",
                                   :value => node_profile,
                                   :operator => "=="})
        end
    
        rpc_get_fact('capacity', nil, forceRediscovery, additional_filters) do |server, capacity|
          Rails.logger.debug "Next server: #{server} capacity: #{capacity}"
          if !current_capacity || capacity.to_i < current_capacity.to_i
            current_server = server
            current_capacity = capacity
          end
          Rails.logger.debug "Current server: #{current_server} capacity: #{current_capacity}"
        end
        return current_server, current_capacity
      end
      
      def self.rpc_options
        # Make a deep copy of the default options
        Marshal::load(Marshal::dump(Rails.application.config.cdk[:rpc_opts]))
      end
    
      #
      # Return the value of the MCollective response
      # for both a single result and a multiple result
      # structure
      #
      def self.rvalue(response)
        result = nil
    
        if response[:body]
          result = response[:body][:data][:value]
        elsif response[:data]
          result = response[:data][:value]
        end
    
        result
      end
    
      def rsuccess(response)
        response[:body][:statuscode].to_i == 0
      end
    
      #
      # Returns the fact value from the specified server.
      # Yields to the supplied block if there is a non-nil
      # value for the fact.
      #
      def self.rpc_get_fact(fact, server=nil, forceRediscovery=false, additional_filters=nil)
        result = nil
        options = rpc_options
        options[:filter]['fact'] = options[:filter]['fact'] + additional_filters if additional_filters
    
        Rails.logger.debug("DEBUG: rpc_get_fact: fact=#{fact}")
        rpc_exec('rpcutil', server, forceRediscovery, options) do |client|
          client.get_fact(:fact => fact) do |response|
            next unless Integer(response[:body][:statuscode]) == 0
    
            # Yield the server and the value to the block
            result = rvalue(response)
            yield response[:senderid], result if result
          end
        end
    
        result
      end
    
      #
      # Given a known fact and node, get a single fact directly.
      # This is significantly faster then the get_facts method
      # If multiple nodes of the same name exist, it will pick just one
      #
      def rpc_get_fact_direct(fact)
          options = ApplicationContainerProxy.rpc_options
    
          rpc_client = rpcclient("rpcutil", :options => options)
          begin
            result = rpc_client.custom_request('get_fact', {:fact => fact}, @id, {'identity' => @id})[0]
            if (result && defined? result.results && result.results.has_key?(:data))
              value = result.results[:data][:value]
            else
              raise NodeException.new(143), "Node execution failure (error getting fact).  If the problem persists please contact Red Hat support."
            end
          ensure
            rpc_client.disconnect
          end
    
          return value
      end
    
      #
      # Execute direct rpc call directly against a node
      # If more then one node exists, just pick one
      def rpc_exec_direct(agent)
          options = ApplicationContainerProxy.rpc_options
          rpc_client = rpcclient(agent, :options => options)
          Rails.logger.debug("DEBUG: rpc_exec_direct: rpc_client=#{rpc_client}")
          rpc_client
      end
    end
  end
end
