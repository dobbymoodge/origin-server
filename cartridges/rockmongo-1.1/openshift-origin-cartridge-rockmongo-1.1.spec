%global cartridgedir %{_libexecdir}/openshift/cartridges/embedded/rockmongo-1.1
%global frameworkdir %{_libexecdir}/openshift/cartridges/rockmongo-1.1

Name: openshift-origin-cartridge-rockmongo-1.1
Version: 1.17.0
Release: 1%{?dist}
Summary: Embedded RockMongo support for OpenShift

Group: Applications/Internet
License: ASL 2.0
URL: http://openshift.redhat.com
Source0: %{name}-%{version}.tar.gz
BuildRoot:    %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
BuildArch: noarch

Obsoletes: cartridge-rockmongo-1.1

Requires: openshift-origin-cartridge-abstract
Requires: openshift-origin-cartridge-mongodb-2.2

%description
Provides rhc RockMongo cartridge support

%prep
%setup -q

%build

%install
rm -rf $RPM_BUILD_ROOT
rm -rf %{buildroot}
mkdir -p %{buildroot}%{cartridgedir}
mkdir -p %{buildroot}/%{_sysconfdir}/openshift/cartridges
ln -s %{cartridgedir}/info/configuration/ %{buildroot}/%{_sysconfdir}/openshift/cartridges/%{name}
cp -r info %{buildroot}%{cartridgedir}/
cp LICENSE %{buildroot}%{cartridgedir}/
cp COPYRIGHT %{buildroot}%{cartridgedir}/
ln -s %{cartridgedir} %{buildroot}/%{frameworkdir}

%post

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%attr(0750,-,-) %{cartridgedir}/info/hooks/
%attr(0750,-,-) %{cartridgedir}/info/build/
%attr(0750,-,-) %{cartridgedir}/info/html/
%attr(0755,-,-) %{frameworkdir}
%config(noreplace) %{cartridgedir}/info/configuration/
%attr(0755,-,-) %{cartridgedir}/info/bin/
 %{cartridgedir}/info/rockmongo/
%{_sysconfdir}/openshift/cartridges/%{name}
%{cartridgedir}/info/changelog
%{cartridgedir}/info/control
%{cartridgedir}/info/manifest.yml
%doc %{cartridgedir}/COPYRIGHT
%doc %{cartridgedir}/LICENSE

%changelog
* Fri Nov 16 2012 Adam Miller <admiller@redhat.com> 1.16.2-1
- BZ 877325: Added websites. (rmillner@redhat.com)

* Thu Nov 01 2012 Adam Miller <admiller@redhat.com> 1.16.1-1
- bump_minor_versions for sprint 20 (admiller@redhat.com)

* Fri Oct 19 2012 Adam Miller <admiller@redhat.com> 1.15.6-1
- BZ 843286: Enable auth files via htaccess (rmillner@redhat.com)

* Mon Oct 08 2012 Dan McPherson <dmcphers@redhat.com> 1.15.5-1
- Fixing renames, paths, configs and cleaning up old packages. Adding
  obsoletes. (kraman@gmail.com)

* Thu Oct 04 2012 Krishna Raman <kraman@gmail.com> 1.15.4-1
- new package built with tito

* Thu Oct 04 2012 Adam Miller <admiller@redhat.com> 1.15.3-1
- Typeless gear changes for US 2105 (jhonce@redhat.com)

* Thu Sep 20 2012 Adam Miller <admiller@redhat.com> 1.15.2-1
- Change hard-coded references to mongodb-2.2 (rmillner@redhat.com)

* Wed Sep 12 2012 Adam Miller <admiller@redhat.com> 1.15.1-1
- bump_minor_versions for sprint 18 (admiller@redhat.com)

* Fri Sep 07 2012 Adam Miller <admiller@redhat.com> 1.14.4-1
- Merge pull request #340 from pravisankar/dev/ravi/zend-fix-description
  (openshift+bot@redhat.com)
- Modify Display-name/Description fields for all cartridges (rpenta@redhat.com)

* Thu Sep 06 2012 Adam Miller <admiller@redhat.com> 1.14.3-1
- Fix for bugz 852518 - Failed move due to httpd.pid file being empty.
  (ramr@redhat.com)

* Thu Aug 30 2012 Adam Miller <admiller@redhat.com> 1.14.2-1
- Fix for bugz 852518 - Failed move due to httpd.pid file being empty.
  (ramr@redhat.com)

* Thu Aug 02 2012 Adam Miller <admiller@redhat.com> 1.14.1-1
- bump_minor_versions for sprint 16 (admiller@redhat.com)

* Wed Aug 01 2012 Adam Miller <admiller@redhat.com> 1.13.4-1
- Merge pull request #157 from rmillner/dev/rmillner/bug/843326
  (rmillner@redhat.com)
- Some frameworks (ex: mod_wsgi) need HTTPS set to notify the app that https
  was used. (rmillner@redhat.com)

* Tue Jul 31 2012 Adam Miller <admiller@redhat.com> 1.13.3-1
- Move direct calls to httpd init script to httpd_singular locking script
  (rmillner@redhat.com)

* Thu Jul 19 2012 Adam Miller <admiller@redhat.com> 1.13.2-1
- Fixes for bugz 840030 - Apache blocks access to /icons. Remove these as
  mod_autoindex has now been turned OFF (see bugz 785050 for more details).
  (ramr@redhat.com)

* Wed Jul 11 2012 Adam Miller <admiller@redhat.com> 1.13.1-1
- bump_minor_versions for sprint 15 (admiller@redhat.com)

