require 'rubygems'
require 'json'
require 'cloud-sdk-common'

class LegacyRequest < Cloud::Sdk::Model
  attr_accessor :namespace, :rhlogin, :ssh, :app_uuid, :app_name, :node_profile, :debug, :alter, :cartridge, :api, :cart_type, :action, :server_alias
  attr_reader   :invalid_keys
  
  APP_NAME_MAX_LENGTH = 32
  NAMESPACE_MAX_LENGTH = 16

  def initialize
    @invalid_keys = []
  end
  
  validates_each :invalid_keys do |record, attribute, val|
    val.each do |key|
      record.errors.add :base, {:message => "Unknown json key found: #{key}", :exit_code => 1}
    end
  end
  
#  validates_each :rhlogin do |record, attribute, val|
#    if !Util.check_rhlogin(val)
#      record.errors.add attribute, {:message => "Invalid rhlogin: #{val}", :exit_code => 107}
#    end
#  end
  
  validates_each :namespace do |record, attribute, val|
    if !(val =~ /\A[A-Za-z0-9]+\z/)
      record.errors.add attribute, {:message => "Invalid namespace: #{val}", :exit_code => 106}
    end
    if val and (val.length > NAMESPACE_MAX_LENGTH) #or Blacklist.in_blacklist?(val))
      record.errors.add attribute, {:message => "The namespace you entered (#{val}) is not available for use.  Please choose another one.", :exit_code => 106}
    end
  end
  
  validates_each :app_name do |record, attribute, val|
    if !(val =~ /\A[\w]+\z/)
      record.errors.add attribute, {:message => "Invalid #{attribute} specified: #{val}", :exit_code => 105}
    end
    if val and (val.length > APP_NAME_MAX_LENGTH) #or Blacklist.in_blacklist?(val))
      record.errors.add attribute, {:message => "The supplied application name '#{val}' is not allowed", :exit_code => 105}
    end
  end
  
  validates_each :ssh do |record, attribute, val|
    if !(val =~ /\A[A-Za-z0-9\+\/=]+\z/)
      record.errors.add attribute, {:message => "Invalid ssh key: #{val}", :exit_code => 108}
    end
  end

  validates_each :app_uuid do |record, attribute, val|
    if !(val =~ /\A[a-f0-9]+\z/)
      record.errors.add attribute, {:message => "Invalid application uuid: #{val}", :exit_code => 1}
    end
  end
  
  validates_each :node_profile do |record, attribute, val|
    if !(val =~ /\A(jumbo|exlarge|large|micro|std)\z/)
      record.errors.add attribute, {:message => "Invalid Profile: #{val}.  Must be: (jumbo|exlarge|large|micro|std)", :exit_code => 1}
    end
  end
  
  validates_each :debug, :alter do |record, attribute, val|
    if val != true && val != false && !(val =~ /\A(true|false)\z/)
      record.errors.add attribute, {:message => "Invalid value for #{attribute} specified: #{val}", :exit_code => 1}
    end
  end
  
  validates_each :cartridge do |record, attribute, val|
    if !(val =~ /\A[\w\-\.]+\z/)
      record.errors.add attribute, {:message => "Invalid cartridge specified: #{val}", :exit_code => 1}
    end
  end
  
  validates_each :api do |record, attribute, val|
    if !(val =~ /\A\d+\.\d+\.\d+\z/)
      record.errors.add attribute, {:message => "Invalid API value specified: #{val}", :exit_code => 112}
    end
  end
  
  validates_each :cart_type do |record, attribute, val|
    if !(val =~ /\A[\w\-\.]+\z/)
      record.errors.add attribute, {:message => "Invalid cart_type specified: #{val}", :exit_code => 109}
    end
  end
  
  validates_each :action do |record, attribute, val|
    if !(val =~ /\A[\w\-\.]+\z/)
      record.errors.add attribute, {:message => "Invalid action specified: #{val}", :exit_code => 111}
    end
  end

  validates_each :server_alias do |record, attribute, val|
    if !(val =~ /\A[\w\-\.]+\z/) or (val =~ /rhcloud.com$/)
      record.errors.add attribute, {:message => "Invalid ServerAlias specified: #{val}", :exit_code => 105}
    end
  end
  
  def alter
    @alter == "true" || @alter == true
  end
  
  def debug
    @debug == "true" || @debug == true
  end
  
  def attributes=(hash)
    hash.each do |key,value|
      begin
        self.public_send("#{key}=",value)
      rescue NoMethodError => e
        @invalid_keys.push key
      end
    end
  end
end