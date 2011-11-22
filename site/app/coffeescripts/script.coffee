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

  stuck = false

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
    should_stick = top > nav_top

    if should_stick and !stuck
      nav.css sticky_css
      ($ 'body > section:first').css 'marginTop', nav.height() + 'px'
      stuck = true
    else if stuck and !should_stick
      nav.css unsticky_css
      ($ 'body > section:first').css 'marginTop', 0
      stuck = false
      
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
    if trackLink?
      if body.hasClass 'express'
        product = 'Express'
      else if body.hasClass 'flex'
        product = 'Flex'
      else if body.hasClass 'home'
        product = 'Home'
      else
        product = 'Other'
      
      trackLink this, product

## Outage Notification ##
  outage_notification = $ '#outage_notification'
  if outage_notification.length > 0
    show_outage_txt = '☟ Service Outages'
    hide_outage_txt = '☝ Hide'
    outage_notification_neg_height = '-' + outage_notification.outerHeight() + 'px'
    outage_animation_length = 1000

    # Initial css changes
    outage_notification.css {
      position: 'absolute'
      top: outage_notification_neg_height
      left: 0
      zIndex: 1000
    }

    # Add overlay
    ($ 'body').append '<div id="overlay"></div>'
    overlay = $ '#overlay'
    overlay.hide()

    # Add toggle
    outage_notification.append '<a href="#" id="outage_toggle">' + show_outage_txt + '</a>'
    outage_toggle = $ '#outage_toggle'
    outage_toggle_state = 'hidden'

    show_notification = () ->
      # Slide down notification
      outage_notification.css 'z-index', 2000
      outage_notification.stop()
      outage_notification.animate {top: 0}, outage_animation_length

      # Fade in Overlay
      overlay.show()

      # Change toggle text
      outage_toggle.text hide_outage_txt
      outage_toggle_state = 'shown'

    hide_notification = () ->
      # Slide up notification
      outage_notification.css 'z-index', 1000
      outage_notification.stop()
      outage_notification.animate {top: outage_notification_neg_height}, outage_animation_length

      # Scroll back to top of page
      containers = ($ 'html, body, document')
      containers.stop()
      containers.animate {scrollTop: 0}, outage_animation_length

      # Fade out overlay
      overlay.hide()

      # Change toggle text
      outage_toggle.text show_outage_txt
      outage_toggle_state = 'hidden'

    # Toggle bindings
    outage_toggle.click (event) ->
      event.preventDefault()
      if outage_toggle_state == 'hidden'
        show_notification()
      else
        hide_notification()

    # Check if notification has already been displayed
    if 'true' != ($.cookie 'outage_notification_displayed')
      # Display notification in an initially intrusive way so it can't be missed!
      show_notification()

      # Set cookie
      $.cookie 'outage_notification_displayed', 'true', {'expires': 14, 'path': '/app'}
  else
    # Clear cookie if it exists
    $.cookie 'outage_notification_displayed', null, {'path': '/app'}