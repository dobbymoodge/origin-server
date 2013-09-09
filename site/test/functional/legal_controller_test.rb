require File.expand_path('../../test_helper', __FILE__)

class LegalControllerTest < ActionDispatch::IntegrationTest

  test "show legal index" do
    get '/legal'
    assert_redirected_to community_base_url('legal')
  end

  test "show site terms" do
    get '/legal/site_terms'
    assert_redirected_to community_base_url('legal/site_terms')
  end

  test "show services agreement" do
    get '/legal/services_agreement'
    assert_redirected_to community_base_url('legal/services_agreement')
  end

  test "show privacy" do
    get '/legal/openshift_privacy'
    assert_redirected_to community_base_url('legal/openshift_privacy')
  end

  test "show acceptable use" do
    get '/legal/acceptable_use'
    assert_redirected_to community_base_url('legal/acceptable_use')
  end

end