#!/usr/bin/env ruby
require 'rubygems'
require 'mongo'
$:.unshift('/var/www/openshift/broker')
require 'config/environment'

# Configurable params
$config = Rails.application.config.datastore

def mongo_connect
  if $config[:replica_set]
    con = Mongo::ReplSetConnection.new(*$config[:host_port] \
                                       << {:read => :secondary})
  else
    con = Mongo::Connection.new($config[:host_port][0], 
                                $config[:host_port][1])
  end
  db = con.db($config[:db])
  db.authenticate($config[:user], $config[:password])
  $coll = con.db($config[:db]).collection($config[:collections][:user])
end

def mongo_migrate
  puts "Checking for all users "
  cursor = $coll.find( { }, { :fields => ["apps.group_instances.gears.configured_components", "apps.group_instances.name", "apps.group_instances.gears.uuid", "apps.comp_instances.name", "apps.name", "_id"] })
  cursor.each { |uhash|
    userid = uhash["_id"]
    apps = uhash["apps"]
    app_index = 0
    apps.each { |ahash|
      print "."
      clist = ahash["comp_instances"].map { |aci| aci["name"] }
      appname = ahash["name"]
      gi_index = 0
      ahash["group_instances"].each { |gi_hash|
        gear_index = 0
        gi_hash["gears"].each { |ghash|
          gear_uuid = ghash["uuid"]
          ghash["configured_components"].dup.each { |comp|
            if not clist.include? comp
              puts ""
              puts "Fixing #{userid}/#{appname}/group_instances[#{gi_index}]/gears[#{gear_index}]/configured_components/#{comp}"
              updates = { "$pull" => { "apps.$.group_instances.#{gi_index}.gears.#{gear_index}.configured_components" => comp } }
              $coll.update( { "_id" => userid, "apps.name" => appname, "apps.#{app_index}.group_instances.#{gi_index}.gears.#{gear_index}.uuid" => gear_uuid }, updates )
            end
          } if ghash["configured_components"]
          gear_index += 1
        } if gi_hash["gears"]
        gi_index += 1
      } if ahash["group_instances"]
      app_index += 1
    } if apps
  }
end

mongo_connect
puts "User migration Started"
mongo_migrate
puts "User migration Done!"
