require 'open4'
require 'pp'

module Cloud
  module Sdk
    class ApplicationContainerProxy
      @proxy_provider = Cloud::Sdk::ApplicationContainerProxy
      
      def self.provider=(provider_class)
        @proxy_provider = provider_class
      end
      
      def self.instance(id)
        @proxy_provider.new(id)
      end
      
      def self.find_available(node_profile=nil)
        @proxy_provider.find_available_impl(node_profile)
      end
      
      def self.find_one(node_profile=nil)
        @proxy_provider.find_one_impl(node_profile)
      end
      
      def self.blacklisted?(name)
      end
      
      attr_accessor :id
      def self.find_available_impl(node_profile=nil)
        @proxy_provider.instance('localhost')
      end
      
      def self.find_one_impl(node_profile=nil)
        @proxy_provider.instance('localhost')
      end
      
      def initialize(id)
        @id = id
      end
     
      def reserve_uid
      end
 
      def get_available_cartridges
        reply = exec_command('cdk-cartridge-list', '--porcelain --with-descriptors')
        result = parse_result(reply)
        cart_data = JSON.parse(result.resultIO.string)
        cart_data.map! {|c| Cloud::Sdk::Cartridge.new.from_descriptor(YAML.load(c))}
      end
      
      def create(app, gear)
        cmd = "cdk-app-create"
        args = "--with-app-uuid '#{app.uuid}' --named '#{app.name}' --with-container-uuid '#{gear.uuid}'"
        Rails.logger.debug("App creation command: #{cmd} #{args}")
        reply = exec_command(cmd, args)
        parse_result(reply)
      end
    
      def destroy(app, gear)
        cmd = "cdk-app-destroy"
        args = "--with-app-uuid '#{app.uuid}' --with-container-uuid '#{gear.uuid}'"
        Rails.logger.debug("App destroy command: #{cmd} #{args}")
        reply = exec_command(cmd, args)
        parse_result(reply)
      end
      
      def add_authorized_ssh_key(app, gear, ssh_key, key_type=nil, comment=nil)
        cmd = "cdk-authorized-ssh-key-add"
        args = "--with-app-uuid '#{app.uuid}' --with-container-uuid '#{gear.uuid}' -s '#{ssh_key}'"
        args += " -t '#{key_type}'" if key_type
        args += " -m '-#{comment}'" if comment
        Rails.logger.debug("App ssh key: #{cmd} #{args}")
        result = exec_command(cmd, args)
        parse_result(result)
      end
      
      def remove_authorized_ssh_key(app, gear, ssh_key)
        cmd = "cdk-authorized-ssh-key-remove"
        args = "--with-app-uuid '#{app.uuid}' --with-container-uuid '#{gear.uuid}' -s '#{ssh_key}'" 
        Rails.logger.debug("Remove ssh key: #{cmd} #{args}")
        result = exec_command(cmd, args)
        parse_result(result)
      end

      def add_env_var(app, gear, key, value)
        cmd = "cdk-env-var-add"
        args = "--with-app-uuid '#{app.uuid}' --with-container-uuid '#{gear.uuid}' -k '#{key}' -v '#{value}'"
        Rails.logger.debug("Env var add command: #{cmd} #{args}")
        reply = exec_command(cmd, args)
        parse_result(reply)
      end
      
      def remove_env_var(app, gear, key)
        cmd = "cdk-env-var-remove"
        args = "--with-app-uuid '#{app.uuid}' --with-container-uuid '#{gear.uuid}' -k '#{key}'"
        Rails.logger.debug("Env var remove command: #{cmd} #{args}")
        reply = exec_command(cmd, args)
        parse_result(reply)
      end
    
      def add_broker_auth_key(app, gear, iv, token)
        cmd = "cdk-broker-auth-key-add"
        args = "--with-app-uuid '#{app.uuid}' --with-container-uuid '#{gear.uuid}' -i '#{iv}' -t '#{token}'"
        Rails.logger.debug("Add broker auth key command: #{cmd} #{args}")
        reply = exec_command(cmd, args)
        parse_result(reply)
      end
    
      def remove_broker_auth_key(app, gear)
        cmd = "cdk-broker-auth-key-remove"
        args = "--with-app-uuid '#{app.uuid}' --with-container-uuid '#{gear.uuid}'"
        Rails.logger.debug("Add broker auth key command: #{cmd} #{args}")
        reply = exec_command(cmd, args)
        parse_result(reply)
      end
      
      def preconfigure_cartridge(app, gear, cart)
        Rails.logger.debug("Inside preconfigure_cartridge :: application: #{app.name} :: cartridge name: #{cart}")

        if framework_carts.include? cart
          run_cartridge_command(cart, app, gear, "preconfigure")
        else
          #no-op
          ResultIO.new
        end
      end
      
      def configure_cartridge(app, gear, cart)
        Rails.logger.debug("Inside configure_cartridge :: application: #{app.name} :: cartridge name: #{cart}")

        result_io = ResultIO.new
        cart_data = nil
                  
        if framework_carts.include? cart
          result_io = run_cartridge_command(cart, app, gear, "configure")
        elsif embedded_carts.include? cart
          result_io, cart_data = add_component(app, gear, cart)
        else
          #no-op
        end
        
        return result_io, cart_data
      end
      
      def deconfigure_cartridge(app, gear, cart)
        Rails.logger.debug("Inside deconfigure_cartridge :: application: #{app.name} :: cartridge name: #{cart}")

        if framework_carts.include? cart
          run_cartridge_command(cart, app, gear, "deconfigure")
        elsif embedded_carts.include? cart
          remove_component(app,gear,cart)
        else
          ResultIO.new
        end        
      end
      
      def get_public_hostname
      end
      
      def start(app, gear, cart)
        if framework_carts.include?(cart)
          run_cartridge_command(cart, app, gear, "start")
        elsif embedded_carts.include? cart
          start_component(app, gear, cart)
        else
          ResultIO.new
        end
      end
      
      def stop(app, gear, cart)
        if framework_carts.include?(cart)
          run_cartridge_command(cart, app, gear, "stop")
        elsif embedded_carts.include? cart
          stop_component(app, gear, cart)
        else
          ResultIO.new
        end
      end
      
      def force_stop(app, gear, cart)
        if framework_carts.include?(cart)
          run_cartridge_command(cart, app, gear, "force-stop")
        else
          ResultIO.new
        end          
      end
      
      def expose_port(app, gear, cart)
        run_cartridge_command(cart, app, gear, "expose-port")
      end

      def conceal_port(app, gear, cart)
        run_cartridge_command(cart, app, gear, "conceal-port")
      end

      def show_port(app, gear, cart)
        run_cartridge_command(cart, app, gear, "show-port")
      end

      def restart(app, gear, cart)
        if framework_carts.include?(cart)
          run_cartridge_command(cart, app, gear, "restart")
        elsif embedded_carts.include? cart
          restart_component(app, gear, cart)
        else
          ResultIO.new                  
        end
      end

      def reload(app, gear, cart)
        if framework_carts.include?(cart)
          run_cartridge_command(cart, app, gear, "reload")
        elsif embedded_carts.include? cart
          reload_component(app, gear, cart)
        else
          ResultIO.new          
        end
      end
      
      def status(app, gear, cart)
        if framework_carts.include?(cart)
          run_cartridge_command(cart, app, gear, "status")
        elsif embedded_carts.include? cart
          component_status(app, gear, cart)
        else
          ResultIO.new          
        end
      end
      
      def tidy(app, gear, cart)
        if framework_carts.include?(cart)        
          run_cartridge_command(cart, app, gear, "tidy") 
        else
          ResultIO.new
        end
      end
      
      def threaddump(app, gear, cart)
        if framework_carts.include?(cart)
          run_cartridge_command(cart, app, gear, "threaddump")
        else
          ResultIO.new
        end          
      end
      
      def system_messages(app, gear, cart)
        if framework_carts.include?(cart)
          run_cartridge_command(cart, app, gear, "system-messages")
        else
          ResultIO.new
        end          
      end
      
      def add_alias(app, gear, cart, server_alias)
        if framework_carts.include?(cart)
          run_cartridge_command(cart, app, gear, "add-alias", server_alias)
        else
          ResultIO.new
        end
      end
      
      def remove_alias(app, gear, cart, server_alias)
        if framework_carts.include?(cart)        
          run_cartridge_command(cart, app, gear, "remove-alias", server_alias)
        else
          ResultIO.new
        end
      end
      
      def framework_carts
        @framework_carts ||= CartridgeCache.cartridge_names('standalone')
      end
      
      def embedded_carts
        @embedded_carts ||= CartridgeCache.cartridge_names('embedded')
      end
      
      def add_component(app, gear, component)
        reply = ResultIO.new
        begin
          reply.append run_cartridge_command('embedded/' + component, app, gear, 'configure')
        rescue Exception => e
          begin
            Rails.logger.debug "DEBUG: Failed to embed '#{component}' in '#{app.name}' for user '#{app.user.login}'"
            reply.debugIO << "Failed to embed '#{component} in '#{app.name}'"
            reply.append run_cartridge_command('embedded/' + component, app, gear, 'deconfigure')
          ensure
            raise
          end
        end
        
        component_details = reply.appInfoIO.string.empty? ? '' : reply.appInfoIO.string
        reply.debugIO << "Embedded app details: #{component_details}"
        [reply, component_details]
      end
      
      def remove_component(app, gear, component)
        Rails.logger.debug "DEBUG: Deconfiguring embedded application '#{component}' in application '#{app.name}' on node '#{@id}'"
        return run_cartridge_command('embedded/' + component, app, gear, 'deconfigure')
      end

      def start_component(app, gear, component)
        run_cartridge_command('embedded/' + component, app, gear, "start")
      end
      
      def stop_component(app, gear, component)
        run_cartridge_command('embedded/' + component, app, gear, "stop")
      end
      
      def restart_component(app, gear, component)
        run_cartridge_command('embedded/' + component, app, gear, "restart")    
      end
      
      def reload_component(app, gear, component)
        run_cartridge_command('embedded/' + component, app, gear, "reload")    
      end
      
      def component_status(app, gear, component)
        run_cartridge_command('embedded/' + component, app, gear, "status")    
      end
      
      def move_app(app, destination_container_proxy, node_profile=nil)
      end
      
      def update_namespace(app, cart, new_ns, old_ns)
      end
      
      def run_cartridge_command(framework, app, gear, command, arg=nil)
        if app.scalable and framework!=app.proxy_cartridge
          appname = gear.uuid[0..9] 
        else
          appname = app.name
        end
        arguments = "'#{appname}' '#{app.user.namespace}' '#{gear.uuid}'"
        arguments += " '#{arg}'" if arg

        reply = {}
        if File.exists? "/usr/libexec/li/cartridges/#{framework}/info/hooks/#{command}"
          reply = exec_command("/usr/libexec/li/cartridges/#{framework}/info/hooks/#{command}", arguments)
        else
          reply[:output] = "run_cartridge_command ERROR action '#{command}' not found."
          reply[:exitcode] = 127
          Rails.logger.error("run_cartridge_command failed: 127.  Output: Cartridge hook not found: /usr/libexec/li/cartridges/#{framework}/info/hooks/#{command}")
        end
        
        resultIO = parse_result(reply, app, command)
        if resultIO.exitcode != 0
          resultIO.debugIO << "Cartridge return code: " + resultIO.exitcode.to_s
          begin
            raise Cloud::Sdk::NodeException.new("Node execution failure (invalid exit code from node).  If the problem persists please contact Red Hat support.", 143, resultIO)
          rescue Cloud::Sdk::NodeException => e
            if command == 'deconfigure'
              if framework.start_with?('embedded/')
                if has_embedded_app?(app.uuid, framework[9..-1])
                  raise
                else
                  Rails.logger.debug "DEBUG: Component '#{framework}' in application '#{app.name}' not found on node '#{@id}'.  Continuing with deconfigure."
                end
              else
                if has_app?(app.uuid, app.name)
                  raise
                else
                  Rails.logger.debug "DEBUG: Application '#{app.name}' not found on node '#{@id}'.  Continuing with deconfigure."
                end
              end
            else
              raise
            end
          end
        end
        resultIO
      end
      
      def exec_command(cmd, args)
        reply = {}
        exitcode = 1
        pid, stdin, stdout, stderr = nil, nil, nil, nil

        Bundler.with_clean_env {
          pid, stdin, stdout, stderr = Open4::popen4("#{cmd} #{args} 2>&1")
          stdin.close
          ignored, status = Process::waitpid2 pid
          exitcode = status.exitstatus
        }
        
        # Do this to avoid cartridges that might hold open stdout
        output = ""
        begin
          Timeout::timeout(5) do
            while (line = stdout.gets)
              output << line
            end
          end
        rescue Timeout::Error
          Rails.logger.debug("exec_command WARNING - stdout read timed out")
        end

