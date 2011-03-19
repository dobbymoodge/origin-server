# Rakefile for li-express
#
#

require 'rbconfig'
require 'build/ami'
require 'build/test'

DEST_DIR = ENV["DESTDIR"] || "/"
BIN_DIR = ENV["BINDIR"] || "#{DEST_DIR}/usr/bin"
FACTER_DIR = ENV["FACTERDIR"] || "#{DEST_DIR}/#{Config::CONFIG['sitelibdir']}/facter"
MCOLLECTIVE_DIR = ENV["MCOLLECTIVEDIR"] || "#{DEST_DIR}/usr/libexec/mcollective/mcollective/agent/"
MCOLLECTIVE_CONN_DIR = ENV["MCOLLECTIVECONNDIR"] || "#{DEST_DIR}/usr/libexec/mcollective/mcollective/connector/"
INITRD_DIR = ENV["INITRDDIR"] || "#{DEST_DIR}/etc/init.d/"
LIBEXEC_DIR = ENV["LIBEXECDIR"] || "#{DEST_DIR}/usr/libexec/li/"
LIBRA_DIR = ENV["LIBRADIR"] || "#{DEST_DIR}/var/lib/libra"
CONF_DIR = ENV["CONFDIR"] || "#{DEST_DIR}/etc/libra"
MAN_DIR = ENV["MANDIR"] || "#{DEST_DIR}/usr/share/man/"
HTML_DIR = ENV["PHPDIR"] || "#{DEST_DIR}/var/www/html/"
SITE_DIR = ENV["SITEDIR"] || "#{DEST_DIR}/var/www/html/"
HTTP_CONF_DIR = ENV["HTTPCONFDIR"] || "#{DEST_DIR}/etc/httpd/conf.d/"

NODE_FILES = ["backend/facter/libra.rb",
              "backend/mcollective/libra.rb",
              "backend/mcollective/connector/amqp.rb"]

C_DIR = "backend/controller"
MOCK_ENV = "li-6-x86_64"
RPM_SPEC = "packaging/li.spec"
RPM_REGEX = /(Version: )(\d+\.\d+)/
RPM_REL_REGEX = /(Release: )(\d)(.*)/

desc "Install php files"
task :install_php do
    mkdir_p HTML_DIR
    cp_r "php/", HTML_DIR
end

desc "Install site files"
task :install_site do
    mkdir_p SITE_DIR
    cp_r "site/", SITE_DIR
    mkdir_p HTTP_CONF_DIR
    cp "docs/rails.conf", HTTP_CONF_DIR
end

task :test_client do
    Dir.glob("client/rhc*").each{|client_file| sh "ruby", "-c", client_file}
end

task :install_client => [:test_client] do
    mkdir_p "#{BIN_DIR}"
    mkdir_p "#{MAN_DIR}/man1"
    mkdir_p "#{MAN_DIR}/man5"
    mkdir_p "#{CONF_DIR}"
    Dir.glob("client/rhc*").each {|file_name|
        cp file_name, "#{BIN_DIR}/"
    }
    Dir.glob("client/man/*").each {|file_name|
        man_section = file_name.to_s.split('').last
        cp file_name, "#{MAN_DIR}/man#{man_section}/"
    }
    cp "client/libra.conf.sample", "#{CONF_DIR}/libra.conf" unless File.exists? "#{CONF_DIR}/libra.conf"
end

task :test_node do
    NODE_FILES.each{|node_file| sh "ruby", "-c", node_file}
end

task :install_node => [:test_node] do
    mkdir_p FACTER_DIR
    cp "backend/facter/libra.rb", FACTER_DIR
    mkdir_p MCOLLECTIVE_DIR
    cp "backend/mcollective/libra.rb", MCOLLECTIVE_DIR
    mkdir_p MCOLLECTIVE_CONN_DIR
    cp "backend/mcollective/connector/amqp.rb", MCOLLECTIVE_CONN_DIR
    mkdir_p INITRD_DIR
    cp "backend/scripts/libra", INITRD_DIR
    cp "backend/scripts/libra-data", INITRD_DIR
    cp "backend/scripts/libra-cgroups", INITRD_DIR
    cp "backend/scripts/libra-tc", INITRD_DIR
    mkdir_p BIN_DIR
    cp "backend/scripts/trap-user", BIN_DIR
    cp "backend/scripts/rhc-restorecon", BIN_DIR
    mkdir_p LIBRA_DIR
    mkdir_p "#{DEST_DIR}/usr/share/selinux/packages"
    cp "backend/selinux/libra.pp", "#{DEST_DIR}/usr/share/selinux/packages"
    cp "backend/selinux/rhc-ip-prep.sh", "#{BIN_DIR}"
    mkdir_p "#{HTTP_CONF_DIR}/libra/"
    cp "docs/000000_default.conf", HTTP_CONF_DIR
end

