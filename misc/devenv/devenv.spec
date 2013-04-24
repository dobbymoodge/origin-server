%define htmldir %{_var}/www/html
%define libradir %{_var}/www/openshift
%define brokerdir %{_var}/www/openshift/broker
%define sitedir %{_var}/www/openshift/site
%define devenvdir %{_sysconfdir}/openshift/devenv
%define jenkins %{_sharedstatedir}/jenkins
%define policydir %{_datadir}/selinux/packages

Summary:   Dependencies for OpenShift development
Name:      rhc-devenv
Version: 1.7.9
Release:   1%{?dist}
Group:     Development/Libraries
License:   GPLv2
URL:       http://openshift.redhat.com
Source0:   rhc-devenv-%{version}.tar.gz

BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
Requires:  rhc
Requires:  rhc-node
Requires:  rhc-site
Requires:  rhc-broker
Requires:  openshift-origin-cartridge-php-5.3
Requires:  openshift-origin-cartridge-python-2.6
Requires:  openshift-origin-cartridge-ruby-1.8
Requires:  openshift-origin-cartridge-jbossas-7
Requires:  openshift-origin-cartridge-jbosseap-6.0
Requires:  openshift-origin-cartridge-switchyard-0.6
Requires:  openshift-origin-cartridge-jbossews-1.0
Requires:  openshift-origin-cartridge-jbossews-2.0
Requires:  openshift-origin-cartridge-perl-5.10
Requires:  openshift-origin-cartridge-mysql-5.1
Requires:  openshift-origin-cartridge-phpmyadmin-3.4
Requires:  openshift-origin-cartridge-jenkins-1.4
Requires:  openshift-origin-cartridge-diy-0.1
Requires:  openshift-origin-cartridge-jenkins-client-1.4
Requires:  openshift-origin-cartridge-metrics-0.1
Requires:  openshift-origin-cartridge-mongodb-2.2
Requires:  openshift-origin-cartridge-rockmongo-1.1
Requires:  openshift-origin-cartridge-rockmongo
Requires:  openshift-origin-cartridge-10gen-mms-agent-0.1
Requires:  openshift-origin-cartridge-postgresql-8.4
Requires:  openshift-origin-cartridge-cron-1.4
Requires:  openshift-origin-cartridge-haproxy-1.4
Requires:  openshift-origin-cartridge-nodejs-0.6
Requires:  openshift-origin-cartridge-ruby-1.9-scl
Requires:  openshift-origin-cartridge-zend-5.6
Requires:  openshift-origin-cartridge-community-python-2.7
Requires:  openshift-origin-cartridge-community-python-3.3
Requires:  openshift-origin-cartridge-mock
Requires:  openshift-origin-cartridge-mock-plugin
Requires:  openshift-origin-cartridge-jbosseap
Requires:  openshift-origin-cartridge-jbossas
Requires:  openshift-origin-cartridge-php
Requires:  openshift-origin-cartridge-perl
Requires:  openshift-origin-cartridge-python
Requires:  openshift-origin-cartridge-ruby
Requires:  openshift-origin-cartridge-jenkins
Requires:  openshift-origin-cartridge-jenkins-client
Requires:  openshift-origin-cartridge-mysql
Requires:  openshift-origin-cartridge-postgresql
Requires:  openshift-origin-cartridge-jbossews
Requires:  openshift-origin-cartridge-diy
Requires:  openshift-origin-cartridge-haproxy
Requires:  openshift-origin-cartridge-mongodb
Requires:  openshift-origin-cartridge-metrics
Requires:  openshift-origin-cartridge-nodejs
Requires:  openshift-origin-cartridge-10gen-mms-agent
Requires:  openshift-origin-cartridge-cron
Requires:  openshift-origin-cartridge-phpmyadmin
Requires:  activemq
Requires:  activemq-client
#Requires:  qpid-cpp-server
#Requires:  qpid-cpp-server-ssl
Requires:  puppet
Requires:  ruby193-rubygem-cucumber
Requires:  ruby193-rubygem-mocha
Requires:  ruby193-rubygem-rspec
Requires:  ruby193-rubygem-webmock
Requires:  ruby193-rubygem-nokogiri
Requires:  ruby193-build
Requires:  ruby193-rubygems-devel
Requires:  ruby193-rubygem-aws-sdk
Requires:  ruby193-rubygem-net-ssh
Requires:  ruby193-rubygem-archive-tar-minitar
Requires:  ruby193-rubygem-commander
Requires:  charlie
Requires:  pam
Requires:  pam-devel
Requires:  bind
Requires:  memcached

# CI Requirements
Requires:  jenkins
Requires:  tito

# Drupal Requirements
Requires:  php-domxml-php4-php5
Requires:  php-gd
Requires:  php-mbstring
Requires:  php-mysql
Requires:  php-pdo
Requires:  php-pear-MDB2-Driver-mysql
Requires:  php-pear-MDB2-Driver-mysqli
Requires:  php-pecl-memcached
Requires:  php-pecl-apc
Requires:  php-soap
Requires:  php-tidy
Requires:  drupal6
Requires:  drupal6-drush
# Note: this RPM has a fix for getting mysql
# running in the devenv w/o breaking because
# of pam_namespace.
Requires:  drupal6-openshift-devenv-dbdump
#
Requires:  drupal6-addthis
Requires:  drupal6-admin_menu
Requires:  drupal6-advanced-help
Requires:  drupal6-ajax_poll
Requires:  drupal6-better_formats
Requires:  drupal6-block_class
Requires:  drupal6-calendar
Requires:  drupal6-cck
Requires:  drupal6-comment_bonus_api
Requires:  drupal6-context
Requires:  drupal6-context_menu_block
Requires:  drupal6-ctools
Requires:  drupal6-custom_breadcrumbs
Requires:  drupal6-date
Requires:  drupal6-devel
Requires:  drupal6-diff
Requires:  drupal6-eazylaunch
Requires:  drupal6-emfield
Requires:  drupal6-faq
Requires:  drupal6-features
Requires:  drupal6-filefield
Requires:  drupal6-fivestar
Requires:  drupal6-flag
Requires:  drupal6-freelinking
Requires:  drupal6-geshifilter
Requires:  drupal6-geoip
Requires:  drupal6-homebox
Requires:  drupal6-image
Requires:  drupal6-image_resize_filter
Requires:  drupal6-imageapi
Requires:  drupal6-imagecache

