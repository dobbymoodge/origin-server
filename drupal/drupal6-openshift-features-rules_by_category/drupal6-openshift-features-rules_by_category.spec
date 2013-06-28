%global drupal_release      6
%global drupal_base         %{_datadir}/drupal%{drupal_release}
%global drupal_sites_all    %{drupal_base}/sites/all        
%global drupal_modules      %{drupal_sites_all}/modules/features
%global modname             rules_by_category

Name:    drupal%{drupal_release}-openshift-features-%{modname}
Version: 1.6.2
Release: 1%{?dist}
Summary: Openshift Red Hat Custom Rules by Category Feature for Drupal6
Group:   Applications/Publishing
License: GPLv2+
Source0: %{name}-%{version}.tar.gz
BuildArch: noarch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires:  drupal6, drupal6-votingapi, drupal6-rules, drupal6-flag, drupal6-og, drupal6-token, drupal6-userpoints

%description
Openshift Red Hat Custom Rules by Category Feature for Drupal6


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
* Fri Jun 28 2013 Adam Miller <admiller@redhat.com> 1.6.2-1
- Drupal feature export from prod server (jforrest@redhat.com)

* Fri Jun 07 2013 Adam Miller 1.6.1-5
- Bump spec for mass drupal rebuild

* Thu Jun 06 2013 Adam Miller 1.6.1-4
- Bump spec for mass drupal rebuild

* Wed Jun 05 2013 Adam Miller 1.6.1-3
- Bump spec for mass drupal rebuild

* Mon Jun 03 2013 Adam Miller 1.6.1-2
- Bump spec for mass drupal rebuild

* Thu Apr 25 2013 Adam Miller <admiller@redhat.com> 1.6.1-1
- bump_minor_versions for sprint XX (tdawson@redhat.com)

* Thu Apr 11 2013 Adam Miller <admiller@redhat.com> 1.5.2-1
- Bug 909055 - Rule was calling a missing bit of code, never copied over from
  original Acquia instance (ccoleman@redhat.com)
- Bug 912027 - Change string references to 'Active Contributor'
  (ccoleman@redhat.com)

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

* Sat Nov 17 2012 Adam Miller <admiller@redhat.com> 1.4.1-1
- bump_minor_versions for sprint 21 (admiller@redhat.com)

* Tue Nov 13 2012 Adam Miller <admiller@redhat.com> 1.3.2-1
- Bug 872912 - Prevent HTML in about user box (ccoleman@redhat.com)

* Wed Jul 11 2012 Adam Miller <admiller@redhat.com> 1.3.1-1
- bump_minor_versions for sprint 15 (admiller@redhat.com)

* Sat Jun 23 2012 Dan McPherson <dmcphers@redhat.com> 1.2.4-1
- 

* Sat Jun 23 2012 Dan McPherson <dmcphers@redhat.com> 1.2.3-1
- 

* Sat Jun 23 2012 Dan McPherson <dmcphers@redhat.com> 1.2.2-1
- new package built with tito

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
- Merge branch 'master' into dev/clayton/console-branding (ccoleman@redhat.com)
- Update with more recent feature behaviors (ccoleman@redhat.com)

* Wed Apr 18 2012 Dan McPherson <dmcphers@redhat.com> 1.0.3-1
- Touch all drupal modules to ensure a build. (ccoleman@redhat.com)

* Mon Apr 16 2012 Anderson Silva <ansilva@redhat.com> 1.0.2-1
- new package built with tito

* Mon Apr 16 2012 Anderson Silva <ansilva@redhat.com> - 1.0.1-1
- update version 

* Mon Mar 5 2012 Anderson Silva <ansilva@redhat.com> - 1.0-1
- Initial rpm package
