DEST_DIR = ENV["DESTDIR"] || "/"
BIN_DIR = ENV["BINDIR"] || "#{DEST_DIR}/usr/bin"
FACTER_DIR = ENV["FACTERDIR"] || "#{DEST_DIR}/#{Config::CONFIG['sitelibdir']}/facter"
MCOLLECTIVE_DIR = ENV["MCOLLECTIVEDIR"] || "#{DEST_DIR}/usr/libexec/mcollective/mcollective/agent"
MCOLLECTIVE_CONN_DIR = ENV["MCOLLECTIVECONNDIR"] || "#{DEST_DIR}/usr/libexec/mcollective/mcollective/connector"
INITRD_DIR = ENV["INITRDDIR"] || "#{DEST_DIR}/etc/init.d"
LIBEXEC_DIR = ENV["LIBEXECDIR"] || "#{DEST_DIR}/usr/libexec/li"
LIBRA_DIR = ENV["LIBRADIR"] || "#{DEST_DIR}/var/lib/libra"
CONF_DIR = ENV["CONFDIR"] || "#{DEST_DIR}/etc/libra"
MAN_DIR = ENV["MANDIR"] || "#{DEST_DIR}/usr/share/man"
HTML_DIR = ENV["HTMLDIR"] || "#{DEST_DIR}/var/www/html"
HTTP_CONF_DIR = ENV["HTTPCONFDIR"] || "#{DEST_DIR}/etc/httpd/conf.d"
ROOT = File.expand_path(File.expand_path(__FILE__) + "/../../")
BUILD_ROOT = ROOT + "/build"
CLIENT_ROOT = ROOT + "/client"
COMMON_ROOT = ROOT + "/common"
NODE_ROOT = ROOT + "/node"
SERVER_ROOT = ROOT + "/server"
RPM_SPEC = ROOT + "/build/specs/li.spec"
RPM_REGEX = /(Version: )(\d)(.*)/
RPM_REL_REGEX = /(Release: )(\d)(.*)/
