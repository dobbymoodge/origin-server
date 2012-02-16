#
# The REST API model object representing an application instance.
#
class Application < RestApi::Base
  schema do
    string :name, :creation_time
    string :uuid, :domain_id
    string :cartridge, :server_identity
  end

  custom_id :name
  # TODO: Bug 789752: Rename server attribute to domain_name and replace domain_id with domain_name everywhere
  alias_attribute :domain_name, :domain_id

  has_many :aliases
  belongs_to :domain
  self.prefix = "#{RestApi::Base.site.path}/domains/:domain_name/"

  def domain_id=(id)
    self.prefix_options[:domain_name] = id
    super
  end

  def domain
    Domain.find domain_name, :as => as
  end
  def domain=(domain)
    self.domain_id = domain.is_a?(String) ? domain : domain.namespace
  end

  def web_url
    'http://' << url_authority
  end
  def git_url
    "ssh://#{uuid}@#{url_authority}/~/git/#{name}.git/"
  end

  def framework_name
    ApplicationType.find(framework).name rescue framework
  end
  
  def application_type
    ApplicationType.find(framework)
  end

  protected
    def url_authority
      "#{name}-#{domain_name}.#{Rails.configuration.base_domain}"
    end
end
