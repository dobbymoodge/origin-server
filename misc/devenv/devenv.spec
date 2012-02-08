%define htmldir %{_localstatedir}/www/html
%define libradir %{_localstatedir}/www/libra
%define brokerdir %{_localstatedir}/www/libra/broker
%define sitedir %{_localstatedir}/www/libra/site
%define devenvdir %{_sysconfdir}/libra/devenv
%define jenkins %{_sharedstatedir}/jenkins

Summary:   Dependencies for OpenShift development
Name:      rhc-devenv
Version:   0.86.1
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
Requires:  rhc-cartridge-php-5.3
Requires:  rhc-cartridge-wsgi-3.2
Requires:  rhc-cartridge-rack-1.1
Requires:  rhc-cartridge-jbossas-7.0
Requires:  rhc-cartridge-perl-5.10
Requires:  rhc-cartridge-mysql-5.1
Requires:  rhc-cartridge-phpmyadmin-3.4
Requires:  rhc-cartridge-jenkins-1.4
Requires:  rhc-cartridge-raw-0.1
Requires:  rhc-cartridge-jenkins-client-1.4
Requires:  rhc-cartridge-metrics-0.1
Requires:  rhc-cartridge-mongodb-2.0
Requires:  rhc-cartridge-phpmoadmin-1.0
Requires:  rhc-cartridge-rockmongo-1.1
Requires:  rhc-cartridge-10gen-mms-agent-0.1
Requires:  rhc-cartridge-postgresql-8.4
Requires:  rhc-cartridge-cron-1.4
Requires:  rhc-cartridge-haproxy-1.4
Requires:  qpid-cpp-server
Requires:  qpid-cpp-server-ssl
Requires:  puppet
Requires:  rubygem-cucumber
Requires:  rubygem-mechanize
Requires:  rubygem-mocha
Requires:  rubygem-rspec
Requires:  rubygem-nokogiri
Requires:  charlie
Requires:  pam
Requires:  pam-devel

# CI Requirements
Requires:  jenkins
Requires:  tito

BuildArch: noarch

%description
Provides all the development dependencies to be able to run the OpenShift tests

%prep
%setup -q

%build

%install
rm -rf %{buildroot}

mkdir -p %{buildroot}%{devenvdir}
cp -adv * %{buildroot}%{devenvdir}

