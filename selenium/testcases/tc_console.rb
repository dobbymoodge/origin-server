#!/usr/bin/env ruby
class ExpressConsole < OpenShift::SeleniumTestCase

  def setup
    super
  end

  def test_create_namespace_blank
    @login, pass = dummy_credentials
    signin(@login, pass)

    @express_console.open

    form = @express_console.domain_form

    form.expand
    await("form expanded") { !form.collapsed? }

    assert !form.in_error?(:namespace)

    form.submit

    assert form.in_error?(:namespace)
    assert_equal_no_case "This field is required.", form.error_message(:namespace)
  end

  def test_create_namespace_invalid
    @login, pass = dummy_credentials
    signin(@login, pass)

    @express_console.open

    form = @express_console.domain_form

    form.expand
    await("form expanded") { !form.collapsed? }

    assert !form.in_error?(:namespace)

    form.set_value(:namespace, "non-alphanumeric!")

    form.submit

    assert form.in_error?(:namespace)
    assert_equal_no_case "Only letters and numbers are allowed", form.error_message(:namespace)
  end

  def test_create_namespace_valid
    @login, pass = dummy_credentials
    create_namespace(@login, pass, @login)
  end

  def test_update_namespace
    @login, pass = dummy_credentials
    create_namespace(@login, pass, @login)

    # leave and come back
    @express.open
    @express_console.open

    form = @express_console.domain_form
    assert form.collapsed?

    form.expand
    await("form expanded") { !form.collapsed? }

    new_namespace = @login + "a"

    form.set_value(:namespace, new_namespace)
    assert form.get_value(:namespace) != @login

    form.submit

    await("form collapsed", 30) { form.collapsed? }

    await("namespace updated on page") { new_namespace == form.get_collapsed_value(:namespace) }
  end

  def test_app_create_validation
    @login, pass = dummy_credentials
    create_namespace(@login, pass, @login)

    jump_to "apps"

    form = @express_console.app_form

    assert !form.in_error?(:app_name)
    assert !form.in_error?(:cartridge)

    # try with no input

    form.submit
    wait_for_ajax

    assert form.in_error?(:app_name)
    assert form.in_error?(:cartridge)

    assert_equal_no_case "This field is required.", form.error_message(:app_name)
    assert_equal_no_case "This field is required.", form.error_message(:cartridge)

    # try to use non-alphanumeric app name

    form.set_value(:app_name, "Non-alphanumeric")

    assert form.in_error?(:app_name)
    assert_equal_no_case "Only letters and numbers are allowed", form.error_message(:app_name)

    # try to use app name that exceeds max length (32)

    app_name = "abcdefghijklmnopqrstuvwxyz0123456789"

    form.set_value(:app_name, app_name)

    assert !form.in_error?(:app_name)

    assert_equal app_name[0..31], form.get_value(:app_name)

  end

  def test_app_create
    @login, pass = dummy_credentials
    create_namespace(@login, pass, @login)

    form = @express_console.app_form

    jump_to "apps"

    n = 5
    for i in 1.upto(n) do
      type = get_option_value(form.fields[:cartridge], i)
      create_app(@login, pass, "app#{i}", type)
    end

    # TODO assert cannot create more
  end

  def get_option_value(select_id, preferred_index)
    select = driver.find_elements(:xpath => "//select[@id='#{select_id}']")[0]
    options = select.find_elements(:css => "option")

    i = preferred_index % options.length
    options[i].attribute "value"
  end

  def jump_to(id)
    exec_js "jQuery('html,body').scrollTop(jQuery('##{id}').offset().top - 50)"
  end

  # helper method for creating an app
  # pre: user is signed in already
  # post: user is on express console page
  def create_app(login, password, app_name, type)
    form = @express_console.app_form

    assert !form.in_error?(:app_name)
    assert !form.in_error?(:cartridge)

    form.set_value(:app_name, app_name)
    form.set_value(:cartridge, type)

    jump_to "apps"

    form.submit

    wait_for_ajax 30

    # presence of deletion form indicates successful creation
    await("#{type} app created") { exists? "form##{app_name}_delete_form" }
  end

  # helper method for creating a namespace
  # post: user is on express console page
  def create_namespace(login, password, namespace)
    signin(login, password)

    @express_console.open

    form = @express_console.domain_form

    form.expand
    await("form expanded") { !form.collapsed? }

    assert !form.in_error?(:namespace)

    form.set_value(:namespace, namespace)

    form.submit

    wait_for_ajax 30

    await("namespace created") { namespace == form.get_collapsed_value(:namespace) }
  end

  def dummy_credentials
    return ["test#{data[:uid]}", data[:password]]
  end
end
