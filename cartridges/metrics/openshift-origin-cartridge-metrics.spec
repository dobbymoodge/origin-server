%define cartridgedir %{_libexecdir}/openshift/cartridges/metrics

Name: openshift-origin-cartridge-metrics
Version: 1.7.3
Release: 1%{?dist}
Summary: Metrics cartridge

Group: Applications/Internet
License: GPLv2
URL: https://engineering.redhat.com/trac/Libra
Source0: %{name}-%{version}.tar.gz
BuildRoot:    %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
BuildArch: noarch

Requires: openshift-origin-cartridge-abstract
Requires: rubygem(openshift-origin-node)

%description
Provides metrics cartridge support

%prep
%setup -q


%build


%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{cartridgedir}
cp -r * %{buildroot}%{cartridgedir}/

%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%dir %{cartridgedir}
%attr(0755,-,-) %{cartridgedir}/bin/
%attr(0755,-,-) %{cartridgedir}
%{cartridgedir}/metadata/manifest.yml
%doc %{cartridgedir}/README.md

%changelog
* Tue Apr 02 2013 Dan McPherson <dmcphers@redhat.com> 1.7.3-1
- Automatic commit of package [openshift-origin-cartridge-metrics] release
  [1.7.2-1]. (dmcphers@redhat.com)

* Tue Apr 02 2013 Dan McPherson <dmcphers@redhat.com> 1.7.2-1
- new package built with tito

* Thu Mar 28 2013 Adam Miller <admiller@redhat.com> 1.7.1-1
- bump_minor_versions for sprint 26 (admiller@redhat.com)