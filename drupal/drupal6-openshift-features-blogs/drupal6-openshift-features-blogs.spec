%global drupal_release      6
%global drupal_base         %{_datadir}/drupal%{drupal_release}
%global drupal_sites_all    %{drupal_base}/sites/all        
%global drupal_modules      %{drupal_sites_all}/modules/features
%global modname             blogs

Name:    drupal%{drupal_release}-openshift-features-%{modname}
Version: 1.16.2
Release: 1%{?dist}
Summary: Openshift Red Hat Custom Blog Feature for Drupal6
Group:   Applications/Publishing
License: GPLv2+
Source0: %{name}-%{version}.tar.gz
BuildArch: noarch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires:  drupal6, drupal6-features, drupal6-views, drupal6-votingapi, drupal6-imagefield

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
* Fri Jun 07 2013 Adam Miller <admiller@redhat.com> 1.16.2-1
- Site summit changes, backported from bbe7f47f293c826be00ead46457377f475b810b7
  in master (ccoleman@redhat.com)

* Wed May 08 2013 Adam Miller <admiller@redhat.com> 1.16.1-1
- bump_minor_versions for sprint 28 (admiller@redhat.com)

* Wed May 08 2013 Adam Miller <admiller@redhat.com> 1.15.4-1
- Fix a typo in lists view and add a moderator permission (ccoleman@redhat.com)

* Mon May 06 2013 Adam Miller <admiller@redhat.com> 1.15.3-1
- Bug 956794 - adds timestamp info to blog posts (ffranz@redhat.com)
- Bug 956794 - adds timestamp info to blog posts (ffranz@redhat.com)

* Mon Apr 29 2013 Adam Miller <admiller@redhat.com> 1.15.2-1
- Support semantic views (ccoleman@redhat.com)
- Unformatted lists should write nothing (ccoleman@redhat.com)

* Thu Apr 25 2013 Adam Miller <admiller@redhat.com> 1.15.1-1
- bump_minor_versions for sprint XX (tdawson@redhat.com)

* Thu Apr 11 2013 Adam Miller <admiller@redhat.com> 1.14.2-1
- Limit the content the blogs feed can display for perf reasons
  (ccoleman@redhat.com)

* Thu Mar 28 2013 Adam Miller <admiller@redhat.com> 1.14.1-1
- bump_minor_versions for sprint 26 (admiller@redhat.com)

* Thu Mar 14 2013 Adam Miller <admiller@redhat.com> 1.13.2-1
- Doc edit link for docs team (ccoleman@redhat.com)

* Thu Mar 07 2013 Adam Miller <admiller@redhat.com> 1.13.1-1
- bump_minor_versions for sprint 25 (admiller@redhat.com)

* Wed Mar 06 2013 Adam Miller 1.12.2-3
- Bump spec for mass drupal rebuild

* Mon Feb 18 2013 Adam Miller <admiller@redhat.com> 1.12.2-2
- Bump spec for mass drupal rebuild

* Fri Feb 08 2013 Adam Miller <admiller@redhat.com> 1.12.2-1
- bump Release: for all drupal packages for rebuild (admiller@redhat.com)
- US3291 US3292 US3293 - Move community to www.openshift.com
  (ccoleman@redhat.com)

* Fri Feb 08 2013 Adam Miller <admiller@redhat.com> - 1.12.1-2
- rebuilt

* Thu Feb 07 2013 Adam Miller <admiller@redhat.com> 1.12.1-1
- bump_minor_versions for sprint 24 (admiller@redhat.com)

* Mon Feb 04 2013 Adam Miller <admiller@redhat.com> 1.11.3-1
- Bug 906879 - Fixed FAQ JSON API root object name (hripps@redhat.com)

* Thu Jan 31 2013 Adam Miller <admiller@redhat.com> 1.11.2-1
- US3318: Updated Blog feature to include FAQ API (hripps@redhat.com)

* Wed Jan 23 2013 Adam Miller <admiller@redhat.com> 1.11.1-1
- bump_minor_versions for sprint 23 (admiller@redhat.com)

* Thu Jan 10 2013 Adam Miller <admiller@redhat.com> 1.10.2-1
- Add event city, state, and start date to upcoming event json so it shows up
  on login page (ccoleman@redhat.com)

* Sat Nov 17 2012 Adam Miller <admiller@redhat.com> 1.10.1-1
- bump_minor_versions for sprint 21 (admiller@redhat.com)

* Thu Nov 15 2012 Adam Miller <admiller@redhat.com> 1.9.3-1
- Add blog content as well (overlap, view changes) (ccoleman@redhat.com)

* Tue Nov 13 2012 Adam Miller <admiller@redhat.com> 1.9.2-1
- Bug 872912 - Prevent HTML in about user box (ccoleman@redhat.com)

* Thu Nov 01 2012 Adam Miller <admiller@redhat.com> 1.9.1-1
- bump_minor_versions for sprint 20 (admiller@redhat.com)

* Mon Oct 08 2012 Adam Miller <admiller@redhat.com> 1.8.3-1
- Implement recent blogs and upcoming events views. (ccoleman@redhat.com)

* Wed Oct 03 2012 Adam Miller <admiller@redhat.com> 1.8.2-1
- Add taxonomy support for blogs and a json export for the most recent release
  (ccoleman@redhat.com)

* Wed Sep 12 2012 Adam Miller <admiller@redhat.com> 1.8.1-1
- bump_minor_versions for sprint 18 (admiller@redhat.com)

