%global cartridgedir %{_libexecdir}/openshift/cartridges/zend-5.6

Summary:   Provides zend-5.6 support
Name:      openshift-origin-cartridge-zend-5.6
Version: 1.7.3
Release:   1%{?dist}
Group:     Development/Languages
License:   ASL 2.0
URL:       http://openshift.redhat.com
Source0:   %{name}-%{version}.tar.gz 


BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildArch: noarch

Obsoletes: cartridge-zend-5.6

BuildRequires: git
Requires: openshift-origin-cartridge-abstract
Requires: rubygem(openshift-origin-node)
Requires: zend-server-php-5.3 >= 5.6.0-11
Requires: mod_bw
Requires: rubygem-builder

# PHP extensins that are not enabled by default in zend-server-php-5.3 pkg:
Requires: php-5.3-mongo-zend-server
Requires: php-5.3-imagick-zend-server
Requires: php-5.3-uploadprogress-zend-server

%description
Provides zend support to OpenShift

%prep
%setup -q

%build
rm -rf git_template
cp -r template/ git_template/
cd git_template
git init
git add -f .
git config user.email "builder@example.com"
git config user.name "Template builder"
git commit -m 'Creating template'
cd ..
git clone --bare git_template git_template.git
rm -rf git_template
touch git_template.git/refs/heads/.gitignore

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{cartridgedir}
mkdir -p %{buildroot}/%{_sysconfdir}/openshift/cartridges
ln -s %{cartridgedir}/info/configuration/ %{buildroot}/%{_sysconfdir}/openshift/cartridges/%{name}
cp -r info %{buildroot}%{cartridgedir}/
cp -r files %{buildroot}%{cartridgedir}/
cp LICENSE %{buildroot}%{cartridgedir}/
cp COPYRIGHT %{buildroot}%{cartridgedir}/
mkdir -p %{buildroot}%{cartridgedir}/info/data/
cp -r git_template.git %{buildroot}%{cartridgedir}/info/data/
ln -s %{cartridgedir}/../abstract/info/hooks/add-module %{buildroot}%{cartridgedir}/info/hooks/add-module
ln -s %{cartridgedir}/../abstract/info/hooks/info %{buildroot}%{cartridgedir}/info/hooks/info
ln -s %{cartridgedir}/../abstract/info/hooks/reload %{buildroot}%{cartridgedir}/info/hooks/reload
ln -s %{cartridgedir}/../abstract/info/hooks/remove-module %{buildroot}%{cartridgedir}/info/hooks/remove-module
ln -s %{cartridgedir}/../abstract/info/hooks/restart %{buildroot}%{cartridgedir}/info/hooks/restart
ln -s %{cartridgedir}/../abstract/info/hooks/start %{buildroot}%{cartridgedir}/info/hooks/start
ln -s %{cartridgedir}/../abstract-httpd/info/hooks/status %{buildroot}%{cartridgedir}/info/hooks/status
ln -s %{cartridgedir}/../abstract/info/hooks/stop %{buildroot}%{cartridgedir}/info/hooks/stop
ln -s %{cartridgedir}/../abstract/info/hooks/update-namespace %{buildroot}%{cartridgedir}/info/hooks/update-namespace
ln -s %{cartridgedir}/../abstract/info/hooks/deploy-httpd-proxy %{buildroot}%{cartridgedir}/info/hooks/deploy-httpd-proxy
ln -s %{cartridgedir}/../abstract/info/hooks/remove-httpd-proxy %{buildroot}%{cartridgedir}/info/hooks/remove-httpd-proxy
ln -s %{cartridgedir}/../abstract/info/hooks/tidy %{buildroot}%{cartridgedir}/info/hooks/tidy
ln -s %{cartridgedir}/../abstract/info/hooks/threaddump %{buildroot}%{cartridgedir}/info/hooks/threaddump
ln -s %{cartridgedir}/../abstract/info/hooks/system-messages %{buildroot}%{cartridgedir}/info/hooks/system-messages
mkdir -p %{buildroot}%{cartridgedir}/info/connection-hooks/
ln -s %{cartridgedir}/../abstract/info/connection-hooks/publish-gear-endpoint %{buildroot}%{cartridgedir}/info/connection-hooks/publish-gear-endpoint
ln -s %{cartridgedir}/../abstract/info/connection-hooks/publish-http-url %{buildroot}%{cartridgedir}/info/connection-hooks/publish-http-url
ln -s %{cartridgedir}/../abstract/info/connection-hooks/set-db-connection-info %{buildroot}%{cartridgedir}/info/connection-hooks/set-db-connection-info
ln -s %{cartridgedir}/../abstract/info/connection-hooks/set-nosql-db-connection-info %{buildroot}%{cartridgedir}/info/connection-hooks/set-nosql-db-connection-info
ln -s %{cartridgedir}/../abstract/info/bin/sync_gears.sh %{buildroot}%{cartridgedir}/info/bin/sync_gears.sh

