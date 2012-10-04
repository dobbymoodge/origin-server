%define ruby_sitelibdir            %(ruby -rrbconfig -e "puts Config::CONFIG['sitelibdir']")

Summary:       Multi-tenant cloud management system node tools
Name:          rhc-node
Version: 0.99.6
Release:       1%{?dist}
Group:         Network/Daemons
License:       GPLv2
URL:           http://openshift.redhat.com
Source0:       rhc-node-%{version}.tar.gz

BuildRoot:     %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
BuildRequires: ruby
BuildRequires: pam-devel
BuildRequires: libselinux-devel
BuildRequires: gcc-c++
Requires:      rhc-common
Requires:      rhc-selinux >= 0.84.7-1
Requires:      git
Requires:      libcgroup
Requires:      mcollective
Requires:      perl
Requires:      ruby
Requires:      rubygem-open4
Requires:      rubygem-parseconfig
Requires:      rubygem-openshift-origin-node
Requires:      rubygem-systemu
Requires:      openshift-origin-cartridge-abstract
Requires:      mcollective-qpid-plugin
Requires:      openshift-origin-msg-node-mcollective
Requires:      openshift-origin-port-proxy
Requires:      quota
Requires:      lsof
Requires:      wget
Requires:      nano
Requires:      emacs-nox
Requires:      oddjob
Requires:      libjpeg-devel
Requires:      libcurl-devel
Requires:      libpng-devel
Requires:      giflib-devel
Requires:      mod_ssl
Requires:      haproxy
Requires:      procmail
Requires:      libevent
Requires:      libevent-devel
Requires:      mod_vhost_choke
Requires(post):   /usr/sbin/semodule
Requires(post):   /usr/sbin/semanage
Requires(postun): /usr/sbin/semodule
Requires(postun): /usr/sbin/semanage


%description
Turns current host into a OpenShift managed node


%prep
%setup -q

%build

# Build pam_libra
pwd
cd pam_libra
make
cd -


%install
rm -rf $RPM_BUILD_ROOT

mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_libexecdir}
mkdir -p %{buildroot}%{_initddir}
mkdir -p %{buildroot}%{ruby_sitelibdir}
mkdir -p %{buildroot}%{_libexecdir}/openshift
mkdir -p %{buildroot}/usr/share/selinux/packages
mkdir -p %{buildroot}%{_sysconfdir}/cron.daily/
mkdir -p %{buildroot}%{_sysconfdir}/oddjobd.conf.d/
mkdir -p %{buildroot}%{_sysconfdir}/dbus-1/system.d/
mkdir -p %{buildroot}%{_sysconfdir}/cron.daily/
mkdir -p %{buildroot}%{_sysconfdir}/openshift/skel
mkdir -p %{buildroot}/%{_localstatedir}/www/html/
mkdir -p %{buildroot}/%{_sysconfdir}/security/
mkdir -p %{buildroot}%{_localstatedir}/lib/openshift
mkdir -p %{buildroot}%{_localstatedir}/run/openshift
mkdir -p %{buildroot}%{_localstatedir}/lib/openshift/.httpd.d
mkdir -p %{buildroot}/%{_sysconfdir}/httpd/conf.d/
mkdir -p %{buildroot}/lib64/security/
mkdir -p %{buildroot}/sandbox
# ln -s %{_localstatedir}/lib/openshift/.httpd.d/ %{buildroot}/%{_sysconfdir}/httpd/conf.d/openshift

