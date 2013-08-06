%global drupal_release      6
%global drupal_base         %{_datadir}/drupal%{drupal_release}
%global drupal_sites_all    %{drupal_base}/sites/all        
%global drupal_themedir     %{drupal_sites_all}/themes
%global drupal_themename    openshift-theme

Name:           drupal6-%{drupal_themename}
Version: 3.20.4
Release:        1%{?dist}
Summary:        Red Hat Openshift theme for Drupal %{drupal_release}

Group:          Applications/Publishing
License:        GPLv2+ and GPL+ or MIT
Source0:        %{name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
Requires:       drupal6

%description
Red Hat Openshift Drupal Theme

%prep
%setup -q
# Remove empty index.html and others
find -size 0 | xargs rm -f


%build


%install
rm -rf $RPM_BUILD_ROOT
%{__mkdir} -p $RPM_BUILD_ROOT/%{drupal_themedir}/%{drupal_themename} 
cp -pr . $RPM_BUILD_ROOT/%{drupal_themedir}/%{drupal_themename}


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%{drupal_themedir}/%{drupal_themename}


%changelog
* Tue Aug 06 2013 Adam Miller <admiller@redhat.com> 3.20.4-1
- Bug 990431 - community XSS vulnerability in page header (jforrest@redhat.com)

* Fri Jul 26 2013 Adam Miller <admiller@redhat.com> 3.20.3-1
- Merge pull request #1765 from
  jwforres/community_login_redirect_with_account_create
  (dmcphers+openshiftbot@redhat.com)
- Redirect back to forums/openshift after Log in to post a new thread
  (jforrest@redhat.com)
- Create account from drupal redirects back to drupal after email confirm
  (jforrest@redhat.com)

* Wed Jul 24 2013 Adam Miller <admiller@redhat.com> 3.20.2-1
- Change set: (sgoodwin@redhat.com)

* Fri Jul 12 2013 Adam Miller <admiller@redhat.com> 3.20.1-1
- bump_minor_versions for sprint 31 (admiller@redhat.com)

* Fri Jul 12 2013 Adam Miller <admiller@redhat.com> 3.19.2-1
- Addition fix for bug 980095 add descriptive text (sgoodwin@redhat.com)

* Tue Jun 25 2013 Adam Miller <admiller@redhat.com> 3.19.1-1
- bump_minor_versions for sprint 30 (admiller@redhat.com)

* Mon Jun 24 2013 Adam Miller <admiller@redhat.com> 3.18.6-1
- Merge pull request #1670 from sg00dwin/617dev
  (dmcphers+openshiftbot@redhat.com)
- condense markup (sgoodwin@redhat.com)
- revove non-used code (sgoodwin@redhat.com)
- Merge branch 'master' of github.com:openshift/li into 617dev
  (sgoodwin@redhat.com)
- CHANGE SET Updated favicon.ico with multiple sizes embedded, which IE can
  serve according to function -
  http://iconhandbook.co.uk/reference/chart/windows/ Addition of touch-icon-
  precomposed.png at 144x144 size which will be used by iOS and android phones
  and tablets Addition of meta data to create tile used by IE pinned sites -
  and associate 3 jump links (Reference)
  http://www.buildmypinnedsite.com/windows7/en New style added to force
  width:100%% for responsive video still image on Chrome (sgoodwin@redhat.com)

* Fri Jun 21 2013 Adam Miller <admiller@redhat.com> 3.18.5-1
- Fix call to get_variable to remove warnings (jliggitt@redhat.com)

* Wed Jun 19 2013 Adam Miller <admiller@redhat.com> 3.18.4-1
- Fix bug 975724 - don't output nav header unless there is nav content
  (jliggitt@redhat.com)
- Merge pull request #1649 from sg00dwin/617dev
  (dmcphers+openshiftbot@redhat.com)
- Merge branch 'master' of github.com:openshift/li into 617dev
  (sgoodwin@redhat.com)
- CHANGES Addition of print specific rules Correct incorrectly closed tag
  around social-sharing - required updated margin-bottom values on comments and
  thread Slightly muted stars on planets and stars graphics - updated
  positioning of stars.png (sgoodwin@redhat.com)

* Tue Jun 18 2013 Adam Miller <admiller@redhat.com> 3.18.3-1
- Bug 975365 - 404 on Deploy Now button on QuickStart (jforrest@redhat.com)

* Mon Jun 17 2013 Adam Miller <admiller@redhat.com> 3.18.2-1
- Merge pull request #1620 from smarterclayton/bug_972878_version_assets
  (dmcphers+openshiftbot@redhat.com)
- Bug 972878 - More effectively cache assets for the site and community.
  (ccoleman@redhat.com)
- Fix the url to the user guide (jliggitt@redhat.com)
- Merge pull request #1609 from
  smarterclayton/bug_972890_add_search_meta_and_block_to_show
  (dmcphers+openshiftbot@redhat.com)
- Bug 972890 - Allow homepage to have a meta description (site_mission) and
  inject content onto every page (ccoleman@redhat.com)
- Merge pull request #1578 from smarterclayton/textarea_fonts
  (dmcphers+openshiftbot@redhat.com)
- Bug 972241 - Bad google+ link (ccoleman@redhat.com)
- Strip 'devel' as a required module (ccoleman@redhat.com)

* Fri Jun 07 2013 Adam Miller 3.18.1-5
- Bump spec for mass drupal rebuild

* Thu Jun 06 2013 Adam Miller 3.18.1-4
- Bump spec for mass drupal rebuild

* Wed Jun 05 2013 Adam Miller 3.18.1-3
- Bump spec for mass drupal rebuild

* Mon Jun 03 2013 Adam Miller 3.18.1-2
- Bump spec for mass drupal rebuild

* Thu May 30 2013 Adam Miller <admiller@redhat.com> 3.18.1-1
- bump_minor_versions for sprint 29 (admiller@redhat.com)

* Thu May 30 2013 Adam Miller <admiller@redhat.com> 3.17.4-1
- Fixes Bug 968411 (ffranz@redhat.com)

* Tue May 21 2013 Troy Dawson <tdawson@redhat.com> 3.17.3-1
- 

* Thu May 16 2013 Adam Miller <admiller@redhat.com> 3.17.2-1
- Merge pull request #1340 from spurtell/spurtell/analytics
  (dmcphers+openshiftbot@redhat.com)
- Added Google AdWords remarketing script (spurtell@redhat.com)
- Remove old resources that should not be used, remove comment about secret
  key. (ccoleman@redhat.com)

* Wed May 08 2013 Adam Miller <admiller@redhat.com> 3.17.1-1
- bump_minor_versions for sprint 28 (admiller@redhat.com)

* Wed May 08 2013 Adam Miller <admiller@redhat.com> 3.16.5-1
- Merge pull request #1322 from fabianofranz/master
  (dmcphers+openshiftbot@redhat.com)
- Bug 959600 - fixes double slashes on share url (ffranz@redhat.com)
- Bug 959600 - fixes Twitter share button on forum posts (ffranz@redhat.com)

* Mon May 06 2013 Adam Miller <admiller@redhat.com> 3.16.4-1
- Bug 956794 - adds timestamp info to blog posts (ffranz@redhat.com)
- Bug 956794 - added timestamp to Forum threads (ffranz@redhat.com)

* Thu May 02 2013 Adam Miller <admiller@redhat.com> 3.16.3-1
- Added openshift_assets_url conf to allow loading assets from local site
  (jforrest@redhat.com)

* Mon Apr 29 2013 Adam Miller <admiller@redhat.com> 3.16.2-1
- Unformatted lists should write nothing (ccoleman@redhat.com)

* Thu Apr 25 2013 Adam Miller <admiller@redhat.com> 3.16.1-1
- Update permissions, add content_author role, prepare for site IA changes
  (ccoleman@redhat.com)
- bump_minor_versions for sprint XX (tdawson@redhat.com)

* Mon Apr 15 2013 Adam Miller <admiller@redhat.com> 3.15.4-1
- Bug 952077 - drupal_urlencode encodes poorly for real websites
  (ccoleman@redhat.com)

* Thu Apr 11 2013 Adam Miller <admiller@redhat.com> 3.15.3-1
- Minor tweaks to twitter (ccoleman@redhat.com)
- Final styling tweaks, allegedly fix facebook (ccoleman@redhat.com)
- Fix google and facebook links (ccoleman@redhat.com)
- Social sharing links, cleanup, styling fixes (ccoleman@redhat.com)
- Update quickstarts with correct icon sizes, fix typos and spelling errors.
  (ccoleman@redhat.com)

* Mon Apr 08 2013 Adam Miller <admiller@redhat.com> 3.15.2-1
- replace favicon.ico with new (sgoodwin@redhat.com)
- Bug 928970: fixes Forums heading (ffranz@redhat.com)
- Make forum login to post links buttons so they are recognizable/standout,
  since it's a key path to submitting questions. (sgoodwin@redhat.com)

* Thu Mar 28 2013 Adam Miller <admiller@redhat.com> 3.15.1-1
- bump_minor_versions for sprint 26 (admiller@redhat.com)

* Mon Mar 25 2013 Adam Miller <admiller@redhat.com> 3.14.4-1
- Eloqua integration,Omniture updates,AdWords Conversion Tracker Update
  (spurtell@redhat.com)

* Fri Mar 22 2013 Adam Miller <admiller@redhat.com> 3.14.3-1
- Final tweaks, last round of items (ccoleman@redhat.com)
- Switch to div based layout, lock taxonomies.  Follow Rob's changes to views
  and remove excess output. (ccoleman@redhat.com)
- US3113:  detabbing _community.scss, addressing .links.inline a { } bug, and
  first cut at styling of a quick start page (rhamilto@redhat.com)
- Add quickstart features, simplify markup for blogs and quickstarts to be
  consistent (ccoleman@redhat.com)
- Implement a quickstart content view with popular and recent results
  (ccoleman@redhat.com)

* Thu Mar 14 2013 Adam Miller <admiller@redhat.com> 3.14.2-1
- Merge pull request #983 from fabianofranz/master
  (dmcphers+openshiftbot@redhat.com)
- Merge remote-tracking branch 'upstream/master' (ffranz@redhat.com)
- Reverted the ajax XHR hack previously used to fix bug 876681 and bug 874645
  (was fixed on the latest verison of drupal) (ffranz@redhat.com)

* Thu Mar 07 2013 Adam Miller <admiller@redhat.com> 3.14.1-1
- bump_minor_versions for sprint 25 (admiller@redhat.com)

* Wed Mar 06 2013 Adam Miller 3.13.4-2
- Bump spec for mass drupal rebuild

* Tue Mar 05 2013 Adam Miller <admiller@redhat.com> 3.13.4-1
- Merge pull request #960 from smarterclayton/bug_916536_link_author_names
  (dmcphers@redhat.com)
- Bug 916536 - Link author names to their profile (ccoleman@redhat.com)
- Bug 916495 - Fix more broken relative URLs (ccoleman@redhat.com)

* Mon Feb 25 2013 Adam Miller <admiller@redhat.com> 3.13.3-1
- Bug 909992 - Fix login errors outside of login (ccoleman@redhat.com)
- Bug 912286 - Cleanup robots.txt and others for split (ccoleman@redhat.com)

* Mon Feb 18 2013 Adam Miller <admiller@redhat.com> 3.13.2-2
- Bump spec for mass drupal rebuild

* Fri Feb 08 2013 Adam Miller <admiller@redhat.com> 3.13.2-1
- bump Release: for all drupal packages for rebuild (admiller@redhat.com)
- US3291 US3292 US3293 - Move community to www.openshift.com
  (ccoleman@redhat.com)

* Fri Feb 08 2013 Adam Miller <admiller@redhat.com> - 3.13.1-2
- rebuilt

* Thu Feb 07 2013 Adam Miller <admiller@redhat.com> 3.13.1-1
- bump_minor_versions for sprint 24 (admiller@redhat.com)

* Mon Feb 04 2013 Adam Miller <admiller@redhat.com> 3.12.2-1
- Merge pull request #838 from sg00dwin/partnerslink
  (dmcphers+openshiftbot@redhat.com)
- add partners link in footer (sgoodwin@redhat.com)

* Wed Jan 23 2013 Adam Miller <admiller@redhat.com> 3.12.1-1
- bump_minor_versions for sprint 23 (admiller@redhat.com)

* Wed Jan 23 2013 Adam Miller <admiller@redhat.com> 3.11.2-1
- Bug 880854 - Fix community favicon in some browsers (ccoleman@redhat.com)

* Wed Dec 12 2012 Adam Miller <admiller@redhat.com> 3.11.1-1
- bump_minor_versions for sprint 22 (admiller@redhat.com)

* Thu Nov 29 2012 Adam Miller <admiller@redhat.com> 3.10.2-1
- US3055 - Enterprise content for stage (ccoleman@redhat.com)
- Merge pull request #653 from sg00dwin/master (ccoleman@redhat.com)
- images in correct dir, change to masthead-div (sgoodwin@redhat.com)
- Merge pull request #652 from sg00dwin/master (ccoleman@redhat.com)
- Addition of masthead for homepage, banner files, enterprise files, swap
  pricing and plans link for enterprise link (sgoodwin@redhat.com)
- Revert "BZ846514 fixed" - caused bug 869203 (ccoleman@redhat.com)

* Sat Nov 17 2012 Adam Miller <admiller@redhat.com> 3.10.1-1
- bump_minor_versions for sprint 21 (admiller@redhat.com)

* Fri Nov 16 2012 Adam Miller <admiller@redhat.com> 3.9.5-1
- Fixes BZ876681 and BZ874645 (ffranz@redhat.com)
- Merge pull request #626 from
  smarterclayton/bug_876726_cleanup_profile_attributes_consistently
  (openshift+bot@redhat.com)
- Bug 876726 - Be more consistent about user profiles (ccoleman@redhat.com)

* Thu Nov 15 2012 Adam Miller <admiller@redhat.com> 3.9.4-1
- Bug 873781 - Do not output extra info about the user in Drupal omniture
  (ccoleman@redhat.com)

* Wed Nov 14 2012 Adam Miller <admiller@redhat.com> 3.9.3-1
- Merge pull request #602 from sg00dwin/master (openshift+bot@redhat.com)
- newsletter link change (sgoodwin@redhat.com)

* Tue Nov 13 2012 Adam Miller <admiller@redhat.com> 3.9.2-1
- Styled the events list by country, sync date and country views, ical feed
  improvements (ffranz@redhat.com)
- Improved styling for events list (ffranz@redhat.com)
- Added more data to the iCal feed, added iCal link, improved tabs styling in
  the events list page (ffranz@redhat.com)
- Events RSS feed (ffranz@redhat.com)
- Improved Events page with better styles, logo upload, venue info, etc
  (ffranz@redhat.com)
- New Events section styles, added event detail page (ffranz@redhat.com)

* Thu Nov 01 2012 Adam Miller <admiller@redhat.com> 3.9.1-1
- bump_minor_versions for sprint 20 (admiller@redhat.com)

* Mon Oct 22 2012 Adam Miller <admiller@redhat.com> 3.8.4-1
- Fixes BZ 856733 (ffranz@redhat.com)

* Thu Oct 04 2012 Adam Miller <admiller@redhat.com> 3.8.3-1
- Bug 862362 Move remaining js to assets to avoid errors and simplify links
  (ccoleman@redhat.com)

* Fri Sep 28 2012 Adam Miller <admiller@redhat.com> 3.8.2-1
- Bug 860892 - No CSS or JS in drupal, need to update theme to point to new
  directories (ccoleman@redhat.com)

* Wed Sep 12 2012 Adam Miller <admiller@redhat.com> 3.8.1-1
- bump_minor_versions for sprint 18 (admiller@redhat.com)

* Wed Sep 12 2012 Adam Miller <admiller@redhat.com> 3.7.4-1
- bug fixes - 835843, 828111 (sgoodwin@redhat.com)

* Thu Sep 06 2012 Adam Miller <admiller@redhat.com> 3.7.3-1
- removed empty meta description tag from Drupal template (spurtell@redhat.com)

* Thu Aug 30 2012 Adam Miller <admiller@redhat.com> 3.7.2-1
- Add thread timeout safety to the async_aware gem method, and a test.  This
  fixes intermittent test failures with account dashboard (5s join timeout
  before).  Default timeout is now 15s. Also fix cases with parallel test
  cleanup (domain is stomping on other domains). (ccoleman@redhat.com)

* Wed Aug 22 2012 Adam Miller <admiller@redhat.com> 3.7.1-1
- bump_minor_versions for sprint 17 (admiller@redhat.com)

* Mon Aug 20 2012 Adam Miller <admiller@redhat.com> 3.6.5-1
- Merge pull request #251 from smarterclayton/header_and_footer_updates
  (openshift+bot@redhat.com)
- Tests were looking for old link name.  Moved newsletter into footer.
  (ccoleman@redhat.com)
- Update header and footer to fix doc links, and begin simplification of the
  header. (ccoleman@redhat.com)

* Fri Aug 17 2012 Adam Miller <admiller@redhat.com> 3.6.4-1
- US2592 and US2583 (ffranz@redhat.com)
- BZ846514 fixed (ffranz@redhat.com)

* Tue Aug 14 2012 Adam Miller <admiller@redhat.com> 3.6.3-1
- Make sure individual videos have the left nav.  Add SEO to pages.
  (ccoleman@redhat.com)
- Merge pull request #211 from fabianofranz/master (openshift+bot@redhat.com)
- US2583: changed footer links and added redirects for the Legal content
  (ffranz@redhat.com)

* Thu Aug 09 2012 Adam Miller <admiller@redhat.com> 3.6.2-1
- Move remaining openshift content in drupal (ccoleman@redhat.com)
- Add a new $messaging region (ccoleman@redhat.com)

* Thu Aug 02 2012 Adam Miller <admiller@redhat.com> 3.6.1-1
- bump_minor_versions for sprint 16 (admiller@redhat.com)

* Tue Jul 31 2012 Adam Miller <admiller@redhat.com> 3.5.2-1
- add custom forum only search; minor work of breadcrumb partials and spacing,
  headings at <480px get small line-height (sgoodwin@redhat.com)

* Wed Jul 11 2012 Adam Miller <admiller@redhat.com> 3.5.1-1
- bump_minor_versions for sprint 15 (admiller@redhat.com)

* Tue Jul 10 2012 Adam Miller <admiller@redhat.com> 3.4.4-1
- Updated links to pricing page to point to full url (contact@fabianofranz.com)
- Links to pricing page all over the website, related to BZ 837902
  (contact@fabianofranz.com)

* Mon Jul 09 2012 Dan McPherson <dmcphers@redhat.com> 3.4.3-1
- At Legal's request, change the footer link for 'Terms of Service' to point to
  the preview services agreement. (ccoleman@redhat.com)

* Sat Jun 23 2012 Dan McPherson <dmcphers@redhat.com> 3.4.2-1
- new package built with tito

* Wed Jun 20 2012 Adam Miller <admiller@redhat.com> 3.4.1-1
- bump_minor_versions for sprint 14 (admiller@redhat.com)

* Mon Jun 18 2012 Adam Miller <admiller@redhat.com> 3.3.6-1
- 

* Mon Jun 18 2012 Adam Miller <admiller@redhat.com> 3.3.5-1
- 

* Mon Jun 18 2012 Adam Miller <admiller@redhat.com> 3.3.4-1
- Bug 820861 - Remove broken button from ideas page. (ccoleman@redhat.com)
- Bug 807570 - Improve visual display of Youku videos (ccoleman@redhat.com)

* Thu Jun 14 2012 Adam Miller <admiller@redhat.com> 3.3.3-1
- Add caching to drupal views and blocks for better performance.  Remove
  unnecessary sections from UI (ccoleman@redhat.com)

* Tue Jun 12 2012 Adam Miller <admiller@redhat.com> 3.3.2-1
- incorporate search field within header of site pages, reset headings to use
  line-height instead of margin-bottom, reset /stylesheets/_type.scss to
  bootstrap/_type.scss and merge customizations within so that we only use
  single _type file, minor tinkerings and condensing of styles
  (sgoodwin@redhat.com)
- modifications to search in header within drupal pages (sgoodwin@redhat.com)
- Initial incorporation of search within ui header (sgoodwin@redhat.com)

* Fri Jun 01 2012 Adam Miller <admiller@redhat.com> 3.3.1-1
- bumping spec versions (admiller@redhat.com)

* Fri May 25 2012 Adam Miller <admiller@redhat.com> 3.2.3-1
- Remove comment title permanently (ccoleman@redhat.com)
- css/markup to enable responsive nav for mobile views and lots of fine tuning
  of ui components in both site and console (sgoodwin@redhat.com)

* Thu May 17 2012 Adam Miller <admiller@redhat.com> 3.2.2-1
- community search field fix for ipad/chrome width issue (sgoodwin@redhat.com)

* Thu May 10 2012 Adam Miller <admiller@redhat.com> 3.2.1-1
- bumping spec versions (admiller@redhat.com)

* Wed May 09 2012 Adam Miller <admiller@redhat.com> 3.1.5-1
- Make forum thread list much simpler (ccoleman@redhat.com)
- Remove extra title attributes from user profile (ccoleman@redhat.com)
- Use article element on blog posts (ccoleman@redhat.com)
- Remove all titles from comments, including those that have escaped HTML
  entities (ccoleman@redhat.com)
- Avoid a warning message on template.php for altering comment form.
  (ccoleman@redhat.com)

* Tue May 08 2012 Adam Miller <admiller@redhat.com> 3.1.4-1
-  minor updates to the visual presentation of the forums threat list and blog
  details views (sgoodwin@redhat.com)

* Mon May 07 2012 Adam Miller <admiller@redhat.com> 3.1.3-1
- Add tracking.js to community (ccoleman@redhat.com)

* Mon May 07 2012 Adam Miller <admiller@redhat.com> 3.1.2-1
- Add more compact row layout (separators with , will collapse whitespace)
  Update events module to export a new format. (ccoleman@redhat.com)
- Hide comment title if it exists in the comment body (ccoleman@redhat.com)
- Updated requirements from legal regarding removal of opensource disclaimer
  page and changes to language on download page. (ccoleman@redhat.com)

* Thu Apr 26 2012 Adam Miller <admiller@redhat.com> 3.1.1-1
- bumping spec versions (admiller@redhat.com)

* Wed Apr 25 2012 Adam Miller <admiller@redhat.com> 3.0.11-1
- Automatic commit of package [drupal6-openshift-theme] release [3.0.10-1].
  (admiller@redhat.com)

* Wed Apr 25 2012 Adam Miller <admiller@redhat.com> 3.0.10-1
- 

* Wed Apr 25 2012 Adam Miller <admiller@redhat.com> 3.0.9-1
- Bug 815173 - Set header in drupal to force IE edge mode in devenv.   Ensure
  that status messages won't be shown for N-1 compat with site   Update
  copyright colors to be black background   Update copyright date
  (ccoleman@redhat.com)

* Tue Apr 24 2012 Adam Miller <admiller@redhat.com> 3.0.8-1
- Bug 814573 - Fix up lots of links to www.redhat.com/openshift/community
  (ccoleman@redhat.com)

* Mon Apr 23 2012 Adam Miller <admiller@redhat.com> 3.0.7-1
- Automatic commit of package [drupal6-openshift-theme] release [3.0.6-1].
  (admiller@redhat.com)

* Mon Apr 23 2012 Adam Miller <admiller@redhat.com> 3.0.6-1
- Reorder items in user_profile_box to work better with Steve's styling
  (ccoleman@redhat.com)
- Touch up blog theme prior to ship (ccoleman@redhat.com)

* Sat Apr 21 2012 Dan McPherson <dmcphers@redhat.com> 3.0.5-1
- Merge commits dd5326df1f0d5bf05d51aeaae0cc4c457ba45816..ab1d91739634c80b3a9db
  5f468e5ceb277824c7d. Did not merge all of the changes made to core code -
  those are upstream and we can't integrate those directly.
  (ccoleman@redhat.com)
- Drupal updates based on latest changes (ccoleman@redhat.com)
- community comments changes (sgoodwin@redhat.com)
- Simplify link generation to reflect that Drupal can't handle server relative
  menu urls (ccoleman@redhat.com)
- Reformat forum thread and comments (sgoodwin@redhat.com)
- community forum layout changes and remove input box-shadow from console
  (sgoodwin@redhat.com)

* Wed Apr 18 2012 Dan McPherson <dmcphers@redhat.com> 3.0.4-1
- Touch all drupal modules to ensure a build. (ccoleman@redhat.com)

* Wed Apr 18 2012 Adam Miller <admiller@redhat.com> 3.0.3-1
- Bug 813613 (ccoleman@redhat.com)
- Abstract out messaging and handle navbar bottom margin a bit cleaner
  (ccoleman@redhat.com)

* Mon Apr 16 2012 Anderson Silva <ansilva@redhat.com> 3.0.2-1
- new package built with tito

* Tue Apr 16 2012 Anderson Silva <ansilva@redhat.com> - 3.0.1-1
- update version

* Tue Mar 20 2012 Anderson Silva <ansilva@redhat.com> - 3.0-1
- Openshif new theme 

* Wed Mar 14 2012 Anderson Silva <ansilva@redhat.com> - 2.0-2
- Rename RPM for consistency

* Wed Mar 5 2012 Anderson Silva <ansilva@redhat.com> - 2.0-1
- Fix requirements
