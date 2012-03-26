module OpenShift
  module Rest
    class Page
      include ::OpenShift::CSSHelpers
      attr_accessor :fields, :items, :path

      def initialize(page, path)
        @path = path
        @page = page
        @expected_redirects = [path]
      end

      def open
        @page.get @path
        wait
      end

      def title
        @page.find_element(:css, "title").text
      end

      def click(element)
        text = @items[element]
        @page.find_element(:link_text, text).click
      end

      def wait(timeout=10)
        wait_for_pages @expected_redirects, timeout
      end

      def add_redirect path
        @expected_redirects.push(path)
      end
    end

    class Login < Page
      attr_accessor :login_form

      def initialize(page, path)
        super
        @login_form = OpenShift::Rest::LoginForm.new(page, "web_user_password_input")
      end

      def submit(login=nil,password=nil)
        @login_form.submit(login, password)
      end
    end

    class Account < Page
      attr_accessor :domain_form, :domain_edit_page, :domain_page,
                    :ssh_key_form, :ssh_key_add_page, :ssh_key_page

      def initialize(page,path)
        super
        @domain_form = OpenShift::Rest::DomainForm.new(page, "")
        @domain_edit_page = Page.new(page, "#{@path}/domain/edit")
        @domain_page = Page.new(page, "#{@path}/domain")
        @ssh_key_form = OpenShift::Rest::SshKeyForm.new(page, "new_key")
        @ssh_key_add_page = Page.new(page, "#{@path}/keys/new")
        @ssh_key_page = Page.new(page, "#{@path}/keys")
      end

      def edit_namespace_button
        @page.find_element(:xpath => "//a[@href='/app/account/domain/edit']")
      end

      def ssh_key_add_button
        @page.find_element(:xpath => "//a[@href='/app/account/keys/new']")
      end

      def find_ssh_key_row(key_name)
        @page.find_element(:css => ssh_key_row_selector(key_name))
      end

      def find_ssh_key_delete_button(key_name)
        @page.find_element(:css => ssh_key_row_selector(key_name, ' .delete_button'))
      end

      def find_ssh_key(key_name)
        @page.find_element(:css => ssh_key_row_selector(key_name, ' .sshkey')).text
      end

      def ssh_key_form(name='new')
        OpenShift::Rest::SshKeyForm.new(@page, "ssh_key_#{name}")
      end

      private

      def ssh_key_row_selector(key_name, postfix='')
        "##{key_name}_sshkey#{postfix}"
      end
    end

    class ApplicationTypes < Page
      def initialize(page, path)
        super
      end

      ##
      # get_app_type - take an anchor element and determines the application
      # type from the restful href path
      def get_app_type(link)
        href = link.attribute(:href)

        if !href.start_with? "#{@path}/"
          raise "The link '#{href}' does not point to an application creation page"
        end

        path_components = href.split('/')
        path_components[-1]
      end

      def find_create_buttons
        @page.find_elements(:xpath => "//a[starts-with(@href, '/app/console/application_types/')]")
      end
    end

    class Applications < Page
      def initialize(page, path)
        super
      end
    end

    class GetStartedPage < Page
      def initialize(page, app_name)
        super(page, "/app/console/applications/#{app_name}/get_started")
      end

      def find_app_link
        @page.find_element(:xpath => "//*[contains(@class, 'application-url')]/a")
      end
    end

    class Console < Page
      attr_accessor :domain_form, :app_form, :application_types_page,
                    :applications_page, :application_create_form

      def initialize(page, path)
        super

        @application_types_page = ApplicationTypes.new(page, "#{path}/application_types")
        @applications_page = Applications.new(page, "#{path}/applications")
        @application_create_form = ApplicationCreateForm.new(page, 'application')

        add_redirect(@application_types_page.path)
        add_redirect(@applications_page.path)
        #@domain_form = OpenShift::Express::DomainForm.new(page, "new_express_domain")
       # @app_form = OpenShift::Express::AppForm.new(page, "new_express_app")
      end
    end

    class Home < Page
      def initialize(page,path)
        super
        @fields = {
          :title => /^OpenShift by Red Hat$/,
        }

        @items = {
          :logo => 'header div.brand a'
        }
      end

      def click(css)
        @page.find_element(:css => css).click
      end
    end
  end
end
