module Cloud
  module Sdk
    class AuthService
      @cdk_auth_provider = Cloud::Sdk::AuthService
      
      def self.provider=(provider_class)
        @cdk_auth_provider = provider_class
      end
      
      def self.instance
        @cdk_auth_provider.new
      end
      
      def generate_broker_key(app)
        iv = app.name
        token = app.user.login
        [iv, token]
      end
      
      def authenticate(request, login, password)
        return {:username => login, :auth_method => :login}
      end

      def login(request, params, cookies)
        if params['broker_auth_key'] && params['broker_auth_iv']
          return {:username => params['broker_auth_key'], :auth_method => :broker_auth}
        else
          data = JSON.parse(params['json_data'])          
          return {:username => data["rhlogin"], :auth_method => :login}
        end
      end
    end
  end
end