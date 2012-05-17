require 'rubygems'
require 'etc'
require 'fileutils'
require 'socket'
require 'parseconfig'
require 'pp'
require File.dirname(__FILE__) + "/migrate-util"

REMOVE_GEAR_RUNTIME_DIR = false

module OpenShiftMigration

  def self.get_config_value(key)
    @node_config ||= ParseConfig.new('/etc/stickshift/stickshift-node.conf')
    val = @node_config.get_value(key)
    val.gsub!(/\\:/,":") if not val.nil?
    val.gsub!(/[ \t]*#[^\n]*/,"") if not val.nil?
    val = val[1..-2] if not val.nil? and val.start_with? "\""
    val
  end

  def self.get_mcs_level(uuid)
    userinfo = Etc.getpwnam(uuid)
    uid = userinfo.uid
    setsize=1023
    tier=setsize
    ord=uid
    while ord > tier
      ord -= tier
      tier -= 1
    end
    tier = setsize - tier
    "s0:c#{tier},c#{ord + tier}"
  end

  def self.secure_user_files(uuid, grp, perms, mcs_level, pathlist)
    FileUtils.chown_R uuid, grp, pathlist
    FileUtils.chmod_R perms, pathlist
    %x[ chcon -t libra_var_lib_t -l #{mcs_level} -R #{pathlist.join " "} ]
  end

  def self.remove_dir_if_empty(dirname)
    Dir.rmdir dirname if (File.directory? dirname)  &&  (Dir.entries(dirname) - %w[ . .. ]).empty?
  end

  def self.move_dir_and_symlink(srcdir, destdir, symlink_offset=nil)
    if (not File.symlink? srcdir)  &&  (File.directory? srcdir)
      FileUtils.rm_f destdir  if (File.symlink? destdir)  ||  (not File.directory? destdir)
      FileUtils.mkdir_p destdir
      FileUtils.mv Dir.glob("#{srcdir}/*"), destdir
      FileUtils.rm_rf srcdir
    end

    FileUtils.rm_f srcdir
    if symlink_offset
      FileUtils.ln_sf symlink_offset, srcdir
    else
      FileUtils.ln_sf destdir, srcdir
    end
  end

  def self.migrate_to_appdir(uuid, gear_home)
    zpathlist = []
    grp = uuid
    mcs_level = self.get_mcs_level(uuid)

    gear_name = Util.get_env_var_value(gear_home, "OPENSHIFT_GEAR_NAME")
    app_name = Util.get_env_var_value(gear_home, "OPENSHIFT_APP_NAME")
    gear_dir = File.join(gear_home, gear_name)
    app_dir = File.join(gear_home, "app")

    FileUtils.mkdir_p app_dir
    zpathlist.push app_dir

    data_dir = File.join(gear_home, gear_name, "data")
    app_data_dir = File.join(app_dir, "data")
    zoffset = File.join("..", "app", "data")
    self.move_dir_and_symlink(data_dir, app_data_dir, zoffset)
    Util.set_env_var_value(gear_home, "OPENSHIFT_DATA_DIR", app_data_dir)
    zpathlist.push app_data_dir

    state_file = File.join(gear_home, gear_name, "runtime", ".state")
    app_state_file = File.join(app_dir, ".state")
    FileUtils.mv state_file, app_state_file, :force => true  if File.exists? state_file
    zpathlist.push app_state_file

    #  Move the old repo to the new location and create symlinks
    #  for compatibility to existing apps.
    old_runtime_dir = File.join(gear_home, gear_name, "runtime")
    if File.exists? old_runtime_dir
      old_runtime_repo_dir = File.join(old_runtime_dir, "repo")
      app_repo_dir = File.join(app_dir, "repo")
      self.move_dir_and_symlink(old_runtime_repo_dir, app_repo_dir)
      if REMOVE_GEAR_RUNTIME_DIR
        FileUtils.rm_f old_runtime_repo_dir
        self.remove_dir_if_empty(old_runtime_dir)
      else
        # If we want to keep the old runtime dir around.
        zpathlist.push old_runtime_repo_dir
      end
      Util.set_env_var_value(gear_home, "OPENSHIFT_REPO_DIR", app_repo_dir)
    end

    gear_repo_dir = File.join(gear_home, gear_name, "repo")
    if (gear_name != app_name)  &&  (File.symlink? gear_repo_dir)
      zoffset = File.join("..", "app", "repo")
      FileUtils.rm_f gear_repo_dir
      FileUtils.ln_sf zoffset, gear_repo_dir
      zpathlist.push gear_repo_dir
    end

    self.secure_user_files(uuid, grp, 0750, mcs_level, zpathlist)
  end

  def self.migrate(uuid, namespace, version)
    if version == "2.0.12"
      libra_home = '/var/lib/stickshift' #node_config.get_value('libra_dir')
      libra_server = get_config_value('BROKER_HOST')
      libra_domain = get_config_value('CLOUD_DOMAIN')
      gear_home = "#{libra_home}/#{uuid}"
      gear_name = Util.get_env_var_value(gear_home, "OPENSHIFT_GEAR_NAME")
      gear_dir = "#{gear_home}/#{gear_name}"
      output = ''
      exitcode = 0
      if (File.exists?(gear_home) && !File.symlink?(gear_home))
        gear_type = Util.get_env_var_value(gear_home, "OPENSHIFT_GEAR_TYPE")
        cartridge_root_dir = "/usr/libexec/stickshift/cartridges"
        cartridge_dir = "#{cartridge_root_dir}/#{gear_type}"

        env_echos = []

        self.migrate_to_appdir(uuid, gear_home)

        env_echos.each do |env_echo|
          echo_output, echo_exitcode = Util.execute_script(env_echo)
          output += echo_output
        end

      else
        exitcode = 127
        output += "Application not found to migrate: #{gear_home}\n"
      end
      return output, exitcode
    else
      return "Invalid version: #{version}", 255
    end
  end
end
