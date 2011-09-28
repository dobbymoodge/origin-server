class ExpressCartlist
  include ActiveModel::Validations
  include ActiveModel::Conversion
  include ActiveModel::Serialization
  extend ActiveModel::Naming
  
  include ExpressApi
  
  attr_accessor :list, :cart_type, :debug
  
  validates :cart_type, :presence => true,
                        :inclusion => { :in => ['standalone', 'embedded'] } 
  
  def initialize( cart_type, debug = false )
    @cart_type = cart_type
    @debug = debug ? 'true' : 'false'
    case cart_type
      when 'standalone'
        @list = ['perl-5.10', 'jbossas-7.0', 'wsgi-3.2', 'rack-1.1', 'php-5.3']
      when 'embedded'
        @list = ['mysql-5.1']
    end
  end
  
  #def establish(force=false)
    #@list = Rails.cache.fetch "cartlist_#{@cart_type}", :force => force do
      #data = { :cart_type => @cart_type, :debug => @debug }
      #json_data = ActiveSupport::JSON.encode data
      #Rails.logger.debug "data to post: #{json_data}"
      #http_post @@cartlist_url, json_data do |response|
        #Rails.logger.debug "Cartlist response is #{response.inspect}"
        #unless response['exit_code'] > 0
          #data = ActiveSupport::JSON.decode response['data']
          #data['carts']
        #else
          #errors.add(:base, response['result'])
          #nil
        #end # unless .. else
      #end # http_post block
    #end # cache fetch block
  #end

end
