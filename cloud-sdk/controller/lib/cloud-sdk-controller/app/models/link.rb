class Link < Cloud::Sdk::Model
  attr_accessor :rel, :method, :href, :required_params, :optional_params
  
  def initialize(rel=nil, method=nil, href=nil, required_params=nil, optional_params=nil)
    self.rel = rel
    self.method = method
    self.href = href
    self.required_params ||= Array.new
    self.optional_params ||= Array.new
  end
end