%global drupal_release      6
%global drupal_base         %{_datadir}/drupal%{drupal_release}
%global drupal_sites_all    %{drupal_base}/sites/all        
%global drupal_modules      %{drupal_sites_all}/modules/features
%global modname             forums

Name:    drupal%{drupal_release}-openshift-features-%{modname}
Version: 1.7.2
Release: 1%{?dist}
Summary: Openshift Red Hat Custom Forums Feature for Drupal6
Group:   Applications/Publishing
License: GPLv2+
Source0: %{name}-%{version}.tar.gz
BuildArch: noarch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires:  drupal6, drupal6-features, drupal6-views, drupal6-votingapi 

%description
Openshift Red Hat Custom Blog Feature for Drupal6


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
* Fri Jun 28 2013 Adam Miller <admiller@redhat.com>
- Drupal feature export from prod server (jforrest@redhat.com)

* Fri Jun 07 2013 Adam Miller 1.7.1-5
- Bump spec for mass drupal rebuild

* Thu Jun 06 2013 Adam Miller 1.7.1-4
- Bump spec for mass drupal rebuild

* Wed Jun 05 2013 Adam Miller 1.7.1-3
- Bump spec for mass drupal rebuild

* Mon Jun 03 2013 Adam Miller 1.7.1-2
- Bump spec for mass drupal rebuild

* Thu Mar 07 2013 Adam Miller <admiller@redhat.com> 1.7.1-1
- bump_minor_versions for sprint 25 (admiller@redhat.com)

* Wed Mar 06 2013 Adam Miller 1.6.3-2
- Bump spec for mass drupal rebuild

* Mon Mar 04 2013 Adam Miller <admiller@redhat.com> 1.6.3-1
- Drupal Forums Feature Bug 908456 Added Sort Criteria by desc to
  thread_by_popularity https://bugzilla.redhat.com/show_bug.cgi?id=908456
  (nickharveyonline@gmail.com)

* Mon Feb 18 2013 Adam Miller <admiller@redhat.com> 1.6.2-2
- Bump spec for mass drupal rebuild

* Fri Feb 08 2013 Adam Miller <admiller@redhat.com> 1.6.2-1
- bump Release: for all drupal packages for rebuild (admiller@redhat.com)

* Fri Feb 08 2013 Adam Miller <admiller@redhat.com> - 1.6.1-2
- rebuilt

* Thu Nov 01 2012 Adam Miller <admiller@redhat.com> 1.6.1-1
- bump_minor_versions for sprint 20 (admiller@redhat.com)

* Mon Oct 08 2012 Adam Miller <admiller@redhat.com> 1.5.2-1
- Backport permission changes from production to Drupal. (ccoleman@redhat.com)

* Wed Jul 11 2012 Adam Miller <admiller@redhat.com> 1.5.1-1
- bump_minor_versions for sprint 15 (admiller@redhat.com)

* Mon Jul 02 2012 Adam Miller <admiller@redhat.com> 1.4.3-1
- Remove caching on user_profile_box query so that users don't get clobbered,
  update permissions so everyone can advanced search, and remove forums ctools
  hook. (ccoleman@redhat.com)

* Sat Jun 23 2012 Dan McPherson <dmcphers@redhat.com> 1.4.2-1
- new package built with tito

* Wed Jun 20 2012 Adam Miller <admiller@redhat.com> 1.4.1-1
- bump_minor_versions for sprint 14 (admiller@redhat.com)

* Fri Jun 15 2012 Adam Miller <admiller@redhat.com> 1.3.3-1
- Remove old contexts (ccoleman@redhat.com)

* Thu Jun 14 2012 Adam Miller <admiller@redhat.com> 1.3.2-1
- Add caching to drupal views and blocks for better performance.  Remove
  unnecessary sections from UI (ccoleman@redhat.com)

* Fri Jun 01 2012 Adam Miller <admiller@redhat.com> 1.3.1-1
- bumping spec versions (admiller@redhat.com)

* Tue May 22 2012 Dan McPherson <dmcphers@redhat.com> 1.2.3-1
- Automatic commit of package [drupal6-openshift-features-forums] release
  [1.2.2-1]. (admiller@redhat.com)

* Thu May 10 2012 Adam Miller <admiller@redhat.com> 1.2.2-1
- 

* Thu May 10 2012 Adam Miller <admiller@redhat.com> 1.2.1-1
- bumping spec versions (admiller@redhat.com)

* Wed May 09 2012 Adam Miller <admiller@redhat.com> 1.1.3-1
- Add drupal css classes to two views (ccoleman@redhat.com)

* Mon May 07 2012 Adam Miller <admiller@redhat.com> 1.1.2-1
- Fix all remaining reversion default issues with features
  (ccoleman@redhat.com)
- Remaining drupal backport changes (ccoleman@redhat.com)
- Updated the recent threads view on community home (ffranz@redhat.com)

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
