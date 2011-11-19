%define cartridgedir %{_libexecdir}/li/cartridges/embedded/mongodb-2.0

Name: rhc-cartridge-mongodb-2.0
Version: 0.6
Release: 1%{?dist}
Summary: Embedded mongodb support for express

Group: Network/Daemons
License: GPLv2
URL: https://engineering.redhat.com/trac/Libra
Source0: %{name}-%{version}.tar.gz
BuildRoot:    %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
BuildArch: noarch

Requires: rhc-node
Requires: mongodb-server
Requires: mongodb-devel
Requires: libmongodb
Requires: mongodb

%description
Provides rhc mongodb cartridge support

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


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%attr(0750,-,-) %{cartridgedir}/info/hooks/
%attr(0750,-,-) %{cartridgedir}/info/build/
%config(noreplace) %{cartridgedir}/info/configuration/
%attr(0755,-,-) %{cartridgedir}/info/bin/
%attr(0755,-,-) %{cartridgedir}/info/lib/
%{_sysconfdir}/libra/cartridges/%{name}
%{cartridgedir}/info/changelog
%{cartridgedir}/info/control

%changelog
* Fri Nov 18 2011 Ram Ranganathan <ramr@redhat.com> 0.7-1
- mongodb dump and restore functions

* Fri Nov 18 2011 Dan McPherson <dmcphers@redhat.com> 0.6-1
- moving logic to abstract from li-controller (dmcphers@redhat.com)

* Wed Nov 16 2011 Dan McPherson <dmcphers@redhat.com> 0.5-1
- fix stop/start issue + add convenience user to db '$app' (ramr@redhat.com)
- authorization support + turn off http interface. (ramr@redhat.com)

* Wed Nov 16 2011 Ram Ranganathan <ramr@redhat.com> 0.5-2
- fix stop/start issue + add convenience user to db '$app'

* Wed Nov 16 2011 Ram Ranganathan <ramr@redhat.com> 0.5-1
- authorization support + turn off http interface

* Tue Nov 15 2011 Dan McPherson <dmcphers@redhat.com> 0.4-1
- Merge branch 'master' of ssh://git1.ops.rhcloud.com/srv/git/li
  (mmcgrath@redhat.com)
- disable journal for embedded (mmcgrath@redhat.com)

* Tue Nov 15 2011 Dan McPherson <dmcphers@redhat.com> 0.3-1
- Merge branch 'master' of ssh://express-master/srv/git/li (ramr@redhat.com)
- increasing max filesize (mmcgrath@redhat.com)
- fixup hooks - start/stop/restart/configure + add "scaffolding" for running
  mongo w/ auth - admin user. (ramr@redhat.com)

* Tue Nov 15 2011 Ram Ranganathan <ramr@redhat.com> 0.2-2
- admin user [for auth], plus fixup start/stop/restart/configure hooks

* Tue Nov 15 2011 Mike McGrath <mmcgrath@redhat.com> 0.2-1
- new package built with tito

* Mon Nov 14 2011 Dan McPherson <mmcgrath@redhat.com> 0.1-1
- Initial packaging
