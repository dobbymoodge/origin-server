require File.expand_path('../../test_helper', __FILE__)

class WebFlowsTest < ActionDispatch::IntegrationTest
  web_integration

  test 'login to console' do
    with_unique_user
    visit_console_login

    assert has_content? /Management Console/i

    find('header .nav', :visible => true).click_link 'My Account'

    assert find('.nav > li.active').has_content? 'My Account'
    assert has_content? 'Free Plan'
  end

  test 'logout from console' do
    with_unique_user
    visit_console_login

    assert link = find('#utility-nav a', :text => 'Sign Out', :visible => false)

    assert find('#utility-nav a.dropdown-toggle').click
    assert link.visible?
    assert find('#utility-nav').click_link 'Sign Out'

    visit console_path
    assert_equal login_path, URI(page.current_url).path
  end

  test 'tag dropdown on application types page' do
    with_logged_in_console_user
    
    visit application_types_path

    assert has_css?('.tile h3', :text => /Ruby 1\.(\d)/)
    assert find('.tile h3', :text => /Drupal/)
    assert find('.nav > li.active').has_content? 'Create Application'
    assert page.has_content? /Create an application/i

    assert find('a.dropdown-toggle', :text => /Browse by tag/).click
    assert find('#tag-filter a', :text => /PHP/).click

    assert find('h3', :text => /Tagged with php/)
    assert has_css?('.tile h3', :text => /Drupal/)    
  end

  test 'help page displays' do
    with_logged_in_console_user

    visit console_help_path
    assert has_css? 'h2', :text => /Create/
  end

  test 'jquery form validation triggers on submit' do
    visit login_path

    # Selectors
    username       = "#web_user_rhlogin"
    password       = "#web_user_password"
    username_error = "#web_user_rhlogin_input.error-client #web_user_rhlogin.error"
    password_error = "#web_user_password_input.error-client #web_user_password.error"

    # Fields
    assert has_css?(username), "Missing username field"
    assert has_css?(password), "Missing password field"
    submit = find("input[type=submit]")

    # Initial setup
    assert has_no_css?(username_error), "Username field should not have errors on page load"
    assert has_no_css?(password_error), "Password field should not have errors on page load"

    # Initial invalidation
    submit.click
    assert has_css?(username_error), "Empty username field should have errors after submitting"
    assert has_css?(password_error), "Empty password field should have errors after submitting"

    # Avoid revalidating
    page.execute_script("$('#web_user_rhlogin').val('a')")
    assert has_css?(username_error), "validate should not trigger on value change"
    page.execute_script("$('#web_user_rhlogin').trigger('keypress').trigger('keyup')")
    assert has_css?(username_error), "validate should not trigger on keyup"
    page.execute_script("$('#web_user_rhlogin').focus()")
    assert has_css?(username_error), "validate should not trigger on focus"
    page.execute_script("$('#web_user_rhlogin').blur()")
    assert has_css?(username_error), "validate should not trigger on blur"
    page.execute_script("$('#web_user_rhlogin').click()")
    assert has_css?(username_error), "validate should not trigger on click"

    # Revalidate
    submit.click
    assert has_no_css?(username_error), "revalidate should trigger on submit"
    assert has_css?(password_error), "revalidate should not clear error messages for invalid fields"
  end

end
