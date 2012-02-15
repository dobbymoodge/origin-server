%define cartridgedir %{_libexecdir}/li/cartridges/perl-5.10

Summary:   Provides mod_perl support
Name:      rhc-cartridge-perl-5.10
Version:   0.17.14
Release:   1%{?dist}
Group:     Development/Languages
License:   ASL 2.0
URL:       http://openshift.redhat.com
Source0:   %{name}-%{version}.tar.gz

BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
BuildRequires: git
Requires:  rhc-node >= 0.69.4
Requires:  mod_perl
Requires:  perl-DBD-SQLite
Requires:  perl-DBD-MySQL
Requires:  perl-MongoDB
Requires:  ImageMagick-perl
Requires:  perl-App-cpanminus
# used to do dep resolving for perl
Requires:  rpm-build

BuildArch: noarch

%description
Provides rhc perl cartridge support

%prep
%setup -q

%build
rm -rf git_template
cp -r template/ git_template/
cd git_template
git init
git add -f .
git commit -m 'Creating template'
cd ..
git clone --bare git_template git_template.git
rm -rf git_template
touch git_template.git/refs/heads/.gitignore

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{cartridgedir}
mkdir -p %{buildroot}/%{_sysconfdir}/libra/cartridges
ln -s %{cartridgedir}/info/configuration/ %{buildroot}/%{_sysconfdir}/libra/cartridges/%{name}
cp -r info %{buildroot}%{cartridgedir}/
cp LICENSE %{buildroot}%{cartridgedir}/
cp COPYRIGHT %{buildroot}%{cartridgedir}/
mkdir -p %{buildroot}%{cartridgedir}/info/data/
cp -r git_template.git %{buildroot}%{cartridgedir}/info/data/
ln -s %{cartridgedir}/../abstract/info/hooks/add-module %{buildroot}%{cartridgedir}/info/hooks/add-module
ln -s %{cartridgedir}/../abstract/info/hooks/info %{buildroot}%{cartridgedir}/info/hooks/info
ln -s %{cartridgedir}/../abstract/info/hooks/post-install %{buildroot}%{cartridgedir}/info/hooks/post-install
ln -s %{cartridgedir}/../abstract/info/hooks/post-remove %{buildroot}%{cartridgedir}/info/hooks/post-remove
ln -s %{cartridgedir}/../abstract/info/hooks/reload %{buildroot}%{cartridgedir}/info/hooks/reload
ln -s %{cartridgedir}/../abstract/info/hooks/remove-module %{buildroot}%{cartridgedir}/info/hooks/remove-module
ln -s %{cartridgedir}/../abstract/info/hooks/restart %{buildroot}%{cartridgedir}/info/hooks/restart
ln -s %{cartridgedir}/../abstract/info/hooks/start %{buildroot}%{cartridgedir}/info/hooks/start
ln -s %{cartridgedir}/../abstract-httpd/info/hooks/status %{buildroot}%{cartridgedir}/info/hooks/status
ln -s %{cartridgedir}/../abstract/info/hooks/stop %{buildroot}%{cartridgedir}/info/hooks/stop
ln -s %{cartridgedir}/../abstract/info/hooks/preconfigure %{buildroot}%{cartridgedir}/info/hooks/preconfigure
ln -s %{cartridgedir}/../abstract/info/hooks/update-namespace %{buildroot}%{cartridgedir}/info/hooks/update-namespace
ln -s %{cartridgedir}/../abstract/info/hooks/deploy-httpd-proxy %{buildroot}%{cartridgedir}/info/hooks/deploy-httpd-proxy
ln -s %{cartridgedir}/../abstract/info/hooks/remove-httpd-proxy %{buildroot}%{cartridgedir}/info/hooks/remove-httpd-proxy
ln -s %{cartridgedir}/../abstract/info/hooks/force-stop %{buildroot}%{cartridgedir}/info/hooks/force-stop
ln -s %{cartridgedir}/../abstract/info/hooks/add-alias %{buildroot}%{cartridgedir}/info/hooks/add-alias
ln -s %{cartridgedir}/../abstract/info/hooks/tidy %{buildroot}%{cartridgedir}/info/hooks/tidy
ln -s %{cartridgedir}/../abstract/info/hooks/remove-alias %{buildroot}%{cartridgedir}/info/hooks/remove-alias
ln -s %{cartridgedir}/../abstract/info/hooks/move %{buildroot}%{cartridgedir}/info/hooks/move
ln -s %{cartridgedir}/../abstract/info/hooks/threaddump %{buildroot}%{cartridgedir}/info/hooks/threaddump
ln -s %{cartridgedir}/../abstract/info/hooks/expose-port %{buildroot}%{cartridgedir}/info/hooks/expose-port
ln -s %{cartridgedir}/../abstract/info/hooks/conceal-port %{buildroot}%{cartridgedir}/info/hooks/conceal-port
ln -s %{cartridgedir}/../abstract/info/hooks/system-messages %{buildroot}%{cartridgedir}/info/hooks/system-messages

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%attr(0750,-,-) %{cartridgedir}/info/hooks/
%attr(0750,-,-) %{cartridgedir}/info/data/
%attr(0750,-,-) %{cartridgedir}/info/build/
%attr(0755,-,-) %{cartridgedir}/info/bin/
%config(noreplace) %{cartridgedir}/info/configuration/
%{_sysconfdir}/libra/cartridges/%{name}
%{cartridgedir}/info/changelog
%{cartridgedir}/info/control
%{cartridgedir}/info/manifest.yml
%doc %{cartridgedir}/COPYRIGHT
%doc %{cartridgedir}/LICENSE

