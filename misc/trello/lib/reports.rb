require 'sprint'

module SprintReport
  attr_accessor :title, :headings, :function, :columns, :data, :day, :sort_key, :link, :friendly
  attr_accessor :sprint
  def initialize(opts)
    opts.each do |k,v|
      send("#{k}=",v)
    end

    @columns = headings.map{|x| Column.new(x)}
    @data = []
  end

  def data
    if @data.empty? && sprint && function
      @data = sprint.send(function)
    end
    if sort_key
      @data = @data.sort_by{|x| x.send(sort_key)}
    end
    @data
  end

  def offenders
    data.map{|x| x.members.map{|member| member.email} }.flatten.uniq
  end

  def rows(user = nil)
    _data = data
    if user
      _data = data.select{|x| x.members.map{|member| member.email}.include?(user)}
    end
    _data.map do |row|
      # Get data for each column
      columns.map do |col|
        col.process(row)
      end
    end
  end

  def print_title
    "%s %s" % [title, (!sprint.nil? && first_day?) ? "(to be completed by end of day today)" : '']
  end

  def required?
    if day.nil?
      true
    else
      ($date || Date.today) >= due_date
    end
  end

  def first_day?
    if day.nil?
      false
    else
      ($date || Date.today) == due_date
    end
  end

  def due_date
    sprint.start + day.days
  end

  class Column
    attr_accessor :header, :attr, :fmt, :sub_attr
    def initialize(opts)
      opts.each do |k,v|
        send("#{k}=",v)
      end
    end

    def process(row)
      value = row.is_a?(Hash) ? row[attr.to_sym] : row.send(attr)
      if value.is_a?(Array)
        value.map! { |v| process_sub_attr(v) }
      else
        value = process_sub_attr(value)
      end
      format(value)
    end
    
    def process_sub_attr(value)
      value = sub_attr ? value.send(sub_attr) : value
      value
    end

    # If no attr is specified, just use the heading name
    def attr
      @attr || header.downcase
    end
    
    def format(value)
      if value.is_a? Array
        value.map { |v| format_str(v) }.join(', ')
      else
        format_str(value)
      end
    end

    # Format a string if needed (like for URLs)
    def format_str(value)
      value ||= '<none>'
      fmt ? (fmt % [value]) : value
    end
  end
end

class UserStoryReport
  include SprintReport
  def initialize(opts)
    _opts = {
      :headings => [
        { :header => 'name', :attr => 'short_id' },
        { :header => 'members', :sub_attr => 'full_name' }, 
        { :header => 'Name' },
      ],
      #:link => { :attr => 'url' },
      :sort_key => :pos
    }
    super(_opts.merge(opts))
  end
end

class StatsReport
  include SprintReport

  def initialize
    super({
      :title => "Sprint Stats",
      :function => :stats,
      :headings => [
        {:header => "Count"},
        {:header => "Name"},
      ],
    })
  end
end

class DeadlinesReport
  include SprintReport

  def initialize
    super({
      :title => "Upcoming Deadlines",
      :function => :upcoming,
      :headings => [
        {:header => "Date"},
        {:header => "Title"}
      ],
    })
  end
end

class EnvironmentsReport
  include SprintReport

  def initialize
    super({
      :title => "Environment Pushes",
      :function => :upcoming,
      :headings => [
        {:header => "Date"},
        {:header => "Title"}
      ],
    })
  end
end
