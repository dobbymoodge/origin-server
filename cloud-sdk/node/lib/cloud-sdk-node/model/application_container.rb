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
require 'cloud-sdk-node/model/unix_user'
require 'cloud-sdk-common'

module Cloud::Sdk
  # == Application Container
  class ApplicationContainer < Model
    attr_reader :uuid, :application_uuid, :user
    
    def initialize(application_uuid, container_uuid, user_uid=nil, app_name=nil, quota_blocks=nil, quota_files=nil)
      @uuid = container_uuid
      @application_uuid = application_uuid
      @user = UnixUser.new(application_uuid, container_uuid, user_uid, quota_blocks, quota_files)
    end
    
    def name
      @uuid
    end
    
    def create
      notify_observers(:before_container_create)
      @user.create
      notify_observers(:after_container_create)
    end
    
    def destroy
      notify_observers(:before_container_destroy)
      @user.destroy
      notify_observers(:after_container_destroy)      
    end
  end
end
