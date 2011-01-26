require 'libra/exception.rb'
require 'libra/config.rb'
require 'libra/helper.rb'
require 'libra/server.rb'
require 'libra/user.rb'

module Libra
  #
  # Executes
  #
  def self.execute(framework, action, app_name, username)
    # Lookup the user
    user = User.find(username)

    # App exists check
    if action == 'configure'
      throw :app_already_exists if user.app_info(app_name)
    else
      throw :app_does_not_exist unless user.app_info(app_name)
    end

    # Find the next available server
    Libra.c[:rpc_opts][:disctimeout] = 1
    Libra.c[:rpc_opts][:timeout] = 2
    server = Server.find_available

    puts "Node: #{server.name} - #{server.repos} repos" if Libra.c[:rpc_opts][:verbose]

    # Configure the user on this server if necessary
    Libra.c[:rpc_opts][:disctimeout] = 1
    Libra.c[:rpc_opts][:timeout] = 15
    unless user.servers.index(server) do
      puts "User not found on node.  Creating #{user}" if Libra.c[:rpc_opts][:verbose]
      server.create_user(user)
    end

    # Configure the app on the server using a framework cartridge
    server.execute(framework, action, app_name, user)
    user.create_app(app_name, framework) if action == 'configure'
    user.delete_app(app_name) if action == 'deconfigure'
  end

  #
  # Adjusts the capacity of the Libra cluster if
  # necessary
  #
  def self.adjust_capacity
    # Whether or not we need to add another server
    add_server = true

    # Get the initial capacity
    current_servers = Server.find_all
    current_servers.each do |server|
      # If any server is below the threshold,
      # don't add a new server
      if server.repos < c[:repo_threshold]
        add_server = false
        break
      end
    end

    # Add the additional server if needed
    if add_server
      result = Server.create
      puts "Added EC2 instance #{result[0]}"
    end
  end
end
