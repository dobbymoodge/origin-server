module Aria
  class RecurringLineItem < LineItem

    def self.find_all_by_plan_no(plan_no)
      plan = Aria.cached.get_client_plans_all.find{ |plan| plan.plan_no.to_s == plan_no.to_s }
      plan_services = plan ? plan.plan_services : []
      plan_services.inject([]) do |a, s|
        next a if s.is_usage_based_ind == 1 || s.plan_service_rates.empty?
        rate = s.plan_service_rates.first.monthly_fee
        a << Aria::RecurringLineItem.new({
          'service_name' => s.service_desc,
          'description' => s.service_desc,
          'plan_name' => plan.plan_name,
          'rate_per_unit' => rate,
          'units' => 1.0,
        }, plan_no) if rate >= 0.01
        a
      end || []
    end

    def self.find_all_by_current_plan(acct_no)
      plan = Aria.get_acct_plans_all(acct_no).last
      plan_services = plan ? plan.plan_services : []
      plan_services.inject([]) do |a, s|
        a << Aria::RecurringLineItem.new({
          'service_name' => s.service_desc,
          'description' => s.service_desc,
          'plan_name' => plan.plan_name,
          'rate_per_unit' => s.plan_service_rates.map(&:monthly_fee).max,
          'units' => 1.0,
        }, plan.plan_no) if s.is_recurring_ind == 1
        a
      end || []
    end

    def recurring?
      true
    end
    def tax?
      (service_name || '').include?('Tax')
    end

    def name
      if (service_name == 'Recurring' || service_name == 'Plan: Recurring') && plan_name
        "Plan: #{plan_name}"
      else 
        description
      end
    end

    def date
      date_range_start
    end

    def amount
      attributes['amount'] || (rate_per_unit * units)
    end
    alias_method :total_cost, :amount

    def prorated?
      units != 1.0
    end

    def rate
      rate_per_unit
    end

    protected
      define_attribute_methods [:service_no,
                               :service_name,
                               :amount,
                               :units,
                               :rate_per_unit,
                               :description,
                               :plan_name,
                               :date_range_start]
  end
end
