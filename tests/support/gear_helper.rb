#require '/var/www/openshift/broker/config/environment'

module GearHelper
  def change_max_gears_for_user(name, ngears=20)
    run "oo-admin-ctl-user -l #{name} --setmaxgears #{ngears}"
    #u = CloudUser.find(name)
    #u.max_gears = ngears
    #u.save
  end

end

World(GearHelper)
