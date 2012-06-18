# -*- coding: utf-8 -*-
# = libra.rb: li integration for mcollective
#
# Author:: Mike McGrath
#
# Copyright © 2010 Mike McGrath All rights reserved
# Copyright © 2010 Red Hat, Inc. All rights reserved
#
# This copyrighted material is made available to anyone wishing to use, modify,
# copy, or redistribute it subject to the terms and conditions of the GNU
# General Public License v.2.  This program is distributed in the hope that it
# will be useful, but WITHOUT ANY WARRANTY expressed or implied, including the
# implied warranties of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.  You should have
# received a copy of the GNU General Public License along with this program;
# if not, write to the Free Software Foundation, Inc., 51 Franklin Street,
# Fifth Floor, Boston, MA 02110-1301, USA. Any Red Hat trademarks that are
# incorporated in the source code or documentation are not subject to the GNU
# General Public License and may only be used or replicated with the express
# permission of Red Hat, Inc.
#
# == Description
#
# libra.rb for mcollective does manipulation of libra services and customer
# data.  This can start and stop services, create and destroy applications
# as well as create new customers.
#
require 'rubygems'
require 'open4'
require 'pp'
require 'json'
require 'stickshift-node'
require 'shellwords'
require 'facter'

module MCollective
  #
  # Li mcollective agent
  #
  module Agent
  
    class Libra<RPC::Agent
      metadata    :name        => "Libra Management",
                  :description => "Agent to manage Libra services",
                  :author      => "Mike McGrath",
                  :license     => "GPLv2",
                  :version     => "0.1",
                  :url         => "https://engineering.redhat.com/trac/Libra",
                  :timeout     => 240
        
      #
      # Migrate between versions
      #
      def migrate_action
        Log.instance.debug("migrate_action call / request = #{request.pretty_inspect}")
        validate :uuid, /^[a-zA-Z0-9]+$/
        validate :version, /^.+$/
        validate :namespace, /^.+$/  
        uuid = request[:uuid]
        namespace = request[:namespace]
        version = request[:version]
        output = ""
        exitcode = 0
        begin
          require "#{File.dirname(__FILE__)}/migrate"
          output, exitcode = OpenShiftMigration::migrate(uuid, namespace, version)
        rescue LoadError => e
          exitcode = 127
          output += "Migrate not supported.\n"
        rescue Exception => e
          exitcode = 1
          output += "Gear failed to migrate with exception: #{e.message}\n#{e.backtrace}\n"
        end
        Log.instance.debug("migrate_action (#{exitcode})\n------\n#{output}\n------)")

        reply[:output] = output
        reply[:exitcode] = exitcode
        reply.fail! "migrate_action failed #{exitcode}.  Output #{output}" unless exitcode == 0
      end
      
    end
  end
end
