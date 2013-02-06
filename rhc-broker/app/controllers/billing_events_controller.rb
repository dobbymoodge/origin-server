
class BillingEventsController < BillingController
  respond_to :xml, :json

  # POST /billing/rest/events
  def create
    retval = "FAILED"
#   Rails.logger.info("Request params: #{params.inspect}")
    begin
      event_list = params[:event_id]
      if (event_list - Online::AriaBilling::Event::EVENTS.keys()).empty?
        Online::AriaBilling::Event.handle_event(params)
        retval = "SUCCESS"
      else
        Rails.logger.error "ERROR: Received INVALID event, id: #{event_list}"
      end
    rescue Exception => e
      Rails.logger.error "ERROR: Processing event, #{e.message}"
      Rails.logger.error e
    end
    render :text => retval
  end
end
