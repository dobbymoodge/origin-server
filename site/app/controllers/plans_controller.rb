class PlansController < ApplicationController
  layout 'site'

  def index
    @plans = Aria::MasterPlan.cached.all
    if user_signed_in?
      @user = User.find :one, :as => current_user
      @current_plan = @user.plan
    end
  end

  def edit
  end

  def update
  end

  def show
    @user = User.find :one, :as => current_user
    @plan = @user.plan
  end
end
