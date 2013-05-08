require 'rubygems'
require 'etc'
require 'fileutils'
require 'socket'
require 'parseconfig'
require 'pp'

require_relative "migrate-util"
require_relative "migrate-progress"
require_relative "migrate-v2-diy-0.1"
require_relative "migrate-v2-jbossas-7"
require_relative "migrate-v2-jbosseap-6.0"
require_relative "migrate-v2-jbossews-1.0"
require_relative "migrate-v2-jbossews-2.0"
require_relative "migrate-v2-nodejs-0.6"
require_relative "migrate-v2-perl-5.10"
require_relative "migrate-v2-php-5.3"
require_relative "migrate-v2-python-2.6"
require_relative "migrate-v2-ruby-1.8"
require_relative "migrate-v2-ruby-1.9"
require_relative "migrate-v2-zend-5.6"
require_relative "migrate-v2-metrics-0.1"
require_relative "migrate-v2-jenkins-1.4"
require_relative "migrate-v2-jenkins-client-1.4"
require_relative "migrate-v2-mongodb-2.2"
require_relative "migrate-v2-rockmongo-1.1"
require_relative "migrate-v2-10gen-mms-agent-0.1"
require_relative "migrate-v2-mysql-5.1"
require_relative "migrate-v2-phpmyadmin-3.4"
require_relative "migrate-v2-postgresql-8.4"
require_relative "migrate-v2-switchyard-0.6"

require 'openshift-origin-node/model/cartridge_repository'
require 'openshift-origin-node/model/unix_user'
require 'openshift-origin-node/utils/sdk'
require 'openshift-origin-node/utils/cgroups'
require 'openshift-origin-node/utils/application_state'
require 'openshift-origin-node/utils/environ'
require 'openshift-origin-common'
require 'net/http'
require 'uri'

module OpenShift
  class V2MigrationCartridgeModel < V2CartridgeModel
    ##
    # In this subclass, this method is changed slightly to account for
    # V1 cartridge directories which may exist in the gear.
    def process_cartridges(cartridge_dir = nil) # : yields cartridge_path
      if cartridge_dir
        cart_dir = File.join(@user.homedir, cartridge_dir)
        yield cart_dir if File.exist?(cart_dir)
        return
      end

      Dir[PathUtils.join(@user.homedir, "*")].each do |cart_dir|
        next if cart_dir.end_with?('app-root') || cart_dir =~ /-\d/ || cart_dir.end_with?('git') ||
            (not File.directory? cart_dir)
        yield cart_dir
      end
    end

    def gear_status
      output = ''
      problem = false

      each_cartridge do |cartridge|
        cart_status = do_control('status', cartridge)
        output << cart_status

        if cart_status !~ /running/
          problem = true
        end
      end

      return [problem, output]
    end
  end
end

module OpenShift::Utils
  class MigrationApplicationState < ApplicationState
    def initialize(uuid, state_file = '.state')
      @uuid = uuid

      config      = OpenShift::Config.new
      @state_file = File.join(config.get("GEAR_BASE_DIR"), uuid, "app-root", "runtime", state_file)
    end
  end
end

