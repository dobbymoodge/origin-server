%global drupal_release      6
%global drupal_base         %{_datadir}/drupal%{drupal_release}
%global drupal_sites_all    %{drupal_base}/sites/all        
%global drupal_modules      %{drupal_sites_all}/modules/features
%global modname             reporting_csv_views

Name:    drupal%{drupal_release}-openshift-features-%{modname}
Version: 1.5.1
Release: 5%{?dist}
Summary: Openshift Red Hat Custom Reporting CSV Views Feature for Drupal6
Group:   Applications/Publishing
License: GPLv2+
Source0: %{name}-%{version}.tar.gz
BuildArch: noarch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires:  drupal6, drupal6-votingapi, drupal6-og

%description
Openshift Red Hat Custom Reporting CSV Views Feature for Drupal6


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
* Fri Jun 07 2013 Adam Miller 1.5.1-5
- Bump spec for mass drupal rebuild

* Thu Jun 06 2013 Adam Miller 1.5.1-4
- Bump spec for mass drupal rebuild

* Wed Jun 05 2013 Adam Miller 1.5.1-3
- Bump spec for mass drupal rebuild

* Mon Jun 03 2013 Adam Miller 1.5.1-2
- Bump spec for mass drupal rebuild

* Thu Mar 07 2013 Adam Miller <admiller@redhat.com> 1.5.1-1
- bump_minor_versions for sprint 25 (admiller@redhat.com)

* Wed Mar 06 2013 Adam Miller 1.4.2-3
- Bump spec for mass drupal rebuild

* Mon Feb 18 2013 Adam Miller <admiller@redhat.com> 1.4.2-2
- Bump spec for mass drupal rebuild

* Fri Feb 08 2013 Adam Miller <admiller@redhat.com> 1.4.2-1
- bump Release: for all drupal packages for rebuild (admiller@redhat.com)

* Fri Feb 08 2013 Adam Miller <admiller@redhat.com> - 1.4.1-2
- rebuilt

* Wed Dec 12 2012 Adam Miller <admiller@redhat.com> 1.4.1-1
- bump_minor_versions for sprint 22 (admiller@redhat.com)

* Tue Dec 04 2012 Adam Miller <admiller@redhat.com> 1.3.3-1
- Update moderator permissions to include statistics and reports for shawn,
  user admin for sumana (ccoleman@redhat.com)

* Tue Dec 04 2012 Adam Miller <admiller@redhat.com>
- Update moderator permissions to include statistics and reports for shawn,
  user admin for sumana (ccoleman@redhat.com)

* Wed Aug 22 2012 Adam Miller <admiller@redhat.com> 1.3.1-1
- bump_minor_versions for sprint 17 (admiller@redhat.com)

* Sun Aug 05 2012 Dan McPherson <dmcphers@redhat.com> 1.2.2-1
- 

* Thu May 10 2012 Adam Miller <admiller@redhat.com> 1.2.1-1
- bumping spec versions (admiller@redhat.com)

* Mon May 07 2012 Adam Miller <admiller@redhat.com> 1.1.2-1
- Remaining drupal backport changes (ccoleman@redhat.com)

* Thu Apr 26 2012 Adam Miller <admiller@redhat.com> 1.1.1-1
- bumping spec versions (admiller@redhat.com)

* Sat Apr 21 2012 Dan McPherson <dmcphers@redhat.com> 1.0.4-1
- Merge commits dd5326df1f0d5bf05d51aeaae0cc4c457ba45816..ab1d91739634c80b3a9db
  5f468e5ceb277824c7d. Did not merge all of the changes made to core code -
  those are upstream and we can't integrate those directly.
  (ccoleman@redhat.com)

* Wed Apr 18 2012 Dan McPherson <dmcphers@redhat.com> 1.0.3-1
- Touch all drupal modules to ensure a build. (ccoleman@redhat.com)

* Mon Apr 16 2012 Anderson Silva <ansilva@redhat.com> 1.0.2-1
- new package built with tito

* Mon Apr 16 2012 Anderson Silva <ansilva@redhat.com> - 1.0.1-1
- update version

* Mon Mar 5 2012 Anderson Silva <ansilva@redhat.com> - 1.0-1
- Initial rpm package
