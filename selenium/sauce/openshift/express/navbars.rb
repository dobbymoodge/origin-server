module OpenShift
  module Express
    class NavBar
      include ::OpenShift::CSSHelpers

      def initialize(page,id)
        @page = page
        @id = id
        @base = "nav##{id}"
      end
    end

    class MainNav < NavBar
      @@items = {
        :signin => 'a.sign_in',
        :signout => 'a.sign_out',
        :greeting => 'a.greeting',

        :platform_overview => 'a.overview',
        :express => 'a.express',
        :flex => 'a.flex',
        :community => 'a.community'
      }

      def link(name)
        selector(@@items[name])
      end

      def links
        @@items
      end

      def click(element)
        @page.click(selector(@@items[element]))
      end
    end
  end
end
