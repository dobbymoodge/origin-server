module Aria
  class RecurringLineItem < LineItem

    def recurring?
      true
    end
    def usage?
      false
    end
    def tax?
      rate_per_unit.nil? || service_name.include?('Taxes')
    end

    def name
      if service_name == 'Recurring' && plan_name
        "Plan: #{plan_name}"
      else description
      end
    end

    def total_cost
      amount
    end

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
                               :plan_name]
  end
end
