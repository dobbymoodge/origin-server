require File.expand_path('../../test_helper', __FILE__)

class StreamlineIntegrationTest < ActionDispatch::IntegrationTest

  def confirmed_user
    @@confirmed_user ||= begin
      user = new_streamline_user
      omit_on_register unless user.register('/email_confirm')
      assert user.token
      assert_nil user.login
      assert_nil user.ticket

      assert user.roles.empty?
      assert_nil user.ticket

      assert user.confirm_email
      assert_equal user.email_address, user.login
      assert_nil user.token
      assert user.ticket
      assert user.roles.include? 'simple_authenticated'

      user
    end
  end

  test 'should fail when a token is reused' do
    user = new_streamline_user
    omit_on_register unless user.register('/email_confirm')
    assert user.token
    assert_nil user.login
    assert_nil user.ticket

    assert user.roles.empty?
    assert_nil user.ticket

    token = user.token

    assert user.confirm_email
    assert user.errors.empty?

    user.send(:ticket=, nil)
    user.send(:token=, token)
    omit("Streamline regression - 500 instead of errors being returned.") unless user.confirm_email
    assert user.errors.empty?
    assert_nil user.ticket

    # ensure that duplicate confirmation returns success
    assert user.register('/email_confirm'), user.errors.inspect
    assert user.errors.empty?
  end

  test 'should properly be entitled' do
    user = new_streamline_user
    omit_on_register unless user.register('/email_confirm')
    assert user.confirm_email
    assert_equal ['simple_authenticated'], user.roles
    assert user.entitled?
    assert !user.waiting_for_entitle?

    assert_equal ['simple_authenticated', 'cloud_access_1'].sort, user.roles!.sort
  end

  test 'should be able to retrieve and acknowledge terms' do
    user = new_streamline_user
    omit_on_register unless user.register('/email_confirm')
    assert user.confirm_email

    assert terms = user.terms
    assert terms.length >= 2
    assert !user.accepted_terms?
    assert_equal terms, user.terms!

    assert user.accept_terms
    assert user.accepted_terms?
    assert user.terms.empty?

    assert user.terms!.empty?
  end

  test 'should suppress duplicate registration' do
    user = new_streamline_user
    omit_on_register unless user.register('/email_confirm')
    assert user.register('/email_confirm')
  end

  test 'should give specific message for badly pasted URL' do
    user = new_streamline_user
    omit_on_register unless user.register('/email_confirm')
    assert !user.confirm_email(user.token, 'invalid_email!!')
    assert user.errors.full_messages.first =~ /properly entered the confirmation URL/, user.errors.full_messages.join("\n")
    assert_equal 1, user.errors.size
  end

  test 'should return token and accept it for confirmation' do
    assert confirmed_user

    second_user = Streamline::Base.new(:ticket => confirmed_user.ticket).extend(Streamline::User)
    second_user.establish
    assert_equal confirmed_user.login, second_user.login
  end

  test 'should change password' do
    old_password = confirmed_user.password

    assert !confirmed_user.change_password
    assert confirmed_user.errors[:base], confirmed_user.errors.inspect

    confirmed_user.password = 'testab'
    assert !confirmed_user.change_password
    assert confirmed_user.errors[:base], confirmed_user.errors.inspect

    confirmed_user.password_confirmation = 'testab'
    assert !confirmed_user.change_password
    assert confirmed_user.errors[:base], confirmed_user.errors.inspect

    confirmed_user.old_password = old_password
    assert confirmed_user.change_password, confirmed_user.errors.inspect
    assert confirmed_user.errors.empty?

    second_user = Streamline::Base.new.extend(Streamline::User)
    second_user.authenticate!(confirmed_user.login, 'testab')
    assert second_user.ticket != confirmed_user.ticket
  end

  test 'should accept terms' do
    assert !confirmed_user.accepted_terms?
    assert confirmed_user.accept_terms
    assert confirmed_user.accepted_terms?
  end

  test 'should entitle' do
    assert !confirmed_user.waiting_for_entitle?
    assert confirmed_user.entitled?
    assert !confirmed_user.waiting_for_entitle?
  end

  test 'should promote a simple user to a full user' do
    user = new_streamline_user
    omit_on_register unless user.register('/email_confirm')
    assert user.confirm_email
    assert user.simple_user?
    assert full_user = Streamline::FullUser.new(full_user_args(user))
    unless full_user.promote(user)
      omit('Streamline did not successfully promote a user, environment may be down')
    else
      assert user.full_user?
    end
  end

  test 'should raise an error when the wrong secret key is used' do
    user = new_streamline_user
    omit_on_register unless user.register('/email_confirm')
    assert user.confirm_email
    assert user.simple_user?

    # Missing/wrong secret key test
    assert full_user = Streamline::FullUser.new(full_user_args(user))
    Rails.configuration.streamline[:user_info_secret].reverse!
    assert_raise(Streamline::PromoteInvalidSecretKey){ full_user.promote(user) }
  end

  test 'should print an error message when the password and confirmation fields do not match' do
    user = new_streamline_user
    omit_on_register unless user.register('/email_confirm')
    assert user.confirm_email
    assert user.simple_user?

    # Mismatched password / confirm case
    assert user_args = full_user_args(user)
    assert user_args[:password_confirmation] = user_args[:password].reverse
    assert full_user = Streamline::FullUser.new(user_args)
    assert_equal false, full_user.promote(user)
    assert_equal 1, full_user.errors[:base].count
  end

  test 'should print an error message when a required field is not provided' do
    user = new_streamline_user
    omit_on_register unless user.register('/email_confirm')
    assert user.confirm_email
    assert user.simple_user?

    # Individual missing required field cases
    assert key_list = full_user_args
    key_list.keys.each do |field|
      # Skip special fields and non-required fields
      next if [:email_subscribe, :login, :password, :password_confirmation, :state].include?(field)
      assert user_args = full_user_args(user, [field])
      assert full_user = Streamline::FullUser.new(user_args)
      assert_equal false, full_user.promote(user)
      assert_equal 1, full_user.errors.get(field).count
      assert user.errors.clear
    end
  end

  test 'should make multiple error messages when multiple required fields are not provided' do
    user = new_streamline_user
    omit_on_register unless user.register('/email_confirm')
    assert user.confirm_email
    assert user.simple_user?

    # Multiple missing required fields
    assert user_args = full_user_args(user, [:first_name, :last_name, :company])
    assert full_user = Streamline::FullUser.new(user_args)
    assert_equal false, full_user.promote(user)
    assert_equal 3, full_user.errors.to_hash.keys.count
  end

  test 'should handle multiple errors on the same element' do
    user = new_streamline_user
    omit_on_register unless user.register('/email_confirm')
    assert user.confirm_email
    assert user.simple_user?

    # Right now the streamline API will not produce this case, so we simulate it
    user.errors.add(:first_name, "Mock error 1")
    user.errors.add(:first_name, "Mock error 2")

    assert user_args = full_user_args(user)
    assert full_user = Streamline::FullUser.new(user_args)
    assert_equal false, full_user.promote(user)
    assert_equal 2, full_user.errors[:first_name].count
    assert_equal user.errors[:first_name], full_user.errors[:first_name]
  end

  test 'should change password with token' do
    #assert confirmed_user.request_password_reset('/password_reset')
    #assert user.token
  end
end
