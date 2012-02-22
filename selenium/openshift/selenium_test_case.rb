require "rubygems"
require "test/unit"
require "openshift/base"
require "openshift/sauce_helper"
require "pathname"

module OpenShift
  class SeleniumTestCase < Test::Unit::TestCase
    include ::OpenShift::TestBase
    include ::OpenShift::SauceHelper
    include ::OpenShift::CSSHelpers
    include ::OpenShift::Assertions
    
    attr_reader :driver
    
    alias_method :page, :driver
    alias_method :selenium, :driver

    def self.local?
      # ENV['LOCAL_SELENIUM']
      cfg = Sauce::Config.new()
      return cfg.local?
    end

    def setup
      super

      #hostname = get_my_hostname
      hostname = "localhost"

      if ENV['SAUCE_BROWSER_URL']
        browser_url = ENV['SAUCE_BROWSER_URL']
        uri = URI.parse(browser_url)
        hostname = uri.host
      end

      base_url = "https://#{hostname}"

      unless browser_url
        browser_url = "#{base_url}/app"
      end

      if OpenShift::SeleniumTestCase.local?
        @driver = Selenium::WebDriver.for :firefox
        @driver.navigate.to browser_url
      else
        cfg = Sauce::Config.new()
        opts = cfg.opts

        case opts[:browser] || ''
          when "iexplore"
            caps = Selenium::WebDriver::Remote::Capabilities.internet_explorer
          when "chrome"
            caps = Selenium::WebDriver::Remote::Capabilities.chrome
          when "opera"
            caps = Selenium::WebDriver::Remote::Capabilities.opera
          else
            caps = Selenium::WebDriver::Remote::Capabilities.firefox
        end

        platform = opts[:os] || ''
        case platform.downcase
          when "windows 2008"
            caps.platform = :VISTA
          when "linux"
            caps.platform = :LINUX
          else
            caps.platform = :XP
        end

        caps.version = opts[:browser_version] if opts[:browser_version]

        caps[:name] = get_name
        caps[:build] = ENV['JENKINS_BUILD'] || 'unofficial'

        @driver = Selenium::WebDriver.for(
          :remote,
          :url => "http://#{opts[:username]}:#{opts[:access_key]}@#{opts[:host]}:#{opts[:port]}/wd/hub",
          :desired_capabilities => caps)
      end

      @page    = page
      @home    = OpenShift::Express::Home.new(page, "#{base_url}/app")
      @express = OpenShift::Express::Express.new(page, "#{base_url}/app/express")
      @flex    = OpenShift::Express::Flex.new(page, "#{base_url}/app/flex")
      @express_console = OpenShift::Express::ExpressConsole.new(page, "#{base_url}/app/control_panel")

      @navbar  = OpenShift::Express::MainNav.new(page,'main_nav')
      @signin  = OpenShift::Express::Login.new(page,'signin')
      @reset   = OpenShift::Express::Reset.new(page,'reset_password')
      @signup  = OpenShift::Express::Signup.new(page,'signup')
    end

    def run(*args, &blk)
      # suppress Test::Unit::TestCase#default_test placeholder test
      unless get_name =~ /^default_test/
        super(*args, &blk)
      end
    end

    def teardown
      if @driver
        unless passed?
          begin
            start_time = Time.now # comment out in Ruby 1.9.3
            Dir.mkdir 'output' rescue

            image = "output/#{name}_#{start_time.to_i}.png"
            @driver.save_screenshot(image)

            html = "output/#{name}_#{start_time.to_i}.html"
            File.open(html, 'w') do |f| 
              f.write(@driver.page_source)
            end

            puts "Wrote screenshot to #{Pathname.new(image)} and html to #{Pathname.new(html)}"
          rescue Exception => e
            puts "<unable to output logs for #{name}"
            puts e.inspect
            puts ">"
          end
        end

        @driver.quit

        unless OpenShift::SeleniumTestCase.local?
          set_meta(session_id, {:passed => @test_passed})
        end
      end
      
      super
    end
    
    def get_name
      if self.respond_to? :name
        return self.name
      else
        return self.__name__
      end
    end
  end
end
