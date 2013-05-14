%if 0%{?fedora}
    %global mco_root /usr/libexec/mcollective/mcollective/
%endif
%if 0%{?rhel}
    %global mco_root /opt/rh/ruby193/root/usr/libexec/mcollective/mcollective/
%endif

Summary:       Multi-tenant cloud management system node tools
Name:          rhc-node
Version: 1.8.6
Release:       1%{?dist}
Group:         Network/Daemons
License:       GPLv2
URL:           http://openshift.redhat.com
Source0:       rhc-node-%{version}.tar.gz

BuildRoot:     %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
BuildRequires: ruby
Requires:      rhc-common
Requires:      rhc-selinux >= 0.84.7-1
Requires:      git
Requires:      libcgroup
Requires:      mcollective
Requires:      ruby193-mcollective-common
Requires:      perl
Requires:      ruby
Requires:      ruby193-rubygem-open4
Requires:      ruby193-rubygem-parseconfig
Requires:      rubygem-openshift-origin-node
Requires:      openshift-origin-node-util
Requires:      ruby193-rubygem-systemu
Requires:      openshift-origin-cartridge-abstract
Requires:      openshift-origin-msg-node-mcollective
Requires:      openshift-origin-port-proxy
Requires:      openshift-origin-node-proxy
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
Requires:      GeoIP-devel
Requires:      unixODBC
Requires:      unixODBC-devel
Requires:      Cython
Requires:      Pyrex
Requires(post):   /usr/sbin/semodule
Requires(post):   /usr/sbin/semanage
Requires(postun): /usr/sbin/semodule
Requires(postun): /usr/sbin/semanage


%description
Turns current host into a OpenShift managed node


%prep
%setup -q

%build


%install
rm -rf $RPM_BUILD_ROOT

mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_libexecdir}
mkdir -p %{buildroot}%{_initddir}
mkdir -p %{buildroot}%{_libexecdir}/openshift
mkdir -p %{buildroot}/usr/share/selinux/packages
mkdir -p %{buildroot}%{_sysconfdir}/cron.daily/
mkdir -p %{buildroot}%{_sysconfdir}/oddjobd.conf.d/
mkdir -p %{buildroot}%{_sysconfdir}/dbus-1/system.d/
mkdir -p %{buildroot}%{_sysconfdir}/cron.daily/
mkdir -p %{buildroot}%{_sysconfdir}/openshift/skel
mkdir -p %{buildroot}/%{_var}/www/html/
mkdir -p %{buildroot}/%{_sysconfdir}/security/
mkdir -p %{buildroot}%{_var}/lib/openshift
mkdir -p %{buildroot}%{_var}/run/openshift
mkdir -p %{buildroot}%{_var}/lib/openshift/.httpd.d
mkdir -p %{buildroot}/%{_sysconfdir}/httpd/conf.d/
mkdir -p %{buildroot}/lib64/security/
mkdir -p %{buildroot}/sandbox
mkdir -p %{buildroot}%{mco_root}agent/
mkdir -p %{buildroot}%{mco_root}lib/
# ln -s %{_var}/lib/openshift/.httpd.d/ %{buildroot}/%{_sysconfdir}/httpd/conf.d/openshift

