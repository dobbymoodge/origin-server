require 'rubygems'
require 'uri'
require 'fileutils'
require 'json'
require 'pty'

include AppHelper

def gear_up?(hostname, state='UP')
  csv = `/usr/bin/curl -s -H 'Host: #{hostname}' -s 'http://localhost/haproxy-status/;csv'`
  $logger.debug('============ GEAR CSV ================')
  $logger.debug(csv)
  $logger.debug('============ GEAR CSV END ============')
  csv.split.each do | haproxy_worker |

    worker_attrib_array = haproxy_worker.split(',')
    max_wait = 24 # 2 minutes
    i = 0
    if worker_attrib_array[17] and worker_attrib_array[1].to_s.start_with?('gear') and worker_attrib_array[17].to_s.start_with?(state)
      $logger.debug("Found: #{worker_attrib_array[1]} - #{worker_attrib_array[17]}")
      return 0
    end
  end
  $logger.debug("No gears found")
  return 1
end

When /^a scaled (.+) application is created$/ do |app_type|
  @app = TestApp.create_unique(app_type)
  # Create our app via the curl -s api:
  # Replace when the REST API libraries are complete
  rhc_create_domain(@app)
  command = "curl -s -o /tmp/rhc/json_response_#{@app.name}_#{@app.namespace}.json -k -H 'Accept: application/json' --user '#{@app.login}:fakepw' https://localhost/broker/rest/domains/#{@app.namespace}/applications -X POST -d name=#{@app.name} -d cartridge=#{app_type} -d scale=true"

  exit_code = runcon command, 'unconfined_u', 'unconfined_r', 'unconfined_t'
  raise "Could not create scaled app.  Exit code: #{exit_code}.  Json debug: /tmp/rhc/json_response_#{@app.name}_#{@app.namespace}.json" unless exit_code == 0
  fp = File.open("/tmp/rhc/json_response_#{@app.name}_#{@app.namespace}.json")
  json_string = fp.read
  run("echo '127.0.0.1 #{@app.name}-#{@app.namespace}.dev.rhcloud.com  # Added by cucumber' >> /etc/hosts")
  $logger.debug("json string: #{json_string}")
  app_info = JSON.parse(json_string)
  @app.uid = app_info['data']['uuid']
  fp.close
end

Then /^the haproxy-status page will( not)? be responding$/ do |negate|
  good_status = negate ? 1 : 0

  command = "/usr/bin/curl -s -H 'Host: #{@app.name}-#{@app.namespace}.dev.rhcloud.com' -s 'http://localhost/haproxy-status/;csv' | /bin/grep -q -e '^stats,FRONTEND'"
  exit_status = runcon command, 'unconfined_u', 'unconfined_r', 'unconfined_t'
  exit_status.should == good_status
end

Then /^the gear members will be (UP|DOWN)$/ do |state|
  found = nil

  max_wait = 24 # 2 minutes
  i = 0
  while gear_up?("#{@app.name}-#{@app.namespace}.dev.rhcloud.com", state) != 0 and i <= max_wait
    $logger.debug("loop #{i}")
    i = i + 1
    sleep 5
  end
  raise "Could not find valid gear" if i >= max_wait
end

Then /^(\d+) gears will be in the cluster$/ do |count|
  sleep 2
  $logger.debug('============ GEAR CSV ================')
  $logger.debug(`/usr/bin/curl -s -H 'Host: #{@app.name}-#{@app.namespace}.dev.rhcloud.com' -s 'http://localhost/haproxy-status/;csv'`)
  $logger.debug('============ GEAR CSV END ============')
  gear_count = `/usr/bin/curl -s -H 'Host: #{@app.name}-#{@app.namespace}.dev.rhcloud.com' -s 'http://localhost/haproxy-status/;csv' | grep -c "express,gear"`
  $logger.debug("Gear count: #{gear_count.to_i} should be #{count.to_i}")
  raise "Gear counts do not match: #{gear_count.to_i} should be #{count.to_i}" unless gear_count.to_i == count.to_i
end

Then /^the php-5.3 health\-check will( not)? be successful$/ do |negate|
  good_status = negate ? 1 : 0

  command = "/usr/bin/curl -s -H 'Host: #{@app.name}-#{@app.namespace}.dev.rhcloud.com' -s 'http://localhost/health_check.php' | grep -q -e '^1$'"
  exit_status = runcon command, 'unconfined_u', 'unconfined_r', 'unconfined_t'
  exit_status.should == good_status
end

When /^a gear is (added|removed)$/ do |action|
  if action == "added"
    ssh_cmd = "ssh -t #{@app.uid}@#{@app.hostname} 'rhcsh haproxy_ctld -u'"
  elsif action == "removed"
    ssh_cmd = "ssh -t #{@app.uid}@#{@app.hostname} 'rhcsh haproxy_ctld -d'"
  else
    puts "Invalid gear action specified (must be added/removed)"
    exit 1
  end

  exit_code = runcon ssh_cmd, 'unconfined_u', 'unconfined_r', 'unconfined_t'
  raise "Gear #{action} failed: #{ssh_cmd} exited with code #{exit_code}" unless exit_code == 0
end

When /^haproxy_ctld_daemon is started$/ do
  ssh_cmd = "ssh -t #{@app.uid}@#{@app.hostname} 'rhcsh haproxy_ctld_daemon start'"

  exit_code = runcon ssh_cmd, 'unconfined_u', 'unconfined_r', 'unconfined_t'
  raise "Could not start haproxy_ctld_daemon.  Exit code: #{exit_code}" unless exit_code == 0
end

Then /^haproxy_ctld is running$/ do
  ssh_cmd = "ssh -t #{@app.uid}@#{@app.hostname} 'rhcsh ps auxwww | grep -q haproxy_ctld'"
  exit_code = runcon ssh_cmd, 'unconfined_u', 'unconfined_r', 'unconfined_t'
  raise "haproxy_ctld is not running!" unless exit_code == 0
end

When /^(\d+) concurrent http connections are generated for (\d+) seconds$/ do |concurrent, seconds|
  cmd = "ab -H 'Host: #{@app.name}-#{@app.namespace}.dev.rhcloud.com' -c #{concurrent} -t #{seconds} http://localhost/ > /tmp/rhc/http_load_test_#{@app.name}_#{@app.namespace}.txt"
  exit_status = runcon cmd, 'unconfined_u', 'unconfined_r', 'unconfined_t'
  raise "load test failed.  Exit code: #{exit_status}" unless exit_status == 0
end
