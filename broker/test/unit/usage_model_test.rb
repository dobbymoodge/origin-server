require 'test_helper'

class UsageModelTest < ActiveSupport::TestCase
  def setup
    super
  end

  test "create and find usage event" do
    orig = usage
    ue = Usage.new
    ue.construct(orig.user_id, orig.gear_uuid, orig.gear_type,
                 orig.action, orig.create_time, orig.destroy_time, orig.uuid)
    ue.save!
    ue = Usage.find(orig.uuid)
    ue.updated_at = nil
    assert_equal(orig, ue)
  end

  test "delete usage event" do
    ue = usage
    ue.save!
    ue = Usage.find(ue.uuid)
    assert(ue != nil)
    Usage.delete(ue.uuid)
    ue = Usage.find(ue.uuid)
    assert_equal(nil, ue)
  end
 
  test "find all usage events" do
    ues = Usage.find_all
    ues.each do |ue|
      ue.delete
    end
    2.times do
      ue = usage
      ue.save!
    end
    ues = Usage.find_all
    assert(ues.length == 2)
  end
 
  test "find all usage events by user" do
    ue = usage
    ue.save!
    ue = Usage.find_by_user(ue.user_id)
    assert(ue.length == 1)
  end
 
  test "find all user usage events since given time" do
    ue1 = usage
    ue1.save!
    ue2 = usage
    ue2.user_id = ue1.user_id
    ue2.create_time = ue1.create_time + 100
    ue2.save!
    ue = Usage.find_by_user_after_time(ue1.user_id, ue1.create_time + 10)
    assert(ue.length == 1)
  end

  test "find all user usage events given time range" do
    cur_tm = Time.now
    ue1 = usage
    ue1.create_time = cur_tm - 100
    ue1.destroy_time = cur_tm - 10
    ue1.save!
    ue2 = usage
    ue2.user_id = ue1.user_id
    ue2.create_time = cur_tm
    ue2.destroy_time = cur_tm + 100
    ue2.save!
    ue3 = usage
    ue3.user_id = ue1.user_id
    ue3.create_time = cur_tm + 200
    ue3.save!
    ue = Usage.find_by_user_time_range(ue1.user_id, cur_tm + 10, cur_tm + 150)
    assert(ue.length == 1)
    ue = Usage.find_by_user_time_range(ue1.user_id, cur_tm + 10, cur_tm + 250)
    assert(ue.length == 2)
    ue = Usage.find_by_user_time_range(ue1.user_id, cur_tm -20, cur_tm + 10)
    assert(ue.length == 2)
  end

  test "find usage by gear" do
    ue = usage
    ue.save!
    ue = Usage.find_by_gear(ue.gear_uuid)
    assert(ue != nil)
  end

  def usage
    uuid = "usage#{gen_uuid}"
    obj = Usage.new
    obj.uuid = uuid
    obj._id = uuid
    obj.user_id = "user#{gen_uuid}"
    obj.gear_uuid = "gear#{gen_uuid}"
    obj.gear_type = 'small'
    obj.action = 'create'
    obj.create_time = Time.now
    obj.destroy_time = nil
    obj.updated_at = nil
    obj
  end
end
