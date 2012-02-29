require 'fileutils'

$phpmoadmin_version = "1.0"
$phpmoadmin_cart_root = "/usr/libexec/li/cartridges/embedded/phpmoadmin-#{$phpmoadmin_version}"
$phpmoadmin_hooks = $phpmoadmin_cart_root + "/info/hooks"
$phpmoadmin_config = $phpmoadmin_hooks + "/configure"
$phpmoadmin_config_format = "#{$phpmoadmin_config} %s %s %s"
$phpmoadmin_deconfig = $phpmoadmin_hooks + "/deconfigure"
$phpmoadmin_deconfig_format = "#{$phpmoadmin_deconfig} %s %s %s"
$phpmoadmin_proc_regex = /httpd -C Include .*phpmoadmin/

Given /^a new phpmoadmin$/ do
  account_name = @account['accountname']
  namespace = @app['namespace']
  app_name = @app['name']
  command = $phpmoadmin_config_format % [app_name, namespace, account_name]

  outbuf = []
  exit_code = runcon command,  'unconfined_u', 'system_r', 'libra_initrc_t', outbuf

  if exit_code != 0
    raise "Error running #{command}: returned #{exit_code}"
  end
end

Given /^phpmoadmin is (running|stopped)$/ do | status |
  action = status == "running" ? "start" : "stop"

  acct_name = @account['accountname']
  namespace = @app['namespace']
  app_name = @app['name']
  daemon_name = 'httpd'

  command = "#{$phpmoadmin_hooks}/#{action} #{app_name} #{namespace} #{acct_name}"

  num_daemons = num_procs_like acct_name, $phpmoadmin_proc_regex
  outbuf = []

  case action
  when 'start'
    if num_daemons == 0
      runcon command,  'unconfined_u', 'system_r', 'libra_initrc_t', outbuf
    end
    exit_test = lambda { |tval| tval > 0 }
  when 'stop'
    if num_daemons > 0
      runcon command,  'unconfined_u', 'system_r', 'libra_initrc_t', outbuf
    end
    exit_test = lambda { |tval| tval == 0 }
  # else
  #   raise an exception
  end

  # now loop until it's true
  max_tries = 10
  poll_rate = 3
  tries = 0
  num_daemons = num_procs_like acct_name, $phpmoadmin_proc_regex
  while (not exit_test.call(num_daemons) and tries < max_tries)
    tries += 1
    sleep poll_rate
    num_daemons = num_procs_like acct_name, $phpmoadmin_proc_regex
  end
end

When /^I configure phpmoadmin$/ do
  account_name = @account['accountname']
  namespace = @app['namespace']
  app_name = @app['name']
  command = $phpmoadmin_config_format % [app_name, namespace, account_name]

  outbuf = []
  exit_code = runcon command,  'unconfined_u', 'system_r', 'libra_initrc_t', outbuf

  if exit_code != 0
    raise "Error running #{command}: returned #{exit_code}"
  end
end

When /^I deconfigure phpmoadmin$/ do
  account_name = @account['accountname']
  namespace = @app['namespace']
  app_name = @app['name']
  command = $phpmoadmin_deconfig_format % [app_name, namespace, account_name]
  exit_code = runcon command,  'unconfined_u', 'system_r', 'libra_initrc_t'
  if exit_code != 0
    raise "Command failed with exit code #{exit_code}"
  end
end

When /^I (start|stop|restart) phpmoadmin$/ do |action|
  acct_name = @account['accountname']
  namespace = @app['namespace']
  app_name = @app['name']

  phpmoadmin_user_root = "#{$home_root}/#{acct_name}/phpmoadmin-#{$phpmoadmin_version}"

  outbuf = []
  command = "#{$phpmoadmin_hooks}/#{action} #{app_name} #{namespace} #{acct_name}"
  exit_code = runcon command,  'unconfined_u', 'system_r', 'libra_initrc_t', outbuf

  if exit_code != 0
    raise "Command failed with exit code #{exit_code}"
  end
end

Then /^a phpmoadmin http proxy file will( not)? exist$/ do | negate |
  acct_name = @account['accountname']
  app_name = @app['name']
  namespace = @app['namespace']

  conf_file_name = "#{acct_name}_#{namespace}_#{app_name}/phpmoadmin-#{$phpmoadmin_version}.conf"
  conf_file_path = "#{$libra_httpd_conf_d}/#{conf_file_name}"

  if not negate
    File.exists?(conf_file_path).should be_true
  else
    File.exists?(conf_file_path).should be_false
  end
end

Then /^a phpmoadmin httpd will( not)? be running$/ do | negate |
  acct_name = @account['accountname']
  acct_uid = @account['uid']
  app_name = @app['name']

  max_tries = 20
  poll_rate = 3
  exit_test = negate ? lambda { |tval| tval == 0 } : lambda { |tval| tval > 0 }

  tries = 0
  num_httpds = num_procs_like acct_name, $phpmoadmin_proc_regex
  while (not exit_test.call(num_httpds) and tries < max_tries)
    tries += 1
    sleep poll_rate
  end

  if not negate
    num_httpds.should be > 0
  else
    num_httpds.should be == 0
  end
end

Then /^the phpmoadmin directory will( not)? exist$/ do | negate |
  account_name = @account['accountname']
  namespace = @app['namespace']
  app_name = @app['name']

  phpmoadmin_user_root = "#{$home_root}/#{account_name}/phpmoadmin-#{$phpmoadmin_version}"
  begin
    phpmoadmin_dir = Dir.new phpmoadmin_user_root
  rescue Errno::ENOENT
    phpmoadmin_dir = nil
  end

  unless negate
    phpmoadmin_dir.should be_a(Dir)
  else
    phpmoadmin_dir.should be_nil
  end
end

Then /^phpmoadmin log files will( not)? exist$/ do | negate |
  acct_name = @account['accountname']
  acct_uid = @account['uid']
  app_name = @app['name']
  log_dir_path = "#{$home_root}/#{acct_name}/phpmoadmin-#{$phpmoadmin_version}/logs"
  begin
    log_dir = Dir.new log_dir_path
    status = (log_dir.count > 2)
  rescue
    status = false
  end

  if not negate
    status.should be_true
  else
    status.should be_false
  end
end

Then /^the phpmoadmin control script will( not)? exist$/ do | negate |
  account_name = @account['accountname']
  namespace = @app['namespace']
  app_name = @app['name']

  phpmoadmin_user_root = "#{$home_root}/#{account_name}/phpmoadmin-#{$phpmoadmin_version}"
  phpmoadmin_startup_file = "#{phpmoadmin_user_root}/#{app_name}_phpmoadmin_ctl.sh"

  begin
    startfile = File.new phpmoadmin_startup_file
  rescue Errno::ENOENT
    startfile = nil
  end

  unless negate
    startfile.should be_a(File)
  else
    startfile.should be_nil
  end
end
