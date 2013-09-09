module Aria
  class MasterPlan < Plan

    self.element_name = 'plan'
    allow_anonymous

    has_one :capabilities, :class_name => as_indifferent_hash
    has_one :usage_rates, :class_name => as_indifferent_hash
    has_one :storage, :class_name => as_indifferent_hash

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
      @recurring_line_items ||= Aria::RecurringLineItem.find_all_by_plan_no(plan_no)
    end

    def services
      @services ||= Aria.cached.get_client_plan_services(plan_no)
    end

    def features(currency_cd=nil)
      currency_cd ||= Rails.configuration.default_currency.to_s
      @features ||= Aria::MasterPlanFeature.from_description(aria_plan.plan_desc)
      @features.select {|f| f.currency_cd.nil? or f.currency_cd == currency_cd }
    end

    # Find a feature of the given name or create a new 'null' feature to represent it
    def feature(name, currency_cd=nil)
      features(currency_cd).each do |feat|
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

    def self.for_plan_no(plan_no)
      cached.all.find{ |p| p.plan_no == plan_no }
    end

    protected
      def aria_plan
        @aria_plan ||= Aria.cached.get_client_plans_basic.find{ |plan| plan.plan_no == self.plan_no }
      end
  end
end