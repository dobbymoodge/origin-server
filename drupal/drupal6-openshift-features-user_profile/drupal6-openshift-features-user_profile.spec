%global drupal_release      6
%global drupal_base         %{_datadir}/drupal%{drupal_release}
%global drupal_sites_all    %{drupal_base}/sites/all        
%global drupal_modules      %{drupal_sites_all}/modules/features
%global modname             user_profile

Name:    drupal%{drupal_release}-openshift-features-%{modname}
Version: 1.14.4
Release: 1%{?dist}
Summary: Openshift Red Hat Custom User Profile Feature for Drupal6
Group:   Applications/Publishing
License: GPLv2+
Source0: %{name}-%{version}.tar.gz
BuildArch: noarch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires:  drupal6, drupal6-votingapi, drupal6-rules, drupal6-flag, drupal6-og, drupal6-token, drupal6-userpoints, drupal6-views, drupal6-faq, drupal6-fivestar, drupal6-admin_menu, drupal6-advanced-help, drupal6-better_formats, drupal6-context, drupal6-devel, drupal6-homebox, drupal6-stringoverrides, drupal6-userpoints, drupal6-eazylaunch, drupal6-custom_breadcrumbs, drupal6-views_datasource

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
* Fri Jun 28 2013 Adam Miller <admiller@redhat.com> 1.14.4-1
- Drupal feature export from prod server (jforrest@redhat.com)

* Mon Jun 17 2013 Adam Miller <admiller@redhat.com> 1.14.3-1
- Merge pull request #1578 from smarterclayton/textarea_fonts
  (dmcphers+openshiftbot@redhat.com)
- Merge pull request #1606 from jwforres/partner_logo_click_target
  (dmcphers+openshiftbot@redhat.com)
- Fix the click target of the partner logos to match hover target
  (jforrest@redhat.com)
- Strip 'devel' as a required module (ccoleman@redhat.com)

* Mon Jun 17 2013 Adam Miller <admiller@redhat.com>
- Merge pull request #1578 from smarterclayton/textarea_fonts
  (dmcphers+openshiftbot@redhat.com)
- Merge pull request #1606 from jwforres/partner_logo_click_target
  (dmcphers+openshiftbot@redhat.com)
- Fix the click target of the partner logos to match hover target
  (jforrest@redhat.com)
- Strip 'devel' as a required module (ccoleman@redhat.com)

* Fri Jun 07 2013 Adam Miller 1.14.1-5
- Bump spec for mass drupal rebuild

* Thu Jun 06 2013 Adam Miller 1.14.1-4
- Bump spec for mass drupal rebuild

* Wed Jun 05 2013 Adam Miller 1.14.1-3
- Bump spec for mass drupal rebuild

* Mon Jun 03 2013 Adam Miller 1.14.1-2
- Bump spec for mass drupal rebuild

* Wed May 08 2013 Adam Miller <admiller@redhat.com> 1.14.1-1
- bump_minor_versions for sprint 28 (admiller@redhat.com)

* Wed May 08 2013 Adam Miller <admiller@redhat.com> 1.13.3-1
- Fix a typo in lists view and add a moderator permission (ccoleman@redhat.com)

* Wed May 01 2013 Adam Miller <admiller@redhat.com> 1.13.2-1
- Partner sort criteria. (jharris@redhat.com)

* Thu Apr 25 2013 Adam Miller <admiller@redhat.com> 1.13.1-1
- Update permissions, add content_author role, prepare for site IA changes
  (ccoleman@redhat.com)
- bump_minor_versions for sprint XX (tdawson@redhat.com)

* Thu Apr 11 2013 Adam Miller <admiller@redhat.com> 1.12.2-1
- Bug 912027 - Change string references to 'Active Contributor'
  (ccoleman@redhat.com)

* Thu Mar 28 2013 Adam Miller <admiller@redhat.com> 1.12.1-1
- bump_minor_versions for sprint 26 (admiller@redhat.com)

* Mon Mar 25 2013 Adam Miller <admiller@redhat.com> 1.11.3-1
- Merge pull request #1053 from jtharris/features/Card226
  (dmcphers+openshiftbot@redhat.com)
- Dynamic partner view. (jharris@redhat.com)

* Fri Mar 22 2013 Adam Miller <admiller@redhat.com> 1.11.2-1
- Add left navigation for quickstart tags (ccoleman@redhat.com)
- Add quickstart features, simplify markup for blogs and quickstarts to be
  consistent (ccoleman@redhat.com)
- Add trust rating, export permissions for quickstart fields
  (ccoleman@redhat.com)
- Implement a quickstart content view with popular and recent results
  (ccoleman@redhat.com)

* Thu Mar 07 2013 Adam Miller <admiller@redhat.com> 1.11.1-1
- bump_minor_versions for sprint 25 (admiller@redhat.com)

* Wed Mar 06 2013 Adam Miller 1.10.4-2
- Bump spec for mass drupal rebuild

