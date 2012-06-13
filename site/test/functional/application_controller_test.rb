require File.expand_path('../../test_helper', __FILE__)

class ApplicationControllerTest < ActionController::TestCase

  test 'user_from_session handles exceptions' do
    @request.cookies['rh_sso'] = "im_a_bad_cookie"
    WebUser.expects(:find_by_ticket).raises(AccessDeniedException)
    @controller.send('user_from_session')
  end

  test 'user_to_session stores user' do
    attrs = {:ticket => 'ticket', :rhlogin => 'login', :streamline_type => :simple}
    user = Streamline::User.new(attrs)

    attrs[:login] = attrs.delete(:rhlogin) # different names
    attrs.merge!(session)

    @controller.send('user_to_session', user)

    assert (session[:ticket_verified] - Time.now.to_i) < 100
    attrs[:ticket_verified] = session[:ticket_verified]

    assert_equal attrs.with_indifferent_access, session.to_hash.with_indifferent_access
  end

  test 'user_from_session restores simple user' do
    attrs = {:ticket => 'ticket', :login => 'login', :streamline_type => :simple}
    attrs.each_pair {|k,v| @request.session[k] = v }
    user = @controller.send('user_from_session')
    attrs[:rhlogin] = attrs.delete(:login) # different names
    attrs.each_pair {|k,v| assert_equal v, user.send(k) }
    assert user.simple_user?
  end

  test 'user_from_session restores full user' do
    attrs = {:ticket => 'ticket', :login => 'login', :streamline_type => :full}
    attrs.each_pair {|k,v| @request.session[k] = v }
    user = @controller.send('user_from_session')
    attrs[:rhlogin] = attrs.delete(:login) # different names
    attrs.each_pair {|k,v| assert_equal v, user.send(k) }
    assert !user.simple_user?
  end
end