Requires:  drupal6-imagecache_profiles
Requires:  drupal6-imagefield
Requires:  drupal6-insert
Requires:  drupal6-jquery_ui-lib
Requires:  drupal6-link
Requires:  drupal6-markdown
Requires:  drupal6-media_vimeo
Requires:  drupal6-media_tudou
Requires:  drupal6-media_youtube
Requires:  drupal6-media_youku
Requires:  drupal6-mediawiki_filter
Requires:  drupal6-menu_block
Requires:  drupal6-messaging
Requires:  drupal6-notifications
Requires:  drupal6-node_import
Requires:  drupal6-og
Requires:  drupal6-openshift-custom_forms
Requires:  drupal6-openshift-features-application_quickstarts
Requires:  drupal6-openshift-features-blogs
Requires:  drupal6-openshift-features-forums
Requires:  drupal6-openshift-features-front_page
Requires:  drupal6-openshift-features-global_settings
Requires:  drupal6-openshift-features-reporting_csv_views
Requires:  drupal6-openshift-features-rules_by_category
Requires:  drupal6-openshift-features-user_profile
Requires:  drupal6-openshift-features-recent_activity_report
Requires:  drupal6-openshift-features-video
Requires:  drupal6-openshift-modals
Requires:  drupal6-openshift-og_comment_perms
Requires:  drupal6-openshift-redhat_acquia
Requires:  drupal6-openshift-redhat_events
Requires:  drupal6-openshift-redhat_frontpage
Requires:  drupal6-openshift-redhat_ideas
Requires:  drupal6-openshift-redhat_sso
Requires:  drupal6-openshift-theme
Requires:  drupal6-pathauto
Requires:  drupal6-path_redirect
Requires:  drupal6-prepopulate
Requires:  drupal6-rules
Requires:  drupal6-stringoverrides
Requires:  drupal6-token
Requires:  drupal6-user_badges
Requires:  drupal6-userpoints
Requires:  drupal6-userpoints_votingapi
Requires:  drupal6-vertical_tabs
Requires:  drupal6-views
Requires:  drupal6-views_bonus
Requires:  drupal6-views_customfield
Requires:  drupal6-views_datasource
Requires:  drupal6-vote_up_down
Requires:  drupal6-votingapi
Requires:  drupal6-wikitools
Requires:  drupal6-wysiwyg
Requires:  drupal6-openshift-features-community_wiki
Requires:  drupal6-clamav
Requires:  drupal6-xmlsitemap

# Security ClamAV Requirements
Requires:  clamav
Requires:  clamav-db

# Security RKHunter Requirements
Requires:  rkhunter

# Security OpenSCAP Requirements
Requires:  openscap
Requires:  openscap-content
Requires:  openscap-extra-probes
Requires:  openscap-python
Requires:  openscap-utils
Requires:  html2text

# Security mod_security Requirements for Apache
Requires:  mod_security

# Match the rubygem-activesupport RPM in STG and PROD
Requires: rubygem-activesupport

BuildArch: noarch

%description
Provides all the development dependencies to be able to run the OpenShift tests

%prep
%setup -q

%build

%install
rm -rf %{buildroot}

mkdir -p %{buildroot}%{devenvdir}
/bin/cp -adv * %{buildroot}%{devenvdir}

