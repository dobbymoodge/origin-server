require 'test_helper'

class UsageModelTest < ActiveSupport::TestCase
  def setup
    super
  end

  test "create and find usage event" do
    orig = usage
    ue = Usage.new(orig.login, orig.gear_uuid, orig.begin_time, orig.end_time, orig.uuid, UsageRecord::USAGE_TYPES[:gear_usage])
    ue.gear_size = orig.gear_size
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
    ue = Usage.find_by_user(ue.login)
    assert(ue.length == 1)
  end
 
  test "find all user usage events since given time" do
    ue1 = usage
    ue1.save!
    ue2 = usage
    ue2.login = ue1.login
    ue2.begin_time = ue1.begin_time + 100
    ue2.save!
    ue = Usage.find_by_user_after_time(ue1.login, ue1.begin_time + 10)
    assert(ue.length == 1)
  end
  
  test "find latest by gear" do
    ue1 = usage
    ue1.save!
    ue2 = usage
    ue2.gear_uuid = ue1.gear_uuid
    ue2.begin_time = ue1.begin_time + 1
    ue2.save!
    ue = Usage.find_latest_by_gear(ue1.gear_uuid)
    assert(ue == ue2)
  end

  test "find all user usage events given time range" do
    cur_tm = Time.now
    ue1 = usage
    ue1.begin_time = cur_tm - 100
    ue1.end_time = cur_tm - 10
    ue1.save!
    ue2 = usage
    ue2.login = ue1.login
    ue2.begin_time = cur_tm
    ue2.end_time = cur_tm + 100
    ue2.save!
    ue3 = usage
    ue3.login = ue1.login
    ue3.begin_time = cur_tm + 200
    ue3.save!
    ue = Usage.find_by_user_time_range(ue1.login, cur_tm + 10, cur_tm + 150)
    assert(ue.length == 1)
    ue = Usage.find_by_user_time_range(ue1.login, cur_tm + 10, cur_tm + 250)
    assert(ue.length == 2)
    ue = Usage.find_by_user_time_range(ue1.login, cur_tm -20, cur_tm + 10)
    assert(ue.length == 2)
  end

  test "find usage by gear" do
    ue = usage
    ue.save!
    ue1 = Usage.find_by_gear(ue.gear_uuid)
    assert(ue1 != nil)
    ue1 = Usage.find_by_gear(ue.gear_uuid, ue.begin_time)
    assert(ue1 != nil)
  end

  test "find user usage summary" do
    cur_tm = Time.now
    ue1 = usage
    ue1.gear_size = 'small'
    ue1.begin_time = cur_tm + 1
    ue1.end_time = cur_tm + 101
    ue1.save!
    ue2 = usage
    ue2.login = ue1.login
    ue2.gear_size = 'small'
    ue2.begin_time = cur_tm + 501
    ue2.end_time = cur_tm + 601
    ue2.save!
    ue3 = usage
    ue3.login = ue1.login
    ue3.gear_size = 'medium'
    ue3.begin_time = cur_tm + 201
    ue3.end_time = cur_tm + 301
    ue3.save!
    expected_res = { 'small'  => { 'num_gears' => 2, 'consumed_time' => 200 },
                     'medium' => { 'num_gears' => 1, 'consumed_time' => 100 } }
    res = Usage.find_user_summary(ue1.login)
    assert_equal(res, expected_res)
  end

  def usage
    uuid = "usage#{gen_uuid}"
    obj = Usage.new("user#{gen_uuid}", "gear#{gen_uuid}", Time.now.utc, nil, uuid, UsageRecord::USAGE_TYPES[:gear_usage])
    obj.gear_size = 'small'
    obj.addtl_fs_gb = 5
    obj._id = uuid
    obj.updated_at = nil
    obj
  end
end
