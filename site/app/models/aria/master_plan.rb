module Aria
  class MasterPlan < Plan

    self.element_name = 'plan'
    allow_anonymous

    has_one :capabilities, :class_name => 'rest_api/base/attribute_hash'
    has_one :usage_rates, :class_name => 'rest_api/base/attribute_hash'
    has_one :storage, :class_name => 'rest_api/base/attribute_hash'

    def name
      aria_plan.plan_name
    end

    def description
      @description ||= aria_plan.plan_desc.each_line.map(&:chomp).split{ |s| s =~ /^\s*Features:/ }[0].join("\n").chomp
    end

    def max_gears
      capabilities[:max_gears]
    end

    def gear_sizes
      capabilities[:gear_sizes]
    end

    def recurring_line_items
      @recurring_line_items ||= services.keep_if{ |s| s.is_usage_based_ind == 0 }.map{ |s| Aria::RecurringLineItem.new(s, plan_no) }
    end

    def services
      @services ||= Aria.cached.get_client_plan_services(plan_no)
    end

    def features
      @features ||= Aria::MasterPlanFeature.from_description(aria_plan.plan_desc)
    end

    # Find a feature of the given name or create a new 'null' feature to represent it
    def feature(name)
      features.each do |feat|
        if feat.name == name
          return feat
        end
      end

      null_feature = Aria::MasterPlanFeature.new({ :name => name })
      @features << null_feature
      null_feature
    end

    # Compare plans first by their 'Price' feature, and then by their gear
    # size offerings.
    def <=>(other)
      price_comparison = feature('Price').<=>(other.feature('Price'))
      case
      when price_comparison == 0
        gear_sizes.length.<=>(other.gear_sizes.length)
      else
        price_comparison
      end
    end

    cache_find_method :single, lambda{ |*args| [MasterPlan.name, :find_single, args[0]] },
                      :before => lambda{ |p| p.as = nil; p.send(:aria_plan); p.send(:description); p.send(:features) }
    cache_find_method :every,
                      :before => lambda{ |plans| plans.each{ |p| p.as = nil; p.send(:aria_plan); p.send(:description); p.send(:features) } }

    protected
      def aria_plan
        @aria_plan ||= Aria.cached.get_client_plans_basic.find{ |plan| plan.plan_no == self.plan_no }
      end
  end
end
