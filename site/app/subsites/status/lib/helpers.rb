require 'uri'
require 'net/https'
require 'socket'
require 'models'
require 'logger'

def http_req(url)
  uri = URI.parse(url)
  http = Net::HTTP.new(uri.host,uri.port)
  http.open_timeout = 10

  if uri.kind_of? URI::HTTPS
    http.use_ssl = true
    http.verify_mode = OpenSSL::SSL::VERIFY_NONE
  end

  response = nil
  begin
    response = http.get(uri.path)
  rescue Errno::ECONNREFUSED, Timeout::Error => e
    response = "Server not running"
  rescue Errno::EHOSTUNREACH
    response = "Host unreachable"
  end

  if block_given?
    yield response
  else
    return response
  end
end

def get_hostname
  Socket.gethostname
end

def _log(string)
  logger = defined?(Rails) ? Rails.logger : Logger.new(STDOUT)
  logger.debug("STATUS_APP: #{string}")
end

def overwrite_db(data)
  # Remove current data
  delete_all

  string = "update sqlite_sequence set seq = 0 where name = '%s'"
  ActiveRecord::Base.connection.execute(sprintf(string,'issues'))
  ActiveRecord::Base.connection.execute(sprintf(string,'updates'))

  data['issues'].each do |val|
    issue = val['issue']
    Issue.create issue
  end
  data['updates'].each do |val|
    update = val['update']
    Update.create update
  end
end

def delete_all
  [Issue,Update].each do |x|
    x.delete_all
  end
end

def dump_json
  { :issues => Issue.all, :updates => Update.all }.to_json
end
