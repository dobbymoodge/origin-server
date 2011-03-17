$LOAD_PATH << File.expand_path('../../../backend/controller/lib', __FILE__)
require 'mcollective'
require 'libra'
require 'timeout'
require 'logger'
require 'fileutils'
require 'open3'

World(MCollective::RPC)

#
# Define global variables
#
$curr_dir = File.expand_path(File.dirname(__FILE__))
$mc_client_cfg = File.expand_path("#{$curr_dir}/../misc/mcollective-client.cfg")
$pub_key = File.expand_path("#{$curr_dir}/../misc/id_rsa.pub")
$domain = "rhcloud.com"
$temp = "/tmp/rhc"
$create_app_script = "/usr/bin/rhc-create-app"
$create_domain_script = "/usr/bin/rhc-create-domain"
$client_config = "/etc/libra/client.conf"

# Create the temporary space
FileUtils.mkdir_p $temp

# Remove all temporary data
FileUtils.rm_f Dir.glob(File.join($temp, "*"))

module Libra
  module Test
    module User
      #
      # Obtain a unique namespace from S3.
      #
      #   reserved_namespace = A list of reserved namespaces that may
      #     not be in the global store
      #
      def get_unique_namespace(reserved_namespaces=[])
        result=nil

        loop do
          # Generate a random username
          chars = ("1".."9").to_a
          namespace = "sprint-ns-" + Array.new(5, '').collect{chars[rand(chars.size)]}.join
          $logger.info("li - checking availability of namespace = #{namespace}")

          records = Libra::Server.get_dns_txt(namespace)

          $logger.info("li - namespace lookup result = #{records}")

          unless !records.empty? or reserved_namespaces.index(namespace)
            result = namespace
            break
          end
        end

        $logger.info("li - returning namespace = #{result}")

        return result
      end

      #
      # Obtain a unique username from S3.
      #
      #   reserved_usernames = A list of reserved names that may
      #     not be in the global store
      #
      def get_unique_username(reserved_usernames=[])
        result=nil

        loop do
          # Generate a random username
          chars = ("1".."9").to_a
          username = "sprint" + Array.new(5, '').collect{chars[rand(chars.size)]}.join
          $logger.info("li - checking availability of username = #{username}")

          user = Libra::User.find(username)

          $logger.info("li - username lookup result = #{user}")

          unless user or reserved_usernames.index(username)
            result = username
            break
          end
        end

        $logger.info("li - returning username = #{result}")

        return result
      end

      #
      # Create a user with a unique username and a testing
      # email and ssh key
      #
      def create_unique_test_user
        @user = create_test_user(get_unique_username)
      end

      #
      # Create a user with the supplied username and a testing
      # email and ssh key
      #
      def create_test_user(rhlogin)
        Libra::User.create(rhlogin, $test_ssh_key, get_unique_namespace)
      end
    end

    module Util
      #
      # Run a command with logging.  If the command
      # returns a non-zero error code, raise an exception
      #
      def run(cmd)
          $logger.info("Running: #{cmd}")

          # Open up IO pipes for the sub process communication
          rd1, wr1 = IO.pipe
          rd2, wr2 = IO.pipe

          # Fork a subprocess so we can get an accurate return code
          # In Ruby 1.9, we can replace this with Process.spawn
          pid = fork do
            rd1.close
            rd2.close
            $stdout.reopen(wr1)
            $stderr.reopen(wr2)
            exec(cmd)
            raise "Command execution failed - #{cmd}"
          end

          # Close the end of the pipe we aren't using
          wr1.close
          wr2.close

          # Wait for the process to complete and get the exit code
          Process.wait(pid)
          exit_code = $?.exitstatus

          $logger.error("Standard Output:\n#{rd1.read}")
          $logger.info("Standard Error:\n#{rd2.read}")

          # Close out the streams
          rd1.close
          rd2.close

          raise "ERROR - Non-zero (#{exit_code}) exit code for #{cmd}" if exit_code != 0

          return exit_code
      end
    end
  end
end

# Global, one time setup
$logger = Logger.new(File.join($temp, "cucumber.log"))
$logger.level = Logger::DEBUG
Libra.c[:logger] = $logger
Libra.c[:bypass_user_reg] = true
#Libra.c[:rpc_opts][:verbose] = true

# Setup the MCollective options
Libra.c[:rpc_opts][:config] = $mc_client_cfg

# Setup test user info
$test_ssh_key = ssh_key = File.open($pub_key).gets.chomp.split(' ')[1]

# Default the maximum number of processes
@max_processes = 2
