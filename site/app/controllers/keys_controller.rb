class KeysController < ConsoleController
  def new
    @first = true if params[:first]
    @key = Key.new
  end

  def create
    @first = true if params[:first]
    @key ||= Key.new params[:key]
    @key.as = session_user

    if @key.save
      redirect_to :back, :flash => {:success => 'Your public key has been created'} rescue redirect_to account_path
    else
      render :new
    end

  # If a key already exists with that name
  # FIXME When resource validation is added, we may need the server to return a unique code
  # for this condition with the error, and then this logic should be moved to Key.rescue_save_failure
  # which should throw a more specific exception Key::NameExists / Key::ContentExists
  rescue ActiveResource::ResourceConflict => error
    if @first
      if @key.default?
        @key = Key.default(:as => session_user).load(params[:key])
      else
        @key.make_unique! "#{@key.name}%s"
      end
      retry
    end
    @key.errors.add(:name, 'You have already created a key with that name')
    render :new
  end

  def destroy
    @key = Key.find params[:id], :as => session_user
    if @key.default? #FIXME: Bug 789786 prevents deletion of 'default' key
	    @key.content = 'nossh'
      @key.save!
    else
      @key.destroy
    end
    redirect_to account_path
  end
end