cp -r lib %{buildroot}%{_libexecdir}/openshift
cp -r conf/httpd %{buildroot}%{_sysconfdir}
cp -r conf/openshift %{buildroot}%{_sysconfdir}
cp -r mcollective %{buildroot}%{_libexecdir}
cp -r namespace.d %{buildroot}%{_sysconfdir}/security
cp scripts/bin/* %{buildroot}%{_bindir}
cp scripts/init/* %{buildroot}%{_initddir}
cp scripts/openshift_tmpwatch.sh %{buildroot}%{_sysconfdir}/cron.daily/openshift_tmpwatch.sh
cp conf/oddjob/openshift-restorer.conf %{buildroot}%{_sysconfdir}/dbus-1/system.d/
cp conf/oddjob/oddjobd-restorer.conf %{buildroot}%{_sysconfdir}/oddjobd.conf.d/
cp scripts/restorer.php %{buildroot}/%{_localstatedir}/www/html/
cp pam_libra/pam_libra.so.1  %{buildroot}/lib64/security/pam_libra.so

%clean
rm -rf $RPM_BUILD_ROOT

%post
echo "/usr/bin/trap-user" >> /etc/shells

/sbin/chkconfig --add libra || :
/sbin/chkconfig --add libra-data || :
/sbin/chkconfig --add libra-cgroups || :
/sbin/chkconfig --add libra-tc || :
/sbin/chkconfig --add libra-watchman || :

#/sbin/service mcollective restart > /dev/null 2>&1 || :
/sbin/restorecon /etc/init.d/libra || :
/sbin/restorecon /var/run/openshift || :
/sbin/restorecon /usr/bin/rhc-cgroup-read || :
/sbin/restorecon -r /sandbox
/sbin/restorecon /etc/init.d/libra || :
/sbin/restorecon /etc/init.d/mcollective || :
/sbin/restorecon /usr/bin/rhc-restorer* || :

# Only bounce cgroups if not already initialized
# CAVEAT: if the policy is changed, must run these by hand (release ticket)
if [ ! -e /cgroup/all/libra/cgroup.event_control ]
then
    # mount all desired cgroups under a single root
    perl -p -i -e 's:/cgroup/[^\s]+;:/cgroup/all;:; /blkio|cpuset|devices/ && ($_ = "#$_")' /etc/cgconfig.conf
    /sbin/restorecon /etc/cgconfig.conf || :
    # only restart if it's on
    /sbin/chkconfig cgconfig && /sbin/service cgconfig restart >/dev/null 2>&1 || :
    # only enable if cgconfig is
    chkconfig cgconfig && /sbin/service libra-cgroups start > /dev/null 2>&1 || :
fi

# Only bounce tc if its not already initialized
# CAVEAT: if the policy is changed, must run these by hand (release ticket)
if ! ( tc qdisc show | grep -q 'qdisc htb 1: dev' )
then
    # only enable if cgconfig is
    chkconfig cgconfig && /sbin/service libra-tc start > /dev/null 2>&1 || :
fi

/sbin/chkconfig oddjobd on
/sbin/service messagebus restart
/sbin/service oddjobd restart
# /usr/bin/rhc-restorecon || :    # Takes too long and shouldn't be needded
/sbin/service libra-data start > /dev/null 2>&1 || :
[ $(/usr/sbin/semanage node -l | /bin/grep -c 255.255.255.128) -lt 1000 ] && /usr/bin/rhc-ip-prep.sh || :

# Ensure the default users have a more restricted shell then normal.
#semanage login -m -s guest_u __default__ || :

# If /etc/httpd/conf.d/libra is a dir, make it a symlink
if [[ -d "/etc/httpd/conf.d/openshift.bak" && -L "/etc/httpd/conf.d/openshift" ]]
then
    mv /etc/httpd/conf.d/openshift.bak/* /var/lib/openshift/.httpd.d/
    # not forced to prevent data loss
    rmdir /etc/httpd/conf.d/openshift.bak
fi

# To workaround mcollective 2.0 monkey patch to tmpdir
chmod o+w /tmp

%triggerin -- rubygem-openshift-origin-node
/sbin/service libra-data start > /dev/null 2>&1 || :

%preun
if [ "$1" -eq "0" ]; then
    /sbin/service libra-tc stop > /dev/null 2>&1 || :
    /sbin/service libra-cgroups stop > /dev/null 2>&1 || :
    /sbin/service libra-watchman stop > /dev/null 2>&1 || :
    /sbin/chkconfig --del libra-tc || :
    /sbin/chkconfig --del libra-cgroups || :
    /sbin/chkconfig --del libra-data || :
    /sbin/chkconfig --del libra || :
    /sbin/chkconfig --del libra-watchman || :
    /usr/sbin/semodule -r libra
    sed -i -e '\:/usr/bin/trap-user:d' /etc/shells
fi

%postun

if [ "$1" -eq 0 ]; then
    /sbin/service mcollective restart > /dev/null 2>&1 || :
fi
#/usr/sbin/semodule -r libra

%pre

if [[ -d "/etc/httpd/conf.d/openshift" && ! -L "/etc/httpd/conf.d/openshift" ]]
then
    mv /etc/httpd/conf.d/openshift/ /etc/httpd/conf.d/openshift.bak/
fi

%files
%defattr(-,root,root,-)
%attr(0640,-,-) %{_libexecdir}/mcollective/mcollective/agent/*
%attr(0750,-,-) %{_initddir}/libra
%attr(0750,-,-) %{_initddir}/libra-data
%attr(0750,-,-) %{_initddir}/libra-cgroups
%attr(0750,-,-) %{_initddir}/libra-tc
%attr(0750,-,-) %{_initddir}/libra-watchman
%attr(0755,-,-) %{_bindir}/trap-user
%attr(0750,-,-) %{_bindir}/rhc-ip-prep.sh
%attr(0750,-,-) %{_bindir}/rhc-iptables.sh
%attr(0750,-,-) %{_bindir}/rhc-mcollective-log-profile
%attr(0750,-,-) %{_bindir}/rhc-profiler-merge-report
%attr(0750,-,-) %{_bindir}/rhc-restorecon
%attr(0750,-,-) %{_bindir}/rhc-init-quota
%attr(0750,-,-) %{_bindir}/rhc-list-stale
%attr(0750,-,-) %{_bindir}/rhc-idler
%attr(0750,-,-) %{_bindir}/rhc-last-access
%attr(0750,-,-) %{_bindir}/rhc-app-idle
%attr(0750,-,-) %{_bindir}/rhc-autoidler
%attr(0750,-,-) %{_bindir}/rhc-idler-stats
%attr(0750,-,-) %{_bindir}/rhc-restorer
%attr(0750,-,apache) %{_bindir}/rhc-restorer-wrapper.sh
%attr(0750,-,-) %{_bindir}/ec2-prep.sh
%attr(0750,-,-) %{_bindir}/remount-secure.sh
%attr(0755,-,-) %{_bindir}/rhc-cgroup-read
%attr(0755,-,-) %{_bindir}/rhc-vhost-choke
%dir %attr(0751,root,root) %{_localstatedir}/lib/openshift
%dir %attr(0750,root,root) %{_localstatedir}/lib/openshift/.httpd.d
%dir %attr(0700,root,root) %{_localstatedir}/run/openshift
#%dir %attr(0755,root,root) %{_libexecdir}/openshift/cartridges/abstract-httpd/
#%attr(0750,-,-) %{_libexecdir}/openshift/cartridges/abstract-httpd/info/hooks/
#%attr(0755,-,-) %{_libexecdir}/openshift/cartridges/abstract-httpd/info/bin/
##%{_libexecdir}/openshift/cartridges/abstract-httpd/info
#%dir %attr(0755,root,root) %{_libexecdir}/openshift/cartridges/abstract/
#%attr(0750,-,-) %{_libexecdir}/openshift/cartridges/abstract/info/hooks/
#%attr(0755,-,-) %{_libexecdir}/openshift/cartridges/abstract/info/bin/
#%attr(0755,-,-) %{_libexecdir}/openshift/cartridges/abstract/info/lib/
#%attr(0750,-,-) %{_libexecdir}/li/cartridges/abstract/info/connection-hooks/
%attr(0755,-,-) %{_libexecdir}/openshift/lib/
#%{_libexecdir}/openshift/cartridges/abstract/info
%attr(0750,-,-) %{_bindir}/rhc-accept-node
%attr(0750,-,-) %{_bindir}/rhc-accept-devenv
%attr(0755,-,-) %{_bindir}/rhc-list-ports
%attr(0750,-,-) %{_bindir}/rhc-node-account
%attr(0750,-,-) %{_bindir}/rhc-node-application
%attr(0750,-,-) %{_bindir}/rhc-watchman
%attr(0755,-,-) %{_bindir}/rhcsh
%attr(0700,-,-) %{_bindir}/migration-symlink-as-user
%attr(0640,-,-) %config(noreplace) %{_sysconfdir}/oddjobd.conf.d/oddjobd-restorer.conf
%attr(0640,-,-) %config(noreplace) %{_sysconfdir}/dbus-1/system.d/openshift-restorer.conf
%attr(0644,-,-) %config(noreplace) %{_sysconfdir}/openshift/node.conf.libra
%attr(0644,-,-) %config(noreplace) %{_sysconfdir}/openshift/resource_limits.con*
%attr(0750,-,-) %config(noreplace) %{_sysconfdir}/cron.daily/openshift_tmpwatch.sh
%attr(0644,-,-) %config(noreplace) %{_sysconfdir}/security/namespace.d/*
%{_localstatedir}/www/html/restorer.php
%attr(0750,root,root) %config(noreplace) %{_sysconfdir}/httpd/conf.d/000000_default.conf
#%attr(0640,root,root) %{_sysconfdir}/httpd/conf.d/openshift
%dir %attr(0755,root,root) %{_sysconfdir}/openshift/skel
/lib64/security/pam_libra.so
%dir %attr(1777,root,root) /sandbox


%changelog
* Thu Oct 04 2012 Adam Miller <admiller@redhat.com> 0.99.6-1
- Bug 862439 patch for fix (jhonce@redhat.com)
- Merge pull request #442 from mrunalp/dev/typeless (dmcphers@redhat.com)
- BZ853582: Prevent user from logging in while deleting gear
  (jhonce@redhat.com)
- Fix for Bug 862439 (jhonce@redhat.com)
- Typeless gear changes for US 2105 (jhonce@redhat.com)