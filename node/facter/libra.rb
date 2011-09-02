#
# = libra.rb: Facter integration for li
#
# Author:: Mike McGrath
# 
# Copyright © 2010 Mike McGrath All rights reserved
# Copyright © 2010 Red Hat, Inc. All rights reserved

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
# libra.rb for facter adds several additional li related facts which can then
# be queried by facter (and mcollective).  Examples include the number of git
# repositories on the host, customer information, etc.

require 'rubygems'
require 'parseconfig'

#
# Count the number of git repos on this host
#
Facter.add(:git_repos) do
    @git_repos_count = Dir.glob("/var/lib/libra/**/git/*.git").count
    setcode { @git_repos_count }
end

#
# Pull public_ip out of the node_data config
#
Facter.add(:public_ip) do
    config_file = ParseConfig.new('/etc/libra/node_data.conf')
    public_ip = config_file.get_value('public_ip') ? config_file.get_value('public_ip') : 'UNKNOWN'
    setcode { public_ip }
end

#
# Pull public_hostname out of the node_data config
#
Facter.add(:public_hostname) do
    config_file = ParseConfig.new('/etc/libra/node_data.conf')
    public_hostname = config_file.get_value('public_hostname') ? config_file.get_value('public_hostname') : 'UNKNOWN'
    setcode { public_hostname }
end

#
# Find Max Apps
#
Facter.add(:max_apps) do
    config_file = ParseConfig.new('/etc/libra/resource_limits.conf')
    @max_apps = config_file.get_value('max_apps') ? config_file.get_value('max_apps') : '0'
    setcode { @max_apps }
end

#
# Find capacity
#
Facter.add(:capacity) do
    git_repos =  Facter.value(:git_repos).to_f
    max_apps = Facter.value(:max_apps).to_f
    puts max_apps
    puts git_repos
    capacity = ( git_repos / max_apps ) * 100
    setcode { capacity.to_s }
end


#
# Get sshfp record
#
Facter.add(:sshfp) do
    setcode { %x[/usr/bin/ssh-keygen -r $(hostname) -f /etc/ssh/ssh_host_rsa_key]}
end

=begin
#
# Lists customers on the host as well as what what git repos they currently own
#
if File.exists?("/var/lib/libra") && File.directory?("/var/lib/libra")
    # Determine customers on host and hosted info
    Dir.entries('/var/lib/libra/').each do |customer|
    
        if customer =~ /[A-Za-z0-9]/
            Facter.add("customer_#{customer}") do
                setcode do customer end
            end
        end
        # Repo counts for a customer
        if File.exists?("/var/lib/libra/#{customer}/git/")
            git_repos = Dir.glob("/var/lib/libra/#{customer}/git/*.git")
            Facter.add("git_cnt_#{customer}") do
                setcode do git_repos.size end
            end
        end
    end
end
=end

#
# List cartridges on the host
#   Convert from name-m.n.p to name-m.n
#   This is the *full* list. Public version is
#   obtained via Libra::Util.get_cartridges_list
#
Facter.add(:cart_list) do
    carts = []
    Dir.glob('/usr/libexec/li/cartridges/*/').each do |cart|
        cart = File.basename(cart).sub(/^(.*)-(\d+)\.(\d+)\.?.*$/, '\1-\2.\3')
        carts << cart unless cart.nil? || cart == "embedded"
    end
    setcode { carts.join('|') }
end

#
# List embedded cartridges on the host
#   Convert from name-m.n.p to name-m.n
#   This is the *full* list. Public version is
#   obtained via Libra::Util.get_embedded_cartridges_tbl
#
Facter.add(:embed_cart_list) do
    carts = []
    Dir.glob('/usr/libexec/li/cartridges/embedded/*/').each do |cart|
        cart = File.basename(cart).sub(/^(.*)-(\d+)\.(\d+)\.?.*$/, '\1-\2.\3')
        carts << cart unless cart.nil?
    end
    setcode { carts.join('|') }
end
