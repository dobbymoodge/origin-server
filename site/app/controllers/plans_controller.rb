class PlansController < AccountController
  def index
    @plans = Plan.all
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
