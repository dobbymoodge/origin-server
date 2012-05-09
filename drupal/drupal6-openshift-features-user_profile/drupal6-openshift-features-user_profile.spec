%global drupal_release      6
%global drupal_base         %{_datadir}/drupal%{drupal_release}
%global drupal_sites_all    %{drupal_base}/sites/all        
%global drupal_modules      %{drupal_sites_all}/modules/features
%global modname             user_profile

Name:    drupal%{drupal_release}-openshift-features-%{modname}
Version: 1.1.3
Release: 1%{?dist}
Summary: Openshift Red Hat Custom User Profile Feature for Drupal6
Group:   Applications/Publishing
License: GPLv2+
Source0: %{name}-%{version}.tar.gz
BuildArch: noarch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires:  drupal6, drupal6-votingapi, drupal6-rules, drupal6-flag, drupal6-og, drupal6-token, drupal6-userpoints, drupal6-views, drupal6-faq, drupal6-fivestar, drupal6-admin_menu, drupal6-advanced-help, drupal6-better_formats, drupal6-context, drupal6-devel, drupal6-homebox, drupal6-stringoverrides, drupal6-userpoints, drupal6-eazylaunch, drupal6-custom_breadcrumbs

%description
Openshift Red Hat Custom User Profile Feature for Drupal6


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
* Wed May 09 2012 Adam Miller <admiller@redhat.com> 1.1.3-1
- Add a context for elements that should have the default left community menu
  (ccoleman@redhat.com)
- Bug 820098 - Allow authenticated users to upload documents, add some
  additional guidelines. (ccoleman@redhat.com)

* Mon May 07 2012 Adam Miller <admiller@redhat.com> 1.1.2-1
- Add content_permissions to user profile (ccoleman@redhat.com)
- Merge events recent changes and user profile into code. (ccoleman@redhat.com)
- Ensure search weight is lower (ccoleman@redhat.com)
- Fix all remaining reversion default issues with features
  (ccoleman@redhat.com)
- Remaining drupal backport changes (ccoleman@redhat.com)
- Unrequire eazylaunch (ccoleman@redhat.com)
- Add additional active scope for user (ccoleman@redhat.com)
- Add an ideas active context (ccoleman@redhat.com)
- Update some features from drupal (ccoleman@redhat.com)

* Thu Apr 26 2012 Adam Miller <admiller@redhat.com> 1.1.1-1
- bumping spec versions (admiller@redhat.com)
- Give wiki pages in the community the active menu item of community/open-
  source (ccoleman@redhat.com)

* Mon Apr 23 2012 Adam Miller <admiller@redhat.com> 1.0.6-1
- Reorder items in user_profile_box to work better with Steve's styling
  (ccoleman@redhat.com)

* Sat Apr 21 2012 Dan McPherson <dmcphers@redhat.com> 1.0.5-1
- Merge commits dd5326df1f0d5bf05d51aeaae0cc4c457ba45816..ab1d91739634c80b3a9db
  5f468e5ceb277824c7d. Did not merge all of the changes made to core code -
  those are upstream and we can't integrate those directly.
  (ccoleman@redhat.com)
- Drupal updates based on latest changes (ccoleman@redhat.com)
- Merge branch 'master' into dev/clayton/console-branding (ccoleman@redhat.com)
- Update with more recent feature behaviors (ccoleman@redhat.com)

* Wed Apr 18 2012 Anderson Silva <ansilva@redhat.com> 1.0.4-1
- drupal6-openshift-features-user_profile: Source0 and %%prep step issue
  (ansilva@redhat.com)

* Wed Apr 18 2012 Anderson Silva <ansilva@redhat.com> 1.0.3-1

* Wed Apr 18 2012 Dan McPherson <dmcphers@redhat.com> 1.0.2-1
- new package built with tito

* Mon Apr 16 2012 Anderson Silva <ansilva@redhat.com> - 1.0.1-1
- update version 

* Mon Mar 5 2012 Anderson Silva <ansilva@redhat.com> - 1.0-1
- Initial rpm package
