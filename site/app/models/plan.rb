class Plan < RestApi::Base
  allow_anonymous

  schema do
    string :id, :name
    integer :plan_no
  end
  custom_id :id

  def basic?
    id == 'freeshift'
  end

  cache_find_method :single
  cache_find_method :every
end