# Move over the init scripts so they get the right context
mkdir -p %{buildroot}%{_initddir}
mv %{buildroot}%{devenvdir}/init.d/* %{buildroot}%{_initddir}

mkdir -p %{buildroot}%{brokerdir}/log
mkdir -p %{buildroot}%{sitedir}/log

# Setup mcollective client log
touch %{buildroot}%{brokerdir}/log/mcollective-client.log

# Setup rails development logs
touch %{buildroot}%{brokerdir}/log/development.log
touch %{buildroot}%{sitedir}/log/development.log

# Setup the jenkins jobs
mkdir -p %{buildroot}%{jenkins}/jobs
mv %{buildroot}%{devenvdir}%{jenkins}/jobs/* %{buildroot}%{jenkins}/jobs

%clean
rm -rf %{buildroot}

%post

# Install the Sauce Labs gems
gem install sauce --no-rdoc --no-ri
gem install zip --no-rdoc --no-ri

# Move over all configs and scripts
cp -rf %{devenvdir}/etc/* %{_sysconfdir}
cp -rf %{devenvdir}/bin/* %{_bindir}
cp -rf %{devenvdir}/var/* %{_localstatedir}

# Add rsync key to authorized keys
cat %{brokerdir}/config/keys/rsync_id_rsa.pub >> /root/.ssh/authorized_keys

# Move over new http configurations
cp -rf %{devenvdir}/httpd/* %{libradir}
cp -rf %{devenvdir}/httpd.conf %{sitedir}/httpd/
cp -rf %{devenvdir}/httpd.conf %{brokerdir}/httpd/
cp -f %{devenvdir}/client.cfg %{devenvdir}/server.cfg /etc/mcollective
mkdir -p %{sitedir}/httpd/logs
mkdir -p %{sitedir}/httpd/run
mkdir -p %{brokerdir}/httpd/logs
mkdir -p %{brokerdir}/httpd/run
ln -s %{sitedir}/public/* %{htmldir}
ln -s /usr/lib64/httpd/modules/ %{sitedir}/httpd/modules
ln -s /usr/lib64/httpd/modules/ %{brokerdir}/httpd/modules

# Ensure /tmp and /var/tmp aren't world usable

chmod o-rwX /tmp /var/tmp
setfacl -m u:libra_passenger:rwx /tmp
setfacl -m u:jenkins:rwx /tmp

# Jenkins specific setup
usermod -G libra_user jenkins
chown -R jenkins:jenkins /var/lib/jenkins

# Allow Apache to connect to Jenkins port 8081
/usr/sbin/setsebool -P httpd_can_network_connect=on || :

# Allow polyinstantiation to work
/usr/sbin/setsebool -P allow_polyinstantiation=on || :

# Allow httpd to relay
/usr/sbin/setsebool -P httpd_can_network_relay=on || :

# Increase kernel semaphores to accomodate many httpds
echo "kernel.sem = 250  32000 32  4096" >> /etc/sysctl.conf
sysctl kernel.sem="250  32000 32  4096"

# Move ephemeral port range to accommodate app proxies
echo "net.ipv4.ip_local_port_range = 15000 35534" >> /etc/sysctl.conf
sysctl net.ipv4.ip_local_port_range="15000 35534"

# Setup facts
/usr/libexec/mcollective/update_yaml.rb
crontab -u root %{devenvdir}/crontab

# enable disk quotas
/usr/bin/rhc-init-quota

# Setup swap for devenv
[ -f /.swap ] || ( /bin/dd if=/dev/zero of=/.swap bs=1024 count=1024000
    /sbin/mkswap -f /.swap
    /sbin/swapon /.swap
    echo "/.swap swap   swap    defaults        0 0" >> /etc/fstab
)

# Increase max SSH connections and tries to 40
perl -p -i -e "s/^#MaxSessions .*$/MaxSessions 40/" /etc/ssh/sshd_config
perl -p -i -e "s/^#MaxStartups .*$/MaxStartups 40/" /etc/ssh/sshd_config

# Setup an empty git repository to allow code transfer
mkdir -p /root/li
#mkdir -p /root/cloud-sdk
git init --bare /root/li
git init --bare /root/os-client-tools
#git init --bare /root/cloud-sdk

# Restore permissions
/sbin/restorecon -R %{_sysconfdir}/qpid/pki
/sbin/restorecon -R %{libradir}

# Start services
service iptables restart
service qpidd restart
service mcollective start
service libra-datastore configure
service libra-datastore start
service libra-site restart
service libra-broker restart
service jenkins restart
service httpd restart
service sshd restart
chkconfig iptables on
chkconfig qpidd on
chkconfig mcollective on
chkconfig libra-datastore on
chkconfig libra-site on
chkconfig libra-broker on
chkconfig jenkins on
chkconfig httpd on

# CGroup services
service cgconfig start
service cgred start
service libra-cgroups start
service libra-tc start
chkconfig cgconfig on
chkconfig cgred on
chkconfig libra-cgroups on
chkconfig libra-tc on

# Populate mcollective certs
cd /etc/mcollective/ssl/clients
openssl genrsa -out mcollective-private.pem 1024
openssl rsa -in mcollective-private.pem -out mcollective-public.pem -outform PEM -pubout
chown libra_passenger:root mcollective-private.pem
chmod 460 mcollective-private.pem
cd

# Move static puppet certs in devenv
mkdir -p /var/lib/puppet/ssl/public_keys/
mkdir -p /var/lib/puppet/ssl/private_keys/
cp -f %{devenvdir}/puppet-public.pem /var/lib/puppet/ssl/public_keys/localhost.localdomain.pem
cp -f %{devenvdir}/puppet-private.pem /var/lib/puppet/ssl/private_keys/localhost.localdomain.pem

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

# Add user nagios_monitor to wheel group for running rpm, dmesg, su, and sudo
/usr/bin/gpasswd nagios_monitor wheel

%files
%defattr(-,root,root,-)
%attr(0666,-,-) %{brokerdir}/log/mcollective-client.log
%attr(0666,-,-) %{brokerdir}/log/development.log
%attr(0666,-,-) %{sitedir}/log/development.log
%config(noreplace) %{jenkins}/jobs/*/*
%{jenkins}/jobs/sync.rb
%{devenvdir}
%{_initddir}/libra-datastore
%{_initddir}/libra-broker
%{_initddir}/libra-site
%{_initddir}/sauce-connect

%changelog
* Fri Feb 03 2012 Dan McPherson <dmcphers@redhat.com> 0.86.1-1
- bump spec numbers (dmcphers@redhat.com)
- mongodb: user libra willl have access to openshift_broker_dev db (not an
  admin user any more) (rpenta@redhat.com)

