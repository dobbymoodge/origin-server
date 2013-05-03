module Aria
  class ContactInfo < Base
    @@attribute_names = 'first_name', 'middle_initial', 'last_name', 'address1', 'address2', 'city', 'region', 'country', 'zip', 'email'

    @@region_key_map = Hash.new('locality').merge({ 'US' => 'state_prov', 'CA' => 'state_prov' })

    attr_aria *@@attribute_names.map(&:to_sym)

    # Aria makes us explicitly unset values on update
    @@nullable = [:middle_initial, :address2]

    @@region_save_map = Hash.new(['locality','state_prov']).merge({
      'US' => ['state_prov','locality'],
      'CA' => ['state_prov','locality'],
    })
    @@region_load_map ||= Hash.new('locality').merge({
      'US' => 'state_prov',
      'CA' => 'state_prov',
    })

    # Don't do validation of presence of attributes
    # 1) We create from billing_info, which will do the validation
    # or
    # 2) We create from streamline, and can't edit anything anyway

    # Do validate the country is allowed
    validates_inclusion_of :country, :in => Rails.configuration.allowed_countries.map(&:to_s), :message => "Unsupported country #{:country}"

    account_prefix :from => '',
                   :to => '',
                   :rename_to_save => {
                     'middle_initial' => 'mi',
                   },
                   :rename_to_load => {
                     'alt_email' => 'email',
                     'mi' => 'middle_initial',
                   },
                   :no_rename_to_update => ['middle_initial'],
                   :no_prefix => []

    class << self
      def rename_to_save(hash, action='save')
        super(hash, action)

        (region_set_key, region_clear_key) = @@region_save_map[hash['country']]
        hash[region_set_key] = hash.delete('region')
        hash[region_clear_key] = '~' if action == 'update'

        # Explicitly nil empty string fields within Aria
        @@nullable.each {|n| hash[n.to_s] = "~" if hash[n.to_s] == "" } if action == 'update'
      end

      def rename_to_load(hash)
        super(hash)
        hash['region'] = hash.delete(@@region_load_map[hash['country']])
      end

      def from_billing_info(billing_info)
        new(billing_info.attributes.slice(*@@attribute_names))
      end

      def from_full_user(full_user)
        attributes = full_user.attributes.slice(*@@attribute_names)
        attributes['region'] = full_user.state
        attributes['zip'] = full_user.postal_code
        attributes['email'] = begin
          full_user.email_address || full_user.load_email_address
        rescue
        end
        new(attributes)
      end
    end

    protected
      # A user without a country is invalid
      def self.persisted?(details)
        details.country.present?
      end
  end
end
