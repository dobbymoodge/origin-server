%global drupal_release      6
%global drupal_base         %{_datadir}/drupal%{drupal_release}
%global drupal_sites_all    %{drupal_base}/sites/all        
%global drupal_modules      %{drupal_sites_all}/modules/custom
%global modname             og_comment_perms

Name:    drupal%{drupal_release}-openshift-%{modname}
Version: 1.5.1
Release: 1%{?dist}
Summary: Openshift Red Hat Organic Group Comment Custom Module for Drupal6
Group:   Applications/Publishing
License: GPLv2+
Source0: %{name}-%{version}.tar.gz
BuildArch: noarch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires:  drupal6

%description
Openshift Red Hat Organic Group Comment Custom Module for Drupal6


%prep
%setup -q
# Remove empty index.html and others
find -size 0 | xargs rm -f

%build


%install
rm -rf $RPM_BUILD_ROOT
%{__mkdir} -p $RPM_BUILD_ROOT/%{drupal_modules}/%{modname}
cp -pr . $RPM_BUILD_ROOT/%{drupal_modules}/%{modname}


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%{drupal_modules}/%{modname}

%changelog
* Tue Jun 25 2013 Adam Miller <admiller@redhat.com> 1.5.1-1
- bump_minor_versions for sprint 30 (admiller@redhat.com)

* Mon Jun 17 2013 Adam Miller <admiller@redhat.com> 1.4.2-1
- Bug 917520 - join group on thread, remove modal prompt (jforrest@redhat.com)

* Fri Jun 07 2013 Adam Miller 1.4.1-5
- Bump spec for mass drupal rebuild

* Thu Jun 06 2013 Adam Miller 1.4.1-4
- Bump spec for mass drupal rebuild

* Wed Jun 05 2013 Adam Miller 1.4.1-3
- Bump spec for mass drupal rebuild

* Mon Jun 03 2013 Adam Miller 1.4.1-2
- Bump spec for mass drupal rebuild

* Thu Mar 07 2013 Adam Miller <admiller@redhat.com> 1.4.1-1
- bump_minor_versions for sprint 25 (admiller@redhat.com)

* Wed Mar 06 2013 Adam Miller 1.3.2-3
- Bump spec for mass drupal rebuild

* Mon Feb 18 2013 Adam Miller <admiller@redhat.com> 1.3.2-2
- Bump spec for mass drupal rebuild

* Fri Feb 08 2013 Adam Miller <admiller@redhat.com> 1.3.2-1
- bump Release: for all drupal packages for rebuild (admiller@redhat.com)

* Fri Feb 08 2013 Adam Miller <admiller@redhat.com> - 1.3.1-2
- rebuilt

* Wed Jul 11 2012 Adam Miller <admiller@redhat.com> 1.3.1-1
- bump_minor_versions for sprint 15 (admiller@redhat.com)

* Sat Jun 23 2012 Dan McPherson <dmcphers@redhat.com> 1.2.3-1
- 

* Sat Jun 23 2012 Dan McPherson <dmcphers@redhat.com> 1.2.2-1
- new package built with tito

* Thu May 10 2012 Adam Miller <admiller@redhat.com> 1.2.1-1
- fix up spec versions (dmcphers@redhat.com)
- bumping spec versions (admiller@redhat.com)

* Thu Apr 26 2012 Adam Miller <admiller@redhat.com> 1.1.1-1
- bumping spec versions (admiller@redhat.com)

* Wed Apr 18 2012 Dan McPherson <dmcphers@redhat.com> 1.0.3-1
- Touch all drupal modules to ensure a build. (ccoleman@redhat.com)

* Mon Apr 16 2012 Anderson Silva <ansilva@redhat.com> 1.0.2-1
- new package built with tito

* Mon Apr 16 2012 Anderson Silva <ansilva@redhat.com> - 1.0.1-1
- update version

* Mon Mar 5 2012 Anderson Silva <ansilva@redhat.com> - 1.0-1
- Initial rpm package