* Thu Feb 02 2012 Dan McPherson <dmcphers@redhat.com> 0.85.15-1
- Merge branch 'master' of git1.ops.rhcloud.com:/srv/git/li (rpenta@redhat.com)
- add --namespace to li-users-delete-util helper script (rpenta@redhat.com)

* Wed Feb 01 2012 Dan McPherson <dmcphers@redhat.com> 0.85.14-1
- Merge branch 'master' of git1.ops.rhcloud.com:/srv/git/li (rpenta@redhat.com)
- Helper script to delete all users and their domains in the current devenv
  instance (rpenta@redhat.com)

* Tue Jan 31 2012 Dan McPherson <dmcphers@redhat.com> 0.85.13-1
- Don't kill all mongod processes -- only the libra-datastore one.
  (ramr@redhat.com)

* Tue Jan 31 2012 Dan McPherson <dmcphers@redhat.com> 0.85.12-1
- - Handle both ReplicaSet and normal mongodb connection - Retry for 30 secs
  (60 times in 0.5 sec frequency) in case of mongo connection failure. - On
  devenv, configure/start mongod with replicaSet = 1 (rpenta@redhat.com)

* Mon Jan 30 2012 Dan McPherson <dmcphers@redhat.com> 0.85.11-1
- Revert changes to development.log in site,broker,devenv spec
  (aboone@redhat.com)
- Reduce number of rubygem dependencies in site build (aboone@redhat.com)

* Sat Jan 28 2012 Dan McPherson <dmcphers@redhat.com> 0.85.10-1
- Site build - don't use bundler, install all gems via RPM (aboone@redhat.com)

* Fri Jan 27 2012 Dan McPherson <dmcphers@redhat.com> 0.85.9-1
- build fixes (dmcphers@redhat.com)
- Re-enabling 127.0.0.1 ban (mmcgrath@redhat.com)
- Add back rubygem-rake and rubygem-rspec dependencies for devenv
  (aboone@redhat.com)
- Fix for 532e0e8, also properly set permissions on logs (aboone@redhat.com)
- Remove therubyracer gem dependency, "js" is already being used
  (aboone@redhat.com)
- Since site is touching the development.log during build, remove touches from
  devenv.spec (aboone@redhat.com)
- Provide barista dependencies at site build time (aboone@redhat.com)
- Add BuildRequires: rubygem-crack for site spec (aboone@redhat.com)
- add requires (dmcphers@redhat.com)
- config cleanup for ticket (dmcphers@redhat.com)
- Bug 784809 (dmcphers@redhat.com)
- devenv.spec - changed chgrp before chmod to apply proper rights to su sudo
  dmesg and rpm 01 25 2012 (tkramer@redhat.com)
- cleanup (dmcphers@redhat.com)
- cleanup (dmcphers@redhat.com)
- add rake and rspec to build prereqs (dmcphers@redhat.com)
- cleanup (dmcphers@redhat.com)
- Added rhc-cartridge-cron to list of packages for devenv. (ramr@redhat.com)
- allow install from source plus some districts changes (dmcphers@redhat.com)

* Tue Jan 24 2012 Dan McPherson <dmcphers@redhat.com> 0.85.8-1
- resolve merge conflicts (rpenta@redhat.com)
- Expose internal mongo datastore through rock-mongo UI (rpenta@redhat.com)

* Tue Jan 24 2012 Dan McPherson <dmcphers@redhat.com> 0.85.7-1
- add pam-devel (dmcphers@redhat.com)
- devenv.spec changed comment typo in chmod section 01 24 2012
  (tkramer@redhat.com)
- devenv.spec Added changes for sudo rpm su and dmesg.  Also added nagios
  monitor to wheel group  01 23 2012 (tkramer@redhat.com)
- Merge branch 'master' of ssh://git1.ops.rhcloud.com/srv/git/li
  (rmillner@redhat.com)
- Merge branch 'master' of ssh://git1.ops.rhcloud.com/srv/git/li
  (rmillner@redhat.com)
- Don't overlap range. (rmillner@redhat.com)
- US1371, Move the ephemeral port range down to clear room for proxy.
  (rmillner@redhat.com)

* Mon Jan 23 2012 Tim Kramer <tkramer@redhat.com> 0.85.6-1
- Fixed the o-x permissions on sudo rpm su and dmesg
- Added nagios_monitor to wheel so that it can run sudo rpm su and dmesg

* Fri Jan 20 2012 Mike McGrath <mmcgrath@redhat.com> 0.85.5-1
- more rack/ruby replacements (mmcgrath@redhat.com)
