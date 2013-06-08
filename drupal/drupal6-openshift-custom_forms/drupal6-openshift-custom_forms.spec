%global drupal_release      6
%global drupal_base         %{_datadir}/drupal%{drupal_release}
%global drupal_sites_all    %{drupal_base}/sites/all        
%global drupal_modules      %{drupal_sites_all}/modules/custom
%global modname             custom_forms

Name:    drupal%{drupal_release}-openshift-%{modname}
Version: 1.3.2
Release: 1%{?dist}
Summary: Openshift Red Hat Custom Forms for Drupal6
Group:   Applications/Publishing
License: GPLv2+
Source0: %{name}-%{version}.tar.gz
BuildArch: noarch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires:  drupal6

%description
Summary: Openshift Red Hat Custom Forms for Drupal6


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
* Sat Jun 08 2013 Dan McPherson <dmcphers@redhat.com> 1.3.2-1
- Automatic commit of package [rhc-site] release [1.9.13-2].
  (admiller@redhat.com)

* Fri Jun 07 2013 Adam Miller - 1.3.1-2
- Bumpspec for drupal mass rebuild

* Thu Apr 25 2013 Adam Miller <admiller@redhat.com> 1.3.1-1
- bump_minor_versions for sprint XX (tdawson@redhat.com)

* Mon Apr 08 2013 Adam Miller <admiller@redhat.com> 1.2.2-1
- Admins should be able to edit email addresses in the community
  (ccoleman@redhat.com)

* Thu Mar 07 2013 Adam Miller <admiller@redhat.com> 1.2.1-1
- bump_minor_versions for sprint 25 (admiller@redhat.com)

* Wed Mar 06 2013 Adam Miller 1.1.2-3
- Bump spec for mass drupal rebuild

* Mon Feb 18 2013 Adam Miller <admiller@redhat.com> 1.1.2-2
- Bump spec for mass drupal rebuild

* Fri Feb 08 2013 Adam Miller <admiller@redhat.com> 1.1.2-1
- bump Release: for all drupal packages for rebuild (admiller@redhat.com)
- US3291 US3292 US3293 - Move community to www.openshift.com
  (ccoleman@redhat.com)

* Fri Feb 08 2013 Adam Miller <admiller@redhat.com> - 1.1.1-2
- rebuilt

* Thu Nov 08 2012 Adam Miller <admiller@redhat.com> 1.1.1-1
- Bumping specs to at least 1.1 (dmcphers@redhat.com)

* Tue Oct 30 2012 Adam Miller <admiller@redhat.com> 1.0.1-1
- bumping specs to at least 1.0.0 (dmcphers@redhat.com)

* Wed Jul 11 2012 Adam Miller <admiller@redhat.com> 0.12.1-1
- bump_minor_versions for sprint 15 (admiller@redhat.com)

* Sat Jun 23 2012 Dan McPherson <dmcphers@redhat.com> 0.11.3-1
- 

* Sat Jun 23 2012 Dan McPherson <dmcphers@redhat.com> 0.11.2-1
- new package built with tito

* Thu May 10 2012 Adam Miller <admiller@redhat.com> 0.11.1-1
- fix up spec versions (dmcphers@redhat.com)
- bumping spec versions (admiller@redhat.com)

* Thu Apr 26 2012 Adam Miller <admiller@redhat.com> 1.3.1-1
- bumping spec versions (admiller@redhat.com)

* Wed Apr 18 2012 Dan McPherson <dmcphers@redhat.com> 1.2.5-1
- Touch all drupal modules to ensure a build. (ccoleman@redhat.com)

* Mon Apr 16 2012 Anderson Silva <ansilva@redhat.com> 1.2.4-1
- drupal6-openshift-custom_forms: fix typo Source0 (ansilva@redhat.com)

* Mon Apr 16 2012 Anderson Silva <ansilva@redhat.com> 1.2.3-1
- drupal6-openshift-custom_forms: fix Source0 for tito (ansilva@redhat.com)

* Mon Apr 16 2012 Anderson Silva <ansilva@redhat.com> 1.2.2-1
- drupal6-openshift-custom_forms: fix %%prep for tito release
  (ansilva@redhat.com)
- drupal: changing layout of source code for proper tito rpm
  (ansilva@redhat.com)
- update version to 1.2.1 (ansilva@redhat.com)

* Mon Apr 16 2012 Anderson Silva <ansilva@redhat.com> 1.2.1-1
- update version 

* Mon Apr 16 2012 Dan McPherson <dmcphers@redhat.com> 1.2-1
- new package built with tito

* Mon Mar 5 2012 Anderson Silva <ansilva@redhat.com> - 1.0-1
- Initial rpm package
