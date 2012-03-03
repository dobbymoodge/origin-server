%define cartridgedir %{_libexecdir}/li/cartridges/embedded/phpmyadmin-3.4

Name: rhc-cartridge-phpmyadmin-3.4
Version: 0.10.0
Release: 1%{?dist}
Summary: Embedded phpMyAdmin support for express

Group: Applications/Internet
License: ASL 2.0
URL: https://engineering.redhat.com/trac/Libra
Source0: %{name}-%{version}.tar.gz
BuildRoot:    %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
BuildArch: noarch

Requires: rhc-node
Requires: phpMyAdmin

%description
Provides rhc phpMyAdmin cartridge support

%prep
%setup -q

%build

%install
rm -rf $RPM_BUILD_ROOT
rm -rf %{buildroot}
mkdir -p %{buildroot}%{cartridgedir}
mkdir -p %{buildroot}/%{_sysconfdir}/libra/cartridges
ln -s %{cartridgedir}/info/configuration/ %{buildroot}/%{_sysconfdir}/libra/cartridges/%{name}
cp -r info %{buildroot}%{cartridgedir}/
cp LICENSE %{buildroot}%{cartridgedir}/
cp COPYRIGHT %{buildroot}%{cartridgedir}/

%post
cp %{cartridgedir}/info/configuration/etc/phpMyAdmin/config.inc.php %{_sysconfdir}/phpMyAdmin/config.inc.php

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%attr(0750,-,-) %{cartridgedir}/info/hooks/
%attr(0750,-,-) %{cartridgedir}/info/build/
%config(noreplace) %{cartridgedir}/info/configuration/
%attr(0755,-,-) %{cartridgedir}/info/bin/
%attr(0755,-,-) %{cartridgedir}/info/html/
%attr(0644,-,-) %{cartridgedir}/info/html/*
%{_sysconfdir}/libra/cartridges/%{name}
%{cartridgedir}/info/changelog
%{cartridgedir}/info/control
%{cartridgedir}/info/manifest.yml
%doc %{cartridgedir}/COPYRIGHT
%doc %{cartridgedir}/LICENSE

%changelog
* Tue Feb 28 2012 Dan McPherson <dmcphers@redhat.com> 0.9.3-1
- some cleanup of http -C Include (dmcphers@redhat.com)

* Mon Feb 27 2012 Dan McPherson <dmcphers@redhat.com> 0.9.2-1
- cleanup all the old command usage in help and messages (dmcphers@redhat.com)

* Thu Feb 16 2012 Dan McPherson <dmcphers@redhat.com> 0.9.1-1
- bump spec numbers (dmcphers@redhat.com)

* Mon Feb 13 2012 Dan McPherson <dmcphers@redhat.com> 0.8.2-1
- fix manifest, cant depend on php/www-dynamic yet (rchopra@redhat.com)
- more abstracting out selinux (dmcphers@redhat.com)
- first pass at splitting out selinux logic (dmcphers@redhat.com)
- Updating models to improove schems of descriptor in mongo Moved
  connection_endpoint to broker (kraman@gmail.com)
- Fixing manifest yml files (kraman@gmail.com)
- Creating models for descriptor Fixing manifest files Added command to list
  installed cartridges and get descriptors (kraman@gmail.com)
- change status to use normal client_result instead of special handling
  (dmcphers@redhat.com)

* Fri Feb 03 2012 Dan McPherson <dmcphers@redhat.com> 0.8.1-1
- bump spec numbers (dmcphers@redhat.com)
- Make it clear the phpmyadmin and rockmongo users are just the db users
  (dmcphers@redhat.com)

* Wed Feb 01 2012 Dan McPherson <dmcphers@redhat.com> 0.7.5-1
- Bug 786317 (dmcphers@redhat.com)
- fix postgres move and other selinux move fixes (dmcphers@redhat.com)

* Sun Jan 29 2012 Dan McPherson <dmcphers@redhat.com> 0.7.4-1
- Fixed Bug 749751 (twiest@redhat.com)

* Fri Jan 27 2012 Dan McPherson <dmcphers@redhat.com> 0.7.3-1
- deploy httpd proxy from migration (dmcphers@redhat.com)
- Adding status=I to force proxy layer to attempt to connect every time even in
  error scenarios. (mmcgrath@redhat.com)

* Tue Jan 24 2012 Dan McPherson <dmcphers@redhat.com> 0.7.2-1
- Updated License value in manifest.yml files. Corrected Apache Software
  License Fedora short name (jhonce@redhat.com)
- phpmyadmin-3.4: Modified license to ASL V2 (jhonce@redhat.com)

* Fri Jan 13 2012 Dan McPherson <dmcphers@redhat.com> 0.7.1-1
- bump spec numbers (dmcphers@redhat.com)

* Fri Jan 06 2012 Dan McPherson <dmcphers@redhat.com> 0.6.5-1
- fix build breaks (dmcphers@redhat.com)

* Fri Jan 06 2012 Dan McPherson <dmcphers@redhat.com> 0.6.4-1
- basic descriptors for all cartridges; added primitive structure for a www-
  dynamic cartridge that will abstract all httpd processes that any cartridges
  need (e.g. php, perl, metrics, rockmongo etc). (rchopra@redhat.com)
