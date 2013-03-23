require 'csv'

class BillsController < ConsoleController
  include BillingAware

  before_filter :authenticate_user!
  before_filter :require_aria_account
  before_filter :require_invoices

  def index
    populate_view(@user, @invoices, @invoices.first)
  end

  def export
    columns = ['Transaction Date', 'Transaction ID', 'Transaction Description', 'Description', 'Date Range Start', 'Date Range End', 'Units', 'Rate', 'Amount']
    filename = "history.csv"
    h = self.response.headers
    h["Content-Type"] ||= 'text/csv'
    h["Content-Disposition"] = "attachment; filename=#{filename}"
    h["Content-Transfer-Encoding"] = "binary"
    self.response_body = Enumerator.new do |y|
      y << columns.to_csv
      transactions = Array(Aria.get_acct_trans_history(:account_no => @user.acct_no).history).sort_by(&:transaction_create_date)
      transactions.each do |t|
        case t.transaction_type
        when 1
          Aria.get_invoice_details(@user.acct_no, t.transaction_source_id).each do |li|
            y << [
              t.transaction_create_date, t.transaction_source_id, t.transaction_desc,
              li.plan_name || li.description, li.date_range_start, li.date_range_end, li.units, li.rate_per_unit,
              li.amount
            ].to_csv
          end
        else
          y << [
            t.transaction_create_date, t.transaction_source_id, t.transaction_desc,
            nil, nil, nil, nil, nil,
            t.transaction_amount
          ].to_csv
        end
        y << "\n"
      end
    end    
  end

  def locate
    if params[:id].present?
      redirect_to account_bill_path(params[:id])
    else
      redirect_to account_bills_path
    end
  end

  def show
    invoice = find_invoice(params[:id])
    populate_view(@user, @invoices, invoice)
  end

  def print
    invoice = find_invoice(params[:id])
    render :text => "#{invoice.statement_content} <script>try{window.print();}catch(e){}</script>" and return
  end


  protected
    def require_aria_account
      @user = Aria::UserContext.new(current_user)
      redirect_to account_path and return false unless @user.has_account?
    end

    def require_invoices
      @invoices = @user.invoices_with_amounts
      render :no_bills and return false if @invoices.empty?
    end

    def find_invoice(id)
      invoice = @invoices.detect {|i| i.invoice_no.to_s == params[:id] }
      raise Aria::ResourceNotFound.new("Invoice ##{id} does not exist") if invoice.nil?
      invoice
    end

    def populate_view(user, invoices, invoice)
      @plan = current_api_user.plan

      @invoice_options = invoices.map {|i| [
        "#{i.bill_date.to_datetime.to_s(:billing_date)}",
        i.invoice_no.to_s,
        {"data-url" => account_bill_path(i.invoice_no)}
      ]}
      @id = invoice.invoice_no.to_s
      @bill = @user.bill_for(invoice)

      index = invoices.index(invoice)
      @next_no = invoices[index - 1].invoice_no if index and index > 0
      @prev_no = invoices[index + 1].invoice_no if index and index < invoices.length - 1

      @is_test_user = user.test_user?
      @virtual_time = Aria::DateTime.now if Aria::DateTime.virtual_time?

      @next_bill = user.next_bill
      current_usage_items = @next_bill.unbilled_usage_line_items
      past_usage_items = invoice.line_items.select(&:usage?)
      if current_usage_items.present? and past_usage_items.present?
        @usage_items = {
          "Current" => current_usage_items,
          "This bill" => past_usage_items
        }
      end
      @usage_types = Aria::UsageLineItem.type_info(@usage_items.values.flatten) if @usage_items
    end
end
