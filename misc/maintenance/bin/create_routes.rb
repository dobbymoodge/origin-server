#!/usr/bin/env ruby

$ip_re = /ProxyPass[\s]+\/[\s]+http:\/\/(([0-9]{1,3}.){3}[0-9]{1,3})/
$sn_re = /ServerName[\s]+(\S*)[\s]*$/

def write_routes_file(file_path, host, ipaddress, conn)
  routes_c = <<END
{
  "#{host}": {
    "endpoints": [ "#{ipaddress}:8080" ],
    "limits"   :  {
      "connections": #{conn},
      "bandwidth"  : 100
    }
  }
}
END
  puts routes_c

  File.open(file_path, 'w') {|f| f.write(routes_c) }
end

def create_routes(path)
  puts "Processing gear: #{path}"

  # Find the endpoint i.e. ipaddress for the backend
  # If the gear has haproxy then that should be the endpoint
  # instead of the one in zzzzz_proxy.conf
  haproxy_found = false
  endpoint_file = 'zzzzz_proxy.conf'
  conn = 5

  if File.exists?("#{path}/000000_haproxy.conf")
    puts "HAProxy found on the gear"
    endpoint_file = '000000_haproxy.conf'
    conn = -1
  end

  ep_file_path = File.join(path, endpoint_file)
  unless File.exists?(ep_file_path)
    puts "Skipping standalone db gear"
    return
  end

  epc = File.read(ep_file_path)
  m = epc.match $ip_re
  raise Exception.new "No endpoint found" unless m

  ipaddress = m[1]
  puts "Endpoint: #{ipaddress}"

  # Find the host for the backend server
  dfc = File.read("#{path}/00000_default.conf")
  m = dfc.match $sn_re
  raise Exception.new "No host found" unless m

  host = m[1]
  puts "Host: #{host}"

  # Write the routes.json file
  write_routes_file("#{path}/routes.json", host, ipaddress, conn)

  # Migrate the alias files
  aliases = %x[grep -r ServerAlias #{path} | awk '{print $2}']
  aliases.each_line do |line|
    al = line.strip
    write_routes_file("#{path}/routes_alias-#{al}.json", al, ipaddress, conn)
  end
end

$fail_list = []
$HTTPD_DIR = '/var/lib/openshift/.httpd.d'
ngears = 0
nfailed = 0
Dir.foreach($HTTPD_DIR) do |ent|
  next if ['.', '..'].include? ent
  full_path = File.join($HTTPD_DIR, ent)
  if File.directory? full_path
    begin
      create_routes(full_path)
      ngears += 1
    rescue Exception => e
      nfailed += 1
      puts e.message
      $fail_list << "#{ent}"
    end
  end
end

puts
puts "------ FAILED TO MIGRATE ------- "
$fail_list.each do |e|
  puts e
end

puts
puts "------ Summary ------- "
puts "      Number of failures = #{nfailed}"
puts "Number of gears migrated = #{ngears}"

