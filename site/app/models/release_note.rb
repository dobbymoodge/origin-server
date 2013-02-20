class ReleaseNote < CommunityApi::Base
  include RestApi::Cacheable
  allow_anonymous
  singleton

  self.prefix = '/releases/'

  schema do
    string :title, :summary, :href
  end

  def date
    @date ||= Time.at(attributes[:date].to_i)
  end

  cache_method :find_every, :expires_in => 10.minutes

  class << self
    def latest
      all(:from => "#{prefix}latest.json").first
    end
    def frontpage
      all(:from => "#{prefix}latest.json")
    end
  end
end
