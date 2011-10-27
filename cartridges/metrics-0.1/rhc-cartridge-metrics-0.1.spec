%define cartridgedir %{_libexecdir}/li/cartridges/embedded/metrics-0.1

Name: rhc-cartridge-metrics-0.1
Version: 0.3.1
Release: 1%{?dist}
Summary: Embedded metrics support for express

Group: Applications/Internet
License: GPLv2
URL: https://engineering.redhat.com/trac/Libra
Source0: %{name}-%{version}.tar.gz
BuildRoot:    %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
BuildArch: noarch

Requires: rhc-broker >= 0.70.1

%description
Provides rhc metrics cartridge support

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

%post

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%attr(0750,-,-) %{cartridgedir}/info/hooks/
%attr(0750,-,-) %{cartridgedir}/info/build/
%config(noreplace) %{cartridgedir}/info/configuration/
%attr(0755,-,-) %{cartridgedir}/info/bin/
%attr(0755,-,-) %{cartridgedir}/info/data/
%{_sysconfdir}/libra/cartridges/%{name}
%{cartridgedir}/info/changelog
%{cartridgedir}/info/control

%changelog
* Thu Oct 27 2011 Dan McPherson <dmcphers@redhat.com> 0.3.1-1
- bump spec numbers (dmcphers@redhat.com)

* Wed Oct 26 2011 Dan McPherson <dmcphers@redhat.com> 0.2.10-1
- move app info for embedded carts to separate call (dmcphers@redhat.com)

* Tue Oct 25 2011 Dan McPherson <dmcphers@redhat.com> 0.2.9-1
- Bug 748658 (dmcphers@redhat.com)
- bug 748662 (dmcphers@redhat.com)

* Wed Oct 19 2011 Dan McPherson <dmcphers@redhat.com> 0.2.8-1
- Adding info/data/ (mmcgrath@redhat.com)

* Wed Oct 19 2011 Mike McGrath <mmcgrath@redhat.com> 0.2.7-1
- new package built with tito

* Wed Oct 19 2011 Mike McGrath <mmcgrath@redhat.com> 0.2.6-1
- removing uneeded files (mmcgrath@redhat.com)
- added metrics cartridge (mmcgrath@redhat.com)
