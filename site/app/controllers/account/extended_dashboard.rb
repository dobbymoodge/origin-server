module Account
  module ExtendedDashboard
    extend ActiveSupport::Concern
    include DomainAware
    include AsyncAware

    def show
      @user = current_user
      logger.debug @user.inspect

      async do
        @user.load_email_address
        @identities = Identity.find @user
        @show_email = @identities.any? {|i| i.id != i.email }
      end

      async{ begin; user_default_domain; rescue ActiveResource::ResourceNotFound; end }

      async{ @keys = Key.find :all, :as => @user }

      if user_can_upgrade_plan?
        async do
          api_user = current_api_user
          @plan = api_user.plan.tap{ |c| c.name }
        end
      end

      join!(30)

      render :show_extended
    end
  end
end

