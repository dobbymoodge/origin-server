Rails.application.config.tap do |config|
  # Aria API information
  config.aria_enabled = Console.config.env(:ARIA_ENABLED, true)
  config.aria_uri = Console.config.env(:ARIA_URI, "https://streamline-proxy1.ops.rhcloud.com/api/ws/api_ws_class_dispatcher.php")
  config.aria_auth_key = Console.config.env(:ARIA_AUTH_KEY, "sRvjFqjSadu3AFB8jRAR3tqeH5Qf6XjW")
  config.aria_client_no = Console.config.env(:ARIA_CLIENT_NO, 3754655)
  config.aria_default_plan_no = Console.config.env(:ARIA_DEFAULT_PLAN_NO, 10330329)
  config.aria_force_test_users = Console.config.env(:ARIA_FORCE_TEST_USERS, !Rails.env.production?)
  config.aria_max_parallel_requests = 5
  # Aria direct post configuration - uses public URL
  # Requires rake aria:set_direct_post be called once per Aria system tested against
  config.aria_direct_post_uri = Console.config.env(:ARIA_DIRECT_POST_URI, "https://secure.current.stage.ariasystems.net/api/direct_post.php")
  config.aria_direct_post_name = Console.config.env(:ARIA_DIRECT_POST_NAME, Rails.env.production? ? 'website_new_payment' : nil)
  config.aria_direct_post_redirect_base = Console.config.env(:ARIA_DIRECT_POST_REDIRECT_BASE, Rails.env.production? ? 'https://openshift.redhat.com/app' : nil)

  # Aria invoice template ID map
  # These IDs are generated by Aria to refer to specific invoice templates.
  # These IDs should not change unless Aria changes the templates.
  # NOTE: For now, this simply maps everything to 'Red Hat HTML Statement'
  config.aria_invoice_template_id_map = 
    HashWithIndifferentAccess.new(
      Console.config.env(:ARIA_DEFAULT_INVOICE_TEMPLATE, '37546552')
    ).merge!(
      Console.config.env(:ARIA_INVOICE_TEMPLATE_MAP, { 'US' => '37546551', 'CA' => '37546553' })
    )

  # Supported Currency
  # Specify allowed currencies here, use ISO4217 format
  config.allowed_currencies = [:usd, :cad, :eur]
  config.default_currency = :usd

  # Supported Countries
  # Add a corresponding value in config/countries.yml if the country uses something other than:
  #  - 'State' for the locality
  #  - 'Postcode' for the postal code
  config.allowed_countries = Console.config.env(:ARIA_ALLOWED_COUNTRIES, [:AT, :BE, :CA, :CH, :DE, :DK, :ES, :FI, :FR, :GB, :IE, :IS, :IT, :LU, :NL, :NO, :PT, :SE, :US])
  config.preferred_countries = [:US]
  config.currency_cd_by_country = HashWithIndifferentAccess.new('eur').merge!({ 'US' => 'usd', 'CA' => 'cad' })
  config.collections_group_id_by_country =
    HashWithIndifferentAccess.new(
         Console.config.env(:ARIA_DEFAULT_COLLECTIONS_GROUP_ID, '3')
    ).merge!(
         Console.config.env(:ARIA_COLLECTIONS_GROUP_ID_MAP, { 'US' => '1', 'CA' => '2' })
    )
  config.functional_group_no_by_country =
    HashWithIndifferentAccess.new(
         Console.config.env(:ARIA_DEFAULT_FUNCTIONAL_GROUP_NO, '10018442')
    ).merge!(
         Console.config.env(:ARIA_FUNCTIONAL_GROUP_NO_MAP, { 'US' => '10018440', 'CA' => '10018441' })
    )

  # Supported Credit Cards
  # Specify accepted cards here. Keys can be found in config/credit_cards.yml
  config.accepted_cards = Console.config.env(:ARIA_ACCEPTED_CARDS, [:visa,:mastercard])
  # Disable extended credit card validation rules
  config.disable_cc_validation = Console.config.env(:ARIA_DISABLE_CC_VALIDATION, false)
  # Disable JS based address form updates
  #config.disable_dynamic_country_form = true

  # Account Support contact
  config.acct_help_mail_to = Console.config.env(:ACCOUNT_HELP_MAIL_ADDRESS, 'customerservice@redhat.com')
end

Aria::LogSubscriber.attach_to :aria
