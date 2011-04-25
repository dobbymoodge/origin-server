require 'libra/blacklist'


module Libra
  module Util

    Maxdlen = 16

    TYPES = {
      'php-5.3.2' => :php,
      'rack-1.1.0' => :rack,
      'wsgi-3.2.1' => :wsgi
    }

    def self.get_cartridge_types(sep=', ')
      i = 1
      type_keys = ''
      TYPES.each_key do |key|
        type_keys += key
        if i < TYPES.size
          type_keys += sep
        end
        i += 1
      end
      type_keys
    end

    # Invalid chars (") ($) (^) (<) (>) (|) (%) (/) (;) (:) (,) (\) (*) (=) (~)
    def self.check_rhlogin(rhlogin)
      if rhlogin && rhlogin.length < 6
        #puts 'RHLogin must be at least 6 characters'
        return false
      elsif rhlogin =~ /["\$\^<>\|%\/;:,\\\*=~]/
        #puts 'RHLogin may not contain any of these characters: (\") ($) (^) (<) (>) (|) (%) (/) (;) (:) (,) (\) (*) (=) (~)'
        return false
      else
        return true
      end
    end

    def self.check_app(app)
      check_field(app, 'application', Maxdlen)
    end

    def self.check_namespace(namespace)
      check_field(namespace, 'namespace', Maxdlen)
    end

    def self.check_field(field, type, max=0)
      if field
        if field =~ /[^0-9a-zA-Z]/
          #puts "#{type} contains non-alphanumeric characters!"
          return false
        end
        if Blacklist.in_blacklist?(field)
          return false
        end
        if max != 0 && field.length > Maxdlen
          #puts "maximum #{type} size is #{Maxdlen} characters"
          return false
        end
      else
        #puts "#{type} is required"
        return false
      end
      true
    end

    def self.get_cartridge(type)
      if type && TYPES.has_key?(type)
        return TYPES[type]
      end
      nil
    end

  end
end