%changelog
* Wed Feb 15 2012 Dan McPherson <dmcphers@redhat.com> 0.17.14-1
- Adding expose/conceal port to more cartridges. (rmillner@redhat.com)

* Mon Feb 13 2012 Dan McPherson <dmcphers@redhat.com> 0.17.13-1
- Add sample/empty directories for minutely,hourly,daily and monthly
  frequencies as well. (ramr@redhat.com)
- Add cron example and directories to all the openshift framework templates.
  (ramr@redhat.com)

* Mon Feb 13 2012 Dan McPherson <dmcphers@redhat.com> 0.17.12-1
- add nosql env vars to perl (dmcphers@redhat.com)

* Sat Feb 11 2012 Dan McPherson <dmcphers@redhat.com> 0.17.11-1
- 

* Sat Feb 11 2012 Dan McPherson <dmcphers@redhat.com> 0.17.10-1
- 

* Sat Feb 11 2012 Dan McPherson <dmcphers@redhat.com> 0.17.9-1
- 

* Sat Feb 11 2012 Dan McPherson <dmcphers@redhat.com> 0.17.8-1
- 

* Sat Feb 11 2012 Dan McPherson <dmcphers@redhat.com> 0.17.7-1
- 

* Sat Feb 11 2012 Dan McPherson <dmcphers@redhat.com> 0.17.6-1
- 

* Sat Feb 11 2012 Dan McPherson <dmcphers@redhat.com> 0.17.5-1
- 

* Sat Feb 11 2012 Dan McPherson <dmcphers@redhat.com> 0.17.4-1
- 

* Sat Feb 11 2012 Dan McPherson <dmcphers@redhat.com> 0.17.3-1
- 

* Sat Feb 11 2012 Dan McPherson <dmcphers@redhat.com> 0.17.2-1
- README: added disable_cpan_tests information (tdawson@redhat.com)
- build.sh: adding disable_cpan_tests marker (tdawson@redhat.com)
- bug 722828 (bdecoste@gmail.com)
- more abstracting out selinux (dmcphers@redhat.com)
- better name consistency (dmcphers@redhat.com)
- first pass at splitting out selinux logic (dmcphers@redhat.com)
- Fix wrong link to remove-httpd-proxy (hypens not underscores) and fix
  manifests for Node and Python to allow for nodejs/python app creation.
  (ramr@redhat.com)
- removed dependency on www-dynamic (rchopra@redhat.com)
- Updating models to improove schems of descriptor in mongo Moved
  connection_endpoint to broker (kraman@gmail.com)
- Creating models for descriptor Fixing manifest files Added command to list
  installed cartridges and get descriptors (kraman@gmail.com)

* Fri Feb 03 2012 Dan McPherson <dmcphers@redhat.com> 0.17.1-1
- bump spec numbers (dmcphers@redhat.com)

* Tue Jan 24 2012 Dan McPherson <dmcphers@redhat.com> 0.16.3-1
- Updated License value in manifest.yml files. Corrected Apache Software
  License Fedora short name (jhonce@redhat.com)
- perl-5.10: Modified license to ASL V2 (jhonce@redhat.com)

* Fri Jan 20 2012 Mike McGrath <mmcgrath@redhat.com> 0.16.2-1
- perl-5.10.spec: Added Requires perl-DBD-SQLite and perl-DBD-MySQL
  (tdawson@redhat.com)

* Fri Jan 13 2012 Dan McPherson <dmcphers@redhat.com> 0.16.1-1
- bump spec numbers (dmcphers@redhat.com)

* Wed Jan 11 2012 Dan McPherson <dmcphers@redhat.com> 0.15.5-1
- Gracefully handle threaddump in cartridges that do not support it (BZ772114)
  (aboone@redhat.com)

* Fri Jan 06 2012 Dan McPherson <dmcphers@redhat.com> 0.15.4-1
- fix build breaks (dmcphers@redhat.com)

* Fri Jan 06 2012 Dan McPherson <dmcphers@redhat.com> 0.15.3-1
- basic descriptors for all cartridges; added primitive structure for a www-
  dynamic cartridge that will abstract all httpd processes that any cartridges
  need (e.g. php, perl, metrics, rockmongo etc). (rchopra@redhat.com)