task :install_cartridges do
    mkdir_p LIBEXEC_DIR
    cp_r "cartridges/", LIBEXEC_DIR
    mkdir_p CONF_DIR
    sample_conf = Dir.glob("cartridges/li-controller*/**/node.conf-sample")[0]
    cp_r sample_conf, "#{CONF_DIR}/node.conf" unless File.exists? "#{CONF_DIR}/node.conf"
    cp "./client/resource_limits.conf", "#{CONF_DIR}/resource_limits.conf" unless File.exists? "#{CONF_DIR}/resource_limits.conf"
end

task :test_server do
# Can't run this until rubygem-cucumber is available in EPEL-6
#    cd C_DIR
#    sh "rake", "cuc_unit"
#    cd "../.."
end

task :install_server do
    mkdir_p MCOLLECTIVE_DIR
    cp "backend/mcollective/libra.ddl", MCOLLECTIVE_DIR
    cp "backend/mcollective/update_yaml.pp", "#{MCOLLECTIVE_DIR}/../../"

    mkdir_p BIN_DIR
    Dir.glob("#{C_DIR}/bin/*").each do |script|
      cp script, File.join(BIN_DIR, File.basename(script))
    end

    mkdir_p CONF_DIR
    cp "#{C_DIR}/conf/controller.conf", CONF_DIR unless File.exists? "#{CONF_DIR}/controller.conf"
    cd C_DIR
    sh "rake", "package"
end

desc "Install all the Libra files (e.g. rake DESTDIR='/tmp/test/ install')"
task :install => [:install_client, :install_node, :install_cartridges, :install_server]

task :version do
    @version = RPM_REGEX.match(File.read(RPM_SPEC))[2]
    puts "Current Version is #{@version}"
end

task :buildroot do
    # Get the RPM build root for the system
    @buildroot = `rpm --eval "%{_topdir}"`.chomp!
    puts "Build root is #{@buildroot}"
end

task :commit_check do
    # Get the current spec version
    # Make sure everything is committed - otherwise exit
    sh("git diff-index --quiet HEAD") do |ok, res|
      if !ok
        puts "ERROR - Uncommitted repository changes"
        puts "Checkin / revert before continuing."
        exit 1
      end
    end
end

desc "Build the Libra SRPM"
task :srpm => [:version, :buildroot, :commit_check] do
    # Archive the git repository and compress it for the SOURCES
    src = "#{@buildroot}/SOURCES/li-#{@version}.tar"
    sh "git archive --prefix=li-#{@version}/ HEAD --output #{src}"
    sh "gzip -f #{src}"

    # Move the SPEC file out
    cp "packaging/li.spec", "#{@buildroot}/SPECS"

    # Build the source RPM
    sh "rpmbuild -bs #{@buildroot}/SPECS/li.spec"
end

task :bump_release => [:version, :commit_check] do
    # Bump the version number
    @version = @version.succ
    puts "New Version number is #{@version}"

    # Get the RPM version and reset the release number to 1
    replace = File.read(RPM_SPEC).gsub(RPM_REGEX, "\\1#{@version}")
    replace = replace.gsub(RPM_REL_REGEX, "\\1" + "1" + "\\3")

    # Add a comment to the RPM log
    comment = "* " + Time.now.strftime("%a %b %d %Y")
    comment << " " + `git config --get user.name`.chomp
    comment << " <" + `git config --get user.email`.chomp + ">"
    comment << " " + @version + "-1"
    comment << "\n- Upstream released new version\n"
    replace = replace.gsub(/(%changelog.*)/, "\\1\n#{comment}")

    # Write out and commit the new spec file
    File.open(RPM_SPEC, "w") {|file| file.puts replace}
    sh "git commit -a -m 'Upstream released new version'"
end

desc "Increment release number and build Libra RPMs"
task :release => [:bump_release, :rpm]

desc "Create a brew build based on current info"
task :brew => [:version, :buildroot, :srpm] do
    srpm = Dir.glob("#{@buildroot}/SRPMS/li-#{@version}*.rpm")[0]
    if ! File.exists?("#{ENV['HOME']}/cvs/li/RHEL-6-LIBRA")
        puts "Please check out the li cvs root:"
        puts
        puts "mkdir -p #{ENV['HOME']}/cvs; cd #{ENV['HOME']}/cvs"
        puts "cvs -d :gserver:cvs.devel.redhat.com:/cvs/dist co li"
        exit 206
    end
    cp "packaging/li.spec", "#{ENV['HOME']}/cvs/li/RHEL-6-LIBRA"
    cd "#{ENV['HOME']}/cvs/li/RHEL-6-LIBRA"
    sh "cvs up -d"
    sh "make new-source FILES='#{@buildroot}/SOURCES/li-#{@version}.tar.gz'"
    sh "cvs commit -m 'Updating to most recent li build #{@version}'"
    sh "make tag"
    sh "make build"
end

desc "Build mash repo from latest li builds"
task :mash do
    if ! File.exists?("/etc/mash/li.mash")
        puts
        puts "Please install and configure mash.  Read docs/BREW for setup steps"
        puts
        exit 222
    end
    sh "/usr/bin/mash -o /tmp/li -c /etc/mash/li-mash.conf li"
end
