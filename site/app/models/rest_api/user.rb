module RestApi
  #
  # The REST API model object representing the currently authenticated user.
  #
  class User < Base
    singleton

    has_many :keys

    schema do
      string :login
    end

    has_many :domains
  end
end
