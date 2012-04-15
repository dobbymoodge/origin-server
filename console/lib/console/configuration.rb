require 'active_support/configurable'
require 'active_support/core_ext/hash'

module Console

 # Configures global settings for Console
 # Console.configure do |config|
 # config.disable_assets = 10
 # end
 def self.configure(&block)
   yield config
 end

 # Global settings for Console
 def self.config
   @config ||= Configuration.new
 end

 puts "defined default config args"

 class InvalidConfiguration < StandardError ; end

 class Configuration #:nodoc:
    include ActiveSupport::Configurable

    config_accessor :disable_css
    config_accessor :disable_js
    config_accessor :disable_passthrough
    config_accessor :parent_controller

    Builtin = {
      :openshift => {
        :url => 'https://openshift.redhat.com/broker/rest',
        #:ssl_options => {},
        #:proxy => '',
        :authorization => :passthrough,
        :suffix => 'rhcloud.com'
      },
      :local => {
        :url => 'https://localhost/broker/rest',
        :suffix => 'rhcloud.com'
      }
    }
    Builtin.freeze

    def api=(config=nil)
      puts "Updating api with #{config.inspect}"
      config = case config
        when nil:
          symbol = :local
          config = Builtin[:local]
        when :none:
          return false
        when :external:
          begin
            symbol = :external
            path = File.expand_path('~/.openshift/api.yaml')
            Builtin[:openshift].with_indifferent_access.merge(YAML.load(IO.read(path)))
          rescue Exception => e
            raise InvalidConfiguration, <<-EXCEPTION, e.backtrace
The console is configured to use the external file #{path} (through config.stickshift = :external symbol in your environment file), but the file cannot be loaded.

By default you must only specify user and password in #{path}, but you can set any other attribute that the .stickshift config option accepts.

E.g. to connect to production OpenShift with a test account, you must only provide:

user: my_test_openshift_account@email.com
password: my_password

  #{e.message}
            EXCEPTION
          end
        when Symbol:
          symbol = config
          Builtin[config] || config
        else
          raise "Invalid argument to config.stickshift"
        end

      unless config && defined? config[:url]
        raise InvalidConfiguration, <<-EXCEPTION

The Console requires that Console.config.api be set to a symbol or endpoint configuration object.  Active configuration is #{Rails.env}

'#{config.inspect}' is not valid.

Valid symbols: #{Builtin.each_key.collect {|k| ":#{k}"}.join(', ')}
Valid api object:
  {
    :url => '' # A URL pointing to the root of the REST API, e.g. 
               # https://openshift.redhat.com/broker/rest
  }
        EXCEPTION
      end

      @api = config.clone
      @api[:symbol] = symbol

      @api
    end
    def api
      @api
    end
  end

  configure do |config|
    puts "Setting default config"
    config.disable_js = false
    config.disable_css = false
    config.disable_passthrough = false
    config.parent_controller = 'ApplicationController'
    config.api = nil
  end
end
