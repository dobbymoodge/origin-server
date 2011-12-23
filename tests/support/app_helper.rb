require 'openshift'
require 'active_support'

module AppHelper
  class TestApp
    include ActiveSupport::JSON

    # The regex to parse the ssh output from the create app results
    SSH_OUTPUT_PATTERN = %r|ssh://([^@]+)@([^/]+)|

    # attributes to represent the general information of the application
    attr_accessor :name, :namespace, :login, :type, :hostname, :repo, :file, :embed, :snapshot, :uid

    # attributes to represent the state of the rhc_create_* commands
    attr_accessor :create_domain_code, :create_app_code

    # attributes that contain statistics based on calls to connect
    attr_accessor :response_code, :response_time

    # mysql connection information
    attr_accessor :mysql_hostname, :mysql_user, :mysql_password, :mysql_database

    # Create the data structure for a test application
    def initialize(namespace, login, type, name)
      @name, @namespace, @login, @type = name, namespace, login, type
      @hostname = "#{name}-#{namespace}.#{$domain}"
      @repo = "#{$temp}/#{namespace}_#{name}_repo"
      @file = "#{$temp}/#{namespace}.json"
    end

    def self.create_unique(type, name="test")
      loop do
        # Generate a random username
        chars = ("1".."9").to_a
        namespace = "ci" + Array.new(8, '').collect{chars[rand(chars.size)]}.join
        login = "libra-test+#{namespace}@redhat.com"
        app = TestApp.new(namespace, login, type, name)
        unless app.reserved?
          app.persist
          return app
        end
      end
    end

    def self.find_on_fs
      Dir.glob("#{$temp}/*.json").collect {|f| TestApp.from_file(f)}
    end

    def self.from_file(filename)
      TestApp.from_json(ActiveSupport::JSON.decode(File.open(filename, "r") {|f| f.readlines}[0]))
    end

    def self.from_json(json)
      app = TestApp.new(json['namespace'], json['login'], json['type'], json['name'])
      app.embed = json['embed']
      app.mysql_user = json['mysql_user']
      app.mysql_password = json['mysql_password']
      app.mysql_hostname = json['mysql_hostname']
      return app
    end

    def update_uid(std_output)
      match = std_output.map {|line| line.match(SSH_OUTPUT_PATTERN)}.compact[0]
      @uid = match[1]
    end

    def get_log(prefix)
      "#{$temp}/#{prefix}_#{@name}-#{@namespace}.log"
    end

    def persist
      File.open(@file, "w") {|f| f.puts self.to_json}
    end

    def reserved?
      OpenShift::Server.has_dns_txt?(@namespace) or File.exists?(@file)
    end

    def has_domain?
      return create_domain_code == 0
    end

    def get_index_file
      case @type
        when "php-5.3" then "php/index.php"
        when "rack-1.1" then "config.ru"
        when "wsgi-3.2" then "wsgi/application"
        when "perl-5.10" then "perl/index.pl"
        when "jbossas-7.0" then "src/main/webapp/index.html"
      end
    end

    def get_mysql_file
      case @type
        when "php-5.3" then File.expand_path("../misc/php/db_test.php", File.expand_path(File.dirname(__FILE__)))
      end
    end

    def get_stop_string
      "stopped"
    end

    def curl(url, timeout=30)
      body = `curl --insecure -s --max-time #{timeout} #{url}`
      exit_code = $?.exitstatus

      return exit_code, body
    end

    def curl_head(url, host=nil)
      if host
        `curl --insecure -s --head -H 'Host: #{host}' --max-time 30 #{url} | grep 200`
      else
        `curl --insecure -s --head --max-time 30 #{url} | grep 200`
      end
      exit_code = $?.exitstatus
      return exit_code
    end

    def is_inaccessible?(max_retries=60)
      max_retries.times do |i|
        if curl_head("http://#{hostname}") != 0
          return true
        else
          $logger.info("Connection still accessible / retry #{i} / #{hostname}")
          sleep 1
        end
      end

      return false
    end

    # Host is for the host header
    def is_accessible?(use_https=false, max_retries=120, host=nil)
      prefix = use_https ? "https://" : "http://"
      url = prefix + hostname

      max_retries.times do |i|
        if curl_head(url, host) == 0
          return true
        else
          $logger.info("Connection still inaccessible / retry #{i} / #{url}")
          sleep 1
        end
      end

      return false
    end

    def connect(use_https=false, max_retries=30)
      prefix = use_https ? "https://" : "http://"
      url = prefix + hostname

      $logger.info("Connecting to #{url}")
      beginning_time = Time.now

      max_retries.times do |i|
        code, body = curl(url, 1)

        if code == 0
          @response_code = code.to_i
          @response_time = Time.now - beginning_time
          $logger.info("Connection result = #{code} / #{url}")
          $logger.info("Connection response time = #{@response_time} / #{url}")
          return body
        else
          $logger.info("Connection failed / retry #{i} / #{url}")
          sleep 1
        end
      end

      return nil
    end
  end
end
World(AppHelper)
