require 'sinatra/base'
require 'haml'
require 'json'

MY_ROOT = File.expand_path(File.dirname(__FILE__))
$LOAD_PATH << File.join(MY_ROOT,'lib')

require 'models'
require 'database'
require 'helpers'

HOSTS = YAML.load(File.open(File.join(MY_ROOT,'config','hosts.yml')))

class StatusApp < Sinatra::Base
  configure do
    set :views, File.join(MY_ROOT,'views')
  end

  before do
    #sync(sprintf(HOSTS[:template],HOSTS[:host])) unless defined?(settings.synced)
  end

  get '/app/status' do
    @open = Issue.is_open
    @resolved = Issue.resolved.merge(Issue.year)
    haml :index
  end

  get '/app/status/current.json' do
    content_type :json
    { :issues => Issue.all, :updates => Update.all }.to_json 
  end
  
  get '/app/status/sync/?' do
    redirect "/app/status/sync/#{HOSTS[:host]}"
  end

  get '/app/status/sync/:server' do
    server = params[:server]
    _log "Syncing to #{server}"
    sync(sprintf(HOSTS[:template],server))
    redirect '/app/status'
  end

  get '/app/status/status.js' do
    @open = Issue.is_open
    status = header
    content_type 'text/javascript'
    cache_control 'no-cache'
    :javascript
    <<-eos 
      var div = "                               \
        <div class='status #{status[:class]}'>  \
          <a href='/app/status'>                \
    #{status[:message]}                 \
          </a> \
        </div>" ;
      div = div.replace(/^\s+|\s+$/g, '');
      div = div.replace(/\s+/g, ' ');
      document.write(div);
    eos
  end

  helpers do
    def header
      case @open.length
      when 0
        {
          :class => '',
          :message => 'No known issues',
          :short => 'OK'
        }
      when 1
        {
          :class => 'error',
          :message => '1 known issue',
          :short => '1'
        }
      else
        {
          :class => 'error',
          :message => "#{@open.length} known issues",
          :short => @open.length
        }
      end
    end
    
    def sync(host)
      set :synced, true
      uri = "#{host}/current.json"
      _log "Syncing to #{uri}"  

      http_req(:get,uri) do |resp|
        unless resp.empty?
          data = JSON.parse(resp)

          Issue.delete_all
          Update.delete_all

          string = "update sqlite_sequence set seq = 0 where name = '%s'"
          ActiveRecord::Base.connection.execute(sprintf(string,'issues'))
          ActiveRecord::Base.connection.execute(sprintf(string,'updates'))

          data['issues'].each do |val| 
            issue = val['issue']
            puts YAML.dump issue
            Issue.create issue
          end
          data['updates'].each do |val| 
            update = val['update']
            puts YAML.dump update
            Update.create update
          end
        end
      end

      _log "Done syncing"
    end
  end
end