#        if exitcode == 0
#          Rails.logger.debug("exec_command (#{exitcode})\n------\n#{output}\n------)")
#        else
#          Rails.logger.debug("exec_command ERROR (#{exitcode})\n------\n#{output}\n------)")
#        end

        reply[:output] = output
        reply[:exitcode] = exitcode
        Rails.logger.error("exec_command failed #{exitcode}.  Output #{output}") unless exitcode == 0
        reply
      end

      def parse_result(cmd_result, app=nil, command=nil)
        result = ResultIO.new
        
        Rails.logger.debug("cmd_reply:  #{cmd_result}")
        output = nil
        if (cmd_result && cmd_result.has_key?(:output))
          output = cmd_result[:output]
          result.exitcode = cmd_result[:exitcode]
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
              elsif line =~ /^ATTR: /
                attr = line['ATTR: '.length..-1].chomp.split('=')
                result.cart_commands.push({:command => "ATTR", :args => [attr[0], attr[1]]})
              else
                #result.debugIO << line
              end
            else # exitcode != 0
              result.debugIO << line
              Rails.logger.debug "DEBUG: server results: " + line
            end
          end
        end
        result
      end

      #
      # Returns whether this app is present
      #
      def has_app?(app_uuid, app_name)
        return false
      end
      
      #
      # Returns whether this embedded app is present
      #
      def has_embedded_app?(app_uuid, embedded_type)
        return false
      end
    end
  end
end