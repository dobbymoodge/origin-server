require File.expand_path('../../test_helper', __FILE__)

class LogoutControllerTest < ActionController::TestCase
  test "should get index" do
    get :show
    assert_redirected_to root_path
  end

  test "should clear session and cookies" do
    # Create the test rh_sso cookie
    @request.cookies['rh_sso'] = CGI::Cookie.new({'name'  => 'rh_sso',
                                                  'value' => '123',
                                                  'path'  => '/',
                                                  'domain'=> '.redhat.com',
                                                  'secure'=> 'true'})

    # Create a cookie that should be left alone
    @request.cookies['keep'] = CGI::Cookie.new('keep', 'me')

    # Hit logout with some session data as well
    get(:show, {}, {:test => "value"})
    assert_redirected_to root_path

    # Make sure the cookie is gone and the session is empty
    assert session.empty?
    assert_nil cookies['rh_sso']

    # Make sure we didn't delete all cookies
    assert_not_nil cookies['keep']
  end

  test "should reset a streamline user" do
    set_user(new_user :login => 'foo', :ticket => 'bar')
    WebUser::Mock.any_instance.expects(:logout).returns(true)

    # Hit logout with some session data as well
    get(:show, {}, user_to_session(@user))
    assert_redirected_to root_path

    # Make sure the cookie is gone and the session is empty
    assert session.empty?
  end

  test "should delete an active authorization" do
    set_user(new_user :login => 'foo', :ticket => 'bar')
    auth = Authorization.create(:scope => 'session', :as => @user)
    @user.api_ticket = auth.token

    # Hit logout with some session data as well
    get(:show, {}, user_to_session(@user))
    assert_redirected_to root_path

    @user.api_ticket = nil

    # Make sure the cookie is gone and the session is empty
    assert session.empty?
    assert_raise(RestApi::ResourceNotFound){ Authorization.find(auth.token, :as => @user) }
  end

  test 'should recover from exceptions' do
    @controller.expects(:reset_sso).raises(AccessDeniedException)
    get :show
    assert_redirected_to root_path
  end

  test 'should redirect' do
    get :show, {:then => getting_started_path}
    assert_redirected_to getting_started_path
  end

  test 'should show a message' do
    get :show, {:cause => 'foo', :then => getting_started_path}
    assert_response :success
    assert_select 'a', 'Continue working' do |el|
      assert_equal getting_started_path, el.first['href']
    end
  end

  test 'should show the change_account page' do
    get :show, {:cause => 'change_account', :then => getting_started_path}
    assert_response :success
    assert_template :change_account
    assert_select 'a', 'Continue to a different account' do |el|
      assert_equal getting_started_path, el.first['href']
    end
  end

  test 'should show the expired page' do
    get :show, {:cause => 'expired', :then => getting_started_path}
    assert_response :success
    assert_template :expired
    assert_select 'a', 'Continue working' do |el|
      assert_equal getting_started_path, el.first['href']
    end
  end

  test 'should not redirect outside domain' do
    get :show, {:then => 'http://www.google.com/a_test_page'}
    assert_redirected_to '/a_test_page'
  end

  test 'should redirect from the same host at port 8118' do
    get :show, {:then => "http://#{request.host}:8118"}
    assert_redirected_to "http://#{request.host}:8118/"
  end

  test 'should redirect from the same host at port 8118 on a path' do
    get :show, {:then => "http://#{request.host}:8118/a_test_page"}
    assert_redirected_to "http://#{request.host}:8118/a_test_page"
  end

  test 'should not redirect from the same host at port 8118 when scheme is not http' do
    get :show, {:then => "ftp://#{request.host}:8118/a_test_page"}
    assert_response :success
  end
end
