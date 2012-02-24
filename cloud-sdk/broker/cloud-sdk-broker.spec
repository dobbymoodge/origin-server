%define htmldir %{_localstatedir}/www/html
%define brokerdir %{_localstatedir}/www/cloud-sdk/broker
%define appdir %{_localstatedir}/lib/cloud-sdk

Summary:   Cloud-SDK broker components
Name:      cloud-sdk-broker
Version:   0.5.1
Release:   1%{?dist}
Group:     Network/Daemons
License:   ASL 2.0
URL:       http://openshift.redhat.com
Source0:   cloud-sdk-broker-%{version}.tar.gz

BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
Requires:  httpd
Requires:  mod_ssl
Requires:  oddjob
Requires:  mod_passenger
Requires:  mongodb-server
Requires:  rubygem(rails)
Requires:  rubygem(xml-simple)
Requires:  rubygem(bson_ext)
Requires:  rubygem(rest-client)
Requires:  rubygem(thread-dump)
Requires:  rubygem(parseconfig)
Requires:  rubygem(json)
Requires:  rubygem(cloud-sdk-controller)
Requires:  rubygem(cloud-sdk-node)
Requires:  cloud-sdk-abstract

BuildArch: noarch

%description
This contains the broker 'controlling' components of Cloud-SDK.
This includes the public APIs for the client tools.

%prep
%setup -q

%build

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_initddir}
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{htmldir}
mkdir -p %{buildroot}%{brokerdir}
mkdir -p %{buildroot}%{brokerdir}/httpd/run
mkdir -p %{buildroot}%{brokerdir}/httpd/logs
mkdir -p %{buildroot}%{brokerdir}/httpd/conf
mkdir -p %{buildroot}%{brokerdir}/log
mkdir -p %{buildroot}%{brokerdir}/run
mkdir -p %{buildroot}%{brokerdir}/tmp/cache
mkdir -p %{buildroot}%{brokerdir}/tmp/pids
mkdir -p %{buildroot}%{brokerdir}/tmp/sessions
mkdir -p %{buildroot}%{brokerdir}/tmp/sockets
mkdir -p %{buildroot}%{appdir}
mkdir -p %{buildroot}%{_sysconfdir}/httpd/conf.d/cloud-sdk
mkdir -p %{buildroot}%{_sysconfdir}/oddjobd.conf.d
mkdir -p %{buildroot}%{_sysconfdir}/dbus-1/system.d
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_var}/lib/cloud-sdk

cp -r . %{buildroot}%{brokerdir}
mv %{buildroot}%{brokerdir}/init.d/* %{buildroot}%{_initddir}
ln -s %{brokerdir}/public %{buildroot}%{htmldir}/broker
touch %{buildroot}%{brokerdir}/log/production.log
touch %{buildroot}%{brokerdir}/log/development.log
ln -sf /usr/lib64/httpd/modules %{buildroot}%{brokerdir}/httpd/modules
ln -sf /etc/httpd/conf/magic %{buildroot}%{brokerdir}/httpd/conf/magic
mv %{buildroot}%{brokerdir}/httpd/000000_cloud-sdk_proxy.conf %{buildroot}%{_sysconfdir}/httpd/conf.d/
mv %{buildroot}%{brokerdir}/misc/cloud-sdk-dbus.conf %{buildroot}%{_sysconfdir}/dbus-1/system.d/
mv %{buildroot}%{brokerdir}/misc/oddjobd-cdk-exec.conf %{buildroot}%{_sysconfdir}/oddjobd.conf.d/
mv %{buildroot}%{brokerdir}/script/cdk-exec-command %{buildroot}%{_bindir}
%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(0640,apache,apache,0750)
%attr(0666,-,-) %{brokerdir}/log/production.log
%attr(0666,-,-) %{brokerdir}/log/development.log
%attr(0750,-,-) %{brokerdir}/script
%attr(0750,-,-) %{brokerdir}/tmp
%attr(0750,-,-) %{brokerdir}/tmp/cache
%attr(0750,-,-) %{brokerdir}/tmp/pids
%attr(0750,-,-) %{brokerdir}/tmp/sessions
%attr(0750,-,-) %{brokerdir}/tmp/sockets
%attr(0750,-,-) %{_sysconfdir}/httpd/conf.d/cloud-sdk
%{brokerdir}
%{htmldir}/broker
%config(noreplace) %{brokerdir}/config/environments/production.rb
%config(noreplace) %{brokerdir}/config/environments/development.rb
%config(noreplace) %{_sysconfdir}/httpd/conf.d/000000_cloud-sdk_proxy.conf

%defattr(0640,root,root,0750)
%{_initddir}/cloud-sdk-broker
%attr(0750,-,-) %{_initddir}/cloud-sdk-broker
%config(noreplace) %{_sysconfdir}/oddjobd.conf.d/oddjobd-cdk-exec.conf 
%config(noreplace) %{_sysconfdir}/dbus-1/system.d/cloud-sdk-dbus.conf
%attr(0700,-,-) %{_bindir}/cdk-exec-command
%attr(0755,-,-) %{_var}/lib/cloud-sdk

%post
/bin/touch %{brokerdir}/log/production.log

# Increase kernel semaphores to accomodate many httpds
echo "kernel.sem = 250  32000 32  4096" >> /etc/sysctl.conf
sysctl kernel.sem="250  32000 32  4096"

# Move ephemeral port range to accommodate app proxies
echo "net.ipv4.ip_local_port_range = 15000 35530" >> /etc/sysctl.conf
sysctl net.ipv4.ip_local_port_range="15000 35530"

# Increase the connection tracking table size
echo "net.netfilter.nf_conntrack_max = 1048576" >> /etc/sysctl.conf
sysctl net.netfilter.nf_conntrack_max=1048576

#selinux updated
#setsebool -P httpd_can_network_relay=1 httpd_can_network_connect=1
chcon -t httpd_sys_script_rw_t %{brokerdir}/httpd/run/
chcon -R -t httpd_sys_script_rw_t %{brokerdir}/tmp
chcon -t httpd_sys_script_ra_t %{brokerdir}/httpd/logs
chcon -t httpd_sys_script_ra_t %{brokerdir}/log/*
chcon -t httpd_exec_t `passenger-config --root`/agents/apache2/PassengerHelperAgent

##TODO: instructions for
# Setup swap for devenv
[ -f /.swap ] || ( /bin/dd if=/dev/zero of=/.swap bs=1024 count=1024000
    /sbin/mkswap -f /.swap
    /sbin/swapon /.swap
    echo "/.swap swap   swap    defaults        0 0" >> /etc/fstab
)

# Increase max SSH connections and tries to 40
perl -p -i -e "s/^#MaxSessions .*$/MaxSessions 40/" /etc/ssh/sshd_config
perl -p -i -e "s/^#MaxStartups .*$/MaxStartups 40/" /etc/ssh/sshd_config

rm -f %{brokerdir}/Gemfile.lock
cd %{brokerdir} && bundle show 2>&1 > /dev/null ; cd -
##End TODO
systemctl --system daemon-reload

service cloud-sdk-broker restart
service httpd restart
service sshd restart
service dbus restart
service oddjobd restart
chkconfig cloud-sdk-broker on

echo "Create a new mongodb is not already created"
echo "Edit /etc/mongodb.conf and turn auth=true"

echo "Create a new mongodb is not already created"
echo "$ mongo"
echo "> use cloud_sdk_broker_dev"
echo "> db.addUser(\"cloud_sdk\", \"mooo\")"

%changelog
