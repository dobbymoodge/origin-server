require File.expand_path('../../test_helper', __FILE__)

class TermsControllerTest < ActionController::TestCase
  test "show accept terms unauthenticated" do
    get :new
    assert_redirected_to login_path
    assert_equal new_terms_path, session[:login_workflow]
  end

  test "show accept terms" do
    setup_session
    get :new
    assert_response :success
  end

  test "accept terms unauthenticated" do
    post :create
    assert_redirected_to login_path
    assert_equal new_terms_path, session[:login_workflow]
  end

  test "accept terms with streamline errors" do
    @controller.expects(:check_credentials)

    # Override the returned user with one that has errors
    # to simulate a failure
    user = WebUser.new
    user.terms = ['1']
    user.errors.add(:base, "test")
    @controller.expects(:session_user).returns(user)

    post(:create, {}, {:user => user})
    assert_equal 1, assigns(:term).errors.length
    assert_response :success
  end

  test "accept terms but already accepted" do
    setup_session
    user = session[:user]
    user.terms=[]
    user.expects(:accept_terms).never    
    post :create
    assert_equal 0, assigns(:term).errors.length
    assert_redirected_to root_path
  end

  test "accept terms successfully" do
    setup_session
    user = session[:user]
    user.terms = [{'termId' => '1', 'termUrl' => 'localhost'}]
    user.expects(:accept_terms).once
    post :create
    assert_equal 0, assigns(:term).errors.length
    assert_redirected_to root_path
  end

  test "accept terms successfully with workflow" do
    setup_session
    session[:login_workflow] = login_path
    user = session[:user]
    user.terms = [{'termId' => '1', 'termUrl' => 'localhost'}]
    user.expects(:accept_terms).once
    post :create
    assert_equal 0, assigns(:term).errors.length
    assert_redirected_to login_path
  end

  test "show acceptance terms" do
    setup_session
    user = session[:user]
    user.terms = [{'termId' => '1', 'termUrl' => 'localhost'}]
    get :acceptance_terms
    assert_equal 0, assigns(:term).errors.length
    assert_response :success
  end

  test "verify auto-access doesn't fire before accepting terms" do
    setup_session

    # Remove the key that denotes terms acceptance
    session.delete(:login)

    # Make sure request access is not called in this scenario
    @controller.expects(:request_access).never

    get :new
  end
end
