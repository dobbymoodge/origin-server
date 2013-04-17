module Aria
  class ContactInfo < Base
    @@attribute_names = 'address1', 'address2', 'city', 'region', 'country', 'zip'
    @@region_key_map = Hash.new('locality').merge({ 'US' => 'state_prov', 'CA' => 'state_prov' })

    attr_aria *@@attribute_names.map(&:to_sym)

    # :country -should- be required. For the time being, this rule is relaxed
    # due to a known streamline bug that would affect Commercialization UAT
    validates_presence_of :address1, :city, :region, :zip
    validates_inclusion_of :country, :in => Rails.configuration.allowed_countries.map(&:to_s), :message => "Unsupported country #{:country}", :allow_blank => true

    class << self
      def from_billing_info(billing_info)
        new(billing_info.attributes.slice(*@@attribute_names))
      end

      def from_full_user(full_user)
        attributes = full_user.attributes.slice(*@@attribute_names)
        attributes['region'] = full_user.state
        attributes['zip'] = full_user.postal_code
        new(attributes)
      end
    end

    def to_aria_attributes
      aria = @attributes.clone
      aria[@@region_key_map[country]] = region
      aria.delete('region')
      aria.delete_if {|k,v| v.nil? }
    end
  end
end
