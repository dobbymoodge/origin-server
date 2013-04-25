module Aria
  class ContactInfo < Base
    @@attribute_names = 'first_name', 'middle_initial', 'last_name', 'address1', 'address2', 'city', 'region', 'country', 'zip'

    @@region_key_map = Hash.new('locality').merge({ 'US' => 'state_prov', 'CA' => 'state_prov' })

    attr_aria *@@attribute_names.map(&:to_sym)

    # Don't do validation of presence of attributes
    # 1) We create from billing_info, which will do the validation
    # or
    # 2) We create from streamline, and can't edit anything anyway

    # Do validate the country is allowed, if provided
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
      aria[@@region_key_map[country]] = aria.delete('region')
      aria['mi'] = aria.delete('middle_initial')
      aria.delete_if {|k,v| v.nil? }
    end
  end
end
