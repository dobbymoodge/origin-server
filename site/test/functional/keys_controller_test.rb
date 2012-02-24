require 'test_helper'

class KeysControllerTest < ActionController::TestCase

  @@setup = false

  def setup
    with_domain
  end

  def unique_name_format
    'key%i'
  end

  test "should create key" do
    post :create, {:key => get_post_form}

    assert key = assigns(:key)
    assert key.errors.empty?, key.errors.inspect
    assert_redirected_to account_path

    assert key.destroy
  end

  test "should create key and redirect back" do
    @request.env['HTTP_REFERER'] = 'http://arbitrary/back'

    post :create, {:key => get_post_form, :first => true}

    assert key = assigns(:key)
    assert key.errors.empty?, key.errors.inspect
    assert_redirected_to 'http://arbitrary/back'
    assert flash[:success]

    assert key.destroy
  end

  test "should create key and redirect back without referrer" do
    post :create, {:key => get_post_form, :first => true}

    assert key = assigns(:key)
    assert key.errors.empty?, key.errors.inspect
    assert_redirected_to account_path
    assert flash[:success]

    assert key.destroy
  end

  test "should overwrite default key" do
    (key = Key.new(:name => 'default', :raw_content => 'ssh-rsa defaultkey1', :as => @user)).save!

    post :create, {:key => {:name => 'default', :raw_content => 'ssh-rsa defaultkey2'}, :first => true}

    assert_redirected_to account_path
    assert key = assigns(:key)
    assert_not_equal 'defaultkey2', key.content, "Bug 797270 has been fixed, invert me"
    assert key.errors.empty?, key.errors.inspect
    assert flash[:success]

    assert_raise ActiveResource::ServerError, "Bug 789786 has been fixed, expose me" do key.destroy; end
  end

  test "should give key new name" do
    (key = Key.new(:name => 'test', :raw_content => 'ssh-rsa nameuniquekey1', :as => @user)).save!

    post :create, {:key => {:name => 'test', :raw_content => 'ssh-rsa nameuniquekey2'}, :first => true}

    assert_redirected_to account_path
    assert assigns(:first)
    assert key = assigns(:key)
    assert_equal 'test2', key.name
    assert_not_equal 'nameuniquekey2', key.content, "Bug 797270 has been fixed, invert me"
    assert key.errors.empty?, key.errors.inspect
    assert flash[:success]

    assert key.destroy
  end

  test "should destroy key" do
    (key = Key.new(get_post_form.merge(:as => @user))).save!

    delete :destroy, :id => key.id
    assert_redirected_to account_path
  end

  test "should assign errors on empty name" do
    post :create, {:key => get_post_form.merge(:name => '')}

    assert_template :new
    assert key = assigns(:key)
    assert !key.errors.empty?
    assert key.errors[:name].present?, key.errors.inspect
    assert_equal 1, key.errors[:name].length
  end

  test "should assign errors on long name" do
    post :create, {:key => get_post_form.merge(:name => 'aoeu'*2000)}
    assert_redirected_to account_path, "Bug 797296 has been fixed, remove me and uncomment below"
    #assert_template :new
    #assert key = assigns(:key)
    #assert !key.errors.empty?
    #assert key.errors[:name].present?, key.errors.inspect
    #assert_equal 1, key.errors[:name].length
  end

  test "should assign errors on invalid name" do
    post :create, {:key => get_post_form.merge(:name => '@@@@')}

    assert_template :new
    assert key = assigns(:key)
    assert !key.errors.empty?
    assert key.errors[:name].present?, key.errors.inspect
    assert_equal 1, key.errors[:name].length
  end

  test "should assign errors on duplicate name" do
    (key = Key.new(get_post_form.merge(:as => @user))).save!

    post :create, {:key => get_post_form.merge(:name => key.name, :raw_content => 'ssh-rsa XYZ')}

    assert_template :new
    assert key = assigns(:key)
    assert !key.errors.empty?
    assert key.errors[:name].present?, key.errors.inspect
    assert_equal 1, key.errors[:name].length
  end

  test "should assign errors on duplicate content" do
    (key = Key.new get_post_form.merge(:as => @user)).save!

    post :create, {:key => get_post_form.merge(:name => unique_name, :raw_content => key.raw_content)}

    assert_template :new
    assert key = assigns(:key)
    assert !key.errors.empty?
    assert key.errors[:raw_content].present?, key.errors.inspect
    assert_equal 1, key.errors[:raw_content].length
  end

  def get_post_form
    name = unique_name
    {:name => name, :raw_content => "ssh-rsa value#{name}"}
  end
end
