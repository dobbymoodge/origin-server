class PlansController < BaseController

  skip_before_filter :authenticate_user!

  def index
    plans = []
    OpenShift::BillingService.instance.get_plans.each do |key, value|
      plan = RestPlan.new(key, value[:name], value[:plan_no], value[:capabilities], value[:usage_rates], get_url, nolinks)
      plans.push(plan)
    end
    render_success(:ok, "plans", plans)
  end

  def show
    id = params[:id]
    OpenShift::BillingService.instance.get_plans.each do |key, value|
      return render_success(:ok, "plan",
                            RestPlan.new(key, value[:name], value[:plan_no], value[:capabilities], value[:usage_rates], get_url, nolinks)) if key.to_s == id
    end
    render_error(:not_found, "Plan not found.", 150)
  end
  
  def set_log_tag
    @log_tag = get_log_tag_prepend + "PLAN"
  end
end
