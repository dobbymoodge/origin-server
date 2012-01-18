%define ruby_sitelibdir            %(ruby -rrbconfig -e "puts Config::CONFIG['sitelibdir']")

Summary:       Multi-tenant cloud management system node tools
Name:          rhc-node
Version:       0.85.3
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
Requires:      perl
Requires:      ruby
Requires:      rubygem-open4
Requires:      rubygem-parseconfig
Requires:      rubygem-cloud-sdk-node
Requires:      quota
Requires:      lsof
Requires:      wget
Requires:      oddjob
Requires:      libjpeg-devel
Requires:      libcurl-devel
Requires:      libpng-devel
Requires:      giflib-devel
Requires(post):   /usr/sbin/semodule
Requires(post):   /usr/sbin/semanage
Requires(postun): /usr/sbin/semodule
Requires(postun): /usr/sbin/semanage

BuildArch: noarch

%description
Turns current host into a OpenShift managed node

%prep
%setup -q

%build
for f in **/*.rb
do
  ruby -c $f
done

%install
rm -rf $RPM_BUILD_ROOT

mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_libexecdir}
mkdir -p %{buildroot}%{_initddir}
mkdir -p %{buildroot}%{ruby_sitelibdir}
mkdir -p %{buildroot}%{_libexecdir}/li
mkdir -p %{buildroot}/usr/share/selinux/packages
mkdir -p %{buildroot}%{_sysconfdir}/cron.daily/
mkdir -p %{buildroot}%{_sysconfdir}/oddjobd.conf.d/
mkdir -p %{buildroot}%{_sysconfdir}/dbus-1/system.d/
mkdir -p %{buildroot}%{_sysconfdir}/cron.daily/
mkdir -p %{buildroot}%{_sysconfdir}/libra/skel
mkdir -p %{buildroot}/%{_localstatedir}/www/html/
mkdir -p %{buildroot}/%{_sysconfdir}/security/
mkdir -p %{buildroot}%{_localstatedir}/lib/libra
mkdir -p %{buildroot}%{_localstatedir}/run/libra
mkdir -p %{buildroot}%{_localstatedir}/lib/libra/.httpd.d
mkdir -p %{buildroot}/%{_sysconfdir}/httpd/conf.d/
ln -s %{_localstatedir}/lib/libra/.httpd.d/ %{buildroot}/%{_sysconfdir}/httpd/conf.d/libra

cp -r cartridges %{buildroot}%{_libexecdir}/li
cp -r conf/httpd %{buildroot}%{_sysconfdir}
cp -r conf/libra %{buildroot}%{_sysconfdir}
cp -r facter %{buildroot}%{ruby_sitelibdir}/facter
cp -r mcollective %{buildroot}%{_libexecdir}
cp -r namespace.d %{buildroot}%{_sysconfdir}/security
cp scripts/bin/* %{buildroot}%{_bindir}
cp scripts/init/* %{buildroot}%{_initddir}
cp scripts/libra_tmpwatch.sh %{buildroot}%{_sysconfdir}/cron.daily/libra_tmpwatch.sh
cp conf/oddjob/openshift-restorer.conf %{buildroot}%{_sysconfdir}/dbus-1/system.d/
cp conf/oddjob/oddjobd-restorer.conf %{buildroot}%{_sysconfdir}/oddjobd.conf.d/
cp scripts/restorer.php %{buildroot}/%{_localstatedir}/www/html/

%clean
rm -rf $RPM_BUILD_ROOT

%post
# mount all desired cgroups under a single root
perl -p -i -e 's:/cgroup/[^\s]+;:/cgroup/all;:; /blkio|cpuset|devices/ && ($_ = "#$_")' /etc/cgconfig.conf
/sbin/restorecon /etc/cgconfig.conf || :
# only restart if it's on
/sbin/chkconfig cgconfig && /sbin/service cgconfig restart >/dev/null 2>&1 || :
/sbin/chkconfig oddjobd on
/sbin/service messagebus restart
/sbin/service oddjobd restart
/sbin/chkconfig --add libra || :
/sbin/chkconfig --add libra-data || :
/sbin/chkconfig --add libra-cgroups || :
/sbin/chkconfig --add libra-tc || :
#/sbin/service mcollective restart > /dev/null 2>&1 || :
/sbin/restorecon /etc/init.d/libra || :
/sbin/restorecon /var/lib/libra || :
/sbin/restorecon /var/run/libra || :
/sbin/restorecon /usr/bin/rhc-cgroup-read || :
/sbin/restorecon /var/lib/libra/.httpd.d/ || :
/usr/bin/rhc-restorecon || :
# only enable if cgconfig is
chkconfig cgconfig && /sbin/service libra-cgroups start > /dev/null 2>&1 || :
# only enable if cgconfig is
chkconfig cgconfig && /sbin/service libra-tc start > /dev/null 2>&1 || :
/sbin/service libra-data start > /dev/null 2>&1 || :
echo "/usr/bin/trap-user" >> /etc/shells
/sbin/restorecon /etc/init.d/libra || :
/sbin/restorecon /etc/init.d/mcollective || :
/sbin/restorecon /usr/bin/rhc-restorer* || :
[ $(/usr/sbin/semanage node -l | /bin/grep -c 255.255.255.128) -lt 1000 ] && /usr/bin/rhc-ip-prep.sh || :

# Ensure the default users have a more restricted shell then normal.
#semanage login -m -s guest_u __default__ || :

# If /etc/httpd/conf.d/libra is a dir, make it a symlink
if [[ -d "/etc/httpd/conf.d/libra.bak" && -L "/etc/httpd/conf.d/libra" ]]
then
    mv /etc/httpd/conf.d/libra.bak/* /var/lib/libra/.httpd.d/
    # not forced to prevent data loss
    rmdir /etc/httpd/conf.d/libra.bak
fi



%preun
if [ "$1" -eq "0" ]; then
    /sbin/service libra-tc stop > /dev/null 2>&1 || :
    /sbin/service libra-cgroups stop > /dev/null 2>&1 || :
    /sbin/chkconfig --del libra-tc || :
    /sbin/chkconfig --del libra-cgroups || :
    /sbin/chkconfig --del libra-data || :
    /sbin/chkconfig --del libra || :
    /usr/sbin/semodule -r libra
    sed -i -e '\:/usr/bin/trap-user:d' /etc/shells
fi

%postun
if [ "$1" -eq 0 ]; then
    /sbin/service mcollective restart > /dev/null 2>&1 || :
fi
#/usr/sbin/semodule -r libra

%pre

if [[ -d "/etc/httpd/conf.d/libra" && ! -L "/etc/httpd/conf.d/libra" ]]
then
    mv /etc/httpd/conf.d/libra/ /etc/httpd/conf.d/libra.bak/
fi

%files
%defattr(-,root,root,-)
%attr(0640,-,-) %{_libexecdir}/mcollective/mcollective/agent/*
%attr(0750,-,-) %{_libexecdir}/mcollective/update_yaml.rb
%attr(0640,-,-) %{ruby_sitelibdir}/facter/libra.rb
%attr(0750,-,-) %{_initddir}/libra
%attr(0750,-,-) %{_initddir}/libra-data
%attr(0750,-,-) %{_initddir}/libra-cgroups
%attr(0750,-,-) %{_initddir}/libra-tc
%attr(0755,-,-) %{_bindir}/trap-user
%attr(0750,-,-) %{_bindir}/rhc-ip-prep.sh
%attr(0750,-,-) %{_bindir}/rhc-iptables.sh
%attr(0750,-,-) %{_bindir}/rhc-restorecon
%attr(0750,-,-) %{_bindir}/rhc-init-quota
%attr(0750,-,-) %{_bindir}/rhc-list-stale
%attr(0750,-,-) %{_bindir}/rhc-idler
%attr(0750,-,-) %{_bindir}/rhc-restorer
%attr(0750,-,apache) %{_bindir}/rhc-restorer-wrapper.sh
%attr(0750,-,-) %{_bindir}/ec2-prep.sh
%attr(0750,-,-) %{_bindir}/remount-secure.sh
%attr(0755,-,-) %{_bindir}/rhc-cgroup-read
%dir %attr(0751,root,root) %{_localstatedir}/lib/libra
%dir %attr(0750,root,root) %{_localstatedir}/lib/libra/.httpd.d
%dir %attr(0700,root,root) %{_localstatedir}/run/libra
%dir %attr(0755,root,root) %{_libexecdir}/li/cartridges/abstract-httpd/
%attr(0750,-,-) %{_libexecdir}/li/cartridges/abstract-httpd/info/hooks/
%attr(0755,-,-) %{_libexecdir}/li/cartridges/abstract-httpd/info/bin/
%{_libexecdir}/li/cartridges/abstract-httpd/info
%dir %attr(0755,root,root) %{_libexecdir}/li/cartridges/abstract/
%attr(0750,-,-) %{_libexecdir}/li/cartridges/abstract/info/hooks/
%attr(0755,-,-) %{_libexecdir}/li/cartridges/abstract/info/bin/
%attr(0755,-,-) %{_libexecdir}/li/cartridges/abstract/info/lib/
%{_libexecdir}/li/cartridges/abstract/info
%attr(0750,-,-) %{_bindir}/rhc-accept-node
%attr(0755,-,-) %{_bindir}/rhc-list-ports
%attr(0750,-,-) %{_bindir}/rhc-node-account
%attr(0750,-,-) %{_bindir}/rhc-node-application
%attr(0755,-,-) %{_bindir}/rhcsh
%attr(0640,-,-) %config(noreplace) %{_sysconfdir}/oddjobd.conf.d/oddjobd-restorer.conf
%attr(0640,-,-) %config(noreplace) %{_sysconfdir}/dbus-1/system.d/openshift-restorer.conf
%attr(0640,-,-) %config(noreplace) %{_sysconfdir}/libra/node.conf
%attr(0640,-,-) %config(noreplace) %{_sysconfdir}/libra/resource_limits.con*
%attr(0750,-,-) %config(noreplace) %{_sysconfdir}/cron.daily/libra_tmpwatch.sh
%attr(0644,-,-) %config(noreplace) %{_sysconfdir}/security/namespace.d/*
%{_localstatedir}/www/html/restorer.php
%attr(0750,root,root) %config(noreplace) %{_sysconfdir}/httpd/conf.d/000000_default.conf
%attr(0640,root,root) %{_sysconfdir}/httpd/conf.d/libra
%dir %attr(0755,root,root) %{_sysconfdir}/libra/skel

%changelog
* Tue Jan 17 2012 Dan McPherson <dmcphers@redhat.com> 0.85.3-1
- US1667: threaddump for rack (wdecoste@localhost.localdomain)

* Tue Jan 17 2012 Dan McPherson <dmcphers@redhat.com> 0.85.2-1
- move district lookup to /etc/libra/district.conf (dmcphers@redhat.com)
- districts (work in progress) (dmcphers@redhat.com)

* Fri Jan 13 2012 Dan McPherson <dmcphers@redhat.com> 0.85.1-1
- bump spec numbers (dmcphers@redhat.com)

* Thu Jan 12 2012 Dan McPherson <dmcphers@redhat.com> 0.84.25-1
- fix node.spec install issue (dmcphers@redhat.com)

* Thu Jan 12 2012 Dan McPherson <dmcphers@redhat.com> 0.84.24-1
- Bug 773606 (dmcphers@redhat.com)

* Wed Jan 11 2012 Dan McPherson <dmcphers@redhat.com> 0.84.23-1
- fixing directory copy failures (mmcgrath@redhat.com)
- Merge branch 'master' of ssh://git1.ops.rhcloud.com/srv/git/li
  (rmillner@redhat.com)
- Bugzilla 772753: Add libcurl dependencies to the wsgi cartridge to support
  pycurl. (rmillner@redhat.com)

* Wed Jan 11 2012 Dan McPherson <dmcphers@redhat.com> 0.84.22-1
- Gracefully handle threaddump in cartridges that do not support it (BZ772114)
  (aboone@redhat.com)

* Fri Jan 06 2012 Dan McPherson <dmcphers@redhat.com> 0.84.21-1
- Make table a parameter.  Clean up help message. (rmillner@redhat.com)
- Can't set default policy on user generated table. (rmillner@redhat.com)

* Fri Jan 06 2012 Dan McPherson <dmcphers@redhat.com> 0.84.20-1
- Bug 772173 (dmcphers@redhat.com)
- Bug 772151 (dmcphers@redhat.com)

* Thu Jan 05 2012 Dan McPherson <dmcphers@redhat.com> 0.84.19-1
- fix build break (dmcphers@redhat.com)

* Thu Jan 05 2012 Dan McPherson <dmcphers@redhat.com> 0.84.18-1
- 

* Thu Jan 05 2012 Dan McPherson <dmcphers@redhat.com> 0.84.17-1
- mysql and mongo move (dmcphers@redhat.com)
- Make UID range a command line option (rmillner@redhat.com)
- Output for /etc/sysconfig/iptables or just run the iptables commands.
  (rmillner@redhat.com)
- Merge branch 'master' of ssh://git1.ops.rhcloud.com/srv/git/li
  (rmillner@redhat.com)
- Script to generate app iptables rules (rmillner@redhat.com)

* Wed Jan 04 2012 Dan McPherson <dmcphers@redhat.com> 0.84.16-1
- allow re-entrant update namespace (dmcphers@redhat.com)

* Wed Jan 04 2012 Dan McPherson <dmcphers@redhat.com> 0.84.15-1
- Merge branch 'master' of git1.ops.rhcloud.com:/srv/git/li
  (wdecoste@localhost.localdomain)
- Bug 771716 migration (wdecoste@localhost.localdomain)

* Wed Jan 04 2012 Dan McPherson <dmcphers@redhat.com> 0.84.14-1
- Merge branch 'master' of ssh://git1.ops.rhcloud.com/srv/git/li
  (mmcgrath@redhat.com)
- force a restorecon on httpd.d (mmcgrath@redhat.com)

* Wed Jan 04 2012 Dan McPherson <dmcphers@redhat.com> 0.84.13-1
- pull in a more rhc-selinux (mmcgrath@redhat.com)

* Wed Jan 04 2012 Alex Boone <aboone@redhat.com> 0.84.12-1
- Merge branch 'master' of ssh://git1.ops.rhcloud.com/srv/git/li
  (mmcgrath@redhat.com)
- removed limits.d from /var/lib/libra (mmcgrath@redhat.com)
- adding auto-create of limits.d (mmcgrath@redhat.com)
- check for symlink of conf.d/libra (mmcgrath@redhat.com)
- Merge branch 'master' of ssh://git1.ops.rhcloud.com/srv/git/li
  (mmcgrath@redhat.com)
- Converting /etc/httpd/conf.d/ to a symlink (mmcgrath@redhat.com)

* Wed Jan 04 2012 Alex Boone <aboone@redhat.com> 0.84.11-1
- node.spec: Added Requires for libjpeg-devel libpng-devel giflib-devel
  (tdawson@redhat.com)

* Tue Jan 03 2012 Dan McPherson <dmcphers@redhat.com> 0.84.10-1
- fix case (dmcphers@redhat.com)
- add 2.0.3 migration (dmcphers@redhat.com)

* Thu Dec 22 2011 Dan McPherson <dmcphers@redhat.com> 0.84.9-1
- fix bad merge (dmcphers@redhat.com)
- remove debug (dmcphers@redhat.com)

* Thu Dec 22 2011 Dan McPherson <dmcphers@redhat.com> 0.84.8-1
- rhc-idler: added ability to list idled apps (twiest@redhat.com)

* Thu Dec 22 2011 Dan McPherson <dmcphers@redhat.com> 0.84.7-1
- node - changed namepace location 12 22 2011 (tkramer@redhat.com)
- added /var/run/libra to the node spec file and changed libra init script
  (twiest@redhat.com)

* Thu Dec 22 2011 Tim Kramer <tkramer@redhat.com> 0.84.6-2
- Changed the namespaced.conf to namespace.d <tkramer@redhat.com>

* Wed Dec 21 2011 Dan McPherson <dmcphers@redhat.com> 0.84.6-1
- Bug 769211 (dmcphers@redhat.com)

* Wed Dec 21 2011 Dan McPherson <dmcphers@redhat.com> 0.84.5-1
- Bug 769211 (dmcphers@redhat.com)

* Tue Dec 20 2011 Alex Boone <aboone@redhat.com> 0.84.4-1
- Adding lock and non-lock functionality (mmcgrath@redhat.com)

* Tue Dec 20 2011 Mike McGrath <mmcgrath@redhat.com> 0.84.3-1
- Merge branch 'master' of li-master:/srv/git/li (ramr@redhat.com)
- Set username and password if default call w/o any arguments. Can only set
  default database to admin database as we need to authenticate against the
  admin database. (ramr@redhat.com)
- BZ768815 replaced uniq with sort -u (jhonce@redhat.com)

* Fri Dec 16 2011 Dan McPherson <dmcphers@redhat.com> 0.84.2-1
- rework rekey broker auth logic (dmcphers@redhat.com)
- some cleanup of server-common (dmcphers@redhat.com)

* Wed Dec 14 2011 Dan McPherson <dmcphers@redhat.com> 0.84.1-1
- bump spec numbers (dmcphers@redhat.com)
- Merge remote-tracking branch 'origin/master' (kraman@gmail.com)
- Merge remote-tracking branch 'origin/mirage' (kraman@gmail.com)
- Merge remote-tracking branch 'origin/master' into mirage (kraman@gmail.com)
- Merge remote-tracking branch 'origin/master' into mirage (kraman@gmail.com)
- Checkpoint: cartridge and embedded actions work (kraman@gmail.com)
- engine -> node (dmcphers@redhat.com)
- more work splitting into 3 gems (dmcphers@redhat.com)
- remove li-controller (dmcphers@redhat.com)

* Wed Dec 14 2011 Dan McPherson <dmcphers@redhat.com> 0.83.14-1
- Merge branch 'master' of li-master:/srv/git/li (ramr@redhat.com)
- Fix for bugz 767825. Allow commands to be run non-interactively on rhcsh.
  (ramr@redhat.com)

* Wed Dec 14 2011 Dan McPherson <dmcphers@redhat.com> 0.83.13-1
- threadump returns message for failed non-jbossas calls
  (wdecoste@localhost.localdomain)

* Tue Dec 13 2011 Dan McPherson <dmcphers@redhat.com> 0.83.12-1
- less popen usage (dmcphers@redhat.com)
- Merge branch 'master' of git1.ops.rhcloud.com:/srv/git/li (rpenta@redhat.com)
- Multi-key support: Update <key-name>:<ssh-pubkey> info s3/user.json, nuke app
  specific ssh key info (rpenta@redhat.com)
- fixing redirect to function correctly (mmcgrath@redhat.com)

* Mon Dec 12 2011 Dan McPherson <dmcphers@redhat.com> 0.83.11-1
- add 2.0.2 migration (dmcphers@redhat.com)

* Mon Dec 12 2011 Mike McGrath <mmcgrath@redhat.com> 0.83.10-1
- Adding restorecon to rhc-restorer (mmcgrath@redhat.com)

* Sun Dec 11 2011 Dan McPherson <dmcphers@redhat.com> 0.83.9-1
- Merge branch 'master' of git1.ops.rhcloud.com:/srv/git/li (rpenta@redhat.com)
- minor touchups to the libra init script (twiest@redhat.com)
- Support for managing multiple sub-users for the RHN/openshift account
  (rpenta@redhat.com)
- added parallization to the libra init script (twiest@redhat.com)
- changed libra init script to output startuser and stopuser in clumps
  (twiest@redhat.com)
- changed the output format of the libra init script (twiest@redhat.com)
- removing notice (mmcgrath@redhat.com)
- Don't start disabled apps (mmcgrath@redhat.com)
- We may have to re-open port 25 access in selinux in order to allow
  communicating to localhost:25 (req for some app frameworks to use the local
  mail solution).  Traffic rate application smtp off-box to modem speed.
  (rmillner@redhat.com)
- Merge branch 'master' of ssh://git1.ops.rhcloud.com/srv/git/li
  (rmillner@redhat.com)
- Add a queue underneath the class for each user and then subclass for
  different traffic rates, with outbound e-mail being limited to 256kbit.
  Naming the queues after the user id class keeps from having to invent another
  scheme (ex: by carving up uids). (rmillner@redhat.com)

* Thu Dec 08 2011 Alex Boone <aboone@redhat.com> 0.83.8-1
- fix for bugz 761384 (ramr@redhat.com)
- change default command to rhcsh if nothing is specified (ramr@redhat.com)
- Added warning (mmcgrath@redhat.com)
- Merge branch 'master' of li-master:/srv/git/li (ramr@redhat.com)
- Fix to rename var to not clobber import + comment quota help for now.
  (ramr@redhat.com)
- Use the mcs_level function from the abstract cartridge to get the
  openshift_mcs_level for the current user. (ramr@redhat.com)

* Wed Dec 07 2011 Mike McGrath <mmcgrath@redhat.com> 0.83.7-1
- Merge branch 'master' of ssh://git1.ops.rhcloud.com/srv/git/li
  (mmcgrath@redhat.com)
- increasing possible mcs labels from 1000 to over 12,000 - US1504
  (mmcgrath@redhat.com)

* Wed Dec 07 2011 Matt Hicks <mhicks@redhat.com> 0.83.6-1
- US1550: add threaddump (wdecoste@localhost.localdomain)
- Merge branch 'master' of li-master:/srv/git/li (ramr@redhat.com)
- Add "alias" to mongo shell w/ internal nosql-db-host automatically set.
  Sample usage:  mongo -u admin -p <mongodb-admin-pass> admin (ramr@redhat.com)

* Tue Dec 06 2011 Alex Boone <aboone@redhat.com> 0.83.5-1
- Added rhc-list-ports (mmcgrath@redhat.com)
- Adding port forwarding allowance, explicit removal of gatway ports
  (mmcgrath@redhat.com)
- added some documentation (mmcgrath@redhat.com)

* Mon Dec 05 2011 Alex Boone <aboone@redhat.com> 0.83.4-1
- 

* Mon Dec 05 2011 Alex Boone <aboone@redhat.com> 0.83.3-1
- changed the libra init script to restart each app individually instead of
  stopping all apps and then starting all apps (twiest@redhat.com)

* Fri Dec 02 2011 Dan McPherson <dmcphers@redhat.com> 0.83.2-1
- Adding restorer-wrapper (mmcgrath@redhat.com)
- using new restorer configs and contexts (mmcgrath@redhat.com)
- Merge branch 'master' of ssh://git1.ops.rhcloud.com/srv/git/li
  (mmcgrath@redhat.com)
- script no longer needs to be run ranged (mmcgrath@redhat.com)

* Thu Dec 01 2011 Dan McPherson <dmcphers@redhat.com> 0.83.1-1
- bump spec numbers (dmcphers@redhat.com)

* Tue Nov 29 2011 Dan McPherson <dmcphers@redhat.com> 0.82.19-1
- Correcting oddjobd call (mmcgrath@redhat.com)
- Correcting restorer.php (mmcgrath@redhat.com)
- Added oddjob configs (mmcgrath@redhat.com)
- prepping for an oddjob version of restorer (mmcgrath@redhat.com)
- Merge branch 'master' of ssh://git1.ops.rhcloud.com/srv/git/li
  (mmcgrath@redhat.com)
- prep work for idler/restorer (mmcgrath@redhat.com)
- Added restorer.php and rhc-idler plans (mmcgrath@redhat.com)
- Merge branch 'master' into idler (mmcgrath@redhat.com)
- Merge branch 'master' into idler (mmcgrath@redhat.com)
- Adding rhc-idler system (mmcgrath@redhat.com)

* Mon Nov 28 2011 Dan McPherson <dmcphers@redhat.com> 0.82.18-1
- move start dbs to deploy (dmcphers@redhat.com)

* Fri Nov 25 2011 Dan McPherson <dmcphers@redhat.com> 0.82.17-1
- go back to old popen for now (dmcphers@redhat.com)

* Wed Nov 23 2011 Dan McPherson <dmcphers@redhat.com> 0.82.16-1
- add back li-controller for stability (dmcphers@redhat.com)

* Tue Nov 22 2011 Dan McPherson <dmcphers@redhat.com> 0.82.15-1
- Merge branch 'master' of ssh://git1.ops.rhcloud.com/srv/git/li
  (mmcgrath@redhat.com)
- fixing syslog call (mmcgrath@redhat.com)
- Bug 755878 (dmcphers@redhat.com)

* Mon Nov 21 2011 Dan McPherson <dmcphers@redhat.com> 0.82.14-1
- li controller cleanup (dmcphers@redhat.com)
- Merge branch 'master' of ssh://git1.ops.rhcloud.com/srv/git/li
  (mmcgrath@redhat.com)
- getting configure working (dmcphers@redhat.com)
- first pass at calling cloud-cdk (dmcphers@redhat.com)
- Merge branch 'master' of ssh://git1.ops.rhcloud.com/srv/git/li
  (mmcgrath@redhat.com)
- Merge branch 'master' of ssh://git1.ops.rhcloud.com/srv/git/li
  (mmcgrath@redhat.com)
- Merge branch 'master' of ssh://git1.ops.rhcloud.com/srv/git/li
  (mmcgrath@redhat.com)
- removing rhc-node-app-ctl (mmcgrath@redhat.com)

* Sat Nov 19 2011 Dan McPherson <dmcphers@redhat.com> 0.82.13-1
- changed rhc-list-stale to say 'not movable' when the stale app has mysql
  embedded (twiest@redhat.com)

* Fri Nov 18 2011 Dan McPherson <dmcphers@redhat.com> 0.82.12-1
- moving logic to abstract from li-controller (dmcphers@redhat.com)
- Switching to the popen4 extension that closes fd's (mhicks@redhat.com)

* Fri Nov 18 2011 Dan McPherson <dmcphers@redhat.com> 0.82.11-1
- Merge branch 'master' of ssh://git1.ops.rhcloud.com/srv/git/li
  (mmcgrath@redhat.com)
- Added rhc-node-app-ctl (mmcgrath@redhat.com)

* Fri Nov 18 2011 Dan McPherson <dmcphers@redhat.com> 0.82.10-1
- more php settings + mirage devenv additions (dmcphers@redhat.com)

* Thu Nov 17 2011 Dan McPherson <dmcphers@redhat.com> 0.82.9-1
- 

* Thu Nov 17 2011 Dan McPherson <dmcphers@redhat.com> 0.82.8-1
- 

* Thu Nov 17 2011 Dan McPherson <dmcphers@redhat.com> 0.82.7-1
- handle job being disabled in jenkins build (dmcphers@redhat.com)
- fail better when job not found on jenkins build (dmcphers@redhat.com)

* Thu Nov 17 2011 Dan McPherson <dmcphers@redhat.com> 0.82.6-1
- Bug 754657 (dmcphers@redhat.com)

* Wed Nov 16 2011 Dan McPherson <dmcphers@redhat.com> 0.82.5-1
- 

* Wed Nov 16 2011 Dan McPherson <dmcphers@redhat.com> 0.82.4-1
- more move error handling and deconfigure ugly error fix (dmcphers@redhat.com)
- fix a couple typos (dmcphers@redhat.com)
- add migration for max upload sizes (dmcphers@redhat.com)

* Tue Nov 15 2011 Dan McPherson <dmcphers@redhat.com> 0.82.3-1
- add tidy (dmcphers@redhat.com)
- add deconfigure app on node script (dmcphers@redhat.com)
- correct perms on .gitconfig (dmcphers@redhat.com)
- migration optimization (dmcphers@redhat.com)
- alter permissions on git dir (dmcphers@redhat.com)
- Merge branch 'master' of ssh://git1.ops.rhcloud.com/srv/git/li
  (mmcgrath@redhat.com)
- Added warning to libra-cgroups (mmcgrath@redhat.com)

* Sat Nov 12 2011 Dan McPherson <dmcphers@redhat.com> 0.82.2-1
- remove httpd proxy from new server on failed move (dmcphers@redhat.com)
- Bug 753040 (dmcphers@redhat.com)

* Thu Nov 10 2011 Dan McPherson <dmcphers@redhat.com> 0.82.1-1
- bump spec numbers (dmcphers@redhat.com)

* Wed Nov 09 2011 Dan McPherson <dmcphers@redhat.com> 0.81.19-1
- Merge branch 'master' of ssh://git1.ops.rhcloud.com/srv/git/li
  (mmcgrath@redhat.com)
- Added high density (mmcgrath@redhat.com)
- bug 752339 (dmcphers@redhat.com)

* Tue Nov 08 2011 Alex Boone <aboone@redhat.com> 0.81.18-1
- filled out the phpmyadmin migrate for bug 749751 (twiest@redhat.com)
- add phpmyadmin migrate stub (dmcphers@redhat.com)
- Added check for overriding aliases (mmcgrath@redhat.com)

* Mon Nov 07 2011 Dan McPherson <dmcphers@redhat.com> 0.81.17-1
- Merge branch 'master' of ssh://git1.ops.rhcloud.com/srv/git/li
  (mmcgrath@redhat.com)
- correcting .tmp location (mmcgrath@redhat.com)

* Mon Nov 07 2011 Dan McPherson <dmcphers@redhat.com> 0.81.16-1
- Adding an explicit restorecon on cgroup read (mmcgrath@redhat.com)

* Mon Nov 07 2011 Dan McPherson <dmcphers@redhat.com> 0.81.15-1
- Bug 751743 (dmcphers@redhat.com)
- Bug 751704 (dmcphers@redhat.com)

* Sun Nov 06 2011 Dan McPherson <dmcphers@redhat.com> 0.81.14-1
- less output from carts (dmcphers@redhat.com)

* Sat Nov 05 2011 Dan McPherson <dmcphers@redhat.com> 0.81.13-1
- log statement, add restart, remove 1 last var on deconfig
  (dmcphers@redhat.com)
- add migration for broken mysql ip (dmcphers@redhat.com)

* Sat Nov 05 2011 Dan McPherson <dmcphers@redhat.com> 0.81.12-1
- cumulative migration for broken apps (dmcphers@redhat.com)

* Fri Nov 04 2011 Dan McPherson <dmcphers@redhat.com> 0.81.11-1
- move maven mirror info to ci_build.sh (dmcphers@redhat.com)

* Fri Nov 04 2011 Dan McPherson <dmcphers@redhat.com> 0.81.10-1
- explicitly add skeleton directory for empty user accounts
  (markllama@redhat.com)

* Thu Nov 03 2011 Dan McPherson <dmcphers@redhat.com> 0.81.9-1
- move updates, add pre_build (dmcphers@redhat.com)
- correcting context issues (mmcgrath@redhat.com)

* Thu Nov 03 2011 Dan McPherson <dmcphers@redhat.com> 0.81.8-1
- abstract move into each cart and embedded cart (dmcphers@redhat.com)

* Thu Nov 03 2011 Dan McPherson <dmcphers@redhat.com> 0.81.7-1
- fix typo (dmcphers@redhat.com)
- moving of embedded apps (dmcphers@redhat.com)
- split out deploy httpd proxy/config for embedded apps, change stop to stop
  all for ctl-app and deconfigure and stop and start to all for pre/post
  receive (dmcphers@redhat.com)

* Wed Nov 02 2011 Dan McPherson <dmcphers@redhat.com> 0.81.6-1
- move passwords out of curl command (dmcphers@redhat.com)
- correcting hooks (mmcgrath@redhat.com)
- merging (mmcgrath@redhat.com)
- Allowing alias add / remove (mmcgrath@redhat.com)

* Wed Nov 02 2011 Dan McPherson <dmcphers@redhat.com> 0.81.5-1
- use jenkins api (dmcphers@redhat.com)
- Output tweaks (mhicks@redhat.com)
- Switching build to use the Jenkins REST API (mhicks@redhat.com)

* Wed Nov 02 2011 Dan McPherson <dmcphers@redhat.com> 0.81.4-1
- fix move for jboss (dmcphers@redhat.com)
- disabling new git check for the moment (mmcgrath@redhat.com)
- Merge branch 'master' of ssh://git1.ops.rhcloud.com/srv/git/li
  (mmcgrath@redhat.com)
- working application move (dmcphers@redhat.com)
- Allowing add and remove server alias (mmcgrath@redhat.com)
- Added add/remove server alias hooks (mmcgrath@redhat.com)
- properly escape li-controller commands and remove email call to configure
  (mmcgrath@redhat.com)
- added checks for a missing or empty git dir to rhc-accept-node
  (twiest@redhat.com)

* Tue Nov 01 2011 Dan McPherson <dmcphers@redhat.com> 0.81.3-1
- adding 60 day marker (mmcgrath@redhat.com)
- Adding rhc-list-stale (mmcgrath@redhat.com)

* Fri Oct 28 2011 Dan McPherson <dmcphers@redhat.com> 0.81.2-1
- Fix if ipv6 is in proc to disable it. (tkramer@redhat.com)

* Thu Oct 27 2011 Dan McPherson <dmcphers@redhat.com> 0.81.1-1
- bump spec numbers (dmcphers@redhat.com)

* Wed Oct 26 2011 Dan McPherson <dmcphers@redhat.com> 0.80.24-1
- move app info for embedded carts to separate call (dmcphers@redhat.com)
- Disable ipv6 selinux friendly style (tkramer@tkramer.timtech)
- bug 749133 (dmcphers@redhat.com)
- Change ipv6 disable oin sysctl.conf (tkramer@tkramer.timtech)
- Bug 749113 (dmcphers@redhat.com)

* Wed Oct 26 2011 Dan McPherson <dmcphers@redhat.com> 0.80.23-1
- 749073 and 749076 (dmcphers@redhat.com)

* Wed Oct 26 2011 Dan McPherson <dmcphers@redhat.com> 0.80.22-1
- bug 749069 (dmcphers@redhat.com)

* Tue Oct 25 2011 Dan McPherson <dmcphers@redhat.com> 0.80.21-1
- use repo as the default rather than runtime/repo (dmcphers@redhat.com)
- libra-data init script: changed aws value lookup timeout from 10 seconds to 1
  second so that the script pauses at most 2 minutes instead of 20 minutes
  (twiest@redhat.com)

* Mon Oct 24 2011 Dan McPherson <dmcphers@redhat.com> 0.80.20-1
- make workspace and repo dir the same in jenkins build (dmcphers@redhat.com)
- repo and deploy -> runtime (dmcphers@redhat.com)
- fixed bug in util/force_kill (twiest@redhat.com)
- added retry logic to libra-data for public_hostname (twiest@redhat.com)
- Added override option in node.conf for public_hostname (twiest@redhat.com)
- Update with my ipv6 disable (tkramer@tkramer.timtech)

* Mon Oct 24 2011 Dan McPherson <dmcphers@redhat.com> 0.80.19-1
- disable ipv6 SELinux friendly style (tkramer@tkramer.timtech)

* Fri Oct 21 2011 Dan McPherson <dmcphers@redhat.com> 0.80.18-1
- up app name limit to 32 (dmcphers@redhat.com)

* Fri Oct 21 2011 Dan McPherson <dmcphers@redhat.com> 0.80.17-1
- add ci to and migration for it (dmcphers@redhat.com)

* Wed Oct 19 2011 Dan McPherson <dmcphers@redhat.com> 0.80.16-1
- Adding 100M swap to all nodes (mmcgrath@redhat.com)
- add force-stop to client (dmcphers@redhat.com)
- add ip back to raw (dmcphers@redhat.com)

* Tue Oct 18 2011 Dan McPherson <dmcphers@redhat.com> 0.80.15-1
- Merge branch 'master' of ssh://git1.ops.rhcloud.com/srv/git/li
  (mmcgrath@redhat.com)
- using whoami to get logname (mmcgrath@redhat.com)

* Tue Oct 18 2011 Dan McPherson <dmcphers@redhat.com> 0.80.14-1
- 

* Tue Oct 18 2011 Dan McPherson <dmcphers@redhat.com> 0.80.13-1
- add migration for existing mysql apps (dmcphers@redhat.com)

* Tue Oct 18 2011 Matt Hicks <mhicks@redhat.com> 0.80.12-1
- Bug 745749 (dmcphers@redhat.com)
- add include guard to libs (dmcphers@redhat.com)
- rewrite migration to be multi threaded per node (dmcphers@redhat.com)

* Mon Oct 17 2011 Dan McPherson <dmcphers@redhat.com> 0.80.11-1
- undo redirection (dmcphers@redhat.com)

* Mon Oct 17 2011 Dan McPherson <dmcphers@redhat.com> 0.80.10-1
- less output on configure (dmcphers@redhat.com)

* Mon Oct 17 2011 Dan McPherson <dmcphers@redhat.com> 0.80.9-1
- Merge branch 'master' of ssh://git1.ops.rhcloud.com/srv/git/li
  (mmcgrath@redhat.com)
- Ensuring all services are started when issuing a 'start'
  (mmcgrath@redhat.com)
- add abstract (more generic than httpd)  cart and use from existing carts
  (dmcphers@redhat.com)
- making bash type (mmcgrath@redhat.com)
- increasing nproc limit (mmcgrath@redhat.com)
- Added support for force-stop (mmcgrath@redhat.com)
- Allow force-stop (mmcgrath@redhat.com)

* Mon Oct 17 2011 Dan McPherson <dmcphers@redhat.com> 0.80.8-1
- Bug 746583 (dmcphers@redhat.com)

* Sun Oct 16 2011 Dan McPherson <dmcphers@redhat.com> 0.80.7-1
- abstract out remainder of deconfigure (dmcphers@redhat.com)

* Sat Oct 15 2011 Dan McPherson <dmcphers@redhat.com> 0.80.6-1
- move jenkins specific method back to jenkins (dmcphers@redhat.com)

* Sat Oct 15 2011 Dan McPherson <dmcphers@redhat.com> 0.80.5-1
- abstract out common vars in remaining hooks (dmcphers@redhat.com)
- more abstracting (dmcphers@redhat.com)
- switch error to warning on git removal fail more abstracting
  (dmcphers@redhat.com)
- more abstracting (dmcphers@redhat.com)
- more abstracting of common code (dmcphers@redhat.com)
- move sources to the top and abstract out error method (dmcphers@redhat.com)
- missed a mcs_level in start (dmcphers@redhat.com)
- move simple functions to source files (dmcphers@redhat.com)

* Fri Oct 14 2011 Dan McPherson <dmcphers@redhat.com> 0.80.4-1
- fix param order (dmcphers@redhat.com)

* Fri Oct 14 2011 Dan McPherson <dmcphers@redhat.com> 0.80.3-1
- abstract destroy git repo and rm httpd proxy (dmcphers@redhat.com)

* Fri Oct 14 2011 Dan McPherson <dmcphers@redhat.com> 0.80.2-1
- Bug 746182 (dmcphers@redhat.com)

* Fri Oct 14 2011 Dan McPherson <dmcphers@redhat.com> 0.80.1-1
- fix spec number (dmcphers@redhat.com)

* Fri Oct 14 2011 Dan McPherson <dmcphers@redhat.com> 0.70.3-1
- handle space in desc passing (dmcphers@redhat.com)

* Fri Oct 14 2011 Dan McPherson <dmcphers@redhat.com> 0.70.2-1
- abstract create_repo (dmcphers@redhat.com)
- fix typo (dmcphers@redhat.com)

* Thu Oct 13 2011 Dan McPherson <dmcphers@redhat.com> 0.70.1-1
- bump spec numbers (dmcphers@redhat.com)
- Bug 745749 (dmcphers@redhat.com)

* Wed Oct 12 2011 Dan McPherson <dmcphers@redhat.com> 0.79.18-1
- abstract out find_open_ip (dmcphers@redhat.com)

* Wed Oct 12 2011 Dan McPherson <dmcphers@redhat.com> 0.79.17-1
- abstract rm_symlink (dmcphers@redhat.com)

* Wed Oct 12 2011 Dan McPherson <dmcphers@redhat.com> 0.79.16-1
- abstract out common logic (dmcphers@redhat.com)
- Bug 745373 and remove sessions where not needed (dmcphers@redhat.com)
- Bug 745401 (dmcphers@redhat.com)

* Tue Oct 11 2011 Dan McPherson <dmcphers@redhat.com> 0.79.15-1
- mv pw to password-file and create jenkins-client-1.4 dir
  (dmcphers@redhat.com)

* Tue Oct 11 2011 Dan McPherson <dmcphers@redhat.com> 0.79.14-1
- add authentication to jenkins (dmcphers@redhat.com)
- Disable IPV6 in libra init.d file (tkramer@tkramer.timtech)
- Removed ipv6 disable (tkramer@tkramer.timtech)
- Disable IPV6 (tkramer@tkramer.timtech)

* Tue Oct 11 2011 Dan McPherson <dmcphers@redhat.com> 0.79.13-1
- fix unused get framework too (dmcphers@redhat.com)

* Mon Oct 10 2011 Dan McPherson <dmcphers@redhat.com> 0.79.12-1
- pre_deploy -> pre_build (dmcphers@redhat.com)

* Mon Oct 10 2011 Dan McPherson <dmcphers@redhat.com> 0.79.11-1
- post receive cleanup (dmcphers@redhat.com)
- call build instead of post receive (dmcphers@redhat.com)
- common post receive and add pre deploy (dmcphers@redhat.com)
- Merge branch 'master' of ssh://git1.ops.rhcloud.com/srv/git/li
  (mmcgrath@redhat.com)
- correctly checking for post_deploy script (mmcgrath@redhat.com)
- Allow post_deploy (mmcgrath@redhat.com)
- Adding post_deploy methods (mmcgrath@redhat.com)

* Mon Oct 10 2011 Dan McPherson <dmcphers@redhat.com> 0.79.10-1
- make start/stop blocking (dmcphers@redhat.com)
- Merge branch 'master' of ssh://git1.ops.rhcloud.com/srv/git/li
  (mmcgrath@redhat.com)
- fixing deploy (mmcgrath@redhat.com)
- more jenkins job work (dmcphers@redhat.com)

* Mon Oct 10 2011 Dan McPherson <dmcphers@redhat.com> 0.79.9-1
- add deploy step and call from jenkins with stop start (dmcphers@redhat.com)
- Adding deploy.sh (mmcgrath@redhat.com)
- Merge branch 'master' of ssh://git1.ops.rhcloud.com/srv/git/li
  (mmcgrath@redhat.com)
- Adding ctl_all command and fixing rhcsh path (mmcgrath@redhat.com)

* Sun Oct 09 2011 Dan McPherson <dmcphers@redhat.com> 0.79.8-1
- change fix to be based on suggestion (dmcphers@redhat.com)
- Bug 744513 (dmcphers@redhat.com)
- Bug 744375 (dmcphers@redhat.com)

* Sat Oct 08 2011 Dan McPherson <dmcphers@redhat.com> 0.79.7-1
- use alternate skeleton for new users (markllama@redhat.com)
- added empty skeleton directory for new users (markllama@redhat.com)
- missed one JENKINS_URL (dmcphers@redhat.com)

* Thu Oct 06 2011 Dan McPherson <dmcphers@redhat.com> 0.79.6-1
- add jenkins build kickoff to all post receives (dmcphers@redhat.com)
- add m2_home, java_home, update path, add migration for each and jenkins job
  jboss template (dmcphers@redhat.com)
- Adding rsync support (mmcgrath@redhat.com)
- fix some deconfigures for httpd proxy (dmcphers@redhat.com)

* Wed Oct 05 2011 Dan McPherson <dmcphers@redhat.com> 0.79.5-1
- add ipv4 and split out standalone.sh and standalone.conf
  (dmcphers@redhat.com)

* Wed Oct 05 2011 Dan McPherson <dmcphers@redhat.com> 0.79.4-1
- undo test (dmcphers@redhat.com)

* Wed Oct 05 2011 Dan McPherson <dmcphers@redhat.com> 0.79.3-1
- trying to figure out whats wrong with the ami (dmcphers@redhat.com)
- fixing whitespace (mmcgrath@redhat.com)
- allow libra-data to run on non-EC2 nodes (markllama@redhat.com)

* Tue Oct 04 2011 Dan McPherson <dmcphers@redhat.com> 0.79.2-1
- cleanup (dmcphers@redhat.com)
- cleanup (dmcphers@redhat.com)
- add deploy httpd proxy and migration (dmcphers@redhat.com)
- beginning of migrate 2.1.6 (dmcphers@redhat.com)
- removing agent forward denial (mmcgrath@redhat.com)
- replace update_yaml.pp with update_yaml.rb (blentz@redhat.com)
- properly secure node_data.conf (mmcgrath@redhat.com)

* Thu Sep 29 2011 Dan McPherson <dmcphers@redhat.com> 0.79.1-1
- bump spec numbers (dmcphers@redhat.com)
- add condition around removing env var (dmcphers@redhat.com)
- add : to allowed args (dmcphers@redhat.com)
- env var add/remove (dmcphers@redhat.com)

* Wed Sep 28 2011 Dan McPherson <dmcphers@redhat.com> 0.78.15-1
- add preconfigure for jenkins to split out auth key gen (dmcphers@redhat.com)

* Wed Sep 28 2011 Dan McPherson <dmcphers@redhat.com> 0.78.14-1
- Correcting bandwidth error (mmcgrath@redhat.com)

* Mon Sep 26 2011 Dan McPherson <dmcphers@redhat.com> 0.78.13-1
- let ssh key alter work with multiple keys (dmcphers@redhat.com)

* Fri Sep 23 2011 Dan McPherson <dmcphers@redhat.com> 0.78.12-1
- up upload limit to 10M (dmcphers@redhat.com)
- fixed typo in openshift_mcs_level (markllama@redhat.com)

* Thu Sep 22 2011 Dan McPherson <dmcphers@redhat.com> 0.78.11-1
- add migration of changing path order (dmcphers@redhat.com)

* Tue Sep 20 2011 Dan McPherson <dmcphers@redhat.com> 0.78.10-1
- added sensitivity (s0:) to the openshift_mcs_level function return value
  (markllama@redhat.com)
- call add and remove ssh keys from jenkins configure and deconfigure
  (dmcphers@redhat.com)

* Mon Sep 19 2011 Dan McPherson <dmcphers@redhat.com> 0.78.9-1
- missed a file on a rename (dmcphers@redhat.com)
- rename migration (dmcphers@redhat.com)
- US1056 (dmcphers@redhat.com)

* Thu Sep 15 2011 Dan McPherson <dmcphers@redhat.com> 0.78.8-1
- set execute perms on mcs_level (markllama@redhat.com)
- updated mcs_level generation for app accounts > 522 (markllama@redhat.com)
- broker auth fixes - functional for adding token (dmcphers@redhat.com)

* Wed Sep 14 2011 Dan McPherson <dmcphers@redhat.com> 0.78.7-1
- disable client gem release (temp) beginnings of broker auth adding barista to
  spec (dmcphers@redhat.com)
- unset x-forwarded-for (mmcgrath@redhat.com)
- fixing paths for token and IV file (mmcgrath@redhat.com)
- allowing broker-auth-key (mmcgrath@redhat.com)
- Add broker auth and remove bits (mmcgrath@redhat.com)

* Mon Sep 12 2011 Dan McPherson <dmcphers@redhat.com> 0.78.6-1
- Merge branch 'master' of ssh://git1.ops.rhcloud.com/srv/git/li
  (twiest@redhat.com)
- rhc-accept-node: fixed check_app_dirs bug where it would look at symlinks
  (twiest@redhat.com)
- Merge branch 'master' of ssh://git1.ops.rhcloud.com/srv/git/li
  (mmcgrath@redhat.com)
- Add storage (mmcgrath@redhat.com)
- rhc-accept-node: added check for app dirs without users (twiest@redhat.com)
- rhc-accept-node: added check for empty home dirs (twiest@redhat.com)

* Mon Sep 12 2011 Dan McPherson <dmcphers@redhat.com> 0.78.5-1
- Merge branch 'master' of ssh://git1.ops.rhcloud.com/srv/git/li
  (twiest@redhat.com)
- rhc-accept-node: fixed libra_device function to work in both devenv and PROD
  (twiest@redhat.com)
- rhc-accept-node: refactored failure message into fail function
  (twiest@redhat.com)
- rhc-accept-node: added check for user home directories (twiest@redhat.com)
- rhc-accept-node: fixed bug where quota errors were not being counted
  (twiest@redhat.com)
- rhc-accept-node: changed the default selinux bool list to check for
  httpd_can_network_connect:on since we use that in STG and PROD
  (twiest@redhat.com)
- rhc-accept-node: removed qpidd from default services as per mmcgrath
  (twiest@redhat.com)

* Mon Sep 12 2011 Dan McPherson <dmcphers@redhat.com> 0.78.4-1
- rhc-accept-node: fixed libra_device to work for long device names
  (twiest@redhat.com)

* Fri Sep 09 2011 Matt Hicks <mhicks@redhat.com> 0.78.3-1
- Adding wget to requires (mmcgrath@redhat.com)
- Merge branch 'master' of ssh://git1.ops.rhcloud.com/srv/git/li
  (mmcgrath@redhat.com)
- since some of these are files and some are links, we'll want to ensure we hit
  both of them (mmcgrath@redhat.com)
- correcting jumbo type (mmcgrath@redhat.com)
- Added node profile (mmcgrath@redhat.com)
- Added node profile (mmcgrath@redhat.com)
- Added arbitrary capacity planning (mmcgrath@redhat.com)

* Thu Sep 01 2011 Dan McPherson <dmcphers@redhat.com> 0.78.2-1
- Merge branch 'master' of ssh://git1.ops.rhcloud.com/srv/git/li
  (mmcgrath@redhat.com)
- changed max_apps_multiplier to max_apps (mmcgrath@redhat.com)

* Thu Sep 01 2011 Dan McPherson <dmcphers@redhat.com> 0.78.1-1
- Adding max apps multiplier (mmcgrath@redhat.com)
- Adding proper settings for new resource limits (mmcgrath@redhat.com)
- Merge branch 'master' of ssh://git1.ops.rhcloud.com/srv/git/li
  (mmcgrath@redhat.com)
- bump spec numbers (dmcphers@redhat.com)
- Altering how the default resource limit is determined (mmcgrath@redhat.com)
- adding new resource limits to spec file (mmcgrath@redhat.com)
- add system ssh key support along with the beginning of multiple ssh key
  support (dmcphers@redhat.com)
- Added new resrouce limit types (mmcgrath@redhat.com)

* Wed Aug 31 2011 Dan McPherson <dmcphers@redhat.com> 0.77.10-1
- bz726646 patch attempt #2 (markllama@redhat.com)

* Mon Aug 29 2011 Dan McPherson <dmcphers@redhat.com> 0.77.9-1
- Revert "Revert "reverse patched to removed commit
  d34abaacc98e5b8f5387eff71064c4616a61f24b"" (markllama@gmail.com)
- Revert "reverse patched to removed commit
  d34abaacc98e5b8f5387eff71064c4616a61f24b" (markllama@redhat.com)

* Mon Aug 29 2011 Dan McPherson <dmcphers@redhat.com> 0.77.8-1
- reverse patched to removed commit d34abaacc98e5b8f5387eff71064c4616a61f24b
  (markllama@redhat.com)

* Mon Aug 29 2011 Dan McPherson <dmcphers@redhat.com> 0.77.7-1
- bz736646 - allow pty for ssh commands (markllama@redhat.com)

* Mon Aug 29 2011 Dan McPherson <dmcphers@redhat.com> 0.77.6-1
- Merge branch 'master' of ssh://git1.ops.rhcloud.com/srv/git/li
  (mmcgrath@redhat.com)
- increase proxy timeout to 30 (mmcgrath@redhat.com)

* Fri Aug 26 2011 Dan McPherson <dmcphers@redhat.com> 0.77.5-1
- Bug 733227 (dmcphers@redhat.com)

* Thu Aug 25 2011 Dan McPherson <dmcphers@redhat.com> 0.77.4-1
- Adding mkdir (mmcgrath@redhat.com)
- add cname migration added (dmcphers@redhat.com)
- add CNAME support (turned off) (dmcphers@redhat.com)
- Adding support for jenkins slaves (mmcgrath@redhat.com)

* Wed Aug 24 2011 Dan McPherson <dmcphers@redhat.com> 0.77.3-1
- try adding restorecon of aquota.user (dmcphers@redhat.com)

* Wed Aug 24 2011 Dan McPherson <dmcphers@redhat.com> 0.77.2-1
- add to client tools the ability to specify your rsa key file as well as
  default back to id_rsa as a last resort (dmcphers@redhat.com)
- chgrping env (mmcgrath@redhat.com)
- Merge branch 'master' of ssh://git1.ops.rhcloud.com/srv/git/li
  (mmcgrath@redhat.com)
- do not allow users to alter their own env vars (mmcgrath@redhat.com)
- convert strings to tuples in 'in' comparisons so whole string comparisons get
  done instead of substring (mmcgrath@redhat.com)

* Fri Aug 19 2011 Matt Hicks <mhicks@redhat.com> 0.77.1-1
- fix wsgi apps (dmcphers@redhat.com)
- bump spec numbers (dmcphers@redhat.com)
- splitting app_ctl.sh out (dmcphers@redhat.com)

* Thu Aug 18 2011 Dan McPherson <dmcphers@redhat.com> 0.76.17-1
- fix perms on .env (dmcphers@redhat.com)

* Thu Aug 18 2011 Dan McPherson <dmcphers@redhat.com> 0.76.16-1
- fix repo dir for rack on migration (dmcphers@redhat.com)

* Wed Aug 17 2011 Dan McPherson <dmcphers@redhat.com> 0.76.15-1
- re-adding (mmcgrath@redhat.com)

* Wed Aug 17 2011 Dan McPherson <dmcphers@redhat.com> 0.76.14-1
- moving cgroup-read to correct bin (mmcgrath@redhat.com)
- Merge branch 'master' of ssh://git1.ops.rhcloud.com/srv/git/li
  (mmcgrath@redhat.com)
- Fixing for real this time (mmcgrath@redhat.com)

* Wed Aug 17 2011 Dan McPherson <dmcphers@redhat.com> 0.76.13-1
- Merge branch 'master' of ssh://git1.ops.rhcloud.com/srv/git/li
  (mmcgrath@redhat.com)
- adding cgroup_read (mmcgrath@redhat.com)

* Wed Aug 17 2011 Dan McPherson <dmcphers@redhat.com> 0.76.12-1
- Merge branch 'master' of ssh://git1.ops.rhcloud.com/srv/git/li
  (mmcgrath@redhat.com)
- Added cgroup_read (mmcgrath@redhat.com)

* Wed Aug 17 2011 Dan McPherson <dmcphers@redhat.com> 0.76.11-1
- 731254 (dmcphers@redhat.com)
- fixing kill calls (mmcgrath@redhat.com)

* Wed Aug 17 2011 Dan McPherson <dmcphers@redhat.com> 0.76.10-1
- add app type and db type and migration restart (dmcphers@redhat.com)

* Tue Aug 16 2011 Dan McPherson <dmcphers@redhat.com> 0.76.9-1
- cleanup (dmcphers@redhat.com)

* Tue Aug 16 2011 Dan McPherson <dmcphers@redhat.com> 0.76.8-1
- cleanup how we call snapshot (dmcphers@redhat.com)
- redo the start/stop changes (dmcphers@redhat.com)
- migration fix for post/pre receive (dmcphers@redhat.com)
- split out post and pre receive from the apps (dmcphers@redhat.com)
- Merge branch 'master' of ssh://git1.ops.rhcloud.com/srv/git/li
  (mmcgrath@redhat.com)
- prefixing backup and restore with UUID (mmcgrath@redhat.com)
- Merge branch 'master' of ssh://git1.ops.rhcloud.com/srv/git/li
  (mmcgrath@redhat.com)
- correcting double quote (mmcgrath@redhat.com)

* Tue Aug 16 2011 Matt Hicks <mhicks@redhat.com> 0.76.7-1
- JBoss cgroup and container tuning (mhicks@redhat.com)
- splitting out stop/start, changing snapshot to use stop start and bug 730890
  (dmcphers@redhat.com)
- Added cleanup (mmcgrath@redhat.com)
- allowing user to alter username and password (mmcgrath@redhat.com)
- dirs should end with / (mmcgrath@redhat.com)
- Appending / to dir names (mmcgrath@redhat.com)
- ensuring /tmp ends with a / (mmcgrath@redhat.com)

* Mon Aug 15 2011 Dan McPherson <dmcphers@redhat.com> 0.76.6-1
- adding migration for snapshot/restore (dmcphers@redhat.com)
- snapshot and restore using path (dmcphers@redhat.com)

* Mon Aug 15 2011 Matt Hicks <mhicks@redhat.com> 0.76.5-1
- rename li-controller-0.1 to li-controller (dmcphers@redhat.com)

* Sun Aug 14 2011 Dan McPherson <dmcphers@redhat.com> 0.76.4-1
- adding rhcsh (mmcgrath@redhat.com)
- Added new scripted snapshot (mmcgrath@redhat.com)
- Added rhcsh, as well as _RESTORE functionality (mmcgrath@redhat.com)
- rhcshell bits (mmcgrath@redhat.com)
- restore error handling (dmcphers@redhat.com)
- functional restore (dmcphers@redhat.com)

* Tue Aug 09 2011 Dan McPherson <dmcphers@redhat.com> 0.76.3-1
- get restore to a basic functional level (dmcphers@redhat.com)

* Mon Aug 08 2011 Dan McPherson <dmcphers@redhat.com> 0.76.2-1
- restore work in progress (dmcphers@redhat.com)

* Fri Aug 05 2011 Dan McPherson <dmcphers@redhat.com> 0.76.1-1
- bump spec numbers (dmcphers@redhat.com)

* Wed Aug 03 2011 Dan McPherson <dmcphers@redhat.com> 0.75.3-1
- increase nproc to 100 (dmcphers@redhat.com)

* Tue Jul 26 2011 Dan McPherson <dmcphers@redhat.com> 0.75.2-1
- add passenger tmp dir migration (dmcphers@redhat.com)
- migration work (dmcphers@redhat.com)
- add base migration for 2.1.2 (dmcphers@redhat.com)

* Thu Jul 21 2011 Dan McPherson <dmcphers@redhat.com> 0.75.1-1
- Export vars (mmcgrath@redhat.com)
- fixing .env ownership (mmcgrath@redhat.com)
- renaming USERNAME to APP_UUID to avoid confusion (mmcgrath@redhat.com)
- Adding environment infrastructure (mmcgrath@redhat.com)
- removing email address from persistent data (mmcgrath@redhat.com)
- bump spec numbers (dmcphers@redhat.com)
- add server identity and namespace auto migrate (dmcphers@redhat.com)

* Mon Jul 18 2011 Dan McPherson <dmcphers@redhat.com> 0.74.9-1
- cleanup (dmcphers@redhat.com)

* Mon Jul 18 2011 Dan McPherson <dmcphers@redhat.com> 0.74.8-1
- remove libra specific daemon (mmcgrath@redhat.com)
- 722836 (dmcphers@redhat.com)

* Fri Jul 15 2011 Dan McPherson <dmcphers@redhat.com> 0.74.7-1
- 

* Fri Jul 15 2011 Dan McPherson <dmcphers@redhat.com> 0.74.6-1
- bug 721296 (dmcphers@redhat.com)

* Wed Jul 13 2011 Dan McPherson <dmcphers@redhat.com> 0.74.5-1
- mkdir before copy (mmcgrath@redhat.com)
- Adding tmpwatch (mmcgrath@redhat.com)

* Wed Jul 13 2011 Dan McPherson <dmcphers@redhat.com> 0.74.4-1
- Changing shell for this command (mmcgrath@redhat.com)

* Wed Jul 13 2011 Dan McPherson <dmcphers@redhat.com> 0.74.3-1
- Adding pam_namespace and polyinst /tmp (mmcgrath@redhat.com)

* Tue Jul 12 2011 Dan McPherson <dmcphers@redhat.com> 0.74.2-1
- Automatic commit of package [rhc-node] release [0.74.1-1].
  (dmcphers@redhat.com)
- bumping spec numbers (dmcphers@redhat.com)
- add options to tail-files (dmcphers@redhat.com)
- Automatic commit of package [rhc-node] release [0.73.13-1].
  (dmcphers@redhat.com)
- Be more forceful about cleanup on removal (mmcgrath@redhat.com)
- Automatic commit of package [rhc-node] release [0.73.12-1].
  (dmcphers@redhat.com)
- remove syntax error from libra-data (dmcphers@redhat.com)
- Automatic commit of package [rhc-node] release [0.73.11-1].
  (dmcphers@redhat.com)
- Adding lsof as a req for node (mmcgrath@redhat.com)
- Merge branch 'master' of ssh://git1.ops.rhcloud.com/srv/git/li
  (mmcgrath@redhat.com)
- Automatic commit of package [rhc-node] release [0.73.10-1].
  (edirsh@redhat.com)
- Don't include 'embedded' as a cart, ever. (jimjag@redhat.com)
- Adding polyinstantiated tmp dir for pam_namespace (mmcgrath@redhat.com)
- Automatic commit of package [rhc-node] release [0.73.9-1].
  (edirsh@redhat.com)
- simplifying start script - checking for embedded cartridges
  (mmcgrath@redhat.com)
- Automatic commit of package [rhc-node] release [0.73.8-1].
  (dmcphers@redhat.com)
- Automatic commit of package [rhc-node] release [0.73.7-1].
  (dmcphers@redhat.com)
- fixup embedded cart remove (dmcphers@redhat.com)
- Automatic commit of package [rhc-node] release [0.73.6-1].
  (dmcphers@redhat.com)
- perf improvements for how/when we look up the valid cart types on the server
  (dmcphers@redhat.com)
- Merge remote-tracking branch 'origin/master' (markllama@redhat.com)
- switched deconfigure back to symlink to maintain identity with configure
  (markllama@redhat.com)
- updated (de)configure to remove tc elements (markllama@redhat.com)
- Merge branch 'master' of ssh://git1.ops.rhcloud.com/srv/git/li
  (mmcgrath@redhat.com)
- fixing embedded call and adding debug (mmcgrath@redhat.com)
- ensure any apps still running from the user are actually dead / gone
  (mmcgrath@redhat.com)
- Automatic commit of package [rhc-node] release [0.73.5-1].
  (dmcphers@redhat.com)
- add nurture migration for existing apps (dmcphers@redhat.com)
- undo passing rhlogin to cart (dmcphers@redhat.com)
- add nurture call for git push (dmcphers@redhat.com)
- fixing merge from Dan (mmcgrath@redhat.com)
- proper error handling for embedded cases (mmcgrath@redhat.com)
- Automatic commit of package [rhc-node] release [0.73.4-1].
  (mhicks@redhat.com)
- Merge branch 'master' of ssh://git1.ops.rhcloud.com/srv/git/li
  (mmcgrath@redhat.com)
- Added support to call embedded cartridges (mmcgrath@redhat.com)
- Automatic commit of package [rhc-node] release [0.73.3-1].
  (dmcphers@redhat.com)
- Bug 717168 (dmcphers@redhat.com)
- Added embedded list (mmcgrath@redhat.com)

* Mon Jul 11 2011 Dan McPherson <dmcphers@redhat.com> 0.74.1-1
- bumping spec numbers (dmcphers@redhat.com)
- add options to tail-files (dmcphers@redhat.com)

* Sat Jul 09 2011 Dan McPherson <dmcphers@redhat.com> 0.73.13-1
- Be more forceful about cleanup on removal (mmcgrath@redhat.com)

* Thu Jul 07 2011 Dan McPherson <dmcphers@redhat.com> 0.73.12-1
- remove syntax error from libra-data (dmcphers@redhat.com)

* Tue Jul 05 2011 Dan McPherson <dmcphers@redhat.com> 0.73.11-1
- Adding lsof as a req for node (mmcgrath@redhat.com)
- Merge branch 'master' of ssh://git1.ops.rhcloud.com/srv/git/li
  (mmcgrath@redhat.com)
- Adding polyinstantiated tmp dir for pam_namespace (mmcgrath@redhat.com)

* Tue Jul 05 2011 Emily Dirsh <edirsh@redhat.com> 0.73.10-1
- Don't include 'embedded' as a cart, ever. (jimjag@redhat.com)

* Fri Jul 01 2011 Emily Dirsh <edirsh@redhat.com> 0.73.9-1
- simplifying start script - checking for embedded cartridges
  (mmcgrath@redhat.com)

* Fri Jul 01 2011 Dan McPherson <dmcphers@redhat.com> 0.73.8-1
- 

* Fri Jul 01 2011 Dan McPherson <dmcphers@redhat.com> 0.73.7-1
- fixup embedded cart remove (dmcphers@redhat.com)

* Thu Jun 30 2011 Dan McPherson <dmcphers@redhat.com> 0.73.6-1
- perf improvements for how/when we look up the valid cart types on the server
  (dmcphers@redhat.com)
- Merge remote-tracking branch 'origin/master' (markllama@redhat.com)
- switched deconfigure back to symlink to maintain identity with configure
  (markllama@redhat.com)
- updated (de)configure to remove tc elements (markllama@redhat.com)
- Merge branch 'master' of ssh://git1.ops.rhcloud.com/srv/git/li
  (mmcgrath@redhat.com)
- fixing embedded call and adding debug (mmcgrath@redhat.com)
- ensure any apps still running from the user are actually dead / gone
  (mmcgrath@redhat.com)

* Wed Jun 29 2011 Dan McPherson <dmcphers@redhat.com> 0.73.5-1
- add nurture migration for existing apps (dmcphers@redhat.com)
- undo passing rhlogin to cart (dmcphers@redhat.com)
- add nurture call for git push (dmcphers@redhat.com)
- fixing merge from Dan (mmcgrath@redhat.com)
- proper error handling for embedded cases (mmcgrath@redhat.com)

* Tue Jun 28 2011 Matt Hicks <mhicks@redhat.com> 0.73.4-1
- Merge branch 'master' of ssh://git1.ops.rhcloud.com/srv/git/li
  (mmcgrath@redhat.com)
- Added support to call embedded cartridges (mmcgrath@redhat.com)
- Added embedded list (mmcgrath@redhat.com)

* Tue Jun 28 2011 Dan McPherson <dmcphers@redhat.com> 0.73.3-1
- Bug 717168 (dmcphers@redhat.com)

* Mon Jun 27 2011 Dan McPherson <dmcphers@redhat.com> 0.73.2-1
- migration fix for app_name == framework (dmcphers@redhat.com)

* Mon Jun 27 2011 Dan McPherson <dmcphers@redhat.com> 0.73.1-1
- Merge branch 'master' of ssh://git1.ops.rhcloud.com/srv/git/li
  (jimjag@redhat.com)
- bump spec numbers (dmcphers@redhat.com)
- User.servers not used... clean up factor customer_* and git_cnt_* (US554)
  (jimjag@redhat.com)
- remove git_cnt (jimjag@redhat.com)

* Thu Jun 23 2011 Dan McPherson <dmcphers@redhat.com> 0.72.29-1
- 

* Thu Jun 23 2011 Dan McPherson <dmcphers@redhat.com> 0.72.28-1
- allow for forcing of IP (mmcgrath@redhat.com)

* Tue Jun 21 2011 Dan McPherson <dmcphers@redhat.com> 0.72.27-1
- Adding 256M as default quota type (mmcgrath@redhat.com)

* Mon Jun 20 2011 Dan McPherson <dmcphers@redhat.com> 0.72.26-1
- 

* Mon Jun 20 2011 Dan McPherson <dmcphers@redhat.com> 0.72.25-1
- add no-timestamp to archive tar command (dmcphers@redhat.com)

* Fri Jun 17 2011 Dan McPherson <dmcphers@redhat.com> 0.72.24-1
- missed an if (dmcphers@redhat.com)

* Fri Jun 17 2011 Dan McPherson <dmcphers@redhat.com> 0.72.23-1
- add a loop to the recheck ip (dmcphers@redhat.com)

* Thu Jun 16 2011 Dan McPherson <dmcphers@redhat.com> 0.72.22-1
- 

* Thu Jun 16 2011 Dan McPherson <dmcphers@redhat.com> 0.72.21-1
- trying a longer sleep (dmcphers@redhat.com)

* Thu Jun 16 2011 Dan McPherson <dmcphers@redhat.com> 0.72.20-1
- Merge branch 'master' of git1.ops.rhcloud.com:/srv/git/li (mhicks@redhat.com)
- Adding a sleep if the public ip comes back empty (mhicks@redhat.com)
- fixup path (dmcphers@redhat.com)

* Thu Jun 16 2011 Dan McPherson <dmcphers@redhat.com> 0.72.19-1
- missing require (dmcphers@redhat.com)

* Thu Jun 16 2011 Dan McPherson <dmcphers@redhat.com> 0.72.18-1
- 

* Thu Jun 16 2011 Dan McPherson <dmcphers@redhat.com> 0.72.17-1
- counting newlines fails with only one line and nl suppressed
  (markllama@redhat.com)

* Wed Jun 15 2011 Dan McPherson <dmcphers@redhat.com> 0.72.16-1
- Update to jboss-as7 7.0.0.Beta6OS, brew buildID=167639
  (scott.stark@jboss.org)
- remove tc entries when deconfiguring an account (markllama@redhat.com)
- add runcon changes for ctl.sh to migration (dmcphers@redhat.com)
- fail selinux checks if even one matches (markllama@redhat.com)
- set Selinux label on Express account root directory (markllama@redhat.com)
- li-controller cleanup (dmcphers@redhat.com)
- move context to libra service and configure Part 3 (dmcphers@redhat.com)
- move context to libra service and configure Part 2 (dmcphers@redhat.com)
- move context to libra service and configure (dmcphers@redhat.com)

* Tue Jun 14 2011 Matt Hicks <mhicks@redhat.com> 0.72.15-1
- Adding mcs changes (mmcgrath@redhat.com)
- rename to make more sense... (jimjag@redhat.com)
- Force list to be a string... xfer to array when conv (jimjag@redhat.com)
- cart_list factor returns a string now, with cartridges sep by '|'
  (jimjag@redhat.com)
- /usr/lib/ruby/site_ruby/1.8/facter/libra.rb:86:in `+': can't convert String
  into Array (TypeError) (jimjag@redhat.com)
- force array append (jimjag@redhat.com)
- Adjust for permissions (jimjag@redhat.com)
- debug devenv (jimjag@redhat.com)

* Fri Jun 10 2011 Matt Hicks <mhicks@redhat.com> 0.72.14-1
- Be faster (jimjag@redhat.com)

* Fri Jun 10 2011 Matt Hicks <mhicks@redhat.com> 0.72.13-1
- only restart mcollective on _uninstall_ not upgrade (mmcgrath@redhat.com)
- Creating test commits, this is for jenkins (mmcgrath@redhat.com)

* Thu Jun 09 2011 Matt Hicks <mhicks@redhat.com> 0.72.12-1
- Correcting mcollective check to allow periods (mmcgrath@redhat.com)
- Adding shell safe and other checks (mmcgrath@redhat.com)

* Wed Jun 08 2011 Matt Hicks <mhicks@redhat.com> 0.72.11-1
- handle new symlink on rerun (dmcphers@redhat.com)
- migration bug fixes (dmcphers@redhat.com)
- add link from old apptype to new app home (dmcphers@redhat.com)
- add restart to migration (dmcphers@redhat.com)
- move migration to separate file (dmcphers@redhat.com)

* Wed Jun 08 2011 Dan McPherson <dmcphers@redhat.com> 0.72.10-1
- functioning migration (dmcphers@redhat.com)
- minor change (dmcphers@redhat.com)
- migration progress (dmcphers@redhat.com)
- migration updates (dmcphers@redhat.com)
- fixed test bracket typo (markllama@redhat.com)
- fixed shell equality test typo, and made deconfigure require only the account
  name (markllama@redhat.com)
- remove accidentially checked in file (dmcphers@redhat.com)
- fix rhc-snapshot (dmcphers@redhat.com)
- added deconfigure as a symlink to configure (markllama@redhat.com)
- configure reverts if called as deconfigure (markllama@redhat.com)
- removed empty deconfigure script (markllama@redhat.com)
- migration progress (dmcphers@redhat.com)

* Mon Jun 06 2011 Dan McPherson <dmcphers@redhat.com> 0.72.9-1
- 

* Mon Jun 06 2011 Dan McPherson <dmcphers@redhat.com> 0.72.8-1
- moving to sym links for actions (dmcphers@redhat.com)

* Mon Jun 06 2011 Dan McPherson <dmcphers@redhat.com> 0.72.7-1
- OK, so the build failures aren't me. So fold back in (jimjag@redhat.com)
- nother test (jimjag@redhat.com)
- comment out (jimjag@redhat.com)
- fold back in cart factor (jimjag@redhat.com)

* Fri Jun 03 2011 Dan McPherson <dmcphers@redhat.com> 0.72.6-1
- remove apptype dir cleanup (dmcphers@redhat.com)

* Fri Jun 03 2011 Matt Hicks <mhicks@redhat.com> 0.72.5-1
- readjust logic for consistency (jimjag@redhat.com)
- keep carts private/local/static (jimjag@redhat.com)
- Make sure we're really a Dir (jimjag@redhat.com)
- Add in :carts factor we can grab (jimjag@redhat.com)
- customer -> application rename in cartridges (dmcphers@redhat.com)

* Wed Jun 01 2011 Dan McPherson <dmcphers@redhat.com> 0.72.4-1
- rpm build issues 3 (dmcphers@redhat.com)
- rpm build issues 2 (dmcphers@redhat.com)
- rpm build issues (dmcphers@redhat.com)
- fix node build (dmcphers@redhat.com)
- move common files to abstract httpd (dmcphers@redhat.com)
- remove apptype dir part 1 (dmcphers@redhat.com)
- add base concept of parent cartridge - work in progress (dmcphers@redhat.com)
- add mod_ssl to site and broker (dmcphers@redhat.com)

* Tue May 31 2011 Matt Hicks <mhicks@redhat.com> 0.72.3-1
- updated package list for node acceptance (markllama@redhat.com)

* Thu May 26 2011 Matt Hicks <mhicks@redhat.com> 0.72.2-3
- Adding ruby as runtime dependency

* Thu May 26 2011 Matt Hicks <mhicks@redhat.com> 0.72.2-2
- Readding semanage requirements (mhicks@redhat.com)
- Pulling SELinux RPM out of node (mhicks@redhat.com)

* Thu May 26 2011 Matt Hicks <mhicks@redhat.com> 0.72.1-3
- Adding rake build dep

* Wed May 25 2011 Matt Hicks <mhicks@redhat.com> 0.72.1-2
- Fixing build root dirs

* Tue May 25 2011 Matt Hicks <mhicks@redhat.com> 0.72.1-1
- Initial refactoring
