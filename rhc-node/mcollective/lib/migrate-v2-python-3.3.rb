module OpenShiftMigration
  class Python33Migration
    def post_process(user, progress, env)
      output = "applying python-3.3 migration post-process\n"

      Util.rm_env_var(user.homedir, 'OPENSHIFT_PYTHON_LOG_DIR')

      cartridge_dir = File.join(user.homedir, 'python')

      Util.add_cart_env_var(user, 'python', 'OPENSHIFT_PYTHON_VERSION', '3.3')
      Util.add_cart_env_var(user, 'python', 'OPENSHIFT_PYTHON_PATH_ELEMENT',
                            File.join(cartridge_dir, 'virtenv','venv', 'bin'))
      Util.add_cart_env_var(user, 'python', 'LD_LIBRARY_PATH',
                            File.join(cartridge_dir, 'opt', 'lib'))

      FileUtils.mkpath(File.join(cartridge_dir, 'virtenv'))

      directories = %w(logs virtenv)
      output << Util.move_directory_between_carts(user, 'python-3.3', 'python', directories)

      activate_file_contents = <<-AVEOF
# Set the library path so that the python shared library can be found.
export LD_LIBRARY_PATH="\${OPENSHIFT_PYTHON_DIR}/opt/lib:\${LD_LIBRARY_PATH}"
export LIBRARY_PATH="\${OPENSHIFT_PYTHON_DIR}/opt/lib:\${LIBRARY_PATH}"
source \${OPENSHIFT_PYTHON_DIR}/virtenv/venv/bin/activate
AVEOF

      activate_file_path = File.join(cartridge_dir, 'bin', 'activate_virtenv')

      File.open(activate_file_path, 'w', 0555) do |f|
        f.write(activate_file_contents)
      end

      Util.make_user_owned(activate_file_path, user)

      Util.cp_env_var_value(user.homedir, 'OPENSHIFT_INTERNAL_IP',   'OPENSHIFT_PYTHON_IP')
      Util.cp_env_var_value(user.homedir, 'OPENSHIFT_INTERNAL_PORT', 'OPENSHIFT_PYTHON_PORT')

      output
    end
  end
end
