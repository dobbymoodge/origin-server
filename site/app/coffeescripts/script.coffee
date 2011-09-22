# Compile with --bare flag #
$ = jQuery

$ ->

## Scroll effects ##
  # nav sticks to top when scrolling off page #
  # parallax effect on scroll (undone for now) #
  body = $ 'body'
  nav = ($ 'header.universal > nav').first()
  nav_top = nav.offset().top
  #sm_pos = md_pos = lg_pos = 0
  top = ($ window).scrollTop()
    
  sticky_css =
    position: 'fixed'
    top: 0
    'z-index': 2000
    width: '100%'
  unsticky_css =
    position: 'static'

  ($ window).scroll ->
    # parallax effect #
    #top_diff = ($ this).scrollTop() - top
    top = ($ this).scrollTop()
    
    #sm_pos -= top_diff
    #md_pos -= Math.round top_diff*0.5
    #lg_pos -= Math.round top_diff*0.25
    
    #body.css 'background-position', "-150px #{sm_pos}px, -150px #{md_pos}px, -150px #{lg_pos}px"
    
    # sticky nav #
    # check if nav is supposed to be off the page
    if top > nav_top
      nav.css sticky_css
    else
      nav.css unsticky_css
      
## Dialogs ##
  dialogs = $ '.dialog'

  open_dialog = (dialog) -> 
    # Close any other open dialogs
    dialogs.hide()
    # Show given dialog
    dialog.show()
    # scroll to top
    ($ window, 'html', 'body').scrollTop 0

  close_dialog = (dialog) ->
    dialog.hide()
    
  # Close buttons
  close_btn = $ '.close_button' 
  # Sign up dialog
  signup = $ '#signup'
  # Sign in dialog
  signin = $ '#signin'
  # Password reset dialog
  reset  = $ '#reset_password'

  ($ 'a.sign_up').click (event) ->
    event.preventDefault()
    open_dialog signup

  ($ 'a.sign_in').click (event) ->
    event.preventDefault()
    open_dialog signin

  ($ 'a.password_reset').click (event) ->
    event.preventDefault()
    open_dialog reset
    
  close_btn.click (event) ->
    close_dialog ($ this).parent()

  # Function based on definitions in rails.js:
  login_complete = (xhr,status) ->
    json = $.parseJSON( status.responseText )
    console.log json
    # Clear out error messages
    $(this).parent().find('div.message.error').remove()
    $err_div = $('<div>').addClass('message error').hide().insertBefore(this)

    switch status.status
        when 200 #everything ok
          window.location.replace json.redirectUrl
          break
        when 401 #Unauthorized
          $err_div.text(json.error).show()
          break
        else
          $err_div.html(json.error || "Some unknown error occured,<br/> please try again.").show()
          console.log 'Some unknown AJAX error with the login', status.status

  # Bind to both the JS form and the standard form
  signin.find('form').bind('ajax:complete', login_complete )
  ($ '#login-form').find('form').bind('ajax:complete', login_complete ) 

  registration_complete = (xhr,status) ->
    form = $(this)
    json = $.parseJSON( status.responseText )
    console.log "Reg complete, got JSON", json

    # Clear out error messages
    $(this).parent().find('div.message.error').remove()
    $err_div = $('<div>').addClass('message error').hide().insertBefore(this)

    # Save all errors
    messages = $.map(json, (k,v) -> return k)

    if( json['redirectUrl'] == undefined || json['redirectUrl'] == null )

      $.each(messages, (i,val)->
        $err_div.addClass('error').append($('<div>').html(val))
      )
      $err_div.show()

      if typeof Recaptcha != 'undefined'
        Recaptcha.reload()
    else
      window.location.replace json['redirectUrl']

  signup.find('form').bind('ajax:complete', registration_complete)
  ($ '#new_web_user').bind('ajax:complete', registration_complete)

## Announcements ##
  announcements = ($ '#announcements')
  ann_list = ($ 'ul', announcements)
  on_announcement = 0
  if ($ 'li', ann_list).length > 1
    ann_list.css 'position', 'relative'
    ann_height = ($ 'li', announcements).first().height()
    
    scroll_announcements = ->
      on_announcement++
      if on_announcement >= ($ 'li', ann_list).length
        on_announcement = 0
        ann_list.css 'top', 0
      else
        ann_list.css 'top', -1 * ann_height * on_announcement
    
    setInterval scroll_announcements, 10000

## Product page ##
  if body.hasClass 'product'
    links = $ '.content nav a[href^=#]'
    sections = $ '.content section'
    
    # get current section
    if location.hash
      current = location.hash
    else
      current = '#' + sections.first().attr('id')
    
    # hide sections
    sections.hide()
    links.removeClass 'active'
    # show current section 
    ($ current).show()
    ($ "a[href=#{current}]").addClass 'active'
    
    # hide toc in doc iframe
    # document.domain = 'redhat.com'
    # frame = ($ ($ '#docs').find('iframe')[0].contentDocument)
    # toc = $ '#tocdiv', frame
    # console.log('frame', frame)
    # console.log('toc', toc)
    
    # change sections based on clicked link
    links.click (event) ->
      event.preventDefault()
      
      target = ($ this).attr('href')
      
      # prevent annoying flash for better browsers
      if history.pushState
        history.pushState null, null, target
      else
        location.hash = target
      
      sections.hide()
      ($ target).show()
      
      #change link class
      links.removeClass 'active'
      ($ this).addClass 'active'
    
## Omniture click tracking ##
  ($ 'a.sign_up').click (event) -> 
    if body.hasClass 'express'
      product = 'Express'
    else if body.hasClass 'flex'
      product = 'Flex'
    else if body.hasClass 'home'
      product = 'Home'
    else
      product = 'Other'
    
    trackLink this, product






