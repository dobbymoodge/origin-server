class HomeController < ApplicationController
  def index
    Rails.logger.debug "Index controller"
    # Handle any workflow routing
    Rails.logger.debug "Session workflow in HomeController#index: #{session[:workflow]}" 
    if session[:workflow]
      workflow = session[:workflow]
      session[:workflow] = nil
      redirect_to workflow and return
    end

    # If the user is logged in, send them to the landing page
    # otherwise, send them to the home
    if session[:login]      
      redirect_to getting_started_path and return
    else
      #Assuming at some point news will come from a news source
      @news = [ 'Lorem ipsum dolor si',
                'Amet, consetetur sadipscing elitr, sed diam nonumyeirmod',
                'Tempor invidunt ut labore et dolore magna aliquyam erat, sed' ]
    end
  end

  def getting_started; end
end
