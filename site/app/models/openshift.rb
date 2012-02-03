require 'active_support/core_ext/hash/conversions'
require 'active_resource'

class UserAwareConnection < ActiveResource::Connection
  attr :as

  def initialize(url, format, as)
    super url, format
    @as = as
  end

  def authorization_header(http_method, uri)
    headers = super
    headers['Cookies'] << @as.streamline_cookie if @as.respond_to?(:streamline_cookie) && @as.streamline_cookie
    headers
  end
end

class OpenshiftResource < ActiveResource::Base

  self.site = if defined?(Rails) && Rails.configuration.express_api_url
    Rails.configuration.express_api_url + '/broker/rest'
  else
    ActiveSupport::XmlMini.backend = 'REXML'
    ActiveResource::HttpMock.respond_to do |mock|
      mock.get '/user/keys.xml', {}, [{:type => :rsa, :name => 'test1', :value => '1234' }].to_xml(:root => 'ssh_key')
      mock.post '/user/keys.xml', {}, {:type => :rsa, :name => 'test2', :value => '1234_2' }.to_xml(:root => 'ssh_key')
      mock.delete '/user/keys/test1.xml', {}, {}
    end
    'http://localhost'
  end

  # Track persistence state, merged from 
  # https://github.com/railsjedi/rails/commit/9333e0de7d1b8f63b19c99d21f5f65fef0ce38c3
  #
  def initialize(attributes = {}, persisted=false)
    @persisted = persisted
    super attributes
  end

  def instantiate_record(record, prefix_options = {})
    new(record, true).tap do |resource|
      resource.prefix_options = prefix_options
    end
  end

  def new?
    !persisted?
  end

  def persisted?
    @persisted
  end

  def load_attributes_from_response(response)
    if response['Content-Length'] != "0" && response.body.strip.size > 0
      load(update_root(self.class.format.decode(response.body)))
      @persisted = true
    end
  end

  def update_root(obj)
    obj
  end
 
  # 
  # has_many / belongs_to placeholders
  #
  def self.has_many(sym)
  end
  def self.belongs_to(sym)
    self.prefix = "#{self.prefix}#{sym.to_s}/"
  end


  def self.update_connection(connection)
    connection.proxy = proxy if proxy
    connection.user = user if user
    connection.password = password if password
    connection.auth_type = auth_type if auth_type
    connection.timeout = timeout if timeout
    connection.ssl_options = ssl_options if ssl_options
    connection
  end

  class << self
    #
    # Override methods from ActiveResource to make them contextual connection
    # aware
    #
    def delete(id, options = {})
      connection(options).delete(element_path(id, options))
    end

    #
    # Make connection specific to the instance, and aware of user context
    #
    def connection(options = {}, refresh = false)
      if options[:as]
        puts 'context aware connection'
        update_connection(UserAwareConnection.new(site, format, options[:as]))
      elsif defined?(@connection) || superclass == Object
        puts 'context agnostic connection'
        @connection = update_connection(ActiveResource::Connection.new(site, format)) if @connection.nil? || refresh
        @connection
      else
        superclass.connection
      end
    end

    private
      def find_every(options)
        begin
          case from = options[:from]
          when Symbol
            instantiate_collection(get(from, options[:params]))
          when String
            path = "#{from}#{query_string(options[:params])}"
            instantiate_collection(connection(options).get(path, headers) || []) #changed
          else
            prefix_options, query_options = split_options(options[:params])
            path = collection_path(prefix_options, query_options)
            instantiate_collection( (connection(options).get(path, headers) || []), prefix_options ) #changed
          end
        rescue ActiveResource::ResourceNotFound
          # Swallowing ResourceNotFound exceptions and return nil - as per
          # ActiveRecord.
          nil
        end
    end
  end

  protected
    # Context of calls made to the object
    def as
      return @as
    end

    def as=(as)
      @connection = nil
      @as = as
    end

    def connection(refresh = false)
      @connection = self.class.connection({:as => @as}) if refresh || @connection.nil?
      #raise "No valid user context to run in, set :as" if as.nil?
      #connection.authorization_cookie = as.streamline_cookie
    end
end

class User < OpenshiftResource
  has_many :ssh_key
end

class SshKey < OpenshiftResource
  self.primary_key = 'name'
  self.element_name = 'key'

  belongs_to :user

  schema do
    string :name, :key_type, :value
  end

  validates :name, :length => {:maximum => 50},
                   :presence => true,
                   :allow_blank => false
  validates_format_of :key_type,
                      :with => /^ssh-(rsa|dss)$/,
                      :message => "is not ssh-rsa or ssh-dss"
  validates :value, :length => {:maximum => 2048},
                    :presence => true,
                    :allow_blank => false

  def to_param
    name
  end
end


if __FILE__==$0
  require 'test/unit/ui/console/testrunner'
  require 'test/unit'
  require 'mocha'

  class OpenshiftResourceTest < Test::Unit::TestCase
    def test_get_ssh_keys
      items = SshKey.find :all
      assert_equal 1, items.length
    end

    def test_post_ssh_key
      key = SshKey.new :key_type => 'ssh-rsa', :name => 'test2', :value => '1234_2'
      assert key.save
    end

    def test_ssh_key_validation
      key = SshKey.new :key_type => 'ssh-rsa', :name => 'test2'
      assert !key.save
      assert_equal 1, key.errors[:value].length

      key.value = ''
      assert !key.save
      assert_equal 1, key.errors[:value].length

      key.value = 'a'
      assert key.save
      assert key.errors.empty?
    end

    def test_ssh_key_delete
      items = SshKey.find :all
      assert items[0].destroy
    end
  end

  Test::Unit::UI::Console::TestRunner.run(OpenshiftResourceTest)

  items = SshKey.find :all, :as => {:login => 'test1', :password => 'password'}
  puts items.inspect
end
