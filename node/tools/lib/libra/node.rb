#
# Classes and methods useful for operation and observation of a 
# Red Hat Libra Node
#

require 'rubygems'
require 'nokogiri' # XML processing
require 'json'

#
# Open the password file, find all the entries with the marker in them
# and create a data structure with the usernames of all matching accounts
#
module Libra
  module Node


    # survey the status of the Libra services on a node
    #   Access Controls
    #    SELinux
    #   Messaging
    #     qpid
    #     mcollective
    #   Resource Control
    #     cgconfig
    #     cgred
    #     libra-cgroups
    #     libra-tc
    #     quotas
    #   Service
    #     httpd
    #     user applications

    class Status

      #attr_reader :packages :selinux, :qpid, :mcollective, 
      #attr_reader :cgroups, :tc, :quota, :httpd

      @@package_list = ['qpid-cpp-server', 'qpid-cpp-client', 'ruby-qmf',
                        'mcollective', 'mcollective-client',
                        'li-node',
                        'li-cartridge-php-5.3.2', 
                        'li-rack-1.1.0', 
                        'li-wsgi-3.2.1']

      def initialize
        @packages = nil
        @selinux = nil
        @qpid = nil
        @mcollective = nil
        @cgroups = nil
        @tc = nil
        @quota = nil
        @httpd = nil
        @applications = nil
      end

      def to_s

      end
      
      def to_json

      end

      def self.json_create(o)
        new(*o)
        # add status
      end

      def to_xml

      end

      #
      # Check the set of required packages
      # 
      def packages
        packages = {}
        @@packagelist.each { |pkgname| packages[pkgname => `rpm -q --qf '%{NAME} %{VERSION}' #{pkgname}`]}
      end
    end

    

    class GuestAccount
 
      # Used to find accounts
      @@passwd_file = "/etc/passwd"  # replace with singleton Opts.passwd_file
      def self.passwd_file=(filename)
        @@passwd_file = filename
      end
      @@guest_marker = ":libra guest:" # replace with Opts.guest_marker
 
      attr_reader :username


      def initialize(username)
        @username = username
        @homedir = nil
        @applications = nil
      end

      def to_s
        @username
      end

      def to_xml
        builder = Nokogiri::XML::Builder.new do |xml|
          xml.account(:username => @username)
        end
        builder.doc.root.to_xml
      end
  
      def self.json_create(o)
        new(*o['username'])
      end

      def to_json
        JSON.generate({"json_class" => self.class.name,
                        "username" => @username})
      end

      # find a user's home directory
      def homedir
        return @homedir if @homedir
        File.open(@@passwd_file, "r") do |f|
          while line = f.gets do
            entry = line.split(":")
            return @homedir = entry[5] if entry[0] == @username
          end
        end
      end

      # find the applications associated with this user
      def appnames(homedir=nil)
        return @applications.keys if @applications

        # get the user's home directory
        homedir ||= self.homedir

        # find the git repositories
        apps = []
        Dir[ homedir + "/git/*.git"].each do |gitdir| 
          apps << File.basename(gitdir, ".git")
        end
        apps.sort
      end

      # populate and return the application data structures
      def applications(refresh=false, homedir=nil)
        return @applications if @applications

        apps = {}
        self.appnames.each do |appname|
          apps << Application.new(appname, self)
        end
        @applications = apps
      end
      # ------------------------------------------------------------------------
      # Class Methods
      # ------------------------------------------------------------------------

      # get a list of account names from the password file
      def self.accounts
        userlist = []
        guest_re = Regexp.new(@@guest_marker)
        File.open(@@passwd_file, "r") do |f|
          while line = f.gets
            username = line.split(":")[0]
            if guest_re =~ line
              userlist.push(username)
            end
          end
        end
        userlist
      end

    end

    class Application

      attr_reader :appname, :apptype
      attr :account

      def initialize(appname, account=nil, apptype=nil)
        @appname = appname
        @account = account
        @apptype = apptype
      end


      def to_s
        @appname
      end

      def to_xml
        builder = Nokogiri::XML::Builder.new do |xml|
          xml.application(:appname => @appname)
        end
        builder.doc.root.to_xml
      end
  
      def self.json_create(o)
        new(*o['appname'])
      end

      def to_json
        JSON.generate({"json_class" => self.class.name, 
                        "appname" => @appname})
      end

    end
  end
end
