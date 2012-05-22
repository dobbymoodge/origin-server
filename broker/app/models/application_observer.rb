class ApplicationObserver < ActiveModel::Observer
  observe Application

  BUILDER_SUFFIX = "bldr"
  
  def track_gear_usage(data)
    gear = data[:gear]
    event = data[:event]
    time = data[:time]
    uuid = data[:uuid]
    usage = nil
    if event == UsageRecord::EVENTS[:begin]
      usage = Usage.new
      usage.construct(gear.app.user.login, gear.uuid, gear.node_profile, time, nil, uuid)
    elsif event == UsageRecord::EVENTS[:end]
      usage = Usage.find_latest_by_gear(gear.uuid)
      if usage
        usage.end_time = time
      end
    end
    usage.save! if usage
  end

  def before_application_create(data)
    application = data[:application]
    reply = data[:reply]

    if application.name =~ /.+#{BUILDER_SUFFIX}$/
      reply.messageIO << "
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
WARNING: The '#{BUILDER_SUFFIX}' suffix is used by the CI system (Jenkins) for its slave 
builders.  If you create an app of this name you can't also create an app 
called '#{application.name[0..-(BUILDER_SUFFIX.length+1)]}' and build that app in Jenkins without conflicts.
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
"
    end

    if application.framework_cartridge == 'jenkins'
      application.user.applications.each do |uapp|
        if uapp.framework_cartridge == "jenkins"
          raise StickShift::UserException.new("A jenkins application named '#{uapp.name}' in namespace '#{application.domain.namespace}' already exists.  You can only have 1 jenkins application per account.", 115)
        end

        if application.name == "#{uapp.name}#{BUILDER_SUFFIX}"
          reply.messageIO << "
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
WARNING: You already have an app created named '#{uapp.name}#{BUILDER_SUFFIX}'.  Be aware that
if you build '#{uapp.name}' using Jenkins it will destroy '#{uapp.name}#{BUILDER_SUFFIX}'.  This
may be ok if '#{uapp.name}#{BUILDER_SUFFIX}' was the builder of a previously destroyed app.
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
"
        end
      end
    end

    unless Application.find(application.user, application.name).nil?
      raise StickShift::UserException.new("An application named '#{application.name}' in namespace '#{application.domain.namespace}' already exists", 100)
    end

    if application.framework_cartridge == 'jenkins'
      application.user.applications.each do |app|
        if app.framework_cartridge == 'jenkins'
          raise StickShift::UserException.new("A jenkins application named '#{application.name}' in namespace '#{application.domain.namespace}' already exists. You can only have 1 jenkins application per account.", 115)
        end
      end
    end
    
    if application.user.auth_method == :login and application.user.vip == false and not (application.node_profile.nil? or ["small"].include?(application.node_profile))
      raise StickShift::UserException.new("Invalid Profile: #{application.node_profile}.  Must be: small", 1)
    end
  end
  
  def after_application_destroy(data)
    app = data[:application]
    reply = data[:reply]
    if app.framework_cartridge == "jenkins"
      app.user.applications.each do |uapp|
        begin
          reply.append uapp.remove_dependency('jenkins-client-1.4') if uapp.name != app.name and uapp.embedded and uapp.embedded.has_key?('jenkins-client-1.4')
        rescue Exception => e
          reply.debugIO << "Failed to remove jenkins client from application: #{uapp.name}\n"
        end
      end
    end
  end
end