* Mon Jul 09 2012 Dan McPherson <dmcphers@redhat.com> 1.12.3-1
- cartridge metadata in rockmongo/phpmoadmin (rchopra@redhat.com)

* Sat Jun 23 2012 Dan McPherson <dmcphers@redhat.com> 1.12.2-1
- new package built with tito

* Wed Jun 20 2012 Adam Miller <admiller@redhat.com> 1.12.1-1
- bump_minor_versions for sprint 14 (admiller@redhat.com)

* Mon Jun 18 2012 Adam Miller <admiller@redhat.com> 1.11.2-1
- exposing urls and credentials for metrics, rockmongo, and phpmoadmin
  cartridges through the rest apis (abhgupta@redhat.com)

* Fri Jun 01 2012 Adam Miller <admiller@redhat.com> 1.11.1-1
- bumping spec versions (admiller@redhat.com)

* Tue May 22 2012 Dan McPherson <dmcphers@redhat.com> 1.10.2-1
- Merge branch 'master' into US2109 (jhonce@redhat.com)
- Merge branch 'master' into US2109 (jhonce@redhat.com)
- Modify cartridges for typeless gear changes. (ramr@redhat.com)

* Thu May 10 2012 Adam Miller <admiller@redhat.com> 1.10.1-1
- bumping spec versions (admiller@redhat.com)

* Tue May 08 2012 Adam Miller <admiller@redhat.com> 1.9.4-1
- Bug 819739 (dmcphers@redhat.com)

* Mon May 07 2012 Adam Miller <admiller@redhat.com> 1.9.3-1
- Update user hooks to call with the whole cartridge name (rmillner@redhat.com)
- Merge branch 'master' of ssh://git1.ops.rhcloud.com/srv/git/li
  (rmillner@redhat.com)
- Embedded cartridge pre/post hooks. (rmillner@redhat.com)

* Mon May 07 2012 Adam Miller <admiller@redhat.com> 1.9.2-1
- remove old obsoletes (dmcphers@redhat.com)

* Thu Apr 26 2012 Adam Miller <admiller@redhat.com> 1.9.1-1
- bumping spec versions (admiller@redhat.com)

* Mon Apr 23 2012 Adam Miller <admiller@redhat.com> 1.8.5-1
- remove php-devel as a dependency : for help in Zend work (rchopra@redhat.com)

* Sat Apr 21 2012 Dan McPherson <dmcphers@redhat.com> 1.8.4-1
- forcing builds (dmcphers@redhat.com)
- moved a little too much (dmcphers@redhat.com)
- moving our os code (dmcphers@redhat.com)

* Thu Apr 12 2012 Mike McGrath <mmcgrath@redhat.com> 1.8.2-1
- release bump for tag uniqueness (mmcgrath@redhat.com)

* Mon Apr 02 2012 Krishna Raman <kraman@gmail.com> 1.7.3-1
- 

* Fri Mar 30 2012 Krishna Raman <kraman@gmail.com> 1.7.2-1
- Renaming for open-source release

* Sat Mar 17 2012 Dan McPherson <dmcphers@redhat.com> 1.7.1-1
- bump spec numbers (dmcphers@redhat.com)

* Fri Mar 09 2012 Dan McPherson <dmcphers@redhat.com> 1.6.2-1
- Batch variable name chage (rmillner@redhat.com)
- Adding export control files (kraman@gmail.com)
- loading resource limits config when needed (kraman@gmail.com)
- replacing references to libra with openshift (abhgupta@redhat.com)
- replacing references to libra with openshift in rockmongo cartridge
  (abhgupta@redhat.com)
- Removed new instances of GNU license headers (jhonce@redhat.com)

* Fri Mar 02 2012 Dan McPherson <dmcphers@redhat.com> 1.6.1-1
- bump spec numbers (dmcphers@redhat.com)

* Tue Feb 28 2012 Dan McPherson <dmcphers@redhat.com> 1.5.3-1
- some cleanup of http -C Include (dmcphers@redhat.com)

* Mon Feb 27 2012 Dan McPherson <dmcphers@redhat.com> 1.5.2-1
- cleanup all the old command usage in help and messages (dmcphers@redhat.com)

* Thu Feb 16 2012 Dan McPherson <dmcphers@redhat.com> 1.5.1-1
- bump spec numbers (dmcphers@redhat.com)

* Mon Feb 13 2012 Dan McPherson <dmcphers@redhat.com> 1.4.4-1
- Fix for bugz# 789814. Fixed 10gen-mms-agent and rockmongo descriptors. Fixed
  info sent back by legacy broker when cartridge doesnt not have info for
  embedded cart. (kraman@gmail.com)

* Mon Feb 13 2012 Dan McPherson <dmcphers@redhat.com> 1.4.3-1
- cleaning up specs to force a build (dmcphers@redhat.com)
- remove php dependency from others as well (rchopra@redhat.com)

* Sat Feb 11 2012 Dan McPherson <dmcphers@redhat.com> 1.4.2-1
- more abstracting out selinux (dmcphers@redhat.com)
- first pass at splitting out selinux logic (dmcphers@redhat.com)
- Updating models to improove schems of descriptor in mongo Moved
  connection_endpoint to broker (kraman@gmail.com)
- Fixing manifest yml files (kraman@gmail.com)
- Creating models for descriptor Fixing manifest files Added command to list
  installed cartridges and get descriptors (kraman@gmail.com)
- change status to use normal client_result instead of special handling
  (dmcphers@redhat.com)

* Fri Feb 03 2012 Dan McPherson <dmcphers@redhat.com> 1.4.1-1
- bump spec numbers (dmcphers@redhat.com)
- Make it clear the phpmyadmin and rockmongo users are just the db users
  (dmcphers@redhat.com)
