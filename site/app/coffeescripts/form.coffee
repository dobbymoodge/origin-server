$ = jQuery

find_control_group_parent =
  (child) ->
    parent = $(child).parentsUntil(".control-group").parent().closest(".control-group")
    return parent

$ ->

  # Show/hide loading icons when form buttons are clicked
  loading_match = '*[data-loading=true]'
  ($ 'form '+loading_match).each ->
    ($ window).bind 'pagehide', ->
      ($ loading_match, body).hide()
      ($ 'input[type=submit][disabled]').removeAttr('disabled')
    ($ this).closest('form').bind 'submit', ->
      if ($ 'input.error').length == 0
        ($ loading_match, this).show()
        ($ 'input[type=submit]', this).attr('disabled','disabled')
        true

  $.validator.addMethod "aws_account", ((value) ->
    (/^[\d]{4}-[\d]{4}-[\d]{4}$/).test value
  ), "Account numbers should be a 12-digit number separated by dashes. Ex: 1234-5678-9000"

  $.validator.addMethod "alpha_numeric", ((value) ->
    (/^[A-Za-z0-9]*$/).test value
  ), "Only letters and numbers are allowed"

  $.validator.setDefaults
    errorClass:   'help-inline'
    errorElement: 'p'
    highlight: (element,errorClass,validClass) ->
      $(find_control_group_parent(element)).addClass('error').removeClass(validClass)
    unhighlight: (element,errorClass,validClass) ->
      $el = $(find_control_group_parent(element))
      if typeof($el.attr('data-server-error')) == 'undefined'
        $el.removeClass('error')

  # /app/account/new
  # /app/account
  $('#new-user form').validate
    rules:
      # Require email for new users
      "web_user[email_address]":
        required:   true
        email:      true
      # Require old password for password change
      "web_user[old_password]" :
        required:   true
      "web_user[password]":
        required:   true
        minlength:  6
      "web_user[password_confirmation]":
        required:   true
        equalTo:    "#web_user_password"

  # /app/login 
  $('#login-form form').validate
    rules:
      "web_user[rhlogin]":
        required: true
      "web_user[password]":
        required: true

  # /app/user/request_password_reset_form
  $('#password-reset-form form').validate
    rules:
      "email":
        required: true
        email: true

 # Validate application name
  $.validator.addClassRules
    domain_name:
      required: true
      alpha_numeric: true
    application_name:
      required: true
      alpha_numeric: true

  # /app/account
  # /app/account/domain/edit
  $("#new_domain form").validate
    errorLabelContainer: '#app-errors'
    errorContainer: '#app-errors'

  $("[data-unhide]").click (event) ->
    src = $(this)
    tgt = $(src.attr('data-unhide'))
    if (tgt)
      event.preventDefault() if event?
      src.closest('[data-hide-parent]').addClass('hidden')
      $('input',tgt.removeClass('hidden')).focus()

