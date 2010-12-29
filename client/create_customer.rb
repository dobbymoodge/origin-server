#!/usr/bin/env ruby
# Copyright © 2010 Jim Jagielski All rights reserved
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

require "uri"
require "net/http"
require "getoptlong"

#
# Globals
#
libra_kfile = "#{ENV['HOME']}/.ssh/libra_id_rsa"
libra_kpfile = "#{ENV['HOME']}/.ssh/libra_id_rsa.pub"
li_server = 'li.mmcgrath.libra.mmcgrath.net'
debug = false

def usage()
    puts <<USAGE

Usage: create_customer
Create a new libra user.

  -u|--user   username    Libra username (alphanumeric) (required)
  -e|--email  email       Email address (required)
  -d|--debug              Print Debug info
  -h|--help               Show Usage info

USAGE
exit 255
end

def validate_email(email)
    if email =~ /([^@]+)@([a-zA-Z0-9\.])+\.([a-zA-Z]{2,3})/
        if $1 =~ /[^a-zA-Z0-9\.]/
            false
        else
            true
        end
    else
        false
    end
end

opts = GetoptLong.new(
    ["--debug", "-d", GetoptLong::NO_ARGUMENT],
    ["--help",  "-h", GetoptLong::NO_ARGUMENT],
    ["--user",  "-u", GetoptLong::REQUIRED_ARGUMENT],
    ["--email", "-e", GetoptLong::REQUIRED_ARGUMENT]
)

opt = {}
opts.each do |o, a|
    opt[o[2..-1]] = a.to_s
end

if opt["help"]
    usage()
end

if opt["debug"]
    debug = true
end

if opt["user"]
    if opt["user"] =~ /[^0-9a-zA-Z]/
        puts "username contains non-alphanumeric characters!"
        usage()
    end
else
    puts "Libra username is required"
end

if opt["email"]
    if !validate_email(opt["email"])
        puts "email contains invalid characters!"
        usage()
    end
else
    puts "Libra email address is required"
end

if !opt["email"] || !opt["user"]
    usage()
end

#
# Check to see if a libra_id_rsa key exists, if not create it.
#

if File::readable?(libra_kfile)
    puts "Libra key found at #{libra_kfile}.  Reusing..."
else
    puts "Generating libra ssh key to #{libra_kfile}"
    system("ssh-keygen -t rsa -f #{libra_kfile}")
end

ssh_key = File::open(libra_kpfile).gets.chomp.split(' ')[1]

puts "Contacting server http://#{li_server}"
response = Net::HTTP.post_form(URI.parse("http://#{li_server}/create_customer.php"),
                           {'username' => opt['user'],
                           'email' => opt['email'],
                           'ssh_key' => ssh_key})

if response.code == '200'
    if debug
        puts "HTTP response from server is #{response.body}"
    end
    puts "Creation successful (probably).  You may now create an application"
else
    puts "Problem with server. Response code was #{response.code}"
    puts "HTTP response from server is #{response.body}"
end
0