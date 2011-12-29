#--
# Copyright 2010 Red Hat, Inc.
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#    http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#++


require 'rubygems'
require 'cloud-sdk-node/config'
require 'cloud-sdk-node/utils/shell_exec'
require 'cloud-sdk-node/model/cdk_model'

module Cloud::SDK::Model
  class UserCreationException < Exception
  end

  class UserDeletionException < Exception
  end
  
  # == Unix User
  #
  # Represents a user account on the system.
  class UnixUser < CdkModel
    include Cloud::SDK::Utils::ShellExec
    attr_reader :uuid, :uid, :gid, :gecos, :homedir, :application_uuid, :container_uuid
    
    DEFAULT_SKEL_DIR = File.join(Cloud::SDK::Config::CONF_DIR,"skel")

    def initialize(application_uuid, container_uuid)
      @config = Cloud::SDK::Config.instance
      
      @container_uuid = container_uuid
      @application_uuid = application_uuid
      @uuid = container_uuid
      begin
        user_info = Etc.getpwnam(@uuid)
        @uid = user_info.uid
        @gid = user_info.gid
        @gecos = user_info.gecos
        @homedir = "#{user_info.dir}/"
      rescue ArgumentError => e
        @uid = nil
        @gid = nil
        @gecos = nil
        @homedir = nil
      end
    end
    
    def name
      @uuid
    end
    
    def create
      skel_dir = @config.get("user_skel_dir") || DEFAULT_SKEL_DIR
      shell    = @config.get("user_shell")     || "/bin/bash"
      gecos    = @config.get("user_gecos")     || "CDK application container"
      notify_observers(:before_unix_user_create)
      basedir = @config.get("user_base_dir")
      
      File.open("/var/lock/cdk-create", File::RDWR|File::CREAT, 0o0600) do |lock|
        lock.flock(File::LOCK_EX)
        
        unless @uid
          @uid = @gid = next_uid
          @homedir = File.join(basedir,@uuid)
        end
        
        cmd = "useradd -u #{@uid} -d #{@homedir} -s #{shell} -c '#{gecos}' -m -k #{skel_dir} #{@uuid}"
        out,err,rc = shellCmd(cmd)
        raise UserCreationException.new("ERROR: unable to create user account #{@uuid}") unless rc == 0
        
        FileUtils.chown("root", @uuid, @homedir)
        FileUtils.chmod 0o0750, @homedir
      end
      notify_observers(:after_unix_user_create)
      initialize_homedir
    end
    
    def destroy
      raise UserDeletionException.new("ERROR: unable to create user account #{@uuid}") if @uid.nil? || @homedir.nil? || @uuid.nil?
      notify_observers(:before_unix_user_destroy)
      
      cmd = "/bin/ps -U \"#{@uuid}\" -o pid | /bin/grep -v PID | xargs kill -9 2> /dev/null"
      (1..10).each do |i|
        out,err,rc = shellCmd(cmd)
        break unless rc == 0
      end
      
      FileUtils.rm_rf(@homedir)

      out,err,rc = shellCmd("userdel \"#{@uuid}\"")
      raise UserDeletionException.new("ERROR: unable to create user account #{@uuid}") unless rc == 0
      notify_observers(:after_unix_user_destroy)
    end
    
    def add_ssh_key(key)
      self.class.notify_observers(:before_add_ssh_key, self, key)
      ssh_dir = File.join(@homedir, ".ssh")
      cloud_name = @config.get("cloud_name") || "CDK"
      authorized_keys_file = File.join(ssh_dir,"authorized_keys")
      shell    = @config.get("user_shell")     || "/bin/bash"      
      
      cmd_entry = "command=\"#{shell}\",no-port-forwarding,no-X11-forwarding ssh-rsa #{key} #{cloud_name}-#{@uuid}\n"
      FileUtils.mkdir_p ssh_dir
      FileUtils.chmod(0o0750,ssh_dir)
      File.open(authorized_keys_file, File::WRONLY|File::APPEND|File::CREAT, 0o0440) do |file|
        file.write(cmd_entry)
      end
      FileUtils.chmod 0o0440, authorized_keys_file
      FileUtils.chown_R("root",@uuid,ssh_dir)
      self.class.notify_observers(:after_add_ssh_key, self, key)
    end
    
    def remove_ssh_key(key)
      self.class.notify_observers(:before_remove_ssh_key, self, key)
      ssh_dir = File.join(@homedir, ".ssh")
      authorized_keys_file = File.join(ssh_dir,"authorized_keys")
      
      FileUtils.mkdir_p ssh_dir
      FileUtils.chmod(0o0750,ssh_dir)
      keys = []
      File.open(authorized_keys_file, File::RDONLY|File::CREAT, 0o0440) do |file|
        keys = file.readlines
      end
      
      keys.delete_if{ |k| k.include?(key)}
      
      File.open(authorized_keys_file, File::WRONLY|File::TRUNC|File::CREAT, 0o0440) do |file|
        file.write(keys.join("\n"))
      end
      
      FileUtils.chmod 0o0440, authorized_keys_file
      FileUtils.chown("root",@uuid,ssh_dir)
      self.class.notify_observers(:after_remove_ssh_key, self, key)
    end
    
    def add_env_var(key, value, prefix_cloud_name=false)
      env_dir = File.join(@homedir,".env")
      if prefix_cloud_name
        key = (@config.get("cloud_name") || "CDK") + "_#{key}"
      end
      File.open(File.join(env_dir, key),File::WRONLY|File::TRUNC|File::CREAT) do |file|
        file.write "export #{key}='#{value}'"
      end
    end
    
    def remove_env_var(key, prefix_cloud_name=false)
      env_dir = File.join(@homedir,".env")
      if prefix_cloud_name
        key = (@config.get("cloud_name") || "CDK") + "_#{key}"
      end
      FileUtils.rm_f File.join(env_dir, key)
    end
    
    def add_broker_auth(iv,token)
      broker_auth_dir=File.join(@homedir,".auth")
      FileUtils.mkdir_p broker_auth_dir
      File.open(File.join(broker_auth_dir,"iv"),File::WRONLY|File::TRUNC|File::CREAT) do |file|
        file.write iv
      end
      File.open(File.join(broker_auth_dir,"token"),File::WRONLY|File::TRUNC|File::CREAT) do |file|
        file.write token
      end
      
      FileUtils.chown_R("root",@uuid,broker_auth_dir)
      FileUtils.chmod(0o0750,broker_auth_dir)
      FileUtils.chmod(0o0640,Dir.glob("#{broker_auth_dir}/*"))
    end
    
    def remove_broker_auth
      broker_auth_dir=File.join(@homedir,".auth")
      FileUtils.rm_rf broker_auth_dir
    end

    def run_as(&block)
      old_gid = Process::GID.eid
      old_uid = Process::UID.eid
      fork{
        Process::GID.change_privilege(@gid.to_i)
        Process::UID.change_privilege(@uid.to_i)      
        yield block          
      }
      Process.wait  
    end
    
    private
    
    def initialize_homedir
      notify_observers(:before_initialize_homedir)
      
      tmp_dir = File.join(@homedir,".tmp")
      # Required for polyinstantiated tmp dirs to work
      FileUtils.mkdir_p tmp_dir
      FileUtils.chmod(0o0000,tmp_dir)
            
      env_dir = File.join(@homedir,".env")
      FileUtils.mkdir_p(env_dir)
      FileUtils.chmod(0o0750,env_dir)
      FileUtils.chown(nil,@uuid,env_dir)

      add_env_var("APP_UUID", @application_uuid, true)
      add_env_var("CONTAINER_UUID", @container_uuid, true)
      add_env_var("HOMEDIR", @homedir.end_with?('/') ? @homedir : @homedir + '/', true)
      notify_observers(:after_initialize_homedir)        
    end
    
    def next_uid
      uids = IO.readlines("/etc/passwd").map{ |line| line.split(":")[2].to_i }
      gids = IO.readlines("/etc/group").map{ |line| line.split(":")[2].to_i }
      min_uid = (@config.get("user_min_uid") || "500").to_i
      max_uid = (@config.get("user_max_uid") || "1500").to_i
      
      (min_uid..max_uid).each do |i|
        if !uids.include?(i) and !gids.include?(i)
          return i
        end
      end
    end
  end
end
