#/usr/bin/ruby

require 'test/unit'
require 'libra/node'


class TestHostInfo < Test::Unit::TestCase
  
  class << self
    attr_reader :hostname
  end

  @hostname = `hostname`

  def setup
    @testinfo = {
      "hostname" => "myhost",
      "uptime" => "00:00:00"
    }
  end

  def testConstructor
    h0 = Libra::Node::HostInfo.new

    assert_nil(h0.hostname)
    assert_nil(h0.uptime)
  end

  def testCheck
    h0 = Libra::Node::HostInfo.new true
    assert_equal(self.class.hostname, h0.hostname)
    assert(h0.uptime)
  end

  def testToString
    teststring = "-- HostInfo --\n  Hostname: myhost\n  Uptime: 00:00:00\n\n"
    h0 = Libra::Node::HostInfo.new
    h0.init @testinfo
    assert_equal(teststring, h0.to_s)
  end

  def testToXml
    testxml = '<hostinfo uptime="00:00:00" hostname="myhost"/>'
    h0 = Libra::Node::HostInfo.new
    h0.init @testinfo
    assert_equal(testxml, h0.to_xml)
  end

  def testToJson
    testjson0 = "{\"json_class\":\"Libra::Node::HostInfo\"}"
    testjson1 = "{\"json_class\":\"Libra::Node::HostInfo\",\"uptime\":\"00:00:00\",\"hostname\":\"myhost\"}"
    h0 = Libra::Node::HostInfo.new
    assert_equal(testjson0, h0.to_json)
    h0.init @testinfo
    assert_equal(testjson1, h0.to_json)

  end

  def testParseJson

  end

end
