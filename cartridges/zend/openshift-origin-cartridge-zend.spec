%global cartridgedir %{_libexecdir}/openshift/cartridges/v2/zend
%global frameworkdir %{_libexecdir}/openshift/cartridges/v2/zend

Name:    openshift-origin-cartridge-zend
Version: 0.2.8
Release: 1%{?dist}
Summary: Zend Server cartridge
Group:   Development/Languages
License: ASL 2.0
URL:     https://openshift.redhat.com
Source0: %{name}-%{version}.tar.gz

Requires:      rubygem(openshift-origin-node)
Requires:      openshift-origin-node-util

Requires: rubygem-builder

Requires: zend-server-php-5.3 >= 5.6.0-11
Requires: php-5.3-mongo-zend-server
Requires: php-5.3-imagick-zend-server
Requires: php-5.3-uploadprogress-zend-server
Requires: php-5.3-java-bridge-zend-server
Requires: php-5.3-optimizer-plus-zend-server
Requires: php-5.3-zend-extensions
Requires: php-5.3-extra-extensions-zend-server
Requires: php-5.3-loader-zend-server

#Obsoletes: openshift-origin-cartridge-zend-5.6

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildArch: noarch

%description
Zend Server cartridge for openshift.

%prep
%setup -q

%build

%install
%__rm -rf %{buildroot}
%__mkdir -p %{buildroot}%{cartridgedir}
%__cp -r * %{buildroot}%{cartridgedir}

%clean
%__rm -rf %{buildroot}

%post
%{_sbindir}/oo-admin-cartridge --action install --source %{cartridgedir}
#this copies over files in zend server rpm install that do not work in openshift 
%__cp -rf %{cartridgedir}/versions/5.6/configuration/shared-files/usr/local/zend/* /usr/local/zend/
sh %{cartridgedir}/versions/5.6/rpm/zend_configure_filesystem.sh


%files
%defattr(-,root,root,-)
%dir %{cartridgedir}
%attr(0755,-,-) %{cartridgedir}/bin/
%attr(0755,-,-) %{cartridgedir}/hooks/
%{cartridgedir}
%doc %{cartridgedir}/README.md
%doc %{cartridgedir}/COPYRIGHT
%doc %{cartridgedir}/LICENSE


%changelog
* Sat Jun 01 2013 Dan McPherson <dmcphers@redhat.com> 0.2.8-1
- Merge pull request #1504 from VojtechVitek/stage_bz968943_2
  (dmcphers@redhat.com)
- Make Initial-Build-Required default to false (ironcladlou@gmail.com)
- Fix Zend apachectl deployment settings (vvitek@redhat.com)

* Thu May 30 2013 Adam Miller <admiller@redhat.com> 0.2.7-1
- add zend php binary to env PATH variable (vvitek@redhat.com)

* Fri May 24 2013 Adam Miller <admiller@redhat.com> 0.2.6-1
- Merge pull request #1452 from VojtechVitek/zend_disable_oci_extension
  (dmcphers+openshiftbot@redhat.com)
- disable Zend PHP PDO-OCI extension (vvitek@redhat.com)

* Thu May 23 2013 Adam Miller <admiller@redhat.com> 0.2.5-1
- Merge pull request #1446 from ironcladlou/bz/966255
  (dmcphers+openshiftbot@redhat.com)
- Bug 966255: Remove OPENSHIFT_INTERNAL_* references from v2 carts
  (ironcladlou@gmail.com)

* Wed May 22 2013 Adam Miller <admiller@redhat.com> 0.2.4-1
- Bug 962662 (dmcphers@redhat.com)
- Bug 965537 - Dynamically build PassEnv httpd configuration
  (jhonce@redhat.com)
- Fix but 964348 (pmorie@gmail.com)

* Mon May 20 2013 Dan McPherson <dmcphers@redhat.com> 0.2.3-1
- Bug 963494 - Zend cartridges cannot be created (jhonce@redhat.com)

* Thu May 16 2013 Adam Miller <admiller@redhat.com> 0.2.2-1
- locking fixes and adjustments (dmcphers@redhat.com)
- Merge pull request #1367 from fotioslindiakos/locked_files
  (dmcphers+openshiftbot@redhat.com)
- WIP Cartridge Refactor -- Cleanup spec files (jhonce@redhat.com)
- Added erb processing to managed_files.yml (fotios@redhat.com)
- Card online_runtime_297 - Allow cartridges to use more resources
  (jhonce@redhat.com)
- Card online_runtime_297 - Allow cartridges to use more resources
  (jhonce@redhat.com)

* Wed May 08 2013 Adam Miller <admiller@redhat.com> 0.2.1-1
- bump_minor_versions for sprint 28 (admiller@redhat.com)

* Mon May 06 2013 Adam Miller <admiller@redhat.com> 0.1.11-1
- Merge pull request #1301 from VojtechVitek/zend_bug_fixes
  (dmcphers+openshiftbot@redhat.com)
- Warn users to set Zend Server Console password (vvitek@redhat.com)
- Improve Zend control client_* messages (vvitek@redhat.com)
- Update Zend license key/serial (vvitek@redhat.com)
- fix /ZendServer GUI Console (vvitek@redhat.com)

* Fri May 03 2013 Adam Miller <admiller@redhat.com> 0.1.10-1
- cleanup (dmcphers@redhat.com)
- Converted metadata/{locked_files,snapshot*}.txt (fotios@redhat.com)

* Thu May 02 2013 Adam Miller <admiller@redhat.com> 0.1.9-1
- fix zend configuration (vvitek@redhat.com)

* Tue Apr 30 2013 Adam Miller <admiller@redhat.com> 0.1.8-1
- Merge pull request #1268 from VojtechVitek/zend-v2-setup-install
  (dmcphers+openshiftbot@redhat.com)
- Merge pull request #1269 from rmillner/v2_misc_fixes
  (dmcphers+openshiftbot@redhat.com)
- Add health mapping to Zend. (rmillner@redhat.com)
- fix zend v2 setup/install (vvitek@redhat.com)

* Mon Apr 29 2013 Adam Miller <admiller@redhat.com> 0.1.7-1
- Bug 957073 (dmcphers@redhat.com)

* Thu Apr 25 2013 Adam Miller <admiller@redhat.com> 0.1.6-1
- zend work (dmcphers@redhat.com)

* Thu Apr 25 2013 Dan McPherson <dmcphers@redhat.com> 0.1.5-1
- 

* Thu Apr 25 2013 Dan McPherson <dmcphers@redhat.com> 0.1.4-1
- 

* Wed Apr 24 2013 Dan McPherson <dmcphers@redhat.com> 0.1.3-1
- new package built with tito

* Wed Apr 24 2013 Vojtech Vitek (V-Teq) <vvitek@redhat.com>
- Zend v2 init (vvitek@redhat.com)

* Tue Apr 23 2013 Vojtech Vitek (V-Teq) <vvitek@redhat.com>
- init package built with tito

