%global drupal_release      6
%global drupal_base         %{_datadir}/drupal%{drupal_release}
%global drupal_sites_all    %{drupal_base}/sites/all        
%global drupal_modules      %{drupal_sites_all}/modules/features
%global modname             community_wiki

Name:    drupal%{drupal_release}-openshift-features-%{modname}
Version: 1.6.1
Release: 3%{?dist}
Summary: Openshift Red Hat Community Wiki Feature for Drupal6
Group:   Applications/Publishing
License: GPLv2+
Source0: %{name}-%{version}.tar.gz
BuildArch: noarch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires:  drupal6, drupal6-features, drupal6-views, drupal6-votingapi, drupal6-imagefield

%description
Openshift Red Hat Community Wiki Feature for Drupal6


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
* Wed Jun 05 2013 Adam Miller 1.6.1-3
- Bump spec for mass drupal rebuild

* Mon Jun 03 2013 Adam Miller 1.6.1-2
- Bump spec for mass drupal rebuild

* Wed May 08 2013 Adam Miller <admiller@redhat.com> 1.6.1-1
- bump_minor_versions for sprint 28 (admiller@redhat.com)

* Thu Apr 25 2013 Adam Miller <admiller@redhat.com> 1.5.2-1
- Update permissions, add content_author role, prepare for site IA changes
  (ccoleman@redhat.com)

* Thu Mar 07 2013 Adam Miller <admiller@redhat.com> 1.5.1-1
- bump_minor_versions for sprint 25 (admiller@redhat.com)

* Wed Mar 06 2013 Adam Miller 1.4.3-2
- Bump spec for mass drupal rebuild

* Fri Mar 01 2013 Adam Miller <admiller@redhat.com> 1.4.3-1
- Backport Drupal permission changes - allow bloggers to upload files
  (ccoleman@redhat.com)

* Mon Feb 18 2013 Adam Miller <admiller@redhat.com> 1.4.2-2
- Bump spec for mass drupal rebuild

* Fri Feb 08 2013 Adam Miller <admiller@redhat.com> 1.4.2-1
- bump Release: for all drupal packages for rebuild (admiller@redhat.com)

* Fri Feb 08 2013 Adam Miller <admiller@redhat.com> - 1.4.1-2
- rebuilt

* Thu Nov 01 2012 Adam Miller <admiller@redhat.com> 1.4.1-1
- bump_minor_versions for sprint 20 (admiller@redhat.com)

* Mon Oct 08 2012 Adam Miller <admiller@redhat.com> 1.3.2-1
- Backport permission changes from production to Drupal. (ccoleman@redhat.com)

* Wed Jul 11 2012 Adam Miller <admiller@redhat.com> 1.3.1-1
- bump_minor_versions for sprint 15 (admiller@redhat.com)

* Sat Jun 23 2012 Dan McPherson <dmcphers@redhat.com> 1.2.3-1
- 

* Sat Jun 23 2012 Dan McPherson <dmcphers@redhat.com> 1.2.2-1
- new package built with tito

* Thu May 10 2012 Adam Miller <admiller@redhat.com> 1.2.1-1
- bumping spec versions (admiller@redhat.com)

* Mon May 07 2012 Adam Miller <admiller@redhat.com> 1.1.2-1
- Fix all remaining reversion default issues with features
  (ccoleman@redhat.com)
- View revisions permission already exists in user_profile
  (ccoleman@redhat.com)

* Thu Apr 26 2012 Adam Miller <admiller@redhat.com> 1.1.1-1
- bumping spec versions (admiller@redhat.com)

* Sat Apr 21 2012 Dan McPherson <dmcphers@redhat.com> 1.0.4-1
- Added a few more details to the community_wiki drupal feature
  (ffranz@redhat.com)

* Wed Apr 18 2012 Dan McPherson <dmcphers@redhat.com> 1.0.3-1
- Touch all drupal modules to ensure a build. (ccoleman@redhat.com)

* Mon Apr 16 2012 Anderson Silva <ansilva@redhat.com> 1.0.2-1
- new package built with tito

* Mon Apr 16 2012 Anderson Silva <ansilva@redhat.com> - 1.0.1-1
- update version 

* Thu Apr 5 2012 Clayton Coleman <ccoleman@redhat.com> - 1.0-1
- Initial rpm package
