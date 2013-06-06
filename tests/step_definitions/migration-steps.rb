require 'openshift-origin-node/model/cartridge_repository'

def migrate_gear(app, gear_uuid, cart_migration=false)
  output = ''

  if cart_migration
    output = `rhc-admin-migrate --app-name #{@app.name} --login #{@app.login} --migrate-gear #{gear_uuid} --version 2.0.28a`
  else
    output = `rhc-admin-migrate --app-name #{@app.name} --login #{@app.login} --migrate-gear #{gear_uuid} --version 2.0.28`
  end

  $logger.info("Migration output: #{output}")
  assert_equal 0, $?.exitstatus
end

def get_gear_ids_for_scalable_app(app)
  url = "https://localhost/broker/rest/domains/#{app.namespace}/applications/#{app.name}/gear_groups.json"

  $logger.info("Broker url: #{url}")

  params = {
    'broker_auth_key' => File.read(File.join($home_root, app.uid, '.auth', 'token')).chomp,
    'broker_auth_iv' => File.read(File.join($home_root, app.uid, '.auth', 'iv')).chomp
  }
  
  request = RestClient::Request.new(:method => :get, 
                                    :url => url, 
                                    :timeout => 120,
                                    :headers => { :accept => 'application/json;version=1.0', :user_agent => 'OpenShift' },
                                    :payload => params)
  
  begin
    response = request.execute()

    if 300 <= response.code 
      $logger.warn(response)
      raise response
    end
  rescue 
    raise
  end

  begin
    gear_groups = JSON.parse(response)
  rescue
    raise
  end

  gear_ids = []

  gear_groups['data'].each do |data|
    data['gears'].each do |gear|
      gear_ids << gear['id']
    end
  end

  $logger.info("Gear IDs: #{gear_ids.inspect}")

  gear_ids
end

When /^the application is migrated to the v2 cartridge system$/ do
  if @app.scalable
    get_gear_ids_for_scalable_app(@app).each do |gear_uuid|
      migrate_gear(@app, gear_uuid)
    end
  else
    migrate_gear(@app, @app.uid)
  end
end

Then /^the environment variables will be migrated to raw values$/ do
  Dir.glob(File.join($home_root, @app.uid, '.env', '*')).each do |entry|
    next if File.directory?(entry)
    value = IO.read(entry)
    assert !value.start_with?('export'), entry
  end
end

Then /^the application will be marked as a v2 app$/ do
  marker_file = File.join($home_root, @app.uid, '.env', 'CARTRIDGE_VERSION_2')

  assert_file_exists marker_file
end

Given /^the application has a (USER_VARS|TRANSLATE_GEAR_VARS) env file$/ do |name|
  IO.write(File.join($home_root, @app.uid, '.env', name), '')
end

Then /^the (USER_VARS|TRANSLATE_GEAR_VARS) file will not exist$/ do |name|
  file = File.join($home_root, @app.uid, '.env', name)

  assert_file_not_exists file
end

Given /^the application has a TYPELESS_TRANSLATED_VARS env file$/ do
  typeless_vars = %Q{
export TEST_VAR_1='foo'
export TEST_VAR_2='bar'
export TEST_VAR_3="baz"
export OPENSHIFT_GEAR_CTL_SCRIPT='test'
export OPENSHIFT_TMP_DIR_2=$OPENSHIFT_TMP_DIR
export OPENSHIFT_TMP_DIR_3=$DOES_NOT_EXIST
  }

  IO.write(File.join($home_root, @app.uid, '.env', 'TYPELESS_TRANSLATED_VARS'), typeless_vars)
end

Then /^the TYPELESS_TRANSLATED_VARS variables will be discrete variables$/ do
  check_var('TEST_VAR_1', 'foo')
  check_var('TEST_VAR_2', 'bar')
  check_var('TEST_VAR_3', 'baz')

  tmp_dir_var = File.join($home_root, @app.uid, '.env', 'OPENSHIFT_TMP_DIR')
  tmp_dir_var2 = File.join($home_root, @app.uid, '.env', 'OPENSHIFT_TMP_DIR_2')

  assert_files_equal(tmp_dir_var, tmp_dir_var2)
  assert_file_not_exists File.join($home_root, @app.uid, '.env', 'OPENSHIFT_TMP_DIR_3')
  assert_file_not_exists File.join($home_root, @app.uid, '.env', 'OPENSHIFT_GEAR_CTL_SCRIPT')
  assert_file_not_exists File.join($home_root, @app.uid, '.env', 'TYPELESS_TRANSLATED_VARS')
end

Then /^the OPENSHIFT_LOG_DIR variable will not be present$/ do
  assert_file_not_exists File.join($home_root, @app.uid, '.env', 'OPENSHIFT_LOG_DIR')
end

def check_var(name, content)
  var = File.join($home_root, @app.uid, '.env', name)
  actual_content = IO.read(var)
  assert actual_content == content
end

def assert_files_equal(a, b)
  assert_file_exists a
  assert_file_exists b

  a_content = IO.read(a)
  b_content = IO.read(b)

  assert_equal a_content, b_content
end

Then /^the migration metadata will be cleaned up$/ do 
  assert Dir.glob(File.join($home_root, @app.uid, 'data', '.migration*')).empty?
  assert_file_not_exists File.join($home_root, @app.uid, 'app-root', 'runtime', '.premigration_state')
end

