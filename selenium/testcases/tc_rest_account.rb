require 'openshift/selenium_test_case'

require 'openshift/rest/pages'
require 'openshift/rest/forms'
require 'openshift/rest/testcase'

class RestAccount < OpenShift::Rest::TestCase

  def setup
    super
  end

  def test_create_namespace_blank
    @login, pass = dummy_credentials
    signin(@login, pass)
    @rest_account.open
    form = @rest_account.domain_form
    assert !form.in_error?(:namespace)
    form.submit
    @rest_account.domain_page.wait
    assert form.in_error?(:namespace)
  end

  def test_create_namespace_invalid
    @login, pass = dummy_credentials
    signin(@login, pass)
    @rest_account.open
    form = @rest_account.domain_form
    assert !form.in_error?(:namespace)
    form.set_value(:namespace, "thisnamespaceisoverthemaxsizeallowed")
    form.submit
    @rest_account.domain_page.wait
    assert form.in_error?(:namespace)
  end

  def test_create_namespace_duplicate
    # create a namespace to try and duplicate
    @login, pass = dummy_credentials
    dup_namespace = @login.sub("test", "dup")
    create_namespace(@login, pass, dup_namespace)

    signout
    form = @rest_account.domain_form
    # log in a new user and try and use same namespace
    @login += "dup"
    signin(@login, pass)
    @rest_account.open
    form = @rest_account.domain_form
    assert !form.in_error?(:namespace)
    form.set_value(:namespace, dup_namespace)
    form.submit
    @rest_account.domain_page.wait
    assert form.in_error?(:namespace)

  end

  def test_edit_namespace_invaild
    # test both blank, duplicate and invalid namespace here
    form = @rest_account.domain_form

    # create a namespace to try and duplicate
    @login, pass = dummy_credentials
    dup_namespace = @login.sub("test", "dup")
    create_namespace(@login, pass, dup_namespace)
    signout

    # log in a new user and create a unique namespace
    # we sub to keep the domain name short
    @login = @login.sub("test", "") + "new"
    create_namespace(@login, pass, @login)

    # try to edit with blank namespace
    @rest_account.domain_edit_page.open
    assert_equal @login, form.get_value(:namespace)
    assert !form.in_error?(:namespace)
    form.set_value(:namespace, "")
    form.submit
    @rest_account.domain_page.wait
    assert form.in_error?(:namespace)

    # try to edit with an invalid namespace
    @rest_account.domain_edit_page.open
    assert_equal @login, form.get_value(:namespace)
    assert !form.in_error?(:namespace)
    form.set_value(:namespace, "thisnamespaceisoverthemaxsizeallowed")
    form.submit
    @rest_account.domain_page.wait
    assert form.in_error?(:namespace)

    # try to edit with a duplicate namespace
    @rest_account.domain_edit_page.open
    assert_equal @login, form.get_value(:namespace)
    assert !form.in_error?(:namespace)
    form.set_value(:namespace, dup_namespace)
    form.submit
    @rest_account.domain_page.wait
    assert form.in_error?(:namespace)
  end

  def test_create_namespace_valid
    @login, pass = dummy_credentials
    create_namespace(@login, pass, @login)
  end

  def test_update_namespace
    @login, pass = dummy_credentials
    create_namespace(@login, pass, @login)

    @rest_account.edit_namespace_button.click
    wait_for_page @rest_account.domain_edit_page.path

    form = @rest_account.domain_form

    new_namespace = @login + "a"

    form.set_value(:namespace, new_namespace)
    assert form.get_value(:namespace) != @login

    form.submit

    wait_for_page @rest_account.path
    await("namespace updated on page") { text('.namespace') == new_namespace }
  end

  def test_ssh_key_add_default
    @login, pass = dummy_credentials

    signin(@login, pass)
    @rest_account.open

    create_namespace(@login, pass, @login, false)

    # go back to the account page
    @rest_account.open

    # create a default SSH key
    form = @rest_account.ssh_key_form

    key = dummy_ssh_key
    form.set_value(:key, key)
    form.submit

    await('preview SSH key') { @rest_account.find_ssh_key_row('default') }
    # we shorten key so split and check via regex
    cmp_key = @rest_account.find_ssh_key('default')
    cmp_key = cmp_key.split('..')
    if cmp_key.length > 1:
      key_re = "(#{Regexp.quote(cmp_key[0])}).*(#{Regexp.quote(cmp_key[1])})$"
      assert_match /#{key_re}/, key
    else
      assert_equal key, cmp_key[0]
    end
  end

  def test_ssh_key_add_more_than_one
    @login, pass = dummy_credentials

    signin(@login, pass)
    @rest_account.open

    create_namespace(@login, pass, @login, false)

    # go back to the account page
    @rest_account.open

    # create a default SSH key
    form = @rest_account.ssh_key_form

    key = dummy_ssh_key
    form.set_value(:key, key)
    form.submit

    await('preview SSH key') { @rest_account.find_ssh_key_row('default') }
    # we shorten key so split and check via regex
    cmp_key = @rest_account.find_ssh_key('default')
    cmp_key = cmp_key.split('..')
    if cmp_key.length > 1:
      key_re = "(#{Regexp.quote(cmp_key[0])}).*(#{Regexp.quote(cmp_key[1])})$"
      assert_match /#{key_re}/, key
    else
      assert_equal key, cmp_key[0]
    end

    ['CCCC', 'DDDD', 'EEEE'].each do |name|
      key = dummy_ssh_key2(name)
      @rest_account.ssh_key_add_button.click
      @rest_account.ssh_key_add_page.wait
      form.set_value(:name, name)
      form.set_value(:key, key)
      form.submit

      await('preview SSH key') { @rest_account.find_ssh_key_row(name) }
      # we shorten key so split and check via regex
      cmp_key = @rest_account.find_ssh_key(name)
      cmp_key = cmp_key.split('..')
      if cmp_key.length > 1:
        key_re = "(#{Regexp.quote(cmp_key[0])}).*(#{Regexp.quote(cmp_key[1])})$"
        assert_match /#{key_re}/, key
      else
        assert_equal key, cmp_key[0]
      end
    end
  end

  def test_ssh_key_add_invalid
    @login, pass = dummy_credentials

    signin(@login, pass)
    @rest_account.open

    create_namespace(@login, pass, @login, false)

    # go back to the account page
    @rest_account.open

    # create a default SSH key
    form = @rest_account.ssh_key_form

    key = dummy_ssh_key
    form.set_value(:key, key)
    form.submit

    await('preview SSH key') { @rest_account.find_ssh_key_row('default') }

    # add a duplicate key with a different name
    @rest_account.ssh_key_add_button.click
    @rest_account.ssh_key_add_page.wait

    assert !form.in_error?(:name)
    assert !form.in_error?(:key)

    form.set_value(:name, 'new')
    form.set_value(:key, key)
    form.submit

    @rest_account.ssh_key_page.wait
    assert !form.in_error?(:name)
    assert form.in_error?(:key)

    form.cancel

    # add a duplicate key name with a different key
    key = dummy_ssh_key2
    @rest_account.ssh_key_add_button.click
    @rest_account.ssh_key_add_page.wait

    assert !form.in_error?(:name)
    assert !form.in_error?(:key)

    form.set_value(:name, 'default')
    form.set_value(:key, key)
    form.submit

    @rest_account.ssh_key_page.wait
    assert form.in_error?(:name)
    assert !form.in_error?(:key)

    form.cancel

    # make both form and key blank
    @rest_account.ssh_key_add_button.click
    @rest_account.ssh_key_add_page.wait

    assert !form.in_error?(:name)
    assert !form.in_error?(:key)

    form.submit

    @rest_account.ssh_key_page.wait
    assert form.in_error?(:name)
    assert form.in_error?(:key)

    form.cancel
  end
end
