require File.expand_path('../coverage_helper.rb', __FILE__)

ENV["RAILS_ENV"] = "test"
require File.expand_path('../../config/environment', __FILE__)
require 'rails/test_help'
require 'mocha/setup'

def gen_uuid
  %x[/usr/bin/uuidgen].gsub('-', '').strip 
end