%post
#this copies over files in zend server rpm install that do not work in openshift 
cp -rf %{cartridgedir}/files/shared-files/usr/local/zend/* /usr/local/zend/.
ln -sf /usr/libexec/openshift/cartridges/zend-5.6/info/bin/httpd_ctl.sh /usr/local/zend/bin/apachectl
sh %{cartridgedir}/info/bin/zend_configure_filesystem.sh

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%attr(0755,-,-) %{cartridgedir}/info/hooks
%attr(0750,-,-) %{cartridgedir}/info/hooks/*
%attr(0755,-,-) %{cartridgedir}/info/hooks/tidy
%attr(0750,-,-) %{cartridgedir}/info/data/
%attr(0750,-,-) %{cartridgedir}/info/build/
%attr(0755,-,-) %{cartridgedir}/info/bin/
%attr(0755,-,-) %{cartridgedir}/info/connection-hooks/
%attr(-,-,-) %{cartridgedir}/files/

%config(noreplace) %{cartridgedir}/info/configuration/
%{_sysconfdir}/openshift/cartridges/%{name}
%{cartridgedir}/info/changelog
%{cartridgedir}/info/control
%{cartridgedir}/info/manifest.yml
%doc %{cartridgedir}/COPYRIGHT
%doc %{cartridgedir}/LICENSE

%changelog
* Wed Apr 17 2013 Dan McPherson <dmcphers@redhat.com> 1.7.3-1
- Warn user to set Zend Server Console password on app create
  (vvitek@redhat.com)
- fix /health page for zend-5.6 (vvitek@redhat.com)

* Wed Apr 10 2013 Adam Miller <admiller@redhat.com> 1.7.2-1
- Delete move/pre-move/post-move hooks and any references to these hooks
  (rpenta@redhat.com)

* Thu Mar 28 2013 Adam Miller <admiller@redhat.com> 1.7.1-1
- bump_minor_versions for sprint 26 (admiller@redhat.com)

* Thu Mar 14 2013 Adam Miller <admiller@redhat.com> 1.6.2-1
- Refactor Endpoints to support frontend mapping (ironcladlou@gmail.com)

* Thu Mar 07 2013 Adam Miller <admiller@redhat.com> 1.6.1-1
- bump_minor_versions for sprint 25 (admiller@redhat.com)

* Wed Mar 06 2013 Adam Miller <admiller@redhat.com> 1.5.5-1
- Add some missing Zend Server PHP extensions (vvitek@redhat.com)

* Tue Mar 05 2013 Vojtech Vitek (V-Teq) <vvitek@redhat.com> 1.5.4-1
- Add PHP extensions that were not enabled by default:
  Mongo driver, ImageMagick, Upload Progress

* Tue Feb 26 2013 Adam Miller <admiller@redhat.com> 1.5.3-1
- Missed ZendServer URL. (rmillner@redhat.com)

* Tue Feb 19 2013 Adam Miller <admiller@redhat.com> 1.5.2-1
- Switch from VirtualHosts to mod_rewrite based routing to support high
  density. (rmillner@redhat.com)
- Update cart manifests to be compatible with v2 spec (ironcladlou@gmail.com)

* Thu Feb 07 2013 Adam Miller <admiller@redhat.com> 1.5.1-1
- bump_minor_versions for sprint 24 (admiller@redhat.com)

* Tue Jan 29 2013 Adam Miller <admiller@redhat.com> 1.4.2-1
- fix references to rhc app cartridge (dmcphers@redhat.com)
- 892068 (dmcphers@redhat.com)
- fix typo (dmcphers@redhat.com)

* Wed Jan 23 2013 Adam Miller <admiller@redhat.com> 1.4.1-1
- bump_minor_versions for sprint 23 (admiller@redhat.com)

* Tue Jan 22 2013 Adam Miller <admiller@redhat.com> 1.3.5-1
- Fix typos in rhc instructions displayed to client (ironcladlou@gmail.com)

* Fri Jan 18 2013 Dan McPherson <dmcphers@redhat.com> 1.3.4-1
- Replace expose/show/conceal-port hooks with Endpoints (ironcladlou@gmail.com)

* Thu Jan 10 2013 Adam Miller <admiller@redhat.com> 1.3.3-1
- Fix BZ864797: Add doc for disable_auto_scaling marker (pmorie@gmail.com)

* Tue Dec 18 2012 Adam Miller <admiller@redhat.com> 1.3.2-1
- Fix for Bug 887202 (jhonce@redhat.com)

* Wed Dec 12 2012 Adam Miller <admiller@redhat.com> 1.3.1-1
- bump_minor_versions for sprint 22 (admiller@redhat.com)

* Tue Dec 11 2012 Adam Miller <admiller@redhat.com> 1.2.5-1
- Fix for Bug 880013 (jhonce@redhat.com)

* Wed Dec 05 2012 Adam Miller <admiller@redhat.com> 1.2.4-1
- Made tidy hook accessible to gear users (ironcladlou@gmail.com)

* Tue Dec 04 2012 Adam Miller <admiller@redhat.com> 1.2.3-1
- Move add/remove alias to the node API. (rmillner@redhat.com)

* Thu Nov 29 2012 Adam Miller <admiller@redhat.com> 1.2.2-1
- [cartridges-new] Re-implement scripts (part 1) (jhonce@redhat.com)

* Sat Nov 17 2012 Adam Miller <admiller@redhat.com> 1.2.1-1
- bump_minor_versions for sprint 21 (admiller@redhat.com)

* Wed Nov 14 2012 Adam Miller <admiller@redhat.com> 1.1.2-1
- US3046 - Implement quickstarts in drupal and react to changes in console
  (ccoleman@redhat.com)

* Thu Nov 08 2012 Adam Miller <admiller@redhat.com> 1.1.1-1
- Fix for Bug 874311 (jhonce@redhat.com)
- Bumping specs to at least 1.1 (dmcphers@redhat.com)

* Tue Oct 30 2012 Adam Miller <admiller@redhat.com> 1.0.1-1
- bumping specs to at least 1.0.0 (dmcphers@redhat.com)

* Mon Oct 29 2012 Adam Miller <admiller@redhat.com> 0.96.12-1
- Fixing Zend manifest to mark scaling from 1:1 (non scalable)
  (kraman@gmail.com)

* Fri Oct 26 2012 Adam Miller <admiller@redhat.com> 0.96.11-1
- Fix zend-5.6 move hook (bug# 867713) (rpenta@redhat.com)
- BZ868193 (bdecoste@gmail.com)

* Wed Oct 24 2012 Adam Miller <admiller@redhat.com> 0.96.10-1
- Fix issue w/ incorrect variables sourced in zend cartridge move hook.
  (ramr@redhat.com)

* Mon Oct 22 2012 Adam Miller <admiller@redhat.com> 0.96.9-1
- Bug 867660 - Zend and mongo don't work (lnader@redhat.com)

* Fri Oct 19 2012 Adam Miller <admiller@redhat.com> 0.96.8-1
- Merge pull request #495 from rmillner/dev/rmillner/bugs/843286
  (openshift+bot@redhat.com)
- BZ 843286: Enable auth files via htaccess (rmillner@redhat.com)

* Thu Oct 18 2012 Adam Miller <admiller@redhat.com> 0.96.7-1
- Merge pull request #496 from bdecoste/master (dmcphers@redhat.com)
- BZ856479 (bdecoste@gmail.com)

* Tue Oct 16 2012 Adam Miller <admiller@redhat.com> 0.96.6-1
- fixed error message druing upgrade (lnader@redhat.com)

* Mon Oct 08 2012 Dan McPherson <dmcphers@redhat.com> 0.96.5-1
- Fixing renames, paths, configs and cleaning up old packages. Adding
  obsoletes. (kraman@gmail.com)

* Thu Oct 04 2012 Krishna Raman <kraman@gmail.com> 0.96.4-1
- new package built with tito

* Thu Oct 04 2012 Adam Miller <admiller@redhat.com> 0.96.3-1
- Merge pull request #442 from mrunalp/dev/typeless (dmcphers@redhat.com)
- Typeless gear changes for US 2105 (jhonce@redhat.com)

* Wed Oct 03 2012 Adam Miller <admiller@redhat.com> 0.96.2-1
- Bug 862199 (lnader@redhat.com)
- script to fix migration (lnader@redhat.com)
- Fixed zend upgrade problem (lnader@redhat.com)
- added Zend framework 2 ini file (lnader@redhat.com)
- Bug 859186 (lnader@redhat.com)
- minor change request from zend (lnader@redhat.com)
- Display EULA on users first visit (lnader@redhat.com)
- Merge Zend's and OpenShift's php.ini files (vvitek@redhat.com)

* Wed Sep 12 2012 Adam Miller <admiller@redhat.com> 0.96.1-1
- bump_minor_versions for sprint 18 (admiller@redhat.com)

* Wed Sep 12 2012 Adam Miller <admiller@redhat.com> 0.95.9-1
- Merge pull request #363 from smarterclayton/last_minute_zend_changes
  (openshift+bot@redhat.com)
- Updates for Zend based on last minute feedback (ccoleman@redhat.com)

* Tue Sep 11 2012 Troy Dawson <tdawson@redhat.com> 0.95.8-1
- Merge pull request #358 from lnader/master (openshift+bot@redhat.com)
- Bug 853324 (lnader@redhat.com)

* Mon Sep 10 2012 Dan McPherson <dmcphers@redhat.com> 0.95.7-1
- Merge pull request #355 from lnader/master (openshift+bot@redhat.com)
- Bug 853586 (lnader@redhat.com)

* Fri Sep 07 2012 Adam Miller <admiller@redhat.com> 0.95.6-1
- Merge pull request #350 from sg00dwin/master (openshift+bot@redhat.com)
- Merge pull request #340 from pravisankar/dev/ravi/zend-fix-description
  (openshift+bot@redhat.com)
- Merge branch 'master' of github.com:openshift/li (sgoodwin@redhat.com)
- BZ 849782 - rss button rendering issue BZ 839242 - new app page for zend
  needed css added BZ 820086 - long sshkey name text-overflow issue Check in
  new account plan styleguide pages for billing, payment, review/confirm along
  with new form validation css Misc css - switch heading font-size to be based
  off of $baseFontSize computation - match <legend> style to heading.divide for
  consistency when used on console form pages - addition of <select> to
  standard form field rules (not sure why they aren't included in bootstrap by
  default) - set box-showdow(none) on .btn so there's no conflict when used on
  <input> - create aside rule within console/_core to be used on pages with for
  secondary column (help) - remove input grid system rules that caused
  conflicting widths with inputs set to grid span - add :focus to
  buttonBackground mixin - decrease spacing associated with .control-group -
  added rules for :focus:required:valid :focus:required:invalid to take
  advantage of client side browsers that support them - move rules for field
  feedback states from _custom to _forms - .alert a so link color is optimal on
  all alert states (sgoodwin@redhat.com)
- Modify Display-name/Description fields for all cartridges (rpenta@redhat.com)

* Thu Sep 06 2012 Adam Miller <admiller@redhat.com> 0.95.5-1
- Fix for bugz 852216 - zend /sandbox should be root owned if possible.
  (ramr@redhat.com)
- Bug 852192 - Zend - additional Information (lnader@redhat.com)
- zend spec fix (admiller@redhat.com)

* Tue Sep 04 2012 Adam Miller <admiller@redhat.com> - 0.95.4-1
- spec file clean up, add changelog, fix brew build failures
