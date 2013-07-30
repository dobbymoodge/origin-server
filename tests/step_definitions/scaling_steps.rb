require 'rubygems'
require 'uri'
require 'fileutils'
require 'json'
require 'pty'
require 'test/unit'

include AppHelper
include Test::Unit::Assertions

SSH_OPTS="-o 'BatchMode=yes' -o 'StrictHostKeyChecking=no'"

def set_max_gears(num)
  output = `oo-admin-ctl-user --setmaxgears #{num} -l #{@app.login}`
  assert $?.success?, "Failed to allocate #{num} gears for #{@app.login}: #{output}"
end

When /^a scaled (.+) application is created$/ do |app_type|
  @app = TestApp.create_unique(app_type)
  # Create our app via the curl -s api:
  # Replace when the REST API libraries are complete
  rhc_sshkey_upload @app
  rhc_create_domain(@app)
  command = "curl -s -o /tmp/rhc/json_response_#{@app.name}_#{@app.namespace}.json -k -H 'Accept: application/json' --user '#{@app.login}:fakepw' https://localhost/broker/rest/domains/#{@app.namespace}/applications -X POST -d name=#{@app.name} -d cartridge=#{app_type} -d scale=true"

  exit_code = runcon command, 'unconfined_u', 'unconfined_r', 'unconfined_t'
  assert_equal 0, exit_code, "Could not create scaled app.  Exit code: #{exit_code}.  Json debug: /tmp/rhc/json_response_#{@app.name}_#{@app.namespace}.json"

  File.open("/tmp/rhc/json_response_#{@app.name}_#{@app.namespace}.json") { |file|
    json_string = file.read
    $logger.debug("json string: #{json_string}")

    app_info = JSON.parse(json_string)
    assert_equal 'created', app_info['status'], "Could not create application: #{app_info['messages'][0]['text']}"

    @app.uid = app_info['data']['id']
    run("echo '127.0.0.1 #{@app.name}-#{@app.namespace}.dev.rhcloud.com  # Added by cucumber' >> /etc/hosts")
    set_max_gears(8)
  }
end

Then /^the ([\w\-\.]+) health\-check will( not)? be successful$/ do |type, negate|
  expected_status = negate ? 1 : 0

  case type
  when "php-5.3"
    url='http://localhost/health_check.php'
  when "perl-5.10"
    url='http://localhost/health_check.pl'
  else
    url='http://localhost/health'
  end

  host = "#{@app.name}-#{@app.namespace}.dev.rhcloud.com"
  command = "/usr/bin/curl -L -k -s -H 'Host: #{host}' -s #{url} | grep -q -e '^1$'"
  exit_status = nil
  OpenShift::timeout(60) do
    while exit_status != expected_status
      exit_status = runcon command, 'unconfined_u', 'unconfined_r', 'unconfined_t'
      $logger.info("Waiting for health-check to stabilize #{host}")
      sleep 1
    end
  end
  exit_status.should == expected_status
end

When /^a gear is (added|removed)$/ do |action|
  assert_match %r{added|removed}x, action

  ssh_cmd = "ssh #{SSH_OPTS} -t #{@app.uid}@#{@app.hostname} 'rhcsh haproxy_ctld -u'" if action == "added"
  ssh_cmd = "ssh #{SSH_OPTS} -t #{@app.uid}@#{@app.hostname} 'rhcsh haproxy_ctld -d'" if action == "removed"

  exit_code = runcon ssh_cmd, 'unconfined_u', 'unconfined_r', 'unconfined_t'
  assert_equal 0, exit_code, "Gear #{action} failed: #{ssh_cmd} exited with code #{exit_code}"
end

When /^haproxy_ctld_daemon is (started|stopped)$/ do | action |
  assert_match %r{started|stopped}x, action

  ssh_cmd = "ssh #{SSH_OPTS} -t #{@app.uid}@#{@app.hostname} 'rhcsh haproxy_ctld_daemon start'" if action == "started"
  ssh_cmd = "ssh #{SSH_OPTS} -t #{@app.uid}@#{@app.hostname} 'rhcsh haproxy_ctld_daemon stop'" if action == "stopped"

  exit_code = runcon ssh_cmd, 'unconfined_u', 'unconfined_r', 'unconfined_t'
  assert_equal 0, exit_code, "Could not start haproxy_ctld_daemon.  Exit code: #{exit_code}"
end

Then /^haproxy_ctld is running$/ do
  ssh_cmd = "ssh #{SSH_OPTS} -t #{@app.uid}@#{@app.hostname} 'rhcsh ps auxwww | grep -q haproxy_ctld'"
  exit_code = runcon ssh_cmd, 'unconfined_u', 'unconfined_r', 'unconfined_t'
  assert_equal 0, exit_code, "haproxy_ctld is not running!" 
end

When /^(\d+) concurrent http connections are generated for (\d+) seconds$/ do |concurrent, seconds|
  cmd = "ab -H 'Host: #{@app.name}-#{@app.namespace}.dev.rhcloud.com' -c #{concurrent} -t #{seconds} http://localhost/ > /tmp/rhc/http_load_test_#{@app.name}_#{@app.namespace}.txt"
  exit_status = runcon cmd, 'unconfined_u', 'unconfined_r', 'unconfined_t'
  assert_equal 0, exit_status, "load test failed."
end

When /^mongo is added to the scaled app$/ do
  rhc_embed_add(@app, "mongodb-2.2")
end

Then /^app should be able to connect to mongo$/ do
  command  = "echo 'show dbs' | ssh #{SSH_OPTS} -t 2>/dev/null #{@app.uid}@#{@app.name}-#{@app.namespace}.dev.rhcloud.com rhcsh mongo | grep #{@app.name}"

  OpenShift::timeout(500) do
    exit_status = run(command)
    while exit_status != 0
      $logger.debug("waiting on mongo")
      sleep 1
      exit_status = run(command)
    end
  end

  exit_status.should == 0
end

When /^the haproxy-1.4 cartridge is removed$/ do
  out = `curl -s -k -H 'Accept: application/json' --user '#{@app.login}:fakepw' https://localhost/broker/rest/domains/#{@app.namespace}/applications/#{@app.name}/cartridges/haproxy-1.4 -X DELETE`
  out_obj = JSON.parse(out)
  $rest_exit_code = out_obj["messages"][0]["exit_code"]
end

Then /^the operation is( not)? allowed$/ do |negate|
  if negate
    $rest_exit_code.should == 137
  else
    $rest_exit_code.should == 0
  end
end
