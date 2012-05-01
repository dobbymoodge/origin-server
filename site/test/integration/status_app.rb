require File.expand_path('../../test_helper', __FILE__)

class StatusAppTest < ActionDispatch::IntegrationTest

  def setup
    https!
    open_session
    Issue.create(:title => 'Test issue 1') if Issue.first.nil?
  end

  test 'status app serves js' do
    get "/status/status.js"
    assert_response :success
    assert_equal 'text/javascript', response.content_type
  end

  test 'status app has modifier for id' do
    get "/status/status.js?id=special___"
    assert_response :success
    assert_equal 'text/javascript', response.content_type
    assert headers['Cache-Control'].index('public')
    assert_nil headers['Set-Cookie']
    assert cookies.to_hash.empty?
    assert response.body.index('special___')
    puts response.pretty_inspect
  end

end