# Move over the init scripts so they get the right context
mkdir -p %{buildroot}%{_initddir}
mv %{buildroot}%{devenvdir}/init.d/* %{buildroot}%{_initddir}

mkdir -p %{buildroot}%{_var}/log/openshift/broker/

# Setup mcollective client log
touch %{buildroot}%{_var}/log/openshift/broker/mcollective-client.log

# Setup the jenkins jobs
mkdir -p %{buildroot}%{jenkins}/jobs
mv %{buildroot}%{devenvdir}%{jenkins}/jobs/* %{buildroot}%{jenkins}/jobs

# Add the SELinux policy files
mkdir -p %{buildroot}%{policydir}
/bin/cp %{buildroot}%{devenvdir}%{policydir}/* %{buildroot}%{policydir}

# Marking installation as a devenv
mkdir -p %{buildroot}/etc/openshift
touch %{buildroot}/etc/openshift/development

%clean
rm -rf %{buildroot}

%post

# Ensure httpd can access static content in site/broker (symlinks)
usermod -G libra_user -a apache

echo "
# Setup PATH, LD_LIBRARY_PATH and MANPATH for ruby-1.9
ruby19_dir=\$(dirname \`scl enable ruby193 \"which ruby\"\`)
export PATH=\$ruby19_dir:\$PATH

ruby19_ld_libs=\$(scl enable ruby193 \"printenv LD_LIBRARY_PATH\")
export LD_LIBRARY_PATH=\$ruby19_ld_libs:\$LD_LIBRARY_PATH

ruby19_manpath=\$(scl enable ruby193 \"printenv MANPATH\")
export MANPATH=\$ruby19_manpath:\$MANPATH" >> /etc/profile.d/openshift.sh.bak

source /etc/profile.d/openshift.sh.bak
cat /etc/profile.d/openshift.sh.bak >> /etc/sysconfig/mcollective
cat /etc/profile.d/openshift.sh.bak >> /root/.bashrc


# Install the Sauce Labs gems
gem install sauce --no-rdoc --no-ri
gem install zip --no-rdoc --no-ri

# Install hub for automatic pull request testing
gem install hub --no-rdoc --no-ri

# Install gems for sprint_status_script
gem install rally_rest_api --no-rdoc --no-ri
gem install kramdown --no-rdoc --no-ri

# Install gems for rhc to work on the devenv with ruby-1.9 
gem install rspec --version 1.3.0 --no-rdoc --no-ri
gem install fakefs --no-rdoc --no-ri
gem install httpclient --version 2.3.2 --no-rdoc --no-ri

# Move over all configs and scripts
/bin/cp -rf %{devenvdir}/etc/* %{_sysconfdir}
/bin/cp -rf %{devenvdir}/bin/* %{_bindir}
/bin/cp -rf %{devenvdir}/var/* %{_var}

# Setup node.conf for the devenv
cp -f /etc/openshift/node.conf.libra /etc/openshift/node.conf
restorecon /etc/openshift/node.conf || :
/sbin/service libra-data restart > /dev/null 2>&1 || :

# Clear the console.conf default community URL
sed -i 's|^COMMUNITY_URL=|#COMMUNITY_URL=|' /etc/openshift/console.conf

# Setup OPENSHIFT_CLOUD_DOMAIN for the devenv
mv -f /etc/openshift/env/OPENSHIFT_CLOUD_DOMAIN.libra /etc/openshift/env/OPENSHIFT_CLOUD_DOMAIN
restorecon /etc/openshift/env/OPENSHIFT_CLOUD_DOMAIN || :

# Add rsync key to authorized keys
cat %{brokerdir}/config/keys/rsync_id_rsa.pub >> /root/.ssh/authorized_keys

# Add deploy key
/bin/cp -rf %{devenvdir}/root/.ssh/* /root/.ssh/

chmod 0600 %{jenkins}/.ssh/id_rsa /root/.ssh/id_rsa
chmod 0644 %{jenkins}/.ssh/id_rsa.pub %{jenkins}/.ssh/known_hosts /root/.ssh/id_rsa.pub /root/.ssh/known_hosts 

# Move over new http configurations
/bin/cp -rf %{devenvdir}/httpd/* %{libradir}
/bin/cp -rf %{devenvdir}/httpd.conf %{sitedir}/httpd/
sed -i 's|^ErrorLog.*$|ErrorLog /var/log/openshift/site/httpd/error_log|' %{sitedir}/httpd/httpd.conf
sed -i 's|^CustomLog.*$|CustomLog /var/log/openshift/site/httpd/access_log combined|' %{sitedir}/httpd/httpd.conf
/bin/cp -rf %{devenvdir}/httpd.conf %{brokerdir}/httpd/
sed -i 's|^ErrorLog.*$|ErrorLog /var/log/openshift/broker/httpd/error_log|' %{brokerdir}/httpd/httpd.conf
sed -i 's|^CustomLog.*$|CustomLog /var/log/openshift/broker/httpd/access_log combined|' %{brokerdir}/httpd/httpd.conf
/bin/cp -f %{devenvdir}/client.cfg %{devenvdir}/server.cfg /etc/mcollective
/bin/cp -f %{devenvdir}/activemq.xml /etc/activemq
ln -s %{sitedir}/public/* %{htmldir}
ln -s /usr/lib64/httpd/modules/ %{sitedir}/httpd/modules
ln -s /usr/lib64/httpd/modules/ %{brokerdir}/httpd/modules

# Ensure /tmp and /var/tmp aren't world usable
#chmod o-rwX /tmp /var/tmp
#setfacl -m u:libra_passenger:rwx /tmp
#setfacl -m u:jenkins:rwx /tmp
#setfacl -m u:apache:rwx /tmp
#setfacl -m u:mysql:rwx /tmp
############# FIXME ############
#### Dirty hack until there's a mcollective fix
chmod o+rwX /tmp /var/tmp

# Jenkins specific setup
usermod -G libra_user jenkins
chown -R jenkins:jenkins /var/lib/jenkins

# Allow misc Openshift related Apache options
getsebool httpd_run_stickshift | grep -q -e 'on$' || /usr/sbin/setsebool -P httpd_run_stickshift=on || :

# Allow Apache to connect to Jenkins port 8081
getsebool httpd_can_network_connect | grep -q -e 'on$' || /usr/sbin/setsebool -P httpd_can_network_connect=on || :

# Allow polyinstantiation to work
getsebool allow_polyinstantiation | grep -q -e 'on$' || /usr/sbin/setsebool -P allow_polyinstantiation=on || :

# Allow httpd to relay
getsebool httpd_can_network_relay | grep -q -e 'on$' || /usr/sbin/setsebool -P httpd_can_network_relay=on || :

# Ensure that V8 in Node.js can compile JS for Rails asset compilation
getsebool httpd_execmem | grep -q -e 'on$' || /usr/sbin/setsebool -P httpd_execmem=on || :

# Allow httpd to verify dns records
getsebool httpd_verify_dns | grep -q -e 'on$' || /usr/sbin/setsebool -P httpd_verify_dns=on || :

# Allow memcached to bind to port 11212 so we can test multi-memcached environments
semanage port -l | grep memcache | grep 11212 > /dev/null
if [ $? -ne 0 ]
then
  semanage port -a -t memcache_port_t -p tcp 11212
  semanage port -a -t memcache_port_t -p udp 11212
fi

# Add policy for developement environment
cd %{policydir} ; make -f ../devel/Makefile
semodule -l | grep -q dhcpnamedforward || semodule -i dhcpnamedforward.pp
cd

# Disable IPv6
echo "net.ipv6.conf.all.disable_ipv6 = 1" >> /etc/sysctl.conf
echo "net.ipv6.conf.default.disable_ipv6 = 1" >> /etc/sysctl.conf
sysctl net.ipv6.conf.all.disable_ipv6=1 net.ipv6.conf.default.disable_ipv6=1

# Increase kernel semaphores to accomodate many httpds
echo "kernel.sem = 250  32000 32  4096" >> /etc/sysctl.conf
sysctl kernel.sem="250  32000 32  4096"

# Move ephemeral port range to accommodate app proxies
echo "net.ipv4.ip_local_port_range = 15000 35530" >> /etc/sysctl.conf
sysctl net.ipv4.ip_local_port_range="15000 35530"

# Increase the connection tracking table size
echo "net.netfilter.nf_conntrack_max = 1048576" >> /etc/sysctl.conf
sysctl net.netfilter.nf_conntrack_max=1048576

# Setup facts
/usr/libexec/mcollective/update_yaml.rb /etc/mcollective/facts.yaml
crontab -u root %{devenvdir}/crontab

# enable disk quotas, on initial build of image
[ -f /var/aquota.user ] || (
  /usr/bin/rhc-init-quota
  ls -lZ /var/aquota.user  | grep -q var_t && ( quotaoff /var && restorecon /var/aquota.user && quotaon /var )
)

# Setup swap for devenv
[ -f /.swap ] || ( /bin/dd if=/dev/zero of=/.swap bs=1024 count=1024000
    /sbin/mkswap -f /.swap
    /sbin/swapon /.swap
    echo "/.swap swap   swap    defaults        0 0" >> /etc/fstab
)

# Increase max SSH connections and tries to 40
perl -p -i -e "s/^#MaxSessions .*$/MaxSessions 40/" /etc/ssh/sshd_config
perl -p -i -e "s/^#MaxStartups .*$/MaxStartups 40/" /etc/ssh/sshd_config

# create a submodule repo for the tests
git init /root/submodule_test_repo
pushd /root/submodule_test_repo > /dev/null
    echo Submodule > index
    git add index
    git commit -m 'test'
popd > /dev/null

# Restore permissions
#/sbin/restorecon -R %{_sysconfdir}/qpid/pki
/sbin/restorecon -R %{libradir}
/sbin/restorecon -R /etc/drupal6

# Start services
service iptables restart
service activemq restart
#service qpidd restart
service mcollective start
service memcached-1 start
service memcached-2 start
service rhc-datastore configure
service rhc-datastore start
service rhc-site restart
service rhc-broker restart
service jenkins restart
service httpd restart --verbose 2>&1
service sshd restart
service openshift-node-web-proxy restart
chkconfig iptables on
chkconfig named on
#chkconfig qpidd on
chkconfig activemq on
chkconfig mcollective on
chkconfig memcached-1 on
chkconfig memcached-2 on
chkconfig rhc-datastore on
chkconfig rhc-site on
chkconfig rhc-broker on
chkconfig jenkins on
chkconfig httpd on

# CGroup services
service cgconfig start
service cgred start
service openshift-cgroups start
service libra-tc start
chkconfig cgconfig on
chkconfig cgred on
chkconfig openshift-cgroups on
chkconfig libra-tc on

# DHCP/DNS Service initialization
service network restart
service named restart

# Drupal Requirements
chkconfig mysqld on
service mysqld start

# Watchman services
chkconfig libra-watchman on || :
service libra-watchman start || :

# Populate mcollective certs
cd /etc/mcollective/ssl/clients
openssl genrsa -out mcollective-private.pem 1024 2> /dev/null
openssl rsa -in mcollective-private.pem -out mcollective-public.pem -outform PEM -pubout 2> /dev/null
chown libra_passenger:root mcollective-private.pem
chmod 460 mcollective-private.pem
cd

# Move static puppet certs in devenv
mkdir -p /var/lib/puppet/ssl/public_keys/
mkdir -p /var/lib/puppet/ssl/private_keys/
/bin/cp -f %{devenvdir}/puppet-public.pem /var/lib/puppet/ssl/public_keys/localhost.localdomain.pem
/bin/cp -f %{devenvdir}/puppet-private.pem /var/lib/puppet/ssl/private_keys/localhost.localdomain.pem

# Chgrp to wheel for rpm, dmesg, su, and sudo
/bin/chgrp wheel /bin/rpm
/bin/chgrp wheel /bin/dmesg
/bin/chgrp wheel /bin/su
/bin/chgrp wheel /usr/bin/sudo

# Chmod o-x for rpm, dmesg, su, and sudo
/bin/chmod 0750 /bin/rpm
/bin/chmod 0750 /bin/dmesg
/bin/chmod 4750 /bin/su
/bin/chmod 4110 /usr/bin/sudo

# Remove blank passwd for root in shadow
/bin/echo root:\!! | /usr/sbin/chpasswd -e

# Create OpenScap script
cat > /usr/local/bin/openscap.sh << EOF
# Create OpenScap results
/usr/bin/oscap xccdf eval --profile RHEL6-Default --results /var/log/xccdf-results.xml /usr/share/openscap/scap-rhel6-xccdf.xml
#/usr/bin/oscap oval eval --results /var/log/oval-results.xml /usr/share/openscap/scap-rhel6-oval.xml

# Validate the OpenScap results
#/usr/bin/oscap xccdf validate-xml /usr/share/openscap/scap-rhel6-xccdf.xml
#/usr/bin/oscap oval validate-xml /usr/share/openscap/scap-rhel6-oval.xml

# Create OpenScap HTML reports
/usr/bin/oscap xccdf generate report /var/log/xccdf-results.xml > /var/log/report-xccdf.html
#/usr/bin/oscap oval generate report /var/log/oval-results.xml > /var/log/report-oval.html
#/usr/bin/oscap xccdf generate report --oval-template /var/log/oval-results.xml /var/log/xccdf-results.xml > /var/log/report-xccdf-oval.html

# Create rsyslog file from html
/usr/bin/html2text -o /var/log/openscap_rsyslog.txt /var/log/report-xccdf.html
EOF

# Set mod_security.conf permissions
chmod 0644 /etc/httpd/conf.d/mod_security.conf

# Make OpenScap.sh executable
chmod 0750 /usr/local/bin/openscap.sh

# Remove all SUIDs - tkramer - testing in devenv
chmod u-s /usr/bin/staprun
# chmod u-s /usr/bin/chage
chmod u-s /usr/bin/chfn
# chmod u-s /usr/bin/gpasswd
chmod u-s /usr/bin/chsh
chmod u-s /usr/bin/sudoedit
# chmod u-s /usr/bin/passwd
# chmod u-s /usr/bin/crontab
# chmod u-s /usr/bin/at
chmod u-s /usr/bin/sudo
# chmod u-s /usr/bin/pkexec
# chmod u-s /usr/bin/newgrp
# chmod u-s /usr/libexec/polkit-1/polkit-agent-helper-1
# BZ844881 - was chmod 4711
chmod 4710 /usr/libexec/pt_chown
# chmod u-s /usr/libexec/openssh/ssh-keysign
# chmod u-s /usr/sbin/suexec
# BZ817670 - /usr/sbin/usernetctl was 4755
chmod 4750 /usr/sbin/usernetctl
# BZ817668 - /usr/sbin/userhelper was 4711
chmod 4710 /usr/sbin/userhelper
# BZ873080 - /sbin/pam_timestamp_check was 4755
chmod 4750 /sbin/pam_timestamp_check
chmod u-s /bin/ping6
chmod u-s /bin/mount
# chmod u-s /bin/su
# chmod u-s /bin/ping
chmod u-s /bin/umount
# chmod u-s /sbin/pam_timestamp_check
chmod u-s /sbin/unix_chkpwd
# chmod u-s /lib64/dbus-1/dbus-daemon-launch-helper
chmod 4750 /usr/libexec/polkit-1/polkit-agent-helper-1

# Remove all SGIDs - tkramer
# chmod g-s /usr/bin/ssh-agent
chmod g-s /usr/bin/wall
# chmod g-s /usr/bin/screen
chmod g-s /usr/bin/locate
# chmod g-s /usr/bin/lockfile
# chmod g-s /usr/bin/write
# chmod g-s /usr/libexec/utempter/utempter
# chmod g-s /usr/sbin/postqueue
# chmod g-s /usr/sbin/postdrop
# chmod g-s /bin/cgexec
# chmod g-s /sbin/netreport

# Make grub.conf readable only to user and group - not other - tkramer
chmod 600 /boot/grub/grub.conf

# Turn off rsyslog compatibility check in OpenScap
sed 's/rule-1125" selected="true/rule-1125" selected="false/' /usr/share/openscap/scap-rhel6-xccdf.xml > /usr/share/openscap/scap-rhel6-xccdf.xml.tmp
mv -f /usr/share/openscap/scap-rhel6-xccdf.xml.tmp /usr/share/openscap/scap-rhel6-xccdf.xml

# Add user nagios_monitor to wheel group for running rpm, dmesg, su, and sudo
/usr/bin/gpasswd -a nagios_monitor wheel

# Populate Drupal Database 
echo "select count(*) from users;" | mysql -u root libra > /dev/null 2>&1 || zcat /usr/share/drupal6/sites/default/openshift-dump.gz | mysql -u root

# Create place to drop proxy mod_cache files
mkdir -p /srv/cache/mod_cache
chmod 750 /srv/cache/mod_cache
chown apache:apache /srv/cache/mod_cache

# BZ835097 - remove o-x from tcpdump - was 755
chmod 750 /usr/sbin/tcpdump

# BZ834487 - remove o-x from /etc/openshift/resource_limit files - was 644
chmod 640 /etc/openshift/resource_limits.conf.c9
chmod 640 /etc/openshift/resource_limits.conf.exlarge
chmod 640 /etc/openshift/resource_limits.conf.high_density
chmod 640 /etc/openshift/resource_limits.conf.jumbo
chmod 640 /etc/openshift/resource_limits.conf.large
chmod 640 /etc/openshift/resource_limits.conf.medium
chmod 640 /etc/openshift/resource_limits.conf.micro
chmod 640 /etc/openshift/resource_limits.conf.small
chmod 640 /etc/openshift/resource_limits.template

# BZ949543 - resource_limit.conf now owned by rubygem-o-o-node,
# in devenv use the one supplied by rhc-node
cp /etc/openshift/resource_limits.conf{.small,}

# Remove Other rights from iptables-multi - was 755
chmod 750 /sbin/iptables-multi

# Remove Other rights from ip6tables-multi - was 755
chmod 750 /sbin/ip6tables-multi

# Remove Other rights from crontab - was 4755 - BZ856939
chmod 750 /usr/bin/crontab

# Remove Other rights from at - was 4755 - BZ856933
chmod 750 /usr/bin/at

# Fix devenv log file ownership
chown root:libra_user %{_var}/log/openshift/broker/mcollective-client.log

## For RKHUNTER to not use tmp any more
# Added nagios_monitor user to match STG and PROD
useradd nagios_monitor
# Change /var/log/rkhunter perms
chown -R root:nagios_monitor /var/log/rkhunter
chmod -R 770 /var/log/rkhunter

# Remove Virtual Consoles from /etc/securetty for OpenScap
sed '/^vc\//d' /etc/securetty > /tmp/no_vc
mv /tmp/no_vc /etc/securetty

# Create Disable Transport for OpenScap check
cat > /etc/modprobe.d/disable_transport.conf << EOF
# Disables the latest transports in RHEL6 for OpenScap checks
install dccp /bin/true
install sctp /bin/true
install rds /bin/true
install tipc /bin/true
EOF

# Make sure that the datastore is available before adding test users
for i in {1..5}
do
  echo "show collections" | mongo -u openshift -p mooo openshift_broker_dev
  if [ $? -eq 0 ]
  then
    break
  else
    if [ $i -eq 1 ]
    then
      service rhc-datastore restart
    fi
    echo "Rechecking datastore....."
    sleep 1
  fi
done

# Create a known test user with medium-sized gears - nhr
# This must be done before the deployment of application templates!
cd /var/www/openshift/broker
echo "Creating named test user"
curl -k https://localhost/broker/rest/user -u user_with_multiple_gear_sizes@test.com:pass
if [ $? -eq 0 ]
then
  echo "Adding medium gear size to user"
  /usr/sbin/oo-admin-ctl-user -l user_with_multiple_gear_sizes@test.com --addgearsize medium
else
  echo "user_with_multiple_gear_sizes could not be created!"
fi

# Create a test user with additional storage capabilities
echo "Creating test user:  user_with_extra_storage@test.com"
curl -k https://localhost/broker/rest/user -u user_with_extra_storage@test.com:pass
if [ $? -eq 0 ]
then
  echo "Adding additional storage to user"
  /usr/sbin/oo-admin-ctl-user -l user_with_extra_storage@test.com --setmaxstorage 10 --setmaxgears 10
else
  echo "user_with_extra_storage could not be created!"
fi

# Create a test user with ssl certificates capabilities
echo "Creating test user:  user_with_certificate_capabilities@test.com"
curl -k https://localhost/broker/rest/user -u user_with_certificate_capabilities@test.com:pass
if [ $? -eq 0 ]
then
  echo "Adding ssh certificate capabilities to user"
  /usr/sbin/oo-admin-ctl-user -l user_with_certificate_capabilities@test.com --allowprivatesslcertificates true
else
  echo "user_with_certificate_capabilities could not be created!"
fi

# Hack to resolve parser error
# See https://github.com/cucumber/gherkin/issues/182
if [ -f /usr/lib/ruby/gems/1.8/gems/gherkin-2.2.4/lib/gherkin/i18n.rb ]
then
  sed -i 's/listener, force_ruby=false/listener, force_ruby=true/' \
      /usr/lib/ruby/gems/1.8/gems/gherkin-2.2.4/lib/gherkin/i18n.rb
fi

# BZ864807 - clean up redundant assets to prevent JS oddities
#            in rails development mode.
cd /var/www/openshift/site && /usr/bin/scl enable ruby193 "rake assets:clean"

# Set up ClamAV
/usr/sbin/setsebool -P clamscan_can_scan_system 1

# Configure Drupal for the first time
/etc/drupal6/drupal-setup.sh

# Install the carts
oo-admin-cartridge --recursive -a install -s /usr/libexec/openshift/cartridges/v2/

# PhantomJS install
mkdir /tmp/phantomjs
cd /tmp/phantomjs
wget https://phantomjs.googlecode.com/files/phantomjs-1.9.0-linux-x86_64.tar.bz2
tar --extract --file=phantomjs-1.9.0-linux-x86_64.tar.bz2 phantomjs-1.9.0-linux-x86_64/bin/phantomjs
cp phantomjs-1.9.0-linux-x86_64/bin/phantomjs /usr/local/bin
cd -
rm -rf /tmp/phantomjs

%files
%defattr(-,root,root,-)
%attr(0660,-,-) %{_var}/log/openshift/broker/mcollective-client.log
%config(noreplace) %{jenkins}/jobs/*/*
%{jenkins}/jobs/sync_up.rb
%{jenkins}/jobs/sync_down.rb
%{devenvdir}
%{_initddir}/rhc-datastore
%{_initddir}/rhc-broker
%{_initddir}/rhc-site
%{_initddir}/sauce-connect
%{_initddir}/memcached-1
%{_initddir}/memcached-2
%{policydir}/*
/etc/openshift/development

%changelog
* Wed Apr 24 2013 Adam Miller <admiller@redhat.com> 1.7.9-1
- exclude mongodb from epel (admiller@redhat.com)

* Tue Apr 16 2013 Troy Dawson <tdawson@redhat.com> 1.7.8-1
- Symlink drupal favicon into root drupal directory (ccoleman@redhat.com)
- Merge pull request #1192 from smarterclayton/bug_952187_fix_error_documents
  (dmcphers@redhat.com)
- Bug 952187 - Update correct server file (ccoleman@redhat.com)

* Mon Apr 15 2013 Adam Miller <admiller@redhat.com> 1.7.7-1
- Merge pull request #1179 from fotioslindiakos/postgres_v2
  (dmcphers@redhat.com)
- Fixing devenv.spec (fotios@redhat.com)
- Merge pull request #1178 from jtharris/features/Card6 (dmcphers@redhat.com)
- Added postgres v2 cartridge to spec (fotios@redhat.com)
- Adding basic phantomjs install. (jharris@redhat.com)

* Fri Apr 12 2013 Adam Miller <admiller@redhat.com> 1.7.6-1
- rhc-devenv now needs to ensure openshift-node-web-proxy is started
  (bleanhar@redhat.com)
- Call the ruby mcs label generator directly for speed. (rmillner@redhat.com)
- Merge pull request #1164 from smarterclayton/origin_ui_37_error_pages
  (dmcphers+openshiftbot@redhat.com)
- Adding phpmyadmin (dmcphers@redhat.com)
- Add 404, 500, and 503 to the devenv (ccoleman@redhat.com)
- Merge pull request #1163 from tkramer-
  rh/dev/tkramer/mod_security/remove_rules (dmcphers@redhat.com)
- Security - mod_security remove all rules for devenv (tkramer@redhat.com)
- Add generic error pages to the product. (ccoleman@redhat.com)

* Thu Apr 11 2013 Adam Miller <admiller@redhat.com> 1.7.5-1
- add jbossas to devenv.spec (bdecoste@gmail.com)

* Wed Apr 10 2013 Adam Miller <admiller@redhat.com> 1.7.4-1
- Merge pull request #1141 from sosiouxme/bz949543 (dmcphers@redhat.com)
- <rhc-node> bug 949543 transfer RPM ownership of resource_limits.conf to
  rubygem-o-o-node additionally, have devenv cp the one from rhc-node so it
  will be the same. (lmeyer@redhat.com)

* Tue Apr 09 2013 Adam Miller <admiller@redhat.com> 1.7.3-1
- Adding openshift-origin-cartridge-cron (calfonso@redhat.com)
- Merge pull request #1133 from jwhonce/wip/rockmongo
  (dmcphers+openshiftbot@redhat.com)
- WIP Cartridge Refactor - RockMongo cartridge (jhonce@redhat.com)

* Mon Apr 08 2013 Adam Miller <admiller@redhat.com> 1.7.2-1
- syncing jenkins jobs (dmcphers@redhat.com)
- adding v2 10gen mms agent (dmcphers@redhat.com)
- Merge pull request #1123 from ironcladlou/nodejs_v2
  (dmcphers+openshiftbot@redhat.com)
- Add nodejs v2 package (ironcladlou@gmail.com)
- adding java client merge testing (dmcphers@redhat.com)
- syncing jenkins jobs (dmcphers@redhat.com)
- metrics WIP (dmcphers@redhat.com)
- syncing jenkins jobs (dmcphers@redhat.com)
- syncing jenkins jobs (dmcphers@redhat.com)
- Fix for bug 928625  - Removing extra dashes from command argument
  (abhgupta@redhat.com)

* Thu Mar 28 2013 Adam Miller <admiller@redhat.com> 1.7.1-1
- bump_minor_versions for sprint 26 (admiller@redhat.com)

* Wed Mar 27 2013 Adam Miller <admiller@redhat.com> 1.6.7-1
- Fixed spec for user with SSL certificate capabilities (ffranz@redhat.com)
- More tests to SSL certificates (ffranz@redhat.com)
- cleanup unused snapshots and volumes (dmcphers@redhat.com)
- adding haproxy to devenv (dmcphers@redhat.com)
- Merge pull request #1079 from abhgupta/bad_response_threshold
  (dmcphers@redhat.com)
- Increasing bad response threshold to fix broker_extended tests
  (abhgupta@redhat.com)
- Fix for bug 924717 (abhgupta@redhat.com)
- adding diy (dmcphers@redhat.com)

* Tue Mar 26 2013 Adam Miller <admiller@redhat.com> 1.6.6-1
- getting jenkins working (dmcphers@redhat.com)
- Merge pull request #1069 from
  smarterclayton/hardcode_script_name_for_memcached
  (dmcphers+openshiftbot@redhat.com)
- Hardcode the script name for memcached init.d scripts - it changes depending
  on runlevel (ccoleman@redhat.com)

* Mon Mar 25 2013 Adam Miller <admiller@redhat.com> 1.6.5-1
- adding cron and eap (dmcphers@redhat.com)

* Thu Mar 21 2013 Adam Miller <admiller@redhat.com> 1.6.4-1
- Add openshift-origin-cartridge-jbossews v2 cart to Requires
  (ironcladlou@gmail.com)
- trying a larger shun threshold (dmcphers@redhat.com)
- Add v2 mysql to devenv.spec (pmorie@gmail.com)
- Merge pull request #1037 from danmcp/master (dmcphers@redhat.com)
- Merge pull request #1035 from smarterclayton/selinux_for_alt_memcache_port
  (dmcphers+openshiftbot@redhat.com)
- more work getting carts installed (dmcphers@redhat.com)
- Memcached should be allowed to run on port 11212 in the devenv
  (ccoleman@redhat.com)
- getting jenkins building (dmcphers@redhat.com)

* Mon Mar 18 2013 Adam Miller <admiller@redhat.com> 1.6.3-1
- Adding memcached files to RPM list (mhicks@redhat.com)
- Paths for memcached services were wrong (ccoleman@redhat.com)
- Implement memcached on devenv (ccoleman@redhat.com)
- adjust to the php-5.3 dir (dmcphers@redhat.com)

* Thu Mar 14 2013 Adam Miller <admiller@redhat.com> 1.6.2-1
- Merge pull request #1016 from tkramer-rh/dev/tkramer/security/mod_security
  (dmcphers+openshiftbot@redhat.com)
- install the new carts as part of the devenv (dmcphers@redhat.com)
- Security - mod_security add bad robots and openshift policies
  (tkramer@redhat.com)
- Security - mod_security - re-enable check in mod_security conf to not deny
  just log (tkramer@redhat.com)
- syncing jenkins jobs (dmcphers@redhat.com)
- adding runtime_other tests (dmcphers@redhat.com)
- Security - mod_security - change mod_security config file from an echo in the
  spec to a flat file (tkramer@redhat.com)
- Merge pull request #994 from tkramer-
  rh/dev/tkramer/security/mod_security_conf (dmcphers+openshiftbot@redhat.com)
- Add restart on mongo when doa (dmcphers@redhat.com)
- Security - mod_security.conf standardized configuration file
  (tkramer@redhat.com)
- Add feature to test while waiting on a merge (dmcphers@redhat.com)

* Thu Mar 07 2013 Adam Miller <admiller@redhat.com> 1.6.1-1
- bump_minor_versions for sprint 25 (admiller@redhat.com)

* Thu Mar 07 2013 Adam Miller <admiller@redhat.com> 1.5.9-1
- Masks out testing STS on the app router and we do not need it on devenv.
  (rmillner@redhat.com)

* Tue Mar 05 2013 Adam Miller <admiller@redhat.com> 1.5.8-1
- remove temp mongoid gem patch (dmcphers@redhat.com)
- Security - add mod_security for Apache (tkramer@redhat.com)

* Fri Mar 01 2013 Adam Miller <admiller@redhat.com> 1.5.7-1
- Add mock-plugin to devenv.spec (pmorie@gmail.com)

* Tue Feb 26 2013 Adam Miller <admiller@redhat.com> 1.5.6-1
- Add a crontab line to purge expired authorizations. (ccoleman@redhat.com)
- Merge pull request #925 from smarterclayton/session_auth_support_2
  (dmcphers+openshiftbot@redhat.com)
- Temporarily add mongoid to devenv (ccoleman@redhat.com)
- Merge remote-tracking branch 'origin/master' into session_auth_support_2
  (ccoleman@redhat.com)
- Merge remote-tracking branch 'origin/master' into session_auth_support_2
  (ccoleman@redhat.com)
- Tweak the log change so that is optional for developers running Rails
  directly, has same behavior on devenv, and allows more control over the path
  (ccoleman@redhat.com)
- Merge remote-tracking branch 'origin/master' into session_auth_support_2
  (ccoleman@redhat.com)
- Merge remote-tracking branch 'origin/master' into session_auth_support_2
  (ccoleman@redhat.com)
- Add the read scope.  Curl insecure doesn't create extra storage test.
  (ccoleman@redhat.com)
- Merge remote-tracking branch 'origin/master' into session_auth_support_2
  (ccoleman@redhat.com)
- Merge branch 'isolate_api_behavior_from_base_controller' into
  session_auth_support_2 (ccoleman@redhat.com)
- Changes to the broker to match session auth support in the origin
  (ccoleman@redhat.com)

* Mon Feb 25 2013 Adam Miller <admiller@redhat.com> 1.5.5-2
- bump Release for fixed build target rebuild (admiller@redhat.com)

* Mon Feb 25 2013 Adam Miller <admiller@redhat.com> 1.5.5-1
- Devenv logs not getting output correctly (ccoleman@redhat.com)
- Merge pull request #918 from
  smarterclayton/bug_912286_cleanup_robots_misc_for_split
  (dmcphers+openshiftbot@redhat.com)
- Use a more generic redirect to old content, integrate new URL
  (ccoleman@redhat.com)
- Bug 912286 - Cleanup robots.txt and others for split (ccoleman@redhat.com)
- new brew tag and dist-tag (admiller@redhat.com)
- setup-devenv-repos.sh move to 6.4 (admiller@redhat.com)
- Tweak the log change so that is optional for developers running Rails
  directly, has same behavior on devenv, and allows more control over the path
  (ccoleman@redhat.com)

* Wed Feb 20 2013 Adam Miller <admiller@redhat.com> 1.5.4-1
- add action required prop (dmcphers@redhat.com)

* Tue Feb 19 2013 Adam Miller <admiller@redhat.com> 1.5.3-1
- Switch from VirtualHosts to mod_rewrite based routing to support high
  density. (rmillner@redhat.com)
- Bug 902243 - Guard for existing quotas (jhonce@redhat.com)
- Add V2 mock cartridge to devenv.spec (pmorie@gmail.com)
- syncing jenkins jobs (dmcphers@redhat.com)
- added pam_cgroup.so to initial sshd pam settings (markllama@gmail.com)

* Fri Feb 08 2013 Adam Miller <admiller@redhat.com> 1.5.2-1
- US3291 US3292 US3293 - Move community to www.openshift.com
  (ccoleman@redhat.com)
- Bug 908282 (dmcphers@redhat.com)

* Thu Feb 07 2013 Adam Miller <admiller@redhat.com> 1.5.1-1
- bump_minor_versions for sprint 24 (admiller@redhat.com)

* Wed Feb 06 2013 Adam Miller <admiller@redhat.com> 1.4.7-1
- Bug 908417: Do not force users to https. (mrunalp@gmail.com)
- more coverage adjustments (dmcphers@redhat.com)
- more clean up from log move, fix BZ#907808 (admiller@redhat.com)

* Tue Feb 05 2013 Adam Miller <admiller@redhat.com> 1.4.6-1
- Add Ruby 1.9 httpclient gem to devenv (ironcladlou@gmail.com)

* Mon Feb 04 2013 Adam Miller <admiller@redhat.com> 1.4.5-1
- Merge pull request #827 from fotioslindiakos/storage
  (dmcphers+openshiftbot@redhat.com)
- Merge pull request #812 from maxamillion/dev/admiller/move_logs
  (dmcphers+openshiftbot@redhat.com)
- Give storage user more gears for testing (fotios@redhat.com)
- Use oo-admin-ctl-user script to modify max storage (fotios@redhat.com)
- move all logs to /var/log/openshift/ so we can logrotate properly
  (admiller@redhat.com)

* Mon Feb 04 2013 Adam Miller <admiller@redhat.com> 1.4.4-1
- working on testing coverage (dmcphers@redhat.com)
- Merge pull request #834 from lnader/improve-test-coverage
  (dmcphers+openshiftbot@redhat.com)
- Bug 903325 (lnader@redhat.com)

* Fri Feb 01 2013 Adam Miller <admiller@redhat.com> 1.4.3-1
- Add community carts - python 2.7 + 3.3 to install on a devenv.
  (smitram@gmail.com)

* Tue Jan 29 2013 Adam Miller <admiller@redhat.com> 1.4.2-1
- Bug 892821 (dmcphers@redhat.com)
- Bug 888692 (dmcphers@redhat.com)
- Bug 902286 (dmcphers@redhat.com)
- move clamav update to base ami (dmcphers@redhat.com)
- Merge pull request #789 from tkramer-rh/dev/tkramer/security/rubygem-
  activesupport_match_stg_prod (dmcphers+openshiftbot@redhat.com)
- Security - Added rubygem-activesupport to match stg and prod
  (tkramer@redhat.com)
- fix li-cleanup-util script, delete old mongo datastore tests
  (rpenta@redhat.com)
- Fix li-users-delete-util script (rpenta@redhat.com)
- run rake tests using 'openshift_broker_test' mongo database
  (rpenta@redhat.com)
- Bug 892125 (dmcphers@redhat.com)
- missing call to force delete (dmcphers@redhat.com)
- fix test user creation (rchopra@redhat.com)
- removing txt records (dmcphers@redhat.com)
- fix all the cloud_user.find passing login falls (dmcphers@redhat.com)
- fixup accept node and several cloud user usages (dmcphers@redhat.com)
- test case fixes (dmcphers@redhat.com)

* Wed Jan 23 2013 Adam Miller <admiller@redhat.com> 1.4.1-1
- bump_minor_versions for sprint 23 (admiller@redhat.com)

* Wed Jan 23 2013 Adam Miller <admiller@redhat.com> 1.3.8-1
- Bug 902633 (dmcphers@redhat.com)

* Mon Jan 21 2013 Adam Miller <admiller@redhat.com> 1.3.7-1
- enable direct addressing mode (dmcphers@redhat.com)
- BZ 896364: Fix newline at end of file. (rmillner@redhat.com)

* Thu Jan 17 2013 Adam Miller <admiller@redhat.com> 1.3.6-1
- Security remove other rights from /usr/libexec/polkit-1/polkit-agent-helper-1
  (tkramer@redhat.com)

* Wed Jan 16 2013 Adam Miller <admiller@redhat.com> 1.3.5-1
- Fix BZ875910 (pmorie@gmail.com)

* Thu Jan 10 2013 Adam Miller <admiller@redhat.com> 1.3.4-1
- Round 2: Update broker and site configs to 3.0.17 passenger
  (admiller@redhat.com)
- Revert "Update broker and site configs to 3.0.17 passenger"
  (admiller@redhat.com)
- Update broker and site configs to 3.0.17 passenger (admiller@redhat.com)
- enable ews2 (bdecoste@gmail.com)
- devenv: add drupal6-xmlsitemap to spec (ansilva@redhat.com)
- BZ BZ859471: Conform to section 7.2 of RFC 6797. (rmillner@redhat.com)
- Revert "change site and broker confs for passenger 3.0.17"
  (admiller@redhat.com)

* Thu Dec 20 2012 William DeCoste <wdecoste@redhat.com> 1.3.3-1
- enable ews2

* Tue Dec 18 2012 Adam Miller <admiller@redhat.com> 1.3.2-1
- change site and broker confs for passenger 3.0.17 (admiller@redhat.com)

* Wed Dec 12 2012 Adam Miller <admiller@redhat.com> 1.3.1-1
- bump_minor_versions for sprint 22 (admiller@redhat.com)

* Wed Dec 12 2012 Adam Miller <admiller@redhat.com> 1.2.9-1
- Merge pull request #714 from tkramer-rh/dev/tkramer/security/clamav_drupal
  (openshift+bot@redhat.com)
- Security - Enable ClamAV with Drupal plugin - selinux enabled
  (tkramer@redhat.com)
- workaround for BZ 885905 (admiller@redhat.com)

* Tue Dec 11 2012 Adam Miller <admiller@redhat.com> 1.2.8-1
- Revert "work around for BZ 885905" (admiller@redhat.com)
- work around for BZ 885905 (admiller@redhat.com)
- Security - change ClamAV and Drupal to ondemand scan and run as user clam
  (tkramer@redhat.com)
- Merge pull request #704 from tkramer-rh/dev/tkramer/security/CLAMAV3
  (openshift+bot@redhat.com)
- Security - Change clamav and drupal to run as clam and ondemand scanning
  (tkramer@redhat.com)

* Mon Dec 10 2012 Adam Miller <admiller@redhat.com> 1.2.7-1
- Security - Add more automation to the ClamAV for Drupal install
  (tkramer@redhat.com)

* Fri Dec 07 2012 Adam Miller <admiller@redhat.com> 1.2.6-1
- Merge pull request #694 from tkramer-
  rh/dev/tkramer/security/Add_ClamAV_to_Drupal (dmcphers@redhat.com)
- Security - Added ClamAV for Drupal (tkramer@redhat.com)

* Thu Dec 06 2012 Adam Miller <admiller@redhat.com> 1.2.5-1
- Merge pull request #691 from ramr/dev/websockets (openshift+bot@redhat.com)
- Add dependency on node-proxy and setup ports for node-web-proxy (8000 and
  8443) with appropriate connection limits. (ramr@redhat.com)

* Wed Dec 05 2012 Adam Miller <admiller@redhat.com> 1.2.4-1
- Set proxy-initial-not-pooled on devenv (ccoleman@redhat.com)
- Merge pull request #684 from jtharris/test_user (openshift+bot@redhat.com)
- syncing jenkins jobs (dmcphers@redhat.com)
- Adding test user with extra storage capabilities. (jharris@redhat.com)

* Tue Dec 04 2012 Adam Miller <admiller@redhat.com> 1.2.3-1
- Use activemq connector for mcollective. (pmorie@gmail.com)
- fixing mongo connection issues for build (dmcphers@redhat.com)
- Using better types for mco (dmcphers@redhat.com)

* Thu Nov 29 2012 Adam Miller <admiller@redhat.com> 1.2.2-1
- various mcollective changes getting ready for 2.2 (dmcphers@redhat.com)
- Remove unused phpmoadmin cartridge (jhonce@redhat.com)
- syncing jenkins scripts (dmcphers@redhat.com)
- usage and exit code cleanup (dmcphers@redhat.com)
- use $? the right way (dmcphers@redhat.com)
- using oo-ruby (dmcphers@redhat.com)
- syncing jenkins jobs (dmcphers@redhat.com)

* Sat Nov 17 2012 Adam Miller <admiller@redhat.com> 1.2.1-1
- bump_minor_versions for sprint 21 (admiller@redhat.com)

* Fri Nov 16 2012 Adam Miller <admiller@redhat.com> 1.1.8-1
- Merge pull request #635 from jwhonce/master (openshift+bot@redhat.com)
- Run oo-last-access under Ruby 1.9.3 (jhonce@redhat.com)

* Fri Nov 16 2012 Adam Miller <admiller@redhat.com> 1.1.7-1
- syncing jenkins jobs (dmcphers@redhat.com)

* Thu Nov 15 2012 Adam Miller <admiller@redhat.com> 1.1.6-1
- more ruby 1.9 changes (dmcphers@redhat.com)
- Merge pull request #620 from bdecoste/master (openshift+bot@redhat.com)
- BZ844858 (bdecoste@gmail.com)

* Wed Nov 14 2012 Adam Miller <admiller@redhat.com> 1.1.5-1
- Merge pull request #612 from smarterclayton/us3046_quickstarts_and_app_types
  (openshift+bot@redhat.com)
- Merge remote-tracking branch 'origin/master' into
  us3046_quickstarts_and_app_types (ccoleman@redhat.com)
- Merge remote-tracking branch 'origin/master' into
  us3046_quickstarts_and_app_types (ccoleman@redhat.com)
- Disable reusing a pooled connection so as to avoid the 502 proxy error during
  test runs when PHP apps are created (ccoleman@redhat.com)
- Disable template generation and installation during the build
  (ccoleman@redhat.com)
- US3046 - Implement quickstarts in drupal and react to changes in console
  (ccoleman@redhat.com)

* Wed Nov 14 2012 Adam Miller <admiller@redhat.com> 1.1.4-1
- Merge pull request #614 from danmcp/master (openshift+bot@redhat.com)
- migration efficiency changes (dmcphers@redhat.com)
- fix aria tests (dmcphers@redhat.com)
- Fixing gemspecs (kraman@gmail.com)
- sclizing gems (dmcphers@redhat.com)
- Fix for Bug 876100 (jhonce@redhat.com)
- Fix for Bug 873543 (jhonce@redhat.com)

* Mon Nov 12 2012 Adam Miller <admiller@redhat.com> 1.1.3-1
- Missed a few locations to update the UID. (rmillner@redhat.com)
- trying again (bdecoste@gmail.com)

* Thu Nov 08 2012 Adam Miller <admiller@redhat.com> 1.1.2-1
- Increase the table sizes to cover 15000 nodes in dev and prod.
  (rmillner@redhat.com)
- Fix for Bug 873543 (jhonce@redhat.com)
- Security change perms for BZ817670_BZ817668 BZ873080 (tkramer@redhat.com)
- Security - remove other perms from userhelper and usernetctl -
  BZ817670_BZ817668 (tkramer@redhat.com)
- syncing jenkins jobs (dmcphers@redhat.com)
- syncing jenkins jobs (dmcphers@redhat.com)
- adding enterprise-1.0 repo (dmcphers@redhat.com)

* Thu Nov 01 2012 Adam Miller <admiller@redhat.com> 1.1.1-1
- bump_minor_versions for sprint 20 (admiller@redhat.com)
