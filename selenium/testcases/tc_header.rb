#!/usr/bin/env ruby
class Header < OpenShift::SeleniumTestCase

  def setup
    super
    @home.open
  end

  def test_header_links
    @home.click(@home.items[:logo])
    assert_redirected_to '/app/'
  end

  def test_navbar_links
    links = {
      :learn_more => '/app/platform',
      :community => '/community/',
      :developers => '/community/developers',
      :getting_started => '/app/getting_started'
    }

    links.each do |name,url|
      @home.open
      @navbar.click(name)
      assert_redirected_to("#{url}")
    end
  end
end