* Fri Sep 07 2012 Adam Miller <admiller@redhat.com> 1.7.2-1
- BZ 849782 - rss button rendering issue BZ 839242 - new app page for zend
  needed css added BZ 820086 - long sshkey name text-overflow issue Check in
  new account plan styleguide pages for billing, payment, review/confirm along
  with new form validation css Misc css - switch heading font-size to be based
  off of $baseFontSize computation - match <legend> style to heading.divide for
  consistency when used on console form pages - addition of <select> to
  standard form field rules (not sure why they aren't included in bootstrap by
  default) - set box-showdow(none) on .btn so there's no conflict when used on
  <input> - create aside rule within console/_core to be used on pages with for
  secondary column (help) - remove input grid system rules that caused
  conflicting widths with inputs set to grid span - add :focus to
  buttonBackground mixin - decrease spacing associated with .control-group -
  added rules for :focus:required:valid :focus:required:invalid to take
  advantage of client side browsers that support them - move rules for field
  feedback states from _custom to _forms - .alert a so link color is optimal on
  all alert states (sgoodwin@redhat.com)

* Wed Aug 22 2012 Adam Miller <admiller@redhat.com> 1.7.1-1
- bump_minor_versions for sprint 17 (admiller@redhat.com)

* Wed Aug 22 2012 Adam Miller <admiller@redhat.com> 1.6.3-1
- fix 849782, rss feed icon (sgoodwin@redhat.com)

* Mon Aug 20 2012 Adam Miller <admiller@redhat.com> 1.6.2-1
- Bug 814844 - Ensure that Tudou videos always show up by splitting out the
  second page and make it always browsable (and cacheable).
  (ccoleman@redhat.com)

* Thu Aug 02 2012 Adam Miller <admiller@redhat.com> 1.6.1-1
- bump_minor_versions for sprint 16 (admiller@redhat.com)

* Wed Aug 01 2012 Adam Miller <admiller@redhat.com> 1.5.2-1
- Bug 814844 - Ensure no caching is set for videos in code, fix pager
  (ccoleman@redhat.com)

* Wed Jul 11 2012 Adam Miller <admiller@redhat.com> 1.5.1-1
- bump_minor_versions for sprint 15 (admiller@redhat.com)

* Mon Jul 02 2012 Adam Miller <admiller@redhat.com> 1.4.3-1
- Bug 834725 - Remove blog RSS header from Recent Changes (ccoleman@redhat.com)

* Sat Jun 23 2012 Dan McPherson <dmcphers@redhat.com> 1.4.2-1
- new package built with tito

* Wed Jun 20 2012 Adam Miller <admiller@redhat.com> 1.4.1-1
- bump_minor_versions for sprint 14 (admiller@redhat.com)

* Thu Jun 14 2012 Adam Miller <admiller@redhat.com> 1.3.2-1
- Add caching to drupal views and blocks for better performance.  Remove
  unnecessary sections from UI (ccoleman@redhat.com)

* Fri Jun 01 2012 Adam Miller <admiller@redhat.com> 1.3.1-1
- bumping spec versions (admiller@redhat.com)

* Thu May 24 2012 Adam Miller <admiller@redhat.com> 1.2.4-1
- Bug 822391 - Remove author from full view of blogs (ccoleman@redhat.com)

* Tue May 22 2012 Dan McPherson <dmcphers@redhat.com> 1.2.3-1
- Automatic commit of package [drupal6-openshift-features-blogs] release
  [1.2.2-1]. (admiller@redhat.com)

* Thu May 10 2012 Adam Miller <admiller@redhat.com> 1.2.2-1
- 

* Thu May 10 2012 Adam Miller <admiller@redhat.com> 1.2.1-1
- bumping spec versions (admiller@redhat.com)

* Mon May 07 2012 Adam Miller <admiller@redhat.com> 1.1.3-1
- Fix all remaining reversion default issues with features
  (ccoleman@redhat.com)

* Thu Apr 26 2012 Adam Miller <admiller@redhat.com> 1.1.2-1
- Automatic commit of package [drupal6-openshift-features-blogs] release
  [1.1.1-1]. (admiller@redhat.com)

* Thu Apr 26 2012 Adam Miller <admiller@redhat.com> 1.1.1-1
- bumping spec versions (admiller@redhat.com)

* Tue Apr 24 2012 Adam Miller <admiller@redhat.com> 1.0.7-1
- Bug 814573 - Fix up lots of links to www.redhat.com/openshift/community
  (ccoleman@redhat.com)

* Mon Apr 23 2012 Adam Miller <admiller@redhat.com> 1.0.6-1
- Touch up blog theme prior to ship (ccoleman@redhat.com)

* Sat Apr 21 2012 Dan McPherson <dmcphers@redhat.com> 1.0.5-1
- Merge commits dd5326df1f0d5bf05d51aeaae0cc4c457ba45816..ab1d91739634c80b3a9db
  5f468e5ceb277824c7d. Did not merge all of the changes made to core code -
  those are upstream and we can't integrate those directly.
  (ccoleman@redhat.com)

* Wed Apr 18 2012 Dan McPherson <dmcphers@redhat.com> 1.0.4-1
- Touch all drupal modules to ensure a build. (ccoleman@redhat.com)

* Mon Apr 16 2012 Anderson Silva <ansilva@redhat.com> 1.0.3-1
- drupal6-openshift-features-blogs: fix Source0 (ansilva@redhat.com)

* Mon Apr 16 2012 Anderson Silva <ansilva@redhat.com> 1.0.2-1
- new package built with tito

* Mon Apr 16 2012 Anderson Silva <ansilva@redhat.com> - 1.0.1-1
- update version 

* Mon Mar 5 2012 Anderson Silva <ansilva@redhat.com> - 1.0-1
- Initial rpm package
