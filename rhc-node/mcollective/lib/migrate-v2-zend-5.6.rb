require_relative 'migrate-util'
require 'openshift-origin-node/utils/shell_exec'
require 'openshift-origin-common/utils/path_utils'

module OpenShiftMigration
  class Zend56Migration
    def post_process(user, progress, env)
      output = "applying zend-5.6 migration post-process\n"

      Util.rm_env_var(user.homedir, 'OPENSHIFT_ZEND_LOG_DIR')

      cartridge_dir = File.join(user.homedir, 'zend')
      zend_dir = File.join(user.homedir, 'zend')
      zend_usr_dir = File.join(zend_dir, 'usr/local/zend')

      sandbox_dir = File.join(user.homedir, '.sandbox', user.name)
      zend_sandbox_dir = File.join(sandbox_dir, 'zend')

      output << "fixing " << zend_sandbox_dir << " " << user.name << "\n"

      PathUtils.oo_chown('root', user.name, sandbox_dir)
      FileUtils.chmod(0o0755, sandbox_dir)
      PathUtils.oo_chown('root', user.name, zend_sandbox_dir)
      FileUtils.chmod(0o0755, zend_sandbox_dir)

      FileUtils.rm_f(File.join(zend_sandbox_dir, 'etc'))
      FileUtils.ln_sf(File.join(zend_usr_dir, 'etc'), File.join(zend_sandbox_dir, 'etc'))
      FileUtils.rm_f(File.join(zend_sandbox_dir, 'tmp'))
      FileUtils.ln_sf(File.join(zend_usr_dir, 'tmp'), File.join(zend_sandbox_dir, 'tmp'))
      FileUtils.rm_f(File.join(zend_sandbox_dir, 'var'))
      FileUtils.ln_sf(File.join(zend_usr_dir, 'var'), File.join(zend_sandbox_dir, 'var'))
      FileUtils.rm_f(File.join(zend_sandbox_dir, 'gui/application/data'))
      FileUtils.ln_sf(File.join(zend_usr_dir, 'gui/application/data'), File.join(zend_sandbox_dir, 'gui/application/data'))
      FileUtils.rm_f(File.join(zend_sandbox_dir, 'gui/lighttpd/etc'))
      FileUtils.ln_sf(File.join(zend_usr_dir, 'gui/lighttpd/etc'), File.join(zend_sandbox_dir, 'gui/lighttpd/etc'))
      FileUtils.rm_f(File.join(zend_sandbox_dir, 'gui/lighttpd/logs'))
      FileUtils.ln_sf(File.join(zend_usr_dir, 'gui/lighttpd/logs'), File.join(zend_sandbox_dir, 'gui/lighttpd/logs'))
      FileUtils.rm_f(File.join(zend_sandbox_dir, 'gui/lighttpd/tmp'))
      FileUtils.ln_sf(File.join(zend_usr_dir, 'gui/lighttpd/tmp'), File.join(zend_sandbox_dir, 'gui/lighttpd/tmp'))

      FileUtils.mkdir_p(File.join(zend_sandbox_dir, 'bin'))
      FileUtils.ln_sf(File.join(zend_dir, 'bin/control'), File.join(zend_sandbox_dir, 'bin/apachectl'))

      output << "generating new .pearrc\n"
      FileUtils.rm_f(File.join(user.homedir, '.pearrc'))
      pearrc = File.join(user.homedir, '.pearrc')

      spawn_ops = { chdir: user.homedir,
                    unsetenv_others: true,
                    uid: user.uid,
                    expected_exitstatus: 0
                  }

      OpenShift::Utils.oo_spawn("pear config-create #{zend_dir}/phplib/pear/ #{pearrc}", spawn_ops)
      OpenShift::Utils.oo_spawn("pear -c #{pearrc} config-set php_ini /usr/local/zend/etc/php.ini", spawn_ops)
      OpenShift::Utils.oo_spawn("pear -c #{pearrc} config-set auto_discover 1", spawn_ops)

      output << "fixing ENV vars\n"
      Util.add_cart_env_var(user, 'zend', 'OPENSHIFT_ZEND_VERSION', '5.6')
      Util.add_cart_env_var(user, 'zend', 'OPENSHIFT_ZEND_CONSOLE_PORT', '16081')
      Util.add_cart_env_var(user, 'zend', 'OPENSHIFT_ZEND_ZENDSERVER_PORT', '16083')
      Util.add_cart_env_var(user, 'zend', 'OPENSHIFT_ZEND_UID', user.uid)
      Util.add_cart_env_var(user, 'zend', 'OPENSHIFT_ZEND_PATH_ELEMENT', '/usr/local/zend/bin')

      Util.add_cart_env_var(user, 'zend', 'ORACLE_BASE', File.join(zend_dir, 'oracle'))
      Util.add_cart_env_var(user, 'zend', 'ORACLE_HOME', File.join(zend_dir, 'oracle'))
      FileUtils.mkdir_p(File.join(zend_dir, 'oracle'))

      output << "copying zend 5.6 config files\n"
      FileUtils.mkdir_p(File.join(cartridge_dir, 'configuration/etc/conf.d'))
      FileUtils.cp_r(Dir.glob(File.join(cartridge_dir, 'versions/5.6/configuration/etc/*')), File.join(cartridge_dir, 'configuration/etc/'))

      FileUtils.ln_sf('/usr/lib64/httpd/modules', File.join(cartridge_dir, 'modules'))
      FileUtils.mkdir_p(File.join(cartridge_dir, 'conf'))
      FileUtils.ln_sf('/etc/httpd/conf/magic', File.join(cartridge_dir, 'conf/magic'))

      directories = %w(logs sessions phplib)
      output << Util.move_directory_between_carts(user, 'zend-5.6', 'zend', directories)

      FileUtils.mkdir_p(File.join(cartridge_dir, 'usr/local/zend/etc'))
      FileUtils.mkdir_p(File.join(cartridge_dir, 'usr/local/zend/tmp'))
      FileUtils.mkdir_p(File.join(cartridge_dir, 'usr/local/zend/var'))
      FileUtils.mkdir_p(File.join(cartridge_dir, 'usr/local/zend/gui'))

      directories = %w(etc tmp var gui)
      output << Util.move_directory_between_carts(user, 'zend-5.6', 'zend/usr/local/zend', directories)

      Util.cp_env_var_value(user.homedir, 'OPENSHIFT_INTERNAL_IP',   'OPENSHIFT_ZEND_IP')
      Util.cp_env_var_value(user.homedir, 'OPENSHIFT_INTERNAL_PORT', 'OPENSHIFT_ZEND_PORT')

      output
    end
  end
end
