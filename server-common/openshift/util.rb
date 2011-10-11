require 'openshift/blacklist'
require 'openshift/server'


module Libra
  module Util

    Maxdlen = 16

    def self.get_cart_framework(cart)
      cart_type = cart.split('-')[0..-2].join('-')
      return cart_type
    end

    def self.get_cartridge_listing(cart_type='standalone', carts=nil, server=nil, sep=', ')
      carts = get_cartridges_list(cart_type, server) unless carts
      carts.join(sep)
    end

    def self.get_valid_cart_framework(cartridge, cart_type='standalone', carts=nil, server=nil)
      carts = get_cartridges_list(cart_type, server) unless carts
      if carts.include?(cartridge)
        return get_cart_framework(cartridge)
      end
      return nil
    end


    # Type - standalone or embedded
    def self.get_cartridges_list(cart_type, server=nil)
      server = Server.find_available unless server
      carts = []
      if cart_type == 'standalone'
        server.carts.split('|').each do |cart|
          carts << cart unless Blacklist.ignore_cart?(cart)
        end
      elsif cart_type == 'embedded'
        server.embedcarts.split('|').each do |cart|
          carts << cart unless Blacklist.ignore_cart?(cart)
        end
      end
      return carts
    end

    # Invalid chars (") ($) (^) (<) (>) (|) (%) (/) (;) (:) (,) (\) (*) (=) (~)
    def self.check_rhlogin(rhlogin)
      if rhlogin =~ /["\$\^<>\|%\/;:,\\\*=~]/
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

  end
end
