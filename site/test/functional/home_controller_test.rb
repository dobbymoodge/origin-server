require File.expand_path('../../test_helper', __FILE__)

class HomeControllerTest < ActionController::TestCase
  
  test "should get index unauthorized" do
    get :index
    assert_response :success
  end

  test "should be workflow redirected" do
    get(:index, {}, {:workflow => getting_started_path })
    assert_redirected_to getting_started_path

    assert_nil session[:workflow]
  end

  test "should get index authorized" do
    get(:index, {}, {:login => "test", :ticket => "test" })
    assert :success
  end
end
