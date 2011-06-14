require 'openshift/helper'
require 'openshift/server'
require 'openshift/nurture'
require 'aws'
require 'json'
require 'date'
require 'net/http'
require 'net/https'
require 'pp'

def gen_small_uuid()
    # Put config option for rhlogin here so we can ignore uuid for dev environments
    %x[/usr/bin/uuidgen].gsub('-', '').strip
end

module Libra
  class User
    attr_reader :rhlogin
    attr_accessor :ssh, :namespace, :uuid

    def initialize(rhlogin, ssh, namespace, uuid)
      @rhlogin, @ssh, @namespace, @uuid = rhlogin, ssh, namespace, uuid
    end

    def self.from_json(json)
      data = JSON.parse(json)
      if data['uuid']
        new(data['rhlogin'], data['ssh'], data['namespace'], data['uuid'])
      else
        uuid = gen_small_uuid()
        user = new(data['rhlogin'], data['ssh'], data['namespace'], uuid)
        user.update
        user
      end
    end

    #
    # Creates a new user, raising an exception
    # if the user already exists or invalid chars are found.
    #
    def self.create(rhlogin, ssh, namespace)

      auth_token = nil
      begin
        auth_token = Server.dyn_login
        raise UserException.new(107), "Invalid characters in RHlogin '#{rhlogin}' found", caller[0..5] if !Util.check_rhlogin(rhlogin)
        raise UserException.new(102), "A user with RHLogin '#{rhlogin}' already exists", caller[0..5] if find(rhlogin)

        Server.dyn_has_txt_record?(namespace, auth_token, true)

        Libra.client_debug "Creating user entry rhlogin:#{rhlogin} ssh:#{ssh} namespace:#{namespace}" if Libra.c[:rpc_opts][:verbose]

        Server.dyn_create_txt_record(namespace, auth_token)
        Server.dyn_publish(auth_token) # TODO should we publish on ensure?
        Libra.logger_debug "DEBUG: Attempting to add namespace '#{namespace}' for user '#{rhlogin}'"
        Libra.client_debug "Creating user entry rhlogin:#{rhlogin} ssh:#{ssh} namespace:#{namespace}" if Libra.c[:rpc_opts][:verbose]
        begin
          uuid = gen_small_uuid()
          user = new(rhlogin, ssh, namespace, uuid)
          user.update
          begin
            Nurture.libra_contact(rhlogin, uuid, namespace)
          rescue Exception => e
            Libra.logger_debug "DEBUG: Attempting to delete user '#{rhlogin}' after failing to add nurture contact"
            begin
              user.delete
            ensure
              raise
            end
          end
          return user
        rescue Exception => e
          Libra.logger_debug "DEBUG: Attempting to remove namespace '#{namespace}' after failure to add user '#{rhlogin}'"
          begin
            Server.dyn_delete_txt_record(namespace, auth_token)
            Server.dyn_publish(auth_token) # TODO should we publish on ensure?
          ensure
            raise
          end
        end
      ensure
        Server.dyn_logout(auth_token)
      end
    end
    
    #
    # Returns username if a valid user, nil if not found, and raises an exception if user hasn't requested/been granted access. 
    #
    #   User.login
    #
    def self.login(rhlogin, password)
      username = nil
      if !Libra.c[:bypass_user_reg]
        raise UserException.new(107), "Invalid characters in RHlogin '#{rhlogin}' found", caller[0..5] if !Util.check_rhlogin(rhlogin)
        begin
          url = URI.parse(Libra.c[:streamline_url] + '/wapps/streamline/login.html')
          req = Net::HTTP::Post.new(url.path)
          
          req.set_form_data({ 'login' => rhlogin, 'password' => password })
          http = Net::HTTP.new(url.host, url.port)
          if url.scheme == "https"
            http.use_ssl = true
            http.verify_mode = OpenSSL::SSL::VERIFY_NONE
          end
          response = http.start {|http| http.request(req)}
          
          case response
          when Net::HTTPSuccess
            json = JSON.parse(response.body)
            roles = json['roles']
            if roles.index('cloud_access_1')
              username = json['username'] || json['login'] # remove 'login' if/once streamline changes to username like cloudVerify
            elsif roles.index('cloud_access_request_1')
              raise UserValidationException.new(146), "Found valid credentials but you haven't been granted access to Express yet", caller[0..5]
            else
              raise UserValidationException.new(147), "Found valid credentials but you haven't requested access to Express yet", caller[0..5]
            end
          else
            Libra.client_debug "Response code from authentication: #{response.code}"
            Libra.logger_debug "Response code from authentication: #{response.code}"
            Libra.logger_debug "HTTP response from server is #{response.body}"
          end
        rescue UserValidationException => e
          raise
        rescue Exception => e          
          Libra.logger_debug "Error message from authentication exception: #{e.message}"
          Libra.logger_debug e.backtrace
          raise UserValidationException.new(144), "Error communicating with user validation system.  If the problem persists please contact Red Hat support.", caller[0..5]
        end
        return username
      else
        return rhlogin
      end
    end
    
    #
    # Validates number of apps for a user is below the limit
    #
    def validate_app_limit
      num_apps = apps.length
      Libra.client_debug "Validating application limit #{@rhlogin}: num of apps(#{num_apps.to_s}) must be < app limit (#{Libra.c[:per_user_app_limit]})" if Libra.c[:rpc_opts][:verbose]
      if (num_apps >= Libra.c[:per_user_app_limit])
        raise UserException.new(104), "#{@rhlogin} has already reached the application limit of #{Libra.c[:per_user_app_limit]}", caller[0..5]
      end
    end

    #
    # Finds all registered rhlogins
    #
    #   User.find_all_rhlogins
    #
    def self.find_all_rhlogins
      rhlogins = []

      # Retrieve the current list of rhlogins
      Helper.s3.incrementally_list_bucket(Libra.c[:s3_bucket], { 'prefix' => 'user_info'}) do |result|         
        result[:contents].each do |bucket|
          if bucket[:key] =~ /\/user.json$/
            rhlogins << File.basename(File.dirname(bucket[:key]))
          end
        end
      end
      rhlogins
    end

    #
    # Finds a registered user.
    #
    #   User.find('test_user')
    #
    def self.find(rhlogin)
      begin
        return User.from_json(Helper.s3.get(Libra.c[:s3_bucket], "user_info/#{rhlogin}/user.json")[:object])
      rescue Aws::AwsError => e
        if e.message =~ /^NoSuchKey/
          return nil
        else
          raise e
        end
      end
    end

    #
    # Updates the user with the current information
    #
    def update
      json = JSON.generate({:rhlogin => rhlogin, :namespace => namespace, :ssh => ssh, :uuid => uuid})
      Libra.logger_debug "Updating user json:#{json}" if Libra.c[:rpc_opts][:verbose]
      Helper.s3.put(Libra.c[:s3_bucket], "user_info/#{rhlogin}/user.json", json)
    end
    
    #
    # Updates the user's namespace for txt and full app domains
    #
    def update_namespace(new_namespace)
      auth_token = Server.dyn_login
      begin
        Server.dyn_has_txt_record?(new_namespace, auth_token, true) 
        Server.dyn_create_txt_record(new_namespace, auth_token)
        Server.dyn_delete_txt_record(@namespace, auth_token)
        apps.each do |app_name, app_info|
          Libra.logger_debug "Updating namespaces for app: #{app_name}" if Libra.c[:rpc_opts][:verbose]
          server = Server.new(app_info['server_identity'])
          public_ip = server.get_fact_direct('public_ip')
          sshfp = server.get_fact_direct('sshfp').split[-1]
          
          # Cleanup the previous records 
          Server.dyn_delete_sshfp_record(app_name, @namespace, auth_token)            
          Server.dyn_delete_a_record(app_name, @namespace, auth_token)     
          
          # add the new entries          
          Server.dyn_create_a_record(app_name, new_namespace, public_ip, sshfp, auth_token)         
          Server.dyn_create_sshfp_record(app_name, new_namespace, sshfp, auth_token)
        end
        
        update_namespace_failures = []
        apps.each do |app_name, app_info|
          begin
            Libra.logger_debug "Updating namespace for app: #{app_name}" if Libra.c[:rpc_opts][:verbose]
            server = Server.new(app_info['server_identity'])
            result = server.execute_direct(app_info['framework'], 'update_namespace', "#{app_name} #{new_namespace} #{@namespace} #{app_info['uuid']}")[0]
            if (result && defined? result.results)            
              exitcode = result.results[:data][:exitcode]
              if exitcode != 0
                update_namespace_failures.push(app_name)
                output = result.results[:data][:output]
                Libra.client_debug "Cartridge return code: " + exitcode.to_s
                Libra.client_debug "Cartridge output: " + output
                Libra.logger_debug "DEBUG: execute_direct results: " + output                
              end
            else
              update_namespace_failures.push(app_name)
            end
          rescue Exception => e
            Libra.client_debug "Exception caught updating namespace #{e.message}"
            Libra.logger_debug "DEBUG: Exception caught updating namespace #{e.message}"
            Libra.logger_debug e.backtrace     
            update_namespace_failures.push(app_name)
          end
        end
        
        raise NodeException.new(143), "Error updating apps: #{update_namespace_failures.pretty_inspect.chomp}.  Updates will not be completed until all apps can be updated successfully.  If the problem persists please contact Red Hat support.", caller[0..5] if !update_namespace_failures.empty?
        
        Server.dyn_publish(auth_token)
      rescue LibraException => e
        raise
      rescue Exception => e
        Libra.client_debug "Exception caught updating namespace: #{e.message}"
        Libra.logger_debug "DEBUG: Exception caught updating namespace: #{e.message}"
        Libra.logger_debug e.backtrace
        raise LibraException.new(254), "An error occurred updating the namespace.  If the problem persists please contact Red Hat support.", caller[0..5]
      ensure
        Server.dyn_logout(auth_token)
      end
    end
    
    #
    # Deletes the user with the current information
    #    
    def delete
      Libra.client_debug "DEBUG: Deleting user: #{rhlogin}" if Libra.c[:rpc_opts][:verbose]
      Helper.s3.delete(Libra.c[:s3_bucket], "user_info/#{rhlogin}/user.json")
    end

    #
    # Returns the servers that this user exists on
    #
    def servers
      # Use the cached value if it exists
      unless @servers
        @servers = {}

        # Make the rpc call to check
        Helper.rpc_get_fact("customer_#{rhlogin}") do |server, value|
          # Initialize the hash with the server as the key
          # The applications will eventually become the value
          @servers[Server.new(server)] = nil
        end
      end

      return @servers.keys
    end

    #
    # Returns the applications that this user has running
    #
    def apps
      # Use the cached value if it exists
      unless @apps
        @apps = {}
        app_list = Helper.s3.list_bucket(Libra.c[:s3_bucket],
                  { 'prefix' => "user_info/#{@rhlogin}/apps/"})
        app_list.each do |key|
          json = Helper.s3.get(Libra.c[:s3_bucket], key[:key])
          app_name = key[:key].sub("user_info/#{@rhlogin}/apps/", "").sub(".json", "")
          @apps[app_name] = app_info(app_name)
        end
      end
      @apps
    end

    #
    # Create's an S3 cache of the app for easy tracking and verification
    #
    def create_app(app_name, framework, server,
                   creation_time=DateTime::now().strftime,
                   uuid=nil
                   )
      h = {
        'framework' => framework,
        'server_identity' => server.name,
        'creation_time' => creation_time,
        'uuid' => uuid || gen_small_uuid
      }
      json = JSON.generate h
      Helper.s3.put(Libra.c[:s3_bucket],
                    "user_info/#{@rhlogin}/apps/#{app_name}.json", json)
      h
    end
    
    #
    # Updates the S3 cache of the app
    #
    def update_app(app, app_name)
      json = JSON.generate(app)
      Helper.s3.put(Libra.c[:s3_bucket],
                    "user_info/#{@rhlogin}/apps/#{app_name}.json", json)
    end

    #
    # Delete an S3 cache of an app
    #
    def delete_app(app_name)
      Helper.s3.delete(Libra.c[:s3_bucket],
                        "user_info/#{@rhlogin}/apps/#{app_name}.json")
    end

    #
    # Check if an application already exists
    #
    def app_info(app_name)
      return JSON.parse(Helper.s3.get(Libra.c[:s3_bucket],
            "user_info/#{@rhlogin}/apps/#{app_name}.json")[:object])
    rescue Aws::AwsError => e
      if e.message =~ /^NoSuchKey/
        return nil
      else
        raise e
      end
    end


    #
    # Clears out any cached data
    #
    def reload
      @servers, @apps = nil
    end

    #
    # Base equality on the rhlogin
    #
    def ==(another_user)
      self.rhlogin == another_user.rhlogin
    end

    #
    # Base sorting on the rhlogin
    #
    def <=>(another_user)
      self.rhlogin <=> another_user.rhlogin
    end
  end
end
