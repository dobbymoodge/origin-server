class CloudUserObserver < ActiveModel::Observer
  observe CloudUser

  def before_cloud_user_create(user)
    raise OpenShift::UserException.new("Invalid characters in login '#{user.login}' found", 107) if user.login =~ /["\$\^<>\|%\/;:,\\\*=~]/
  end

  def cloud_user_create_success(user)
    # Notify nurture
    Online::Broker::Nurture.libra_contact(user.login, user._id, nil, 'create')
    # If any of the above fail, it will result in the user being deleted
  end

  def cloud_user_create_error(user)
  end

  def after_cloud_user_create(user)
  end

end
