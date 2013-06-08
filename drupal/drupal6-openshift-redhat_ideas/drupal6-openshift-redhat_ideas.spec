%global drupal_release      6
%global drupal_base         %{_datadir}/drupal%{drupal_release}
%global drupal_sites_all    %{drupal_base}/sites/all        
%global drupal_modules      %{drupal_sites_all}/modules/custom
%global modname             redhat_ideas

Name:    drupal%{drupal_release}-openshift-%{modname}
Version: 1.6.2
Release: 1%{?dist}
Summary: Openshift Red Hat Ideas Custom Module for Drupal6
Group:   Applications/Publishing
License: GPLv2+
Source0: %{name}-%{version}.tar.gz
BuildArch: noarch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires:  drupal6, drupal6-views, drupal6-features

%description
Openshift Red Hat Ideas Custom Module for Drupal6


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
* Fri Jun 07 2013 Adam Miller <admiller@redhat.com> 1.6.2-1
- Site summit changes, backported from bbe7f47f293c826be00ead46457377f475b810b7
  in master (ccoleman@redhat.com)

* Thu Mar 07 2013 Adam Miller <admiller@redhat.com> 1.6.1-1
- bump_minor_versions for sprint 25 (admiller@redhat.com)

* Wed Mar 06 2013 Adam Miller 1.5.2-3
- Bump spec for mass drupal rebuild

* Mon Feb 18 2013 Adam Miller <admiller@redhat.com> 1.5.2-2
- Bump spec for mass drupal rebuild

* Fri Feb 08 2013 Adam Miller <admiller@redhat.com> 1.5.2-1
- bump Release: for all drupal packages for rebuild (admiller@redhat.com)
- US3291 US3292 US3293 - Move community to www.openshift.com
  (ccoleman@redhat.com)

* Fri Feb 08 2013 Adam Miller <admiller@redhat.com> - 1.5.1-2
- rebuilt

* Wed Aug 22 2012 Adam Miller <admiller@redhat.com> 1.5.1-1
- bump_minor_versions for sprint 17 (admiller@redhat.com)

* Thu Aug 09 2012 Adam Miller <admiller@redhat.com> 1.4.2-1
- Adding feature request search field (sgoodwin@redhat.com)

* Wed Jul 11 2012 Adam Miller <admiller@redhat.com> 1.4.1-1
- bump_minor_versions for sprint 15 (admiller@redhat.com)

* Sat Jun 23 2012 Dan McPherson <dmcphers@redhat.com> 1.3.3-1
- 

* Sat Jun 23 2012 Dan McPherson <dmcphers@redhat.com> 1.3.2-1
- new package built with tito

* Fri Jun 01 2012 Adam Miller <admiller@redhat.com> 1.3.1-1
- bumping spec versions (admiller@redhat.com)

* Thu May 17 2012 Adam Miller <admiller@redhat.com> 1.2.2-1
- Add a much improved ideas view and sub pages (ccoleman@redhat.com)

* Thu May 10 2012 Adam Miller <admiller@redhat.com> 1.2.1-1
- bumping spec versions (admiller@redhat.com)

* Mon May 07 2012 Adam Miller <admiller@redhat.com> 1.1.2-1
- Update some features from drupal (ccoleman@redhat.com)

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
