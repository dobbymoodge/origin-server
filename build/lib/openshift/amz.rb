require 'parseconfig'
require 'pp'
require 'aws'

module OpenShift
  module Amazon
    def setup_rsa_key
      unless File.exists?(RSA)
        log.info "Setting up RSA key..."
        libra_key = File.expand_path("../../../../misc/libra.pem", File.expand_path(__FILE__))
        log.info "Key location = " + libra_key
        log.info "Destination = " + RSA
        FileUtils.mkdir_p File.dirname(RSA)
        FileUtils.chmod 0700, File.dirname(RSA)
        FileUtils.cp libra_key, RSA
        FileUtils.chmod 0600, RSA
      end
    end

    def connect
      begin
        # Parse the credentials
        config = ParseConfig.new(File.expand_path("~/.awscred"))

        # Setup the SSH key
        setup_rsa_key

        # Setup the global access configuration
        AWS.config(
          :access_key_id => config.get_value("AWSAccessKeyId"),
          :secret_access_key => config.get_value("AWSSecretKey"),
          :ssl_ca_file => "/etc/pki/tls/certs/ca-bundle.trust.crt"
        )

        # Return the AMZ connection
        AWS::EC2.new
      rescue StandardError => e
        puts <<-eos
          Couldn't access credentials in ~/.awscred

          Please create a file with the following format:
            AWSAccessKeyId=<ACCESS_KEY>
            AWSSecretKey=<SECRET_KEY>
        eos
        puts e
        raise "Error - no credentials"
      end
    end

    def get_version(package)
      yum_output = `yum info #{package}`

      # Process the yum output to get a version
      version = yum_output.split("\n").collect do |line|
        line.split(":")[1].strip if line.start_with?("Version")
      end.compact[-1]

      # Process the yum output to get a release
      release = yum_output.split("\n").collect do |line|
        line.split(":")[1].strip if line.start_with?("Release")
      end.compact[-1]

      return "#{version}-#{release.split('.')[0]}"
    end

    def check_update
      yum_output = `yum check-update rhc-*`

      packages = {}
      yum_output.split("\n").each do |line|
        if line.start_with?("Obsoleting")
          break
        elsif line.start_with?("rhc")
          pkg_name = line.split[0]
          version = line.split[1]
          packages[pkg_name] = version
        end
      end

      packages
    end

    def get_amis(conn, filter = DEVENV_WILDCARD)
      conn.images.with_owner(:self).
        filter("state", "available").
        filter("name", filter)
    end

    def get_latest_ami(conn, filter_val = DEVENV_WILDCARD)
      AWS.memoize do
        # Limit to DevEnv images
        devenv_amis = conn.images.with_owner(:self).
          filter("state", "available").
          filter("name", filter_val)

        # Take the last DevEnv AMI - memoize saves a remote call
        devenv_amis.to_a.sort_by {|ami| ami.name.split("_")[1].to_i}.last
      end
    end

    def instance_status(instance)
      (1..10).each do |index|
        begin
          status = instance.status
          return status
        rescue Exception => e
          raise if index == 10
          log.info "Error getting status(retrying): #{e.message}"
          sleep 30
        end
      end
    end

    def find_instance(conn, name, use_tag=false)
      conn.instances.each do |i|
        if (instance_status(i) != :terminated)
          if (use_tag and i.tags["Name"] == name) or
             (!use_tag and i.dns_name == name)
            puts "Found instance #{i.id}"
            block_until_available(i)
            return i
          end
        end
      end

      return nil
    end

    def launch_instance(image, name, max_retries = 5)
      log.info "Creating new instance..."

      # You may have to retry creating instances since Amazon
      # fails at bringing them up every once in a while
      retries = 0

      # Launch a new instance
      instance = image.run_instance($amz_options)

      begin

        # Block until the instance is accessible
        block_until_available(instance)
      
        # Tag the instance
        instance.add_tag('Name', :value => name)

        return instance
      rescue ScriptError => e
        # Handles retrying instance creation for instances that
        # didn't come up with SSH access in time
        if retries <= max_retries
          log.info "Retrying instance creation (attempt #{retries + 1})..."

          # Terminate the current instance since it didn't load
          instance.terminate

          # Launch a new instance
          instance = image.run_instance($amz_options)

          # Retry the above logic to verify accessibility
          retries += 1
          retry
        else
          puts e.message
          exit 1
        end
      end
    end

    def block_until_available(instance)
      log.info "Waiting for instance to be available..."
      
      (0..12).each do
        break if instance_status(instance) == :running
        log.info "Instance isn't running yet... retrying"
        sleep 5
      end

      unless instance_status(instance) == :running
        instance.terminate
        raise ScriptError, "Timed out before instance was 'running'"
      end

      hostname = instance.dns_name
      (0..12).each do
        break if can_ssh?(hostname)
        log.info "SSH access failed... retrying"
        sleep 5
      end

      unless can_ssh?(hostname)
        instance.terminate 
        raise ScriptError, "SSH availability timed out"
      end

      log.info "Instance (#{hostname}) is accessible"
    end

    def is_valid?(hostname)
      @validation_output = ssh(hostname, '/usr/bin/rhc-accept-node')
      log.info "Node Acceptance Output = #{@validation_output}"
      @validation_output == "PASS"
    end

    def get_private_ip(hostname)
      private_ip = ssh(hostname, "facter ipaddress")
      if !private_ip or private_ip.strip.empty?
        puts "EXITING - AMZ instance didn't return ipaddress fact"
        exit 0
      end
      private_ip
    end
    
    def use_private_ip(hostname)
      private_ip = get_private_ip(hostname)
      set_instance_ip(hostname, private_ip)
    end
    
    def use_public_ip(hostname)
      public_ip = ssh(hostname, "wget -qO- http://169.254.169.254/latest/meta-data/public-ipv4")
      set_instance_ip(hostname, public_ip)
    end
    
    def set_instance_ip(hostname, ip)
      print "Updating the controller to use the ip '#{ip}'..."
      # Both calls below are needed to fix a race condition between ssh and libra-data start times
      ssh(hostname, "sed -i \"s/.*public_ip.*/public_ip='#{ip}'/g\" /etc/libra/node.conf;sed -i \"s/public_ip.*/public_ip='#{ip}'/g\" /etc/libra/node_data.conf")

      # Run update_yaml to correct facter calls
      ssh(hostname, "/usr/libexec/mcollective/update_yaml.rb")
      puts 'Done'
    end

    def verify_image(image)
      log.info "Tagging image (#{image.id}) as '#{VERIFIED_TAG}'..."
      image.add_tag('Name', :value => VERIFIED_TAG)
      log.info "Done"
    end

    def terminate_flagged_instances(conn)
      AWS.memoize do
        conn.instances.each do |i|
          if (instance_status(i) == :stopped) and (i.tags["Name"] =~ TERMINATE_REGEX)
            log.info "Terminating #{i.id}"
            i.terminate
          end
        end
      end
    end

    def stop_untagged_instances(conn)
      AWS.memoize do
        conn.instances.each do |i|
          if (instance_status(i) == :running) and (i.tags["Name"] == nil)
            # Tag the node to give people a heads up
            i.add_tag("Name", :value => "will-terminate")

            # Stop the nodes to save resources
            log.info "Stopping untagged instance #{i.id}"
            i.stop
          end
        end
      end
    end
  end
end