* Fri Mar 01 2013 Adam Miller <admiller@redhat.com> 1.10.4-1
- Backport Drupal permission changes - allow bloggers to upload files
  (ccoleman@redhat.com)

* Mon Feb 25 2013 Adam Miller <admiller@redhat.com> 1.10.3-1
- Bug 909992 - Fix login errors outside of login (ccoleman@redhat.com)

* Mon Feb 18 2013 Adam Miller <admiller@redhat.com> 1.10.2-2
- Bump spec for mass drupal rebuild

* Fri Feb 08 2013 Adam Miller <admiller@redhat.com> 1.10.2-1
- bump Release: for all drupal packages for rebuild (admiller@redhat.com)
- US3291 US3292 US3293 - Move community to www.openshift.com
  (ccoleman@redhat.com)

* Fri Feb 08 2013 Adam Miller <admiller@redhat.com> - 1.10.1-2
- rebuilt

* Wed Jan 23 2013 Adam Miller <admiller@redhat.com> 1.10.1-1
- bump_minor_versions for sprint 23 (admiller@redhat.com)

* Thu Jan 10 2013 Adam Miller <admiller@redhat.com> 1.9.2-1
- Add permissions for xmlsitemap to user profile feature (ccoleman@redhat.com)
- Permissions on KB items aren't available for users with admin role but not
  moderator role. (ccoleman@redhat.com)

* Wed Dec 12 2012 Adam Miller <admiller@redhat.com> 1.9.1-1
- bump_minor_versions for sprint 22 (admiller@redhat.com)

* Fri Dec 07 2012 Adam Miller <admiller@redhat.com> 1.8.4-1
- Sitemap and updates to application quickstarts (ccoleman@redhat.com)

* Wed Dec 05 2012 Adam Miller <admiller@redhat.com> 1.8.3-1
- Bug 882784 - Unable to search quickstart (ccoleman@redhat.com)

* Thu Nov 29 2012 Adam Miller <admiller@redhat.com> 1.8.2-1
- Permissions for event moderation (ccoleman@redhat.com)
- Update moderator permissions to include statistics and reports for shawn,
  user admin for sumana (ccoleman@redhat.com)
- Permissions recently applied to prod (ccoleman@redhat.com)

* Sat Nov 17 2012 Adam Miller <admiller@redhat.com> 1.8.1-1
- bump_minor_versions for sprint 21 (admiller@redhat.com)

* Fri Nov 16 2012 Adam Miller <admiller@redhat.com> 1.7.3-1
- Bug 876726 - Be more consistent about user profiles (ccoleman@redhat.com)

* Tue Nov 13 2012 Adam Miller <admiller@redhat.com> 1.7.2-1
- Summary should be visible (ccoleman@redhat.com)
- Bug 872912 - Prevent HTML in about user box (ccoleman@redhat.com)

* Thu Nov 01 2012 Adam Miller <admiller@redhat.com> 1.7.1-1
- bump_minor_versions for sprint 20 (admiller@redhat.com)

* Mon Oct 08 2012 Adam Miller <admiller@redhat.com> 1.6.4-1
- Backport permission changes from production to Drupal. (ccoleman@redhat.com)

* Wed Oct 03 2012 Adam Miller <admiller@redhat.com> 1.6.3-1
- Add taxonomy support for blogs and a json export for the most recent release
  (ccoleman@redhat.com)

* Wed Sep 26 2012 Adam Miller <admiller@redhat.com> 1.6.2-1
- Arrange content so that the same markup can be shown in the site and console
  (ccoleman@redhat.com)

* Wed Aug 22 2012 Adam Miller <admiller@redhat.com> 1.6.1-1
- bump_minor_versions for sprint 17 (admiller@redhat.com)

* Tue Aug 21 2012 Adam Miller <admiller@redhat.com> 1.5.5-1
- Permissions for the following items needed to be updated and exported: - Blog
  author photo - View/edit search metadata keywords (ccoleman@redhat.com)

* Mon Aug 20 2012 Adam Miller <admiller@redhat.com> 1.5.4-1
- Bug 814844 - Ensure that Tudou videos always show up by splitting out the
  second page and make it always browsable (and cacheable).
  (ccoleman@redhat.com)

* Tue Aug 14 2012 Adam Miller <admiller@redhat.com> 1.5.3-1
- Make sure individual videos have the left nav.  Add SEO to pages.
  (ccoleman@redhat.com)

* Thu Aug 09 2012 Adam Miller <admiller@redhat.com> 1.5.2-1
- Move remaining openshift content in drupal (ccoleman@redhat.com)
- Add messaging blocks to community (ccoleman@redhat.com)

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

* Thu May 17 2012 Adam Miller <admiller@redhat.com> 1.2.2-1
- Add a much improved ideas view and sub pages (ccoleman@redhat.com)

* Thu May 10 2012 Adam Miller <admiller@redhat.com> 1.2.1-1
- bumping spec versions (admiller@redhat.com)

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