Then /^the (mysql|mongodb|postgresql) uservars entries will be migrated to a namespaced env directory$/ do |cart|
  cart_namespaced_dir = File.join($home_root, @app.uid, '.env', cart)

  vars = %w(USERNAME PASSWORD HOST PORT URL GEAR_UUID GEAR_DNS).map { |x| "OPENSHIFT_#{cart.upcase}_DB_#{x}"}

  vars.each do |var|
    assert_file_exists File.join(cart_namespaced_dir, var)
  end
end

Then /^the switchyard env variables will be cleaned up$/ do
  %w(EAP AS).map { |x| "OPENSHIFT_JBOSS#{x}_MODULE_PATH" }.each do |var|
    assert_file_not_exists File.join($home_root, @app.uid, '.env', var)
  end
end

Then /^the ([^ ]+) cartridge directory will exist$/ do |name|
  assert_directory_exists File.join($home_root, @app.uid, name)
end

Then /^no unprocessed ERB templates should exist$/ do
  assert Dir.glob(File.join($home_root, @app.uid, '**', '**', '*.erb')).empty?
end

# TODO: eliminate dependency on 0.0.1 version being hardcoded

Given /^the expected version of the mock cartridge is installed$/ do
  cart_repo = OpenShift::CartridgeRepository.instance
  assert cart_repo.exist?('mock', '0.0.1', '0.1'), 'expected mock version must exist'
end

Given /^a compatible version of the mock cartridge$/ do
  tmp_cart_src = '/tmp/mock-cucumber-rewrite/compat'
  current_manifest = prepare_mock_for_rewrite(tmp_cart_src)

  rewrite_and_install(current_manifest, tmp_cart_src) do |manifest, current_version|
    manifest['Compatible-Versions'] = [ current_version ]
  end
end

Given /^an incompatible version of the mock cartridge$/ do
  tmp_cart_src = '/tmp/mock-cucumber-rewrite/incompat'
  current_manifest = prepare_mock_for_rewrite(tmp_cart_src)

  rewrite_and_install(current_manifest, tmp_cart_src)
end

def prepare_mock_for_rewrite(target)
  cart_repo = OpenShift::CartridgeRepository.instance
  cartridge = cart_repo.select('mock', '0.1')

  FileUtils.rm_rf target
  FileUtils.mkpath target

  %x(shopt -s dotglob; cp -ad #{cartridge.repository_path}/* #{target})

  cartridge
end

def rewrite_and_install(current_manifest, tmp_cart_src)
  cart_manifest = File.join(tmp_cart_src, %w(metadata manifest.yml))

  current_version = current_manifest.cartridge_version
  current_version =~ /(\d+)$/
  current_minor_version = $1.to_i
  next_version = current_version.sub(/\d+$/, (current_minor_version + 1).to_s)

  manifest = YAML.load_file(cart_manifest)
  manifest['Cartridge-Version'] = next_version

  yield manifest, current_version if block_given?

  IO.write(cart_manifest, manifest.to_yaml)
  IO.write(File.join($home_root, @app.uid, %w(app-root data mock_test_version)), next_version)

  assert_successful_install tmp_cart_src, next_version
end

def assert_successful_install(tmp_cart_src, next_version)
  OpenShift::CartridgeRepository.instance.install(tmp_cart_src)
  observed_latest_version = OpenShift::CartridgeRepository.instance.select('mock', '0.1').cartridge_version

  $logger.info "Observed latest version: #{observed_latest_version}"

  assert_equal next_version, observed_latest_version

  %x(pkill -USR1 -f /usr/sbin/mcollectived)
end

Then /^the mock cartridge version should be updated$/ do
  new_version = IO.read(File.join($home_root, @app.uid, %w(app-root data mock_test_version))).chomp

  ident_path                 = Dir.glob(File.join($home_root, @app.uid, %w(mock env OPENSHIFT_*_IDENT))).first
  ident                      = IO.read(ident_path)
  _, _, _, cartridge_version = OpenShift::Runtime::Manifest.parse_ident(ident)

  assert_equal new_version, cartridge_version
end

When /^the ([^ ]+) invocation markers are cleared$/ do |cartridge_name|
  state_dir_name = ".#{cartridge_name.sub('-', '_')}_cartridge_state"
  Dir.glob(File.join($home_root, @app.uid, 'app-root', 'data', state_dir_name, '*')).each { |x| 
    FileUtils.rm_f(x) unless x.end_with?('_process')
  }
end

When /^the application is migrated to the new cartridge versions$/ do
  migrate_gear(@app, @app.uid, true)
end

Then /^the invocation markers from an? (compatible|incompatible) migration should exist$/ do |type|
  should_exist_markers = case type
  when 'compatible'
    %w(control_status)
  when 'incompatible'
    %w(setup_called setup_succeed control_start control_status)
  end

  should_not_exist_markers = case type
  when 'compatible'
    %w(setup_called control_start)
  when 'incompatible'
    # The control_stop marker is deleted during the mock cartridge setup, 
    # so we expect it _not_ to exist after an incompatible migration.
    %w(setup_failure control_stop)
  end

  should_exist_markers.each do |marker|
    marker_file = File.join($home_root, @app.uid, 'app-root', 'data', '.mock_cartridge_state', marker)
    assert_file_exists marker_file
  end

  should_not_exist_markers.each do |marker|
    marker_file = File.join($home_root, @app.uid, 'app-root', 'data', '.mock_cartridge_state', marker)
    assert_file_not_exists marker_file
  end    
end