cp -r lib %{buildroot}%{_libexecdir}/openshift
cp -r conf/httpd %{buildroot}%{_sysconfdir}
cp -r conf/openshift %{buildroot}%{_sysconfdir}
cp mcollective/agent/* %{buildroot}%{mco_root}agent/
cp mcollective/lib/* %{buildroot}%{mco_root}lib/
cp scripts/bin/* %{buildroot}%{_bindir}
cp scripts/init/* %{buildroot}%{_initddir}
cp scripts/openshift_tmpwatch.sh %{buildroot}%{_sysconfdir}/cron.daily/openshift_tmpwatch.sh

%clean
rm -rf $RPM_BUILD_ROOT

%post
echo "/usr/bin/oo-trap-user" >> /etc/shells

/sbin/chkconfig --add openshift-gears || :
/sbin/chkconfig --add libra-data || :
/sbin/chkconfig --add libra-tc || :
/sbin/chkconfig --add libra-watchman || :
/sbin/chkconfig --add openshift-cgroups || :

#/sbin/service mcollective restart > /dev/null 2>&1 || :
/sbin/restorecon /etc/init.d/libra || :
/sbin/restorecon /var/run/openshift || :
/sbin/restorecon -r /sandbox
/sbin/restorecon /etc/init.d/mcollective || :


# Only bounce cgroups if not already initialized
# CAVEAT: if the policy is changed, must run these by hand (release ticket)
if [ ! -e /cgroup/all/openshift/cgroup.event_control ]
then
    # mount all desired cgroups under a single root
    perl -p -i -e 's:/cgroup/[^\s]+;:/cgroup/all;:; /blkio|cpuset|devices/ && ($_ = "#$_")' /etc/cgconfig.conf
    /sbin/restorecon /etc/cgconfig.conf || :
    # only restart if it's on
    /sbin/chkconfig cgconfig && /sbin/service cgconfig restart >/dev/null 2>&1 || :
    # only enable if cgconfig is
    chkconfig cgconfig && /sbin/service openshift-cgroups start > /dev/null 2>&1 || :
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
/sbin/service libra-watchman restart || :
# /usr/bin/rhc-restorecon || :    # Takes too long and shouldn't be needded
/sbin/service libra-data start > /dev/null 2>&1 || :
[ $(/usr/sbin/semanage node -l | /bin/grep -c 255.255.255.128) -lt 1000 ] && /usr/bin/rhc-ip-prep || :

# Ensure the default users have a more restricted shell then normal.
#semanage login -m -s guest_u __default__ || :

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
    /sbin/service openshift-cgroups stop > /dev/null 2>&1 || :
    /sbin/service libra-watchman stop > /dev/null 2>&1 || :
    /sbin/chkconfig --del libra-tc || :
    /sbin/chkconfig --del libra-data || :
    /sbin/chkconfig --del openshift-cgroups || :
    /sbin/chkconfig --del libra-watchman || :
    sed -i -e '\:/usr/bin/oo-trap-user:d' /etc/shells
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
%attr(0640,-,-) %{mco_root}agent/*
%attr(0640,-,-) %{mco_root}lib/*
%attr(0750,-,-) %{_initddir}/libra-data
%attr(0750,-,-) %{_initddir}/libra-tc
%attr(0750,-,-) %{_initddir}/libra-watchman
%attr(0750,-,-) %{_bindir}/rhc-ip-prep
%attr(0750,-,-) %{_bindir}/rhc-iptables.sh
%attr(0750,-,-) %{_bindir}/rhc-mcollective-log-profile
%attr(0750,-,-) %{_bindir}/rhc-profiler-merge-report
%attr(0750,-,-) %{_bindir}/rhc-restorecon
%attr(0750,-,-) %{_bindir}/rhc-init-quota
%attr(0750,-,-) %{_bindir}/rhc-fix-frontend
%attr(0750,-,-) %{_bindir}/rhc-fix-missing-frontend
%attr(0750,-,-) %{_bindir}/rhc-fix-stale-frontend
%attr(0750,-,-) %{_bindir}/ec2-prep.sh
%attr(0750,-,-) %{_bindir}/remount-secure.sh
%dir %attr(0751,root,root) %{_var}/lib/openshift
%dir %attr(0750,root,apache) %{_var}/lib/openshift/.httpd.d
%dir %attr(0700,root,root) %{_var}/run/openshift
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
%attr(0750,-,-) %{_bindir}/rhc-node-account
%attr(0750,-,-) %{_bindir}/rhc-node-application
%attr(0750,-,-) %{_bindir}/rhc-watchman
%attr(0700,-,-) %{_bindir}/migration-symlink-as-user
%attr(0644,-,-) %config(noreplace) %{_sysconfdir}/openshift/resource_limits.conf.*
%attr(0750,-,-) %config(noreplace) %{_sysconfdir}/cron.daily/openshift_tmpwatch.sh
%attr(0750,root,root) %config(noreplace) %{_sysconfdir}/httpd/conf.d/000000_default.conf
#%attr(0640,root,root) %{_sysconfdir}/httpd/conf.d/openshift
%dir %attr(0755,root,root) %{_sysconfdir}/openshift/skel
%dir %attr(1777,root,root) /sandbox


%changelog
* Wed May 08 2013 Adam Miller <admiller@redhat.com> 1.8.6-1
- v2 migrations WIP (dmcphers@redhat.com)
- handle versions with dashes (dmcphers@redhat.com)
- v2 migration WIP (dmcphers@redhat.com)

* Mon May 06 2013 Adam Miller <admiller@redhat.com> 1.8.5-1
- Fix bug 959142 (pmorie@gmail.com)

* Thu May 02 2013 Adam Miller <admiller@redhat.com> 1.8.4-1
- Fix bug 958800: Update v2-migration version (pmorie@gmail.com)
- Add post-migration validation step (pmorie@gmail.com)

* Wed May 01 2013 Adam Miller <admiller@redhat.com> 1.8.3-1
- Add cuke tests for mysql migrations (pmorie@gmail.com)
- V1 -> V2 migrations (pmorie@gmail.com)
- WIP Cartridge Refactor - Fix rhc-watchman for V2 nodes (jhonce@redhat.com)
- WIP: migration cucumber tests (pmorie@gmail.com)

* Mon Apr 29 2013 Adam Miller <admiller@redhat.com> 1.8.2-1
- V1 -> V2 migrations (pmorie@gmail.com)

* Thu Apr 25 2013 Adam Miller <admiller@redhat.com> 1.8.1-1
- WIP: V2 Migrations (pmorie@gmail.com)
- Creating fixer mechanism for replacing all ssh keys for an app
  (abhgupta@redhat.com)
- Merge pull request #1239 from danmcp/master
  (dmcphers+openshiftbot@redhat.com)
- Merge pull request #1238 from jwhonce/wip/raw_envvar
  (dmcphers+openshiftbot@redhat.com)
- implementing install and post-install (dmcphers@redhat.com)
- Card online_runtime_255 - Change environment variable files to be named KEY
  and contain VALUE (jhonce@redhat.com)
- Adding install and post setup steps (dmcphers@redhat.com)
- Use require_relative in v2 migrations (pmorie@gmail.com)
- WIP: V1 -> V2 migrations (pmorie@gmail.com)
- bump_minor_versions for sprint XX (tdawson@redhat.com)

* Fri Apr 12 2013 Adam Miller <admiller@redhat.com> 1.7.3-1
- Call the ruby mcs label generator directly for speed. (rmillner@redhat.com)

* Wed Apr 10 2013 Adam Miller <admiller@redhat.com> 1.7.2-1
- <rhc-node> bug 949543 transfer RPM ownership of resource_limits.conf to
  rubygem-o-o-node additionally, have devenv cp the one from rhc-node so it
  will be the same. (lmeyer@redhat.com)

* Thu Mar 28 2013 Adam Miller <admiller@redhat.com> 1.7.1-1
- bump_minor_versions for sprint 26 (admiller@redhat.com)

* Tue Mar 26 2013 Adam Miller <admiller@redhat.com> 1.6.3-1
- getting jenkins working (dmcphers@redhat.com)

* Thu Mar 21 2013 Adam Miller <admiller@redhat.com> 1.6.2-1
- One-off tool for fixing the front-end configuration. (rmillner@redhat.com)
- update migration to current release (dmcphers@redhat.com)

* Thu Mar 07 2013 Adam Miller <admiller@redhat.com> 1.6.1-1
- bump_minor_versions for sprint 25 (admiller@redhat.com)

* Thu Mar 07 2013 Adam Miller <admiller@redhat.com> 1.5.10-1
- Bug 918383 - Python community cartridges cannot share virtualenv
  (jhonce@redhat.com)
- Bug 918383 - Python community cartridges cannot share virtualenv
  (jhonce@redhat.com)

* Wed Mar 06 2013 Adam Miller <admiller@redhat.com> 1.5.9-1
- Bug 918480 (dmcphers@redhat.com)

* Tue Mar 05 2013 Adam Miller <admiller@redhat.com> 1.5.8-1
- Fix incorrect variable name. (rmillner@redhat.com)

* Fri Mar 01 2013 Adam Miller <admiller@redhat.com> 1.5.7-1
- Removing mcollective qpid plugin and adding some doc (dmcphers@redhat.com)
- Use direct API calls, and set up the results of the proxy hook calls rather
  than calling them.  Boost speed 4x. (rmillner@redhat.com)

* Thu Feb 28 2013 Adam Miller <admiller@redhat.com> 1.5.6-1
- Add the frontend to the migrator. (rmillner@redhat.com)

* Wed Feb 27 2013 Adam Miller <admiller@redhat.com> 1.5.5-1
- Use our own custom format log. (rmillner@redhat.com)

* Tue Feb 26 2013 Adam Miller <admiller@redhat.com> 1.5.4-1
- Merge pull request #926 from rmillner/US3143
  (dmcphers+openshiftbot@redhat.com)
- update migration to current release (dmcphers@redhat.com)
- Put aliases after the hook calls, and was calling the wrong hook.
  (rmillner@redhat.com)
- Migration function. (rmillner@redhat.com)

* Mon Feb 25 2013 Adam Miller <admiller@redhat.com> 1.5.3-2
- bump Release for fixed build target rebuild (admiller@redhat.com)

* Mon Feb 25 2013 Adam Miller <admiller@redhat.com> 1.5.3-1
- Add default NodeLogger configuration (ironcladlou@gmail.com)

* Tue Feb 19 2013 Adam Miller <admiller@redhat.com> 1.5.2-1
- No more vhosts, so no more rhc-vhost-choke. (rmillner@redhat.com)
- Switch from VirtualHosts to mod_rewrite based routing to support high
  density. (rmillner@redhat.com)
- Update node.conf.libra to latest node.conf from origin-server
  (jhonce@redhat.com)

* Thu Feb 07 2013 Adam Miller <admiller@redhat.com> 1.5.1-1
- bump_minor_versions for sprint 24 (admiller@redhat.com)

* Wed Feb 06 2013 Adam Miller <admiller@redhat.com> 1.4.5-1
- express -> online (dmcphers@redhat.com)

* Mon Feb 04 2013 Adam Miller <admiller@redhat.com> 1.4.4-1
- <resource_limits> specify limits in gears, not "apps" (lmeyer@redhat.com)

* Thu Jan 31 2013 Adam Miller <admiller@redhat.com> 1.4.3-1
- Bug 906496: Repair ownership of app Git repo objects (ironcladlou@gmail.com)

* Tue Jan 29 2013 Adam Miller <admiller@redhat.com> 1.4.2-1
- Bug 886182 (dmcphers@redhat.com)
- Bug 874594 (dmcphers@redhat.com)
- Bug 889954 (dmcphers@redhat.com)

* Wed Jan 23 2013 Adam Miller <admiller@redhat.com> 1.4.1-1
- bump_minor_versions for sprint 23 (admiller@redhat.com)

* Wed Jan 23 2013 Adam Miller <admiller@redhat.com> 1.3.4-1
- Reset app git repo file permissions to gear user/group
  (ironcladlou@gmail.com)

* Fri Jan 18 2013 Dan McPherson <dmcphers@redhat.com> 1.3.3-1
- Fix BZ895843: migrate postgresql cartridges (pmorie@gmail.com)

* Wed Jan 16 2013 Adam Miller <admiller@redhat.com> 1.3.2-1
- Fix BZ875910 (pmorie@gmail.com)

* Wed Dec 12 2012 Adam Miller <admiller@redhat.com> 1.3.1-1
- bump_minor_versions for sprint 22 (admiller@redhat.com)

* Wed Dec 12 2012 Adam Miller <admiller@redhat.com> 1.2.6-1
- Allow route files to be read by node web proxy. (mpatel@redhat.com)

* Thu Dec 06 2012 Adam Miller <admiller@redhat.com> 1.2.5-1
- Merge pull request #691 from ramr/dev/websockets (openshift+bot@redhat.com)
- Add dependency on node-proxy and setup ports for node-web-proxy (8000 and
  8443) with appropriate connection limits. (ramr@redhat.com)

* Wed Dec 05 2012 Adam Miller <admiller@redhat.com> 1.2.4-1
- simplify dirs (dmcphers@redhat.com)

* Tue Dec 04 2012 Adam Miller <admiller@redhat.com> 1.2.3-1
- Repacking for mco 2.2 (dmcphers@redhat.com)

* Thu Nov 29 2012 Adam Miller <admiller@redhat.com> 1.2.2-1
- various mcollective changes getting ready for 2.2 (dmcphers@redhat.com)
- increase disc timeout on admin ops (dmcphers@redhat.com)
- using oo-ruby (dmcphers@redhat.com)
- migrate active gears first (dmcphers@redhat.com)

* Sat Nov 17 2012 Adam Miller <admiller@redhat.com> 1.2.1-1
- bump_minor_versions for sprint 21 (admiller@redhat.com)

* Fri Nov 16 2012 Adam Miller <admiller@redhat.com> 1.1.7-1
- Merge pull request #627 from ironcladlou/scl-refactor (dmcphers@redhat.com)
- Only use scl if it's available (ironcladlou@gmail.com)

* Thu Nov 15 2012 Adam Miller <admiller@redhat.com> 1.1.6-1
- more ruby 1.9 changes (dmcphers@redhat.com)

* Wed Nov 14 2012 Adam Miller <admiller@redhat.com> 1.1.5-1
- Merge pull request #610 from danmcp/ruby19 (openshift+bot@redhat.com)
- Merge pull request #611 from ramr/master (openshift+bot@redhat.com)
- Merge pull request #603 from rmillner/inhibitidler (dmcphers@redhat.com)
- sclizing gems (dmcphers@redhat.com)
- Merge pull request #596 from jwhonce/master (openshift+bot@redhat.com)
- Fix for bugz 874454 - can't install bzr. Add missing dependencies.
  (ramr@redhat.com)
- Finish moving stale disable to Origin. (rmillner@redhat.com)
- Fix for Bug 873543 (jhonce@redhat.com)

* Tue Nov 13 2012 Adam Miller <admiller@redhat.com> 1.1.4-1
- Merge pull request #585 from brenton/BZ874587 (openshift+bot@redhat.com)
- Merge pull request #598 from rmillner/BZ875910 (openshift+bot@redhat.com)
- add acceptable errors category (dmcphers@redhat.com)
- better strings (dmcphers@redhat.com)
- Remove duplicate script. (rmillner@redhat.com)
- Add additional timings for migrations (dmcphers@redhat.com)
- Bug 874587 - CLOUD_NAME in /etc/openshift/node.conf does not work
  (bleanhar@redhat.com)

* Mon Nov 12 2012 Adam Miller <admiller@redhat.com> 1.1.3-1
- Old copy of this file was not deleted when it moved to origin.
  (rmillner@redhat.com)
- Fix bugz 874826 - pyodbc install fails - needs odbc libraries + headers.
  (ramr@redhat.com)

* Thu Nov 08 2012 Adam Miller <admiller@redhat.com> 1.1.2-1
- Increase the table sizes to cover 15000 nodes in dev and prod.
  (rmillner@redhat.com)
- Add GeoIP-devel to node to allow for geoip modules to be compiled.
  (ramr@redhat.com)
- update migration to 2.0.20 (dmcphers@redhat.com)
- Fix mongodb permissions issue w/ the migrator - bugz 872494 - affect the
  symlink not the target. (ramr@redhat.com)

* Thu Nov 01 2012 Adam Miller <admiller@redhat.com> 1.1.1-1
- bump_minor_versions for sprint 20 (admiller@redhat.com)
- Remove redundant comment. (rmillner@redhat.com)
- Only set MCS labels on cart dirs, git, app-root, etc... (rmillner@redhat.com)
