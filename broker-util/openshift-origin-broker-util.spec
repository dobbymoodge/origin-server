Summary:        Utility scripts for the OpenShift Origin broker
Name:           openshift-origin-broker-util
Version:        1.0.18
Release:        1%{?dist}
Group:          Network/Daemons
License:        ASL 2.0
URL:            http://openshift.redhat.com
Source0:        http://mirror.openshift.com/pub/openshift-origin/source/%{name}-%{version}.tar.gz

Requires:       openshift-broker
# For oo-admin-broker-auth
Requires:       mcollective-client
Requires:       ruby(abi) >= 1.8
%if 0%{?fedora} >= 17
BuildRequires:  rubygems-devel
%else
BuildRequires:  rubygems
%endif
BuildArch:      noarch

%description
This package contains a set of utility scripts for the broker.  They must be
run on a broker instance.

%prep
%setup -q

%build

%install
rm -rf %{buildroot}

mkdir -p %{buildroot}%{_sbindir}
cp oo-* %{buildroot}%{_sbindir}/

mkdir -p %{buildroot}%{_mandir}/man8/
cp man/*.8 %{buildroot}%{_mandir}/man8/

%clean
rm -rf $RPM_BUILD_ROOT

%files
%attr(0755,-,-) %{_sbindir}/oo-admin-chk
%attr(0755,-,-) %{_sbindir}/oo-admin-ctl-app
%attr(0755,-,-) %{_sbindir}/oo-admin-ctl-district
%attr(0755,-,-) %{_sbindir}/oo-admin-ctl-domain
%attr(0755,-,-) %{_sbindir}/oo-admin-ctl-user
%attr(0755,-,-) %{_sbindir}/oo-admin-move
%attr(0755,-,-) %{_sbindir}/oo-admin-broker-auth
%attr(0755,-,-) %{_sbindir}/oo-register-dns
%attr(0755,-,-) %{_sbindir}/oo-accept-broker
%attr(0755,-,-) %{_sbindir}/oo-accept-systems

%doc LICENSE
%{_mandir}/man8/oo-admin-chk.8.gz
%{_mandir}/man8/oo-admin-ctl-app.8.gz
%{_mandir}/man8/oo-admin-ctl-district.8.gz
%{_mandir}/man8/oo-admin-ctl-domain.8.gz
%{_mandir}/man8/oo-admin-ctl-user.8.gz
%{_mandir}/man8/oo-admin-move.8.gz
%{_mandir}/man8/oo-admin-broker-auth.8.gz
%{_mandir}/man8/oo-register-dns.8.gz
%{_mandir}/man8/oo-accept-broker.8.gz
%{_mandir}/man8/oo-accept-systems.8.gz

%changelog
* Thu Mar 21 2013 Brenton Leanhardt <bleanhar@redhat.com> 1.0.18-1
- Bug 911455 - Unrestricted the session secret in Openshift Origin server
  (bleanhar@redhat.com)

* Wed Mar 20 2013 Brenton Leanhardt <bleanhar@redhat.com> 1.0.17-1
- Bug 921257 - Warn users to change the default AUTH_SALT (bleanhar@redhat.com)
- Adding oo-admin-broker-auth (bleanhar@redhat.com)

* Tue Feb 26 2013 Luke Meyer <lmeyer@redhat.com> 1.0.16-1
- bug 915224 <oo-admin-ctl-user> validate --addgearsize before adding
- bug 895911 - "oo-admin-ctl-user --setmaxgears" validate maxgears  #cherrypick
* Tue Feb 05 2013 Luke Meyer <lmeyer@redhat.com> 1.0.15-1
- <oo-accept-systems> fix bug 893896 - allow -w .5 and improve parameter error
  report (lmeyer@redhat.com)
- <oo-accept-broker> fix bug 905656 - exit message and status
  (lmeyer@redhat.com)

* Tue Jan 08 2013 Chris Alfonso <calfonso@redhat.com> 1.0.14-1
- Adding mongo SSL connection support, default is SSL is off
  (calfonso@redhat.com)

* Tue Dec 18 2012 Luke Meyer <lmeyer@redhat.com> 1.0.13-1
- oo-accept-broker: work around mongo replica sets; changes to man page (lmeyer@redhat.com)

* Thu Dec 13 2012 Luke Meyer <lmeyer@redhat.com> 1.0.12-1
- put title on man pages (lmeyer@redhat.com)
- oo-admin-chk and man page tweaks while looking at BZ874799 and BZ875657
  (lmeyer@redhat.com)
- BZ874750 & BZ874751 fix oo-accept-broker man page; remove useless code and
  options also give friendly advice during FAILs - why not? BZ874757 make man
  page and options match (lmeyer@redhat.com)
- save on the number of rails console calls being made (lmeyer@redhat.com)

* Tue Dec 11 2012 Brenton Leanhardt <bleanhar@redhat.com> 1.0.11-1
- Bug 874845 - oo-admin-ctl-app accepts garbage for a command and returns
  success (bleanhar@redhat.com)

* Tue Dec 11 2012 Brenton Leanhardt <bleanhar@redhat.com> 1.0.10-1
- BZ876644 - oo-register-dns is hardcoded to add entries to a BIND server at
  127.0.0.1 (bleanhar@redhat.com)

* Tue Dec 11 2012 Luke Meyer <lmeyer@redhat.com> 1.0.9-1
- oo-accept-* changes for PUBLIC_* node settings and others. US3215 revisiting
  US3036 (lmeyer@redhat.com)

* Fri Dec 07 2012 Brenton Leanhardt <bleanhar@redhat.com> 1.0.8-1
- BZ873765 -  typo in description of man page for oo-admin-ctl-app
  (bleanhar@redhat.com)

* Thu Dec 06 2012 Brenton Leanhardt <bleanhar@redhat.com> 1.0.7-1
- Bug 873768 - removing oo-admin-ctl-template (bleanhar@redhat.com)

* Thu Dec 06 2012 Brenton Leanhardt <bleanhar@redhat.com> 1.0.6-1
- Removing references to complete-origin-setup (bleanhar@redhat.com)
- Removing oo-setup-broker and oo-setup-bind from Enterprise
  (bleanhar@redhat.com)

* Thu Nov 08 2012 Brenton Leanhardt <bleanhar@redhat.com> 1.0.5-1
- updates to oo-accept-node, oo-admin-chk to detect bad node PUBLIC_* settings.
  * pull changeable node.conf settings to top; remove unused; comment * add
  various oo-accept-node checks for node.conf sanity, including PUBLIC_HOSTNAME
  * have oo-admin-chk validate the PUBLIC_HOSTNAME and PUBLIC_IP of all nodes
  and check for dupes (lmeyer@redhat.com)

* Tue Nov 06 2012 Brenton Leanhardt <bleanhar@redhat.com> 1.0.4-1
- oo-accept-broker: fix check_datastore_mongo (miciah.masters@gmail.com)
- oo-accept-broker: add support for remote-user auth (miciah.masters@gmail.com)

* Tue Nov 06 2012 Brenton Leanhardt <bleanhar@redhat.com> 1.0.3-1
- oo-accept-broker: RHEL6 compatibility (miciah.masters@gmail.com)

* Wed Oct 31 2012 Adam Miller <admiller@redhat.com> 1.0.2-1
- Fixes for LiveCD build (kraman@gmail.com)
- move broker/node utils to /usr/sbin/ everywhere (admiller@redhat.com)
- Bug 871436 - moving the default path for AUTH_PRIVKEYFILE and AUTH_PUBKEYFILE
  under /etc (bleanhar@redhat.com)

* Tue Oct 30 2012 Adam Miller <admiller@redhat.com> 1.0.1-1
- Added man pages for broker-util/node-util, port complete-origin-setup to bash
  (admiller@redhat.com)
- bumping specs to at least 1.0.0 (dmcphers@redhat.com)
- fix broker-util version number (admiller@redhat.com)
- Updating broker setup script (kraman@gmail.com)
- Moving broker config to /etc/openshift/broker.conf Rails app and all oo-*
  scripts will load production environment unless the
  /etc/openshift/development marker is present Added param to specify default
  when looking up a config value in OpenShift::Config Moved all defaults into
  plugin initializers instead of separate defaults file No longer require
  loading 'openshift-origin-common/config' if 'openshift-origin-common' is
  loaded openshift-origin-common selinux module is merged into F16 selinux
  policy. Removing from broker %%postrun (kraman@gmail.com)
- sudo is not allowed within a command that is being executed using su
  (abhgupta@redhat.com)
- Merge pull request #741 from pravisankar/dev/ravi/bug/853082
  (openshift+bot@redhat.com)
- Fix for bug# 853082 (rpenta@redhat.com)
- Updating setup-broker, moving broken gem setup to after bind plugn setup is
  completed. Fixing cucumber test helper to use correct selinux policies
  (kraman@gmail.com)
- Merge pull request #737 from sosiouxme/master (dmcphers@redhat.com)
- have openshift-broker report bundler problems rather than silently fail. also
  fix typo in oo-admin-chk usage (lmeyer@redhat.com)
- Bug 868858 (dmcphers@redhat.com)
- Fixing Origin build scripts (kraman@gmail.com)
- removing remaining cases of SS and config.ss (dmcphers@redhat.com)
- Fix for Bugs# 853082, 847572 (rpenta@redhat.com)
- Set a password on the mongo admin db so that application and ssh'd users
  cannot access the DB. Misc other fixes (kraman@gmail.com)
- Fixed broker/node setup scripts to install cgroup services. Fixed
  mcollective-qpid plugin so it installs during origin package build. Updated
  cgroups init script to work with both systemd and init.d Updated oo-trap-user
  script Renamed oo-cgroups to openshift-cgroups (service and init.d) and
  created oo-admin-ctl-cgroups Pulled in oo-get-mcs-level and abstract/util
  from origin-selinux branch Fixed invalid file path in rubygem-openshift-
  origin-auth-mongo spec Fixed invlaid use fo Mcollective::Config in
  mcollective-qpid-plugin (kraman@gmail.com)
- Merge pull request #681 from pravisankar/dev/ravi/bug/821107
  (openshift+bot@redhat.com)
- Merge pull request #678 from jwhonce/dev/scripts (dmcphers@redhat.com)
- Support more ssh key types (rpenta@redhat.com)
- Automatic commit of package [openshift-origin-broker-util] release
  [0.0.6.2-1]. (admiller@redhat.com)
- Port oo-init-quota command (jhonce@redhat.com)
- Port admin scripts for on-premise (jhonce@redhat.com)
- Centralize plug-in configuration (miciah.masters@gmail.com)
- Fixing a few missed references to ss-* Added command to load openshift-origin
  selinux module (kraman@gmail.com)
- Removing old build scripts Moving broker/node setup utilities into util
  packages Fix Auth service module name conflicts (kraman@gmail.com)

* Mon Oct 15 2012 Adam Miller <admiller@redhat.com> 0.0.6.2-1
- Port admin scripts for on-premise (jhonce@redhat.com)
- Centralize plug-in configuration (miciah.masters@gmail.com)
- Fixing a few missed references to ss-* Added command to load openshift-origin
  selinux module (kraman@gmail.com)
- Removing old build scripts Moving broker/node setup utilities into util
  packages Fix Auth service module name conflicts (kraman@gmail.com)

* Tue Oct 09 2012 Krishna Raman <kraman@gmail.com> 0.0.6.1-1
- Removing old build scripts Moving broker/node setup utilities into util
  packages (kraman@gmail.com)

* Mon Oct 08 2012 Dan McPherson <dmcphers@redhat.com> 0.0.6-1
- Bug 864005 (dmcphers@redhat.com)
- Bug: 861346 - fixing ss-admin-ctl-domain script (abhgupta@redhat.com)

* Fri Oct 05 2012 Krishna Raman <kraman@gmail.com> 0.0.5-1
- Rename pass 3: Manual fixes (kraman@gmail.com)
- Rename pass 1: files, directories (kraman@gmail.com)

* Wed Oct 03 2012 Adam Miller <admiller@redhat.com> 0.0.4-1
- Disable analytics for admin scripts (dmcphers@redhat.com)
- Commiting Rajat's fix for bug#827635 (bleanhar@redhat.com)
- Subaccount user deletion changes (rpenta@redhat.com)
- fixing build requires (abhgupta@redhat.com)

* Mon Sep 24 2012 Adam Miller <admiller@redhat.com> 0.0.3-1
- Removing the node profile enforcement from the oo-admin-ctl scripts
  (bleanhar@redhat.com)
- Adding LICENSE file to new packages and other misc cleanup
  (bleanhar@redhat.com)

* Thu Sep 20 2012 Brenton Leanhardt <bleanhar@redhat.com> 0.0.2-1
- new package built with tito

