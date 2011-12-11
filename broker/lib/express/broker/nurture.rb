module Express
  module Broker
  class Nurture
    def initialize()
    end

    #
    # Send application data (start, stop, etc)
    #
    def self.application(rhlogin, user_uuid, app_name, user_namespace, type, action, app_uuid)
        return unless (Libra.c[:nurture_enabled].to_s.downcase == 'true')
        Libra.logger_debug "DEBUG: Sending to Nurture:application: app_uuid='#{app_uuid}' action='#{action}'"
        # Why curl?  So I could & at the end.  We don't want this blocking requests
        # Please fix if you can :)  - mmcgrath
        `curl -s -O /dev/null -X POST -u '#{Libra.c[:nurture_username]}:#{Libra.c[:nurture_password]}' '#{Libra.c[:nurture_url]}applications' \
    --data-urlencode 'application[action]=#{action}' \
    --data-urlencode 'application[user_name]=#{rhlogin}' \
    --data-urlencode 'application[guid]=#{app_uuid}' \
    --data-urlencode 'application[uuid]=#{user_uuid}' \
    --data-urlencode 'application[name]=#{app_name}' \
    --data-urlencode 'application[version]=na' \
    --data-urlencode 'application[components]=#{type}' \
    --data-urlencode 'application[user_type]=express' &`
        Libra.logger_debug $?.exitstatus
    end
    
    #
    # Send application data (git push, etc)
    #
    def self.application_update(action, app_uuid)
        return unless (Libra.c[:nurture_enabled].to_s.downcase == 'true')
        Libra.logger_debug "DEBUG: Sending to Nurture:application_update: app_uuid='#{app_uuid}' action='#{action}'"
        # Why curl?  So I could & at the end.  We don't want this blocking requests
        # Please fix if you can :)  - mmcgrath
        `curl -s -O /dev/null -X POST -u '#{Libra.c[:nurture_username]}:#{Libra.c[:nurture_password]}' '#{Libra.c[:nurture_url]}applications' \
    --data-urlencode 'application[action]=#{action}' \
    --data-urlencode 'application[guid]=#{app_uuid}' \
    --data-urlencode 'application[version]=na' \
    --data-urlencode 'application[user_type]=express' &`
        Libra.logger_debug $?.exitstatus
    end
 
    #
    # Send account data (actual username)
    #
    def self.libra_contact(rhlogin, uuid, user_namespace, action)
        return unless (Libra.c[:nurture_enabled].to_s.downcase == 'true')
        Libra.logger_debug "DEBUG: Sending to Nurture:libra_contact: rhlogin='#{rhlogin}' namespace='#{user_namespace}' action='#{action}'"
        `curl -s -O /dev/null -X POST -u '#{Libra.c[:nurture_username]}:#{Libra.c[:nurture_password]}' '#{Libra.c[:nurture_url]}/libra_contact' \
     --data-urlencode "user_type=express" \
     --data-urlencode "user[uuid]=#{uuid}" \
     --data-urlencode "user[action]=#{action}" \
     --data-urlencode "user[user_name]=#{rhlogin}" \
     --data-urlencode "user[namespace]=#{user_namespace}" &`
    end
  end
end
