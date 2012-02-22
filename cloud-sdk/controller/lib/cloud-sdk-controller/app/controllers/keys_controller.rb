class KeysController < BaseController
  respond_to :xml, :json
  before_filter :authenticate
  include LegacyBrokerHelper
  #GET /user/keys
  def index
    user = CloudUser.find(@login)
    if(user.nil?)
      @reply = RestReply.new(:not_found)
      @reply.messages.push(Message.new(:error, "User #{@login} not found"))
      respond_with @reply, :status => @reply.status
    return
    end
    ssh_keys = Array.new
    unless user.ssh_keys.nil?
      user.ssh_keys.each do |name, key|
        ssh_key = RestKey.new(name, key["key"], key["type"])
        ssh_keys.push(ssh_key)
      end
    end
    @reply = RestReply.new(:ok, "keys", ssh_keys)
    respond_with @reply, :status => @reply.status
  end

  #GET /user/keys/<id>
  def show
    id = params[:id]
    user = CloudUser.find(@login)
    if user.nil? or user.ssh_keys.nil?
      @reply = RestReply.new(:not_found)
      @reply.messages.push(Message.new(:error, "User #{@login} not found"))
      respond_with @reply, :status => @reply.status
    return
    end
    if user.ssh_keys
      user.ssh_keys.each do |key_name, key|
        if key_name == id
          @reply = RestReply.new(:ok, "key", RestKey.new(key_name, key["key"], key["type"]))
          respond_with @reply, :status => @reply.status
        return
        end
      end
    end

    @reply = RestReply.new(:not_found)
    @reply.messages.push(Message.new(:error, "SSH key #{id} for user #{@login} not found"))
    respond_with @reply, :status => @reply.status
  end

  #POST /user/keys
  def create
    content = params[:content]
    name = params[:name]
    type = params[:type]

    user = CloudUser.find(@login)
    if(user.nil?)
      @reply = RestReply.new(:not_found)
      @reply.messages.push(Message.new(:error, "User #{@login} not found"))
      respond_with @reply, :status => @reply.status
    return
    end

    key = Key.new(name, type, content)
    if key.invalid?
      key.errors.keys.each do |key|
        error_messages = domain.errors.get(key)
        error_messages.each do |error_message|
          @reply.messages.push(Message.new(:error, error_message[:message], error_message[:exit_code], key))
        end
      end
      respond_with @reply, :status => @reply.status
      return
    end
    #check to see if key already exists
    if user.ssh_keys
      user.ssh_keys.each do |key_name, key|
        if key_name == name
          @reply = RestReply.new(:conflict)
          @reply.messages.push(Message.new(:error, "SSH key with name #{name} already exists. Please choose a different name"))
          respond_with @reply, :status => @reply.status
        return
        end
        if key["key"] == content
          @reply = RestReply.new(:conflict)
          @reply.messages.push(Message.new(:error, "Given public key is already in use. Use different key or delete conflicting key and retry"))
          respond_with @reply, :status => @reply.status
        return
        end
      end
    end

    begin
      user.add_ssh_key(name, content, type)
      user.save
      ssh_key = RestKey.new(name, user.ssh_keys[name][:key], user.ssh_keys[name][:type])
      @reply = RestReply.new(:created, "key", ssh_key)
      @reply.messages.push(Message.new(:info, "Created SSH key #{name} for user #{@login}"))
      respond_with @reply, :status => @reply.status
    rescue Exception => e
      Rails.logger.error e
      @reply = RestReply.new(:internal_server_error)
      @reply.messages.push(Message.new(:error, "Failed to create SSH key for user #{@login} due to:#{e.message}") )
      respond_with @reply, :status => @reply.status
    return
    end
  end

  #PUT /user/keys/<id>
  def update

    id = params[:id]
    content = params[:content]
    type = params[:type]

    user = CloudUser.find(@login)
    if(user.nil?)
      @reply = RestReply.new(:not_found)
      @reply.messages.push(Message.new(:error, "User #{@login} not found"))
      respond_with(@reply) do |format|
        format.xml { render :xml => @reply, :status => @reply.status }
        format.json { render :json => @reply, :status => @reply.status }
      end
    return
    end

    key = Key.new(name, type, content)
    if key.invalid?
      key.errors.keys.each do |key|
        error_messages = domain.errors.get(key)
        error_messages.each do |error_message|
          @reply.messages.push(Message.new(:error, error_message[:message], error_message[:exit_code], key))
        end
      end
      respond_with(@reply) do |format|
        format.xml { render :xml => @reply, :status => @reply.status }
        format.json { render :json => @reply, :status => @reply.status }
      end
      return
    end

    begin
      user.update_ssh_key(content, type, id)
      user.save
      ssh_key = RestKey.new(id, user.ssh_keys[id][:key], user.ssh_keys[id][:type])
      @reply = RestReply.new(:ok, "key", ssh_key)
      @reply.messages.push(Message.new(:info, "Updated SSH key with name #{id} for user #{@login}"))
      respond_with(@reply) do |format|
        format.xml { render :xml => @reply, :status => @reply.status }
        format.json { render :json => @reply, :status => @reply.status }
      end
    rescue Exception => e
      Rails.logger.error e
      @reply = RestReply.new(:internal_server_error)
      @reply.messages.push(Message.new(:error, "Failed to update SSH key #{id} for user #{@login} due to:#{e.message}") )
      respond_with(@reply) do |format|
        format.xml { render :xml => @reply, :status => @reply.status }
        format.json { render :json => @reply, :status => @reply.status }
      end
    return
    end
  end

  #DELETE /user/keys/<id>
  def destroy
    id = params[:id]

    user = CloudUser.find(@login)
    if(user.nil?)
      @reply = RestReply.new(:not_found)
      @reply.messages.push(Message.new(:error, "User #{@login} not found"))
      respond_with(@reply) do |format|
        format.xml { render :xml => @reply, :status => @reply.status }
        format.json { render :json => @reply, :status => @reply.status }
      end
    return
    end

    if user.ssh_keys.nil? or not user.ssh_keys.has_key?(id)
      @reply = RestReply.new(:not_found)
      @reply.messages.push(Message.new(:error, "SSH key with name #{id} not found for user #{@login}"))
      respond_with(@reply) do |format|
        format.xml { render :xml => @reply, :status => @reply.status }
        format.json { render :json => @reply, :status => @reply.status }
      end
    return
    end

    begin
      user.remove_ssh_key(id)
      user.save
      @reply = RestReply.new(:no_content)
      @reply.messages.push(Message.new(:info, "Deleted SSH key #{id} for user #{@login}"))
      respond_with(@reply) do |format|
        format.xml { render :xml => @reply, :status => @reply.status }
        format.json { render :json => @reply, :status => @reply.status }
      end
    rescue Exception => e
      Rails.logger.error e
      @reply = RestReply.new(:internal_server_error)
      @reply.messages.push(Message.new(:error, "Failed to delete SSH key #{id} for user #{@login} due to:#{e.message}") )
      respond_with(@reply) do |format|
        format.xml { render :xml => @reply, :status => @reply.status }
        format.json { render :json => @reply, :status => @reply.status }
      end
    return
    end
  end
end
