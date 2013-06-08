%global drupal_release      6
%global drupal_base         %{_datadir}/drupal%{drupal_release}
%global drupal_sites_all    %{drupal_base}/sites/all        
%global drupal_modules      %{drupal_sites_all}/modules/features
%global modname             application_quickstarts

Name:    drupal%{drupal_release}-openshift-features-%{modname}
Version: 1.6.2
Release: 1%{?dist}
Summary: Openshift Application Quickstarts Feature for Drupal6
Group:   Applications/Publishing
License: GPLv2+
Source0: %{name}-%{version}.tar.gz
BuildArch: noarch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires:  drupal6, drupal6-features, drupal6-views, drupal6-votingapi, drupal6-views_datasource

%description
Openshift Application Quickstarts Feature for Drupal6.  Provides a
content type for creating and managing precanned application
definitions.


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

* Thu Apr 25 2013 Adam Miller <admiller@redhat.com> 1.6.1-1
- bump_minor_versions for sprint XX (tdawson@redhat.com)

* Thu Apr 11 2013 Adam Miller <admiller@redhat.com> 1.5.2-1
- Add imagecache presets to application quickstarts (ccoleman@redhat.com)
- Update quickstarts with correct icon sizes, fix typos and spelling errors.
  (ccoleman@redhat.com)

* Thu Mar 28 2013 Adam Miller <admiller@redhat.com> 1.5.1-1
- bump_minor_versions for sprint 26 (admiller@redhat.com)

* Mon Mar 25 2013 Adam Miller <admiller@redhat.com> 1.4.3-1
- Remove deep partials, expose trust provider from quickstart api
  (ccoleman@redhat.com)

* Fri Mar 22 2013 Adam Miller <admiller@redhat.com> 1.4.2-1
- Final tweaks, last round of items (ccoleman@redhat.com)
- Switch to div based layout, lock taxonomies.  Follow Rob's changes to views
  and remove excess output. (ccoleman@redhat.com)
- US3113:  presentational tweaks to quickstarts lists (rhamilto@redhat.com)
- Display partners on quickstarts page. (ccoleman@redhat.com)
- Add quickstart features, simplify markup for blogs and quickstarts to be
  consistent (ccoleman@redhat.com)
- Add trust rating, export permissions for quickstart fields
  (ccoleman@redhat.com)
- Implement a quickstart content view with popular and recent results
  (ccoleman@redhat.com)

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

* Wed Jan 23 2013 Adam Miller <admiller@redhat.com> 1.3.1-1
- bump_minor_versions for sprint 23 (admiller@redhat.com)

* Thu Jan 10 2013 Adam Miller <admiller@redhat.com> 1.2.2-1
- Bug 888699 - initial_git_url not in views after type change
  (ccoleman@redhat.com)

* Wed Dec 12 2012 Adam Miller <admiller@redhat.com> 1.2.1-1
- bump_minor_versions for sprint 22 (admiller@redhat.com)

* Fri Dec 07 2012 Adam Miller <admiller@redhat.com> 1.1.3-1
- Sitemap and updates to application quickstarts (ccoleman@redhat.com)

* Wed Dec 05 2012 Adam Miller <admiller@redhat.com> 1.1.2-1
- Bug 882784 - Unable to search quickstart (ccoleman@redhat.com)

* Sat Nov 17 2012 Adam Miller <admiller@redhat.com> 1.1.1-1
- bump_minor_versions for sprint 21 (admiller@redhat.com)

* Fri Nov 16 2012 Adam Miller <admiller@redhat.com> 1.0.2-1
- Bug 877222 - Help example for quickstarts is wrong and confusing
  (ccoleman@redhat.com)

* Tue Nov 13 2012 Clayton Coleman <ccoleman@redhat.com> 1.0.1-1
- new package built with tito