module OpenShiftMigration
  PREMIGRATION_STATE = '.premigration_state'

  def self.rm_exists(file)
    # We want all errors reported, except for missing file...
    FileUtils.rm(file) if File.exists?(file)
  end

  def self.get_config_value(key)
    @node_config ||= ParseConfig.new('/etc/openshift/node.conf')
    val = @node_config.get_value(key)
    val.gsub!(/\\:/,":") if not val.nil?
    val.gsub!(/[ \t]*#[^\n]*/,"") if not val.nil?
    val = val[1..-2] if not val.nil? and val.start_with? "\""
    val
  end

  # Note: This method must be reentrant, meaning it should be able to
  # be called multiple times on the same gears.  Each time having failed
  # at any point and continue to pick up where it left off or make
  # harmless changes the 2-n times around.
  def self.migrate(uuid, namespace, version)
    unless version == "2.0.28"
      return "Invalid version: #{version}", 255
    end

    start_time = (Time.now.to_f * 1000).to_i
    
    cartridge_root_dir = "/usr/libexec/openshift/cartridges"
    libra_home = '/var/lib/openshift' #node_config.get_value('libra_dir')
    libra_server = get_config_value('BROKER_HOST')
    libra_domain = get_config_value('CLOUD_DOMAIN')
    gear_name = nil
    app_name = nil
    output = "Beginning V1 -> V2 migration\n"

    gear_home = "#{libra_home}/#{uuid}"
    begin
      gear_name = Util.get_env_var_value(gear_home, "OPENSHIFT_GEAR_NAME")
      app_name = Util.get_env_var_value(gear_home, "OPENSHIFT_APP_NAME")
    rescue Errno::ENOENT
      return "***acceptable_error_env_vars_not_found={\"gear_uuid\":\"#{uuid}\"}***\n", 0
    end
    
    exitcode = 0
    env_echos = []

    unless (File.exists?(gear_home) && !File.symlink?(gear_home))
      exitcode = 127
      output += "Application not found to migrate: #{gear_home}\n"
      return output, exitcode
    end

    progress = MigrationProgress.new(uuid)

    output << inspect_gear_state(progress, gear_home)
    output << migrate_stop_lock(progress, uuid, gear_home)
    output << stop_gear(progress, uuid)
    output << migrate_typeless_translated_vars(progress, uuid, gear_home)
    output << cleanup_gear_env(progress, gear_home)
    output << migrate_env_vars_to_raw(progress, gear_home)

    OpenShift::Utils::Sdk.mark_new_sdk_app(gear_home)
    cartridge_migrators = load_cartridge_migrators 

    output << migrate_cartridges(progress, gear_home, uuid, cartridge_migrators)

    start_gear(progress, uuid)

    output << validate_gear(progress, uuid, gear_home)
    output << cleanup(progress, gear_home)

    env_echos.each do |env_echo|
      echo_output, echo_exitcode = Util.execute_script(env_echo)
      output += echo_output
    end

    total_time = (Time.now.to_f * 1000).to_i - start_time
    output += "***time_migrate_on_node_measured_from_node=#{total_time}***\n"
    return output, exitcode
  end

  def self.inspect_gear_state(progress, gear_home)
    output = ''

    if progress.incomplete? 'inspect_gear_state'
      app_state = File.join(gear_home, 'app-root', 'runtime', '.state')
      save_state = File.join(gear_home, 'app-root', 'runtime', PREMIGRATION_STATE)
      FileUtils.cp(app_state, save_state)
      output << progress.mark_complete('inspect_gear_state')
    end

    output
  end

  def self.migrate_stop_lock(progress, uuid, gear_home)
    output = ''

    if progress.incomplete? 'detect_v1_stop_lock'
      stop_lock_found = !Dir.glob(File.join(gear_home, '*-*', 'run', 'stop_lock')).empty?

      if stop_lock_found
        config = OpenShift::Config.new
        state  = OpenShift::Utils::ApplicationState.new(uuid)
        user   = OpenShift::UnixUser.from_uuid(uuid)

        output << "Creating V2 stop_lock\n"

        cart_model = OpenShift::V2MigrationCartridgeModel.new(config, user, state)
        cart_model.create_stop_lock
      else
        output << "V1 stop lock not detected\n"
      end

      output << progress.mark_complete('migrate_stop_lock')
    end

    output
  end

  def self.stop_gear(progress, uuid)
    output = ''

    if progress.incomplete? 'stop_gear'
      container = OpenShift::ApplicationContainer.from_uuid(uuid)
      container.stop_gear(user_initiated: false)
      container.force_stop
      output << progress.mark_complete('stop_gear')
    end

    output
  end

  def self.start_gear(progress, uuid)
    output = ''

    if progress.incomplete? 'start_gear'
      OpenShift::ApplicationContainer.from_uuid(uuid).start_gear(user_initiated: false)
      output << progress.mark_complete('start_gear')
    end

    output
  end

  def self.load_cartridge_migrators
    migrators = {}

    cr = OpenShift::CartridgeRepository.instance

    # TODO: fix problems loading commented out lines
    migrators[cr.select('diy', '0.1')] = Diy01Migration.new
    # migrators[cr.select('jbossas', '7')] = Jbossas7Migration.new # name changed to jbossas-7.1
    migrators[cr.select('jbosseap', '6.0')] = Jbosseap60Migration.new
    #migrators[cr.select('jbossews', '1.0')] = Jbossews10Migration.new
    #migrators[cr.select('jbossews', '2.0')] = Jbossews20Migration.new
    migrators[cr.select('nodejs', '0.6')] = Nodejs06Migration.new
    migrators[cr.select('perl', '5.10')] = Perl510Migration.new
    migrators[cr.select('php', '5.3')] = Php53Migration.new
    migrators[cr.select('python', '2.6')] = Python26Migration.new
    migrators[cr.select('ruby', '1.8')] = Ruby18Migration.new
    migrators[cr.select('ruby', '1.9')] = Ruby19Migration.new
    #migrators[cr.select('zend', '5.6')] = Zend56Migration.new # not in li yet
    migrators[cr.select('metrics', '0.1')] = Metrics01Migration.new
    migrators[cr.select('jenkins', '1.4')] = Jenkins14Migration.new
    migrators[cr.select('jenkins-client', '1.4')] = JenkinsClient14Migration.new
    migrators[cr.select('mongodb', '2.2')] = Mongodb22Migration.new
    migrators[cr.select('rockmongo', '1.1')] = Rockmongo11Migration.new
    migrators[cr.select('10gen-mms-agent', '0.1')] = Tengenmmsagent01Migration.new
    migrators[cr.select('mysql', '5.1')] = Mysql51Migration.new
    migrators[cr.select('phpmyadmin', '3.4')] = Phpmyadmin34Migration.new
    migrators[cr.select('postgresql', '8.4')] = Postgresql84Migration.new
    #migrators[cr.select('switchyard', '0.6')] = Switchyard06Migration.new

    migrators
  end

  def self.migrate_typeless_translated_vars(progress, uuid, gear_home)
    output = ''

    if progress.incomplete? 'typeless_translated_vars'
      blacklist = %w(OPENSHIFT_GEAR_CTL_SCRIPT OPENSHIFT_GEAR_TYPE)
      user = OpenShift::UnixUser.from_uuid(uuid)
      vars_file = File.join(gear_home, '.env', 'TYPELESS_TRANSLATED_VARS')

      if File.exists?(vars_file)
        content = IO.read(vars_file)

        content.each_line do |line|
          if line.chomp =~ /export ([^=]+)=\'([^\']+)\'/
            key = $1
            value = $2

            next if blacklist.include?(key)

            env_var_file = File.join(gear_home, '.env', key)

            IO.write(env_var_file, value)

            mcs_label = OpenShift::Utils::SELinux.get_mcs_label(uuid)
            PathUtils.oo_chown(0, user.gid, env_var_file)
            OpenShift::Utils::SELinux.set_mcs_label(mcs_label, env_var_file)
          end
        end
      end

      output << progress.mark_complete('typeless_translated_vars')
    end

    output
  end

  def self.cleanup_gear_env(progress, gear_home)
    output = ''

    if progress.incomplete? 'gear_env_cleanup'
      FileUtils.rm_rf(File.join(gear_home, '.env', 'USER_VARS'))
      FileUtils.rm_rf(File.join(gear_home, '.env', 'TRANSLATE_GEAR_VARS'))
      output << progress.mark_complete('gear_env_cleanup')
    end

    output
  end

  def self.migrate_env_vars_to_raw(progress, gear_home)
    output = ''

    if progress.incomplete? 'env_vars_to_raw'
      Dir.glob(File.join(gear_home, '.env', '*')).each do |entry|
        content = IO.read(entry).chomp
        if content =~ /^export /
          output << "Migrating #{File.basename(entry)} to raw value\n"
          content.sub!(/^export [^=]+=\'([^\']*)\'/, '\1')
          IO.write(entry, content)
        end
      end

      output << progress.mark_complete('env_vars_to_raw')
    end

    output
  end

  def self.migrate_cartridges(progress, gear_home, uuid, cartridge_migrators)
    output = ''

    # TODO: establish migration order of cartridges
    v1_cartridges(gear_home).each do |cartridge_name|
      tokens = cartridge_name.split('-')
      version = tokens.pop
      name = tokens.join('-')
      output << migrate_cartridge(progress, name, version, uuid, cartridge_migrators)
    end

    output
  end

  def self.v1_cartridges(gear_home)
    v1_carts = []

    Dir.glob(File.join(gear_home, '*-*')).each do |entry|
      # Account for app-root and V2 carts matching the glob which already may be installed
      next if entry.end_with?('app-root') || entry.end_with?('jenkins-client') || entry.end_with?('mms-agent') || !File.directory?(entry)
        
      v1_carts << File.basename(entry)
    end

    v1_carts
  end

  def self.migrate_cartridge(progress, name, version, uuid, cartridge_migrators)
    config = OpenShift::Config.new
    state  = OpenShift::Utils::ApplicationState.new(uuid)
    user   = OpenShift::UnixUser.from_uuid(uuid)

    cart_model = OpenShift::V2MigrationCartridgeModel.new(config, user, state)
    cartridge  = OpenShift::CartridgeRepository.instance.select(name, version)

    output = ''

    OpenShift::Utils::Cgroups.with_no_cpu_limits(uuid) do
      if progress.incomplete? "#{name}_create_directory"
        cart_model.create_cartridge_directory(cartridge, version)
        output << progress.mark_complete("#{name}_create_directory")
      end

      Dir.chdir(user.homedir) do
        cart_model.unlock_gear(cartridge) do |c|
          if progress.incomplete? "#{name}_setup"
            output << cart_model.cartridge_action(c, 'setup', version, true)
            output << progress.mark_complete("#{name}_setup")
          end

          if progress.incomplete? "#{name}_erb"
            cart_model.process_erb_templates(c.directory)
            output << progress.mark_complete("#{name}_erb")
          end

          if progress.incomplete? "#{name}_hook"
            output << migration_post_process_hook(user, c, cartridge_migrators)
            output << progress.mark_complete("#{name}_hook")
          end
        end
      end

      if progress.incomplete? "#{name}_connect_frontend"
        cart_model.connect_frontend(cartridge)
        output << progress.mark_complete("#{name}_connect_frontend")
      end
    end

    FileUtils.rm_rf(File.join(user.homedir, "#{name}-#{version}"))

    output
  end

  def self.migration_post_process_hook(user, cartridge, cartridge_migrators)
    output = ''
    cartridge_migrator = cartridge_migrators[cartridge]

    if cartridge_migrator
      output << cartridge_migrator.post_process(user)
    else
      output << "Unable to find migrator for #{cartridge}\n"
    end

    output
  end

  def self.validate_gear(progress, uuid, gear_home)
    output = ''

    if progress.incomplete? 'validate_gear'
      premigration_state = OpenShift::Utils::MigrationApplicationState.new(uuid, PREMIGRATION_STATE)

      output << "Pre-migration state: #{premigration_state.value}\n"

      if premigration_state.value == 'started'
        config = OpenShift::Config.new
        state  = OpenShift::Utils::ApplicationState.new(uuid)
        user   = OpenShift::UnixUser.from_uuid(uuid)

        cart_model = OpenShift::V2MigrationCartridgeModel.new(config, user, state)

        if cart_model.primary_cartridge
          env = OpenShift::Utils::Environ.for_gear(gear_home)

          dns = env['OPENSHIFT_GEAR_DNS']
          uri = URI.parse("http://#{dns}")

          http = Net::HTTP.new(uri.host, uri.port)
          request = Net::HTTP::Get.new(uri.request_uri)

          response = http.request(request)

          output << "Post-migration response code: #{response.code}\n"
        end

        problem, status = cart_model.gear_status

        if problem
          output << "Leaving migration metadata in place due to problem detected with gear status\n"
          output << "Status: #{status}\n"
          return output
        end
      end

      output << progress.mark_complete('validate_gear')
    end

    output
  end

  def self.cleanup(progress, gear_home)
    output = ''

    if progress.complete? 'validate_gear'
      output << 'Cleaning up after migration'
      FileUtils.rm_f(File.join(gear_home, 'app-root', 'runtime', PREMIGRATION_STATE))
      progress.clear
    end

    output
  end
end
