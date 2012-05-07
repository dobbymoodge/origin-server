class DomainObserver < ActiveModel::Observer
  observe Domain
  def after_domain_create(domain)
    Rails.logger.debug "In after domain create"
    send_data_to_analytics(domain)
  end

  def after_domain_update(domain)
    Rails.logger.debug "In after domain update"
    send_data_to_analytics(domain)
  end

  def after_domain_destroy(domain)
    Rails.logger.debug "In after domain destroy"
    send_data_to_analytics(domain)
  end

  def send_data_to_analytics(domain)
    begin
      Rails.logger.debug "Sending updated domain info #{domain.namespace} to apptegic and nurture"
      Express::Broker::Nurture.libra_contact(domain.user.login, domain.user.uuid, domain.namespace, 'update')
      Express::Broker::Apptegic.libra_contact(domain.user.login, domain.user.uuid, domain.namespace, 'update')
    rescue Exception => e
      Rail.logger.error e.message
    end
  end
end
