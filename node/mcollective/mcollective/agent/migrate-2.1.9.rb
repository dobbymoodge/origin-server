require 'rubygems'
require 'fileutils'
require 'parseconfig'
require 'pp'
require File.dirname(__FILE__) + "/migrate-util"

module LibraMigration

  def self.migrate(uuid, app_name, app_type, namespace, version)
    node_config = ParseConfig.new('/etc/libra/node.conf')
    libra_home = '/var/lib/libra' #node_config.get_value('libra_dir')
    libra_server = node_config.get_value('libra_server')
    libra_domain = node_config.get_value('libra_domain')
    app_home = "#{libra_home}/#{uuid}"
    app_dir = "#{app_home}/#{app_name}"
    output = ''
    exitcode = 0
    if (File.exists?(app_home) && !File.symlink?(app_home))
      #cartridge_root_dir = "/usr/libexec/li/cartridges"
      #cartridge_dir = "#{cartridge_root_dir}/#{app_type}"

      git_dir = "#{app_home}/git/#{app_name}.git/"
      FileUtils.chown(uuid, uuid, git_dir)
      FileUtils.chmod(0755, git_dir)
      
      gitconfig = "#{app_home}/.gitconfig"
      output += "Migrating .gitconfig: #{gitconfig}\n"
      file = File.open(gitconfig, 'w')
      begin
        file.puts <<EOF
[user]
  name = OpenShift System User
[gc]
  auto = 100
EOF
      ensure
        file.close
      end
      
      FileUtils.chown('root', 'root', gitconfig)
      FileUtils.chmod(0644, gitconfig)
      
      if app_type == 'php-5.3'
        output += Util.replace_in_file("#{app_dir}/conf/php.ini", 'upload_max_filesize = 10M', 'upload_max_filesize = 200M')
        output += Util.replace_in_file("#{app_dir}/conf/php.ini", 'post_max_size = 8M', 'post_max_size = 200M')
      end
      
      phpmyadmin_dir = "#{app_home}/phpmyadmin-3.4"
      if File.exists?(phpmyadmin_dir)
        output += Util.replace_in_file("#{phpmyadmin_dir}/conf/php.ini", 'upload_max_filesize = 2M', 'upload_max_filesize = 200M')
        output += Util.replace_in_file("#{phpmyadmin_dir}/conf/php.ini", 'post_max_size = 8M', 'post_max_size = 200M')
      end
      
      mysql_dir = "#{app_home}/mysql-5.1"
      if File.exists?(mysql_dir)
        output += Util.replace_in_file("#{mysql_dir}/etc/my.cnf", 'max_allowed_packet = 1M', 'max_allowed_packet = 200M')
      end
      
    else
      exitcode = 127
      output += "Application not found to migrate: #{app_home}\n"
    end
    return output, exitcode
  end
end
