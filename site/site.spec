%define htmldir %{_localstatedir}/www/html
%define sitedir %{_localstatedir}/www/stickshift/site

Summary:   Li site components
Name:      rhc-site
Version:   0.90.5
Release:   1%{?dist}
Group:     Network/Daemons
License:   GPLv2
URL:       http://openshift.redhat.com
Source0:   rhc-site-%{version}.tar.gz

BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

# Core dependencies to run the build steps
BuildRequires: rubygem-bundler
BuildRequires: rubygem-rake
BuildRequires: js

# Additional dependencies to satisfy the gems, listed in Gemfile order
BuildRequires: rubygem-rails
BuildRequires: rubygem-recaptcha
BuildRequires: rubygem-json
BuildRequires: rubygem-stomp
BuildRequires: rubygem-parseconfig
BuildRequires: rubygem-aws-sdk
BuildRequires: rubygem-xml-simple
BuildRequires: rubygem-haml
BuildRequires: rubygem-compass
BuildRequires: rubygem-formtastic
BuildRequires: rubygem-rack
BuildRequires: rubygem-regin
BuildRequires: rubygem-rdiscount
BuildRequires: rubygem-barista

BuildRequires: rubygem-mocha
BuildRequires: rubygem-hpricot

BuildRequires: rubygem-sinatra
BuildRequires: rubygem-tilt
BuildRequires: rubygem-sqlite3

BuildRequires: rubygem-mail
BuildRequires: rubygem-treetop

Requires:  rhc-common
Requires:  rhc-server-common
Requires:  httpd
Requires:  mod_ssl
Requires:  mod_passenger
Requires:  ruby-geoip
Requires:  rubygem-passenger-native-libs
Requires:  rubygem-rails
Requires:  rubygem-json
Requires:  rubygem-parseconfig
Requires:  rubygem-xml-simple
Requires:  rubygem-formtastic
Requires:  rubygem-haml
Requires:  rubygem-compass
Requires:  rubygem-recaptcha
Requires:  rubygem-hpricot
Requires:  rubygem-barista
Requires:  rubygem-rdiscount
Requires:  js
# The following requires are for the status subsite
Requires:  ruby-sqlite3
Requires:  rubygem-sqlite3
Requires:  rubygem-sinatra

Requires:  rubygem-mail
Requires:  rubygem-treetop

BuildArch: noarch

%description
This contains the OpenShift website which manages user authentication,
authorization and also the workflows to request access.

%prep
%setup -q

%build
bundle exec compass compile
rm -rf tmp/sass-cache
bundle exec rake barista:brew
rm log/development.log

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{htmldir}
mkdir -p %{buildroot}%{sitedir}
cp -r . %{buildroot}%{sitedir}
ln -s %{sitedir}/public %{buildroot}%{htmldir}/app

mkdir -p %{buildroot}%{sitedir}/run
mkdir -p %{buildroot}%{sitedir}/log
mkdir -p -m 770 %{buildroot}%{sitedir}/tmp
touch %{buildroot}%{sitedir}/log/production.log

%clean
rm -rf %{buildroot}                                

%files
%attr(0775,root,libra_user) %{sitedir}/app/subsites/status/db
%attr(0664,root,libra_user) %config(noreplace) %{sitedir}/app/subsites/status/db/status.sqlite3
%attr(0744,root,libra_user) %{sitedir}/app/subsites/status/rhc-outage
%attr(0770,root,libra_user) %{sitedir}/tmp
%attr(0666,root,libra_user) %{sitedir}/log/production.log

%defattr(0640,root,libra_user,0750)
%{sitedir}
%{htmldir}/app
%config(noreplace) %{sitedir}/config/environments/production.rb
%config(noreplace) %{sitedir}/app/subsites/status/config/hosts.yml

%post
/bin/touch %{sitedir}/log/production.log

%changelog
* Wed Apr 04 2012 Mike McGrath <mmcgrath@redhat.com> 0.90.5-1
- modified file download to use mirror.openshift.com (fotios@redhat.com)
- make sure download link is a child of the containing element
  (johnp@redhat.com)
- Added download link to opensource page (fotios@redhat.com)

* Wed Apr 04 2012 Mike McGrath <mmcgrath@redhat.com> 0.90.4-1
- Revert deletion of embedded until the deserialization problem can be fixed
  (ccoleman@redhat.com)
- add basic content and layout to opensource download page (johnp@redhat.com)
- add routes, controller and view for opensource download page
  (johnp@redhat.com)
- US2118: Fedora remix download support (fotios@redhat.com)

* Tue Apr 03 2012 Mike McGrath <mmcgrath@redhat.com> 0.90.3-1
- Logo was missing from the simple header layouts (ccoleman@redhat.com)

* Tue Apr 03 2012 Mike McGrath <mmcgrath@redhat.com> 0.90.2-1
- Add mts-bottom-transparent image for small forms page (edirsh@redhat.com)
- Remove the embedded model object as it is no longer used
  (ccoleman@redhat.com)
- Remove new_forms filter as all output should use new forms
  (ccoleman@redhat.com)
- Merge branch 'master' of git1.ops.rhcloud.com:/srv/git/li (ffranz@redhat.com)
- Fixes 808679 (ffranz@redhat.com)
- [ui] only show gear size if there is more than one option (johnp@redhat.com)

* Sat Mar 31 2012 Dan McPherson <dmcphers@redhat.com> 0.90.1-1
- bump spec numbers (dmcphers@redhat.com)
- Updates all links to docs for the new version that doesnt have Express on the
  URLs (ffranz@redhat.com)
- Fixes 807985 (ffranz@redhat.com)

* Thu Mar 29 2012 Dan McPherson <dmcphers@redhat.com> 0.89.10-1
- check to see if domain is being updated (johnp@redhat.com)
- mitigate race condition due to multiple domain support on the backend
  (johnp@redhat.com)
- Fixes 807985 (ffranz@redhat.com)
- Merge branch 'master' of git1.ops.rhcloud.com:/srv/git/li (ffranz@redhat.com)
- Fixes 806763 and 802699 (ffranz@redhat.com)
- more fixes to gear size UI (johnp@redhat.com)
- add the gear size option to the create app view (johnp@redhat.com)
- Fixes 798128 (ffranz@redhat.com)

* Wed Mar 28 2012 Dan McPherson <dmcphers@redhat.com> 0.89.9-1
- 

* Wed Mar 28 2012 Dan McPherson <dmcphers@redhat.com> 0.89.8-1
- correct links and remove duplicates in opensource dislaimer page
  (johnp@redhat.com)
- Fixes 807063 (ffranz@redhat.com)
- Added logged in user information to console header (ffranz@redhat.com)
- when embedding cart put server output in an escaped pre tag
  (johnp@redhat.com)

* Tue Mar 27 2012 Dan McPherson <dmcphers@redhat.com> 0.89.7-1
- Fixes help links tests (ffranz@redhat.com)
- blacklist haproxy from the cartridge view for now (johnp@redhat.com)
- set error classes on username and password field if base error comes in
  (johnp@redhat.com)
- [sauce] fix error class assignment when creating app (johnp@redhat.com)
- Unit tests for help links so when they break we know (ccoleman@redhat.com)
- Fixed hard coded /app links in form (fotios@redhat.com)
- Fixed odd quotation in terms_controller (fotios@redhat.com)
- Fix for BZ806939: Login form password length validation (fotios@redhat.com)
- Delete .gitignore from public/javascripts (ccoleman@redhat.com)
- Clean up and refine overview and getting started (ccoleman@redhat.com)

* Mon Mar 26 2012 Dan McPherson <dmcphers@redhat.com> 0.89.6-1
- 

* Mon Mar 26 2012 Dan McPherson <dmcphers@redhat.com> 0.89.5-1
- Add treetop for good measure (ccoleman@redhat.com)
- Update site.spec to take a dependency at build and runtime on rubygem-mail
  (not being pulled in by dependency tree of existing rails packages in build
  env, so build fails) (ccoleman@redhat.com)

* Mon Mar 26 2012 Dan McPherson <dmcphers@redhat.com> 0.89.4-1
- 

* Mon Mar 26 2012 Dan McPherson <dmcphers@redhat.com> 0.89.3-1
- 

* Mon Mar 26 2012 Dan McPherson <dmcphers@redhat.com> 0.89.2-1
- remove missed "preview" tag from Management Console header (johnp@redhat.com)
- Whitelist allowable options to getting_started_external_controller
  (ccoleman@redhat.com)
- Clean up markup on appcelerator page (ccoleman@redhat.com)
- Update getting started page to be more attractive, include link to console.
  (ccoleman@redhat.com)
- Fixed merge problem related to app/models/express_cartlist.rb
  (ffranz@redhat.com)
- Removed deprecated node_js_enabled copnfiguration (ffranz@redhat.com)
- Properly clear application list at beginning of each unit test
  (ccoleman@redhat.com)
- remove all of the .to_delete files (johnp@redhat.com)
- fix OS disclaimer page merge issue (johnp@redhat.com)
- remove express models and tests (johnp@redhat.com)
- Removing legacy express code (fotios@redhat.com)
- Removed/changed references to express in current console (fotios@redhat.com)
- OS disclaimer - fix nodejs license (johnp@redhat.com)
- Clean applications at beginning of application controller test cases
  (ccoleman@redhat.com)
- Revert with_domain behavior to previous, add additional methods for tests
  that do or don't need a domain object.  Ensure cleanup in rest_api_tests is
  consistent. (ccoleman@redhat.com)
- Bug 806763 - Change order of rendering of form errors to be before hints
  (ccoleman@redhat.com)
- Bug 806785 - Reset SSO and session when password reset link received Treat
  empty rh_sso cookie as nil rh_sso cookie Remove Rails. prefix from controller
  logging (ccoleman@redhat.com)
- Remove development log from site build (ccoleman@redhat.com)
- Off by one media query errors cause footer columns to be wrong on ipad
  (ccoleman@redhat.com)
- Reorder application types to put node.js at the top (ccoleman@redhat.com)
- No lift-counter needed on the home page (ccoleman@redhat.com)
- Fix Overpass font to use correct Bold style, add OverpassNormal for old
  behavior Revert brand logo to use text, temporary fixes for narrow screens
  Update layout to use counter standard 'lift-counter' Add page titles to most
  pages, fixup markup to be consistent Remove .ribbon-content everywhere.
  (ccoleman@redhat.com)
- Bug 806145 - Removed lurking text. (ccoleman@redhat.com)
- Remove old console message (ccoleman@redhat.com)
- Tone down buzz section at small resolutions (ccoleman@redhat.com)
- Checkin default avatar (ccoleman@redhat.com)
- Add last vestiges of JS generation (ccoleman@redhat.com)
- Bug 806198 - Bow to public pressure, show distinct auth links based on state
  (ccoleman@redhat.com)
- Merge branch 'master' of git1.ops.rhcloud.com:/srv/git/li (lnader@redhat.com)
- Bug 806026 - Revert iframe fix now that getting_started embedded videos are
  gone (ccoleman@redhat.com)
- Bug 805685 - Comment out link temporarily (ccoleman@redhat.com)
- User is not consistently being taken to console after login, because
  http_referrer isn't changed on redirects.  Pass destination as a redirectUrl
  parameter, stop using session variable. (ccoleman@redhat.com)
- Generate CSS and JS during build of site rpm, using bundle exec and
  barista/compass (ccoleman@redhat.com)
- Merge branch 'master' of git1.ops.rhcloud.com:/srv/git/li (lnader@redhat.com)
- Merge branch 'master' of git1.ops.rhcloud.com:/srv/git/li (lnader@redhat.com)
- Support generic URL redirection based on the Rack SCRIPT_NAME
  (ccoleman@redhat.com)
- Getting started headlines (ffranz@redhat.com)
- Removed the last references to Flex from site codebase (ffranz@redhat.com)
- Fixed product controller functional tests (ffranz@redhat.com)
- Merge branch 'master' of git1.ops.rhcloud.com:/srv/git/li (lnader@redhat.com)
- Merge branch 'compass', removed conflicting JS file (ccoleman@redhat.com)
- merged with master (lnader@redhat.com)
- Add default barista config to autogenerate in development mode, and make
  production mode route directly Delete old JS files Delete previously
  generated JS files Fixup all stylesheet and javascript urls to be relative
  (ccoleman@redhat.com)
- Trying to fix broken tests (unable to reproduce), using setup_integrated
  instead of with_domain (ffranz@redhat.com)
- merge with master (lnader@redhat.com)
- Move overpass to app/stylesheets Remove generated CSS from public/stylesheets
  Remove deprecated projekktor_maccaco file (ccoleman@redhat.com)
- Broker and site in devenv should use RackBaseURI and be relative to content
  Remove broker/site app_scope (ccoleman@redhat.com)
- OS disclaimer - fix up licenses and links; remove redundant listings
  (johnp@redhat.com)
- Compass automatically generates stylesheets from app/stylesheets to
  tmp/stylesheets in dev mode, and Rack serves content from both of them in
  development and production. (ccoleman@redhat.com)
- prun some of the -devel packages and subpackages (johnp@redhat.com)
- Revert gemfile.lock back to earlier version (accidental commit)
  (ccoleman@redhat.com)
- Merge branch 'master' of git1.ops.rhcloud.com:/srv/git/li (lnader@redhat.com)
- Merge branch 'master' of git1.ops.rhcloud.com:/srv/git/li (ffranz@redhat.com)
- Merge branch 'master' of git1.ops.rhcloud.com:/srv/git/li (lnader@redhat.com)
- Removed references to Flex on site codebase, some tests may break
  (ffranz@redhat.com)
- Bad require left around (ccoleman@redhat.com)
- Compass initial code (ccoleman@redhat.com)
- Merge branch 'master' of git1.ops.rhcloud.com:/srv/git/li (lnader@redhat.com)
- Merge branch 'master' of git1.ops.rhcloud.com:/srv/git/li (rpenta@redhat.com)
- Fix test cases in site/test/functional/keys_controller_test.rb
  (rpenta@redhat.com)
- -1 is not the same as .1, fix bad site gemfile (ccoleman@redhat.com)
- Merge branch 'master' of git1.ops.rhcloud.com:/srv/git/li (rpenta@redhat.com)
- Fix key create/destroy tests in site/test/integration/rest_api_test.rb
  (rpenta@redhat.com)
- Merge branch 'master' of git1.ops.rhcloud.com:/srv/git/li (ffranz@redhat.com)
- Add dependency on compass to Gem (ccoleman@redhat.com)
- Site needs an RPM dependency on rubygem-compass for CSS generation
  (ccoleman@redhat.com)
- Fixes 803654 (ffranz@redhat.com)
- Removed references to Flex on site codebase (ffranz@redhat.com)
- add initial list of open source packages to disclaimer page
  (johnp@redhat.com)
- Merge branch 'master' of git1.ops.rhcloud.com:/srv/git/li (lnader@redhat.com)
- Removed references to Flex on site codebase (ffranz@redhat.com)
- US1876 (lnader@redhat.com)
- Update to haml 3.1, must use new AMI (ccoleman@redhat.com)
- add initial opensource disclaimer page, links and route (johnp@redhat.com)
- Removed Flex from some pages (ffranz@redhat.com)
- Redirect /user/new to /account/new, replace flex login sequence with generic
  sequence (ccoleman@redhat.com)
- Fix failing unit tests now that flex pages have been removed.
  (ccoleman@redhat.com)
- Improved spacing on getting started page (ffranz@redhat.com)
- Merge branch 'master' of git1.ops.rhcloud.com:/srv/git/li (ffranz@redhat.com)
- Added Node.js on several marketing pages (ffranz@redhat.com)
- Use with_domain on Cart type controller vs setup_integrated (better cleanup)
  (ccoleman@redhat.com)
- Remove extra spaces which cause warnings (ccoleman@redhat.com)
- merge (mmcgrath@redhat.com)
- Update stickshift gemfiles to new rack versions, remove multimap which is no
  longer required by rack (versions before .7 had a dependency, it has since
  been inlined) (ccoleman@redhat.com)
- Merge branch 'rack' (ccoleman@redhat.com)
- Added redirect for legacy routes (ffranz@redhat.com)
- Merge branch 'master' of git1.ops.rhcloud.com:/srv/git/li (ffranz@redhat.com)
- Removed Flex from top header nav links (ffranz@redhat.com)
- Fixes for BZ804845 and BZ803679 (fotios@redhat.com)
- Update rack dependencies (ccoleman@redhat.com)
- Update rack to 1.3 (ccoleman@redhat.com)
- Remove overly aggressive site rack dependency (should be open)
  (ccoleman@redhat.com)
- Merge branch 'dev/clayton/login' (ccoleman@redhat.com)
- Remove excess puts (ccoleman@redhat.com)
- check to see if conflicts and requires are available (johnp@redhat.com)
- Update login parameter in unit tests (ccoleman@redhat.com)
- Don't generate urls to the confirmation pages for flex/express - go only to
  confirm (ccoleman@redhat.com)
- Merge remote-tracking branch 'origin/master' into dev/clayton/login
  (ccoleman@redhat.com)
- Fix login tests to use new param (ccoleman@redhat.com)
- Testing flex confirmation redirects, more tests of email confirmation
  (ccoleman@redhat.com)
- Adding a default cfs_quota (mmcgrath@redhat.com)
- Redirect old /app/user/new/flex|express paths, fix unit tests
  (ccoleman@redhat.com)
- renamed haproxy (mmcgrath@redhat.com)
- Fix broken keys controller tests (ccoleman@redhat.com)
- fix for help-inline msg on _form.html.haml (sgoodwin@redhat.com)
- fix 803995 (sgoodwin@redhat.com)
- error msg display fix 803995 (sgoodwin@redhat.com)
- Bug 798128 (sgoodwin@redhat.com)
- Fix warning (ccoleman@redhat.com)
- Add more debugger logging to streamline for auth failures, fix problem with
  parameter names in login controller. (ccoleman@redhat.com)
- Merge branch 'master' into dev/clayton/login (ccoleman@redhat.com)
- Add new methods to streamline_mock (ccoleman@redhat.com)
- Combine confirmation and success messages into a single form, remove old
  signin form, and fix redirection of new user to prefill email address.
  (ccoleman@redhat.com)
- Remove dead password code and views, everything moved to app/views/password
  and app/controllers/password_controller.rb (ccoleman@redhat.com)
- Redirect old password reset links to new password reset links
  (ccoleman@redhat.com)
- Autofocus on signin flow (ccoleman@redhat.com)
- Refresh login flow with updated code to streamline, clean up error text.
  (ccoleman@redhat.com)
- Add link to return to main page after reset (ccoleman@redhat.com)
- Cleanup email confirmation and signup controllers for better flow.
  (ccoleman@redhat.com)
- nav additions coming over from original _navbar (sgoodwin@redhat.com)
- fix header backgrounds, ie8 and chrome logo issues (sgoodwin@redhat.com)
- Display errors using formtastic, make login model driven
  (ccoleman@redhat.com)
- New forms are active everywhere (ccoleman@redhat.com)
- bug #802354 - disable details button for jenkins server (johnp@redhat.com)
- Bug 803854 - Remove https (ccoleman@redhat.com)
- Bug 790695 - User guide link broken (ccoleman@redhat.com)
- Bug 804177 - icons missing, visually unaligned (ccoleman@redhat.com)
- Merge branch 'master' into dev/clayton/login (ccoleman@redhat.com)
- More cookies hacking, no success, give up and admin defeat.
  (ccoleman@redhat.com)
- Round out some remaining tests. Slight tweaks to behavior of :cookie_domain
  => :current Comment out unit tests related to cookies until I can debug
  (ccoleman@redhat.com)
- Fix duplicate constant error by making status site autoload
  (ccoleman@redhat.com)
- Merge branch 'master' into login (ccoleman@redhat.com)
- Remove useless file (ccoleman@redhat.com)
- Dealing with complexities of cookie handling in functional tests, whittling
  down dead code. (ccoleman@redhat.com)
- Additional tests, support referrer redirection (ccoleman@redhat.com)
- Merge branch 'master' into login (ccoleman@redhat.com)
- Further cleaning up login flow (ccoleman@redhat.com)
- Add more unit tests for cookie behavior (ccoleman@redhat.com)
- Incremental testing (ccoleman@redhat.com)
- Add configurable cookie domain for rh_sso (allow site to work outside of
  .redhat.com) Begin simplifying login flow (ccoleman@redhat.com)

* Sat Mar 17 2012 Dan McPherson <dmcphers@redhat.com> 0.89.1-1
- bump spec numbers (dmcphers@redhat.com)
- Capitalization of node.js (ccoleman@redhat.com)
- Feedback from Dan J about message (ccoleman@redhat.com)
- Reorganize cartridge page to avoid visual bugs, other minor arrangements
  (ccoleman@redhat.com)
- don't error out if server doesn't send back messages (johnp@redhat.com)
- Bug 803854 - bad URL for php my admin (ccoleman@redhat.com)
- Fixes 803934 (ffranz@redhat.com)

* Thu Mar 15 2012 Dan McPherson <dmcphers@redhat.com> 0.88.12-1
- when creating cart make sure to pass the server results back to the UI
  (johnp@redhat.com)
- Fixed embedding display (fotios@redhat.com)
- Cleaned up embedded cart listing (fotios@redhat.com)
- Merge branch 'master' of git1.ops.rhcloud.com:/srv/git/li (ffranz@redhat.com)
- Added more blocked type to scaled application and error message
  (fotios@redhat.com)
- Fixes 802713 (ffranz@redhat.com)
- Added support for scaling app to block certain embedded cartridges
  (fotios@redhat.com)
- Updated homepage copy based on Dan's feedback, disabled images until we can
  get styles. (ccoleman@redhat.com)
- Fixes 803674, improved terms layout (ffranz@redhat.com)
- Fixed form validation to be more consistant (fotios@redhat.com)
- fix cartridge_type index view to check if there are any carts to be displayed
  (johnp@redhat.com)
- Fixes 803665 (ffranz@redhat.com)
- Merge branch 'master' of git1.ops.rhcloud.com:/srv/git/li (ffranz@redhat.com)
- Fixes 803212 (ffranz@redhat.com)
- mark the metrics cart as experimental and tag it in the UI (johnp@redhat.com)
- Merge branch 'devweb' (sgoodwin@redhat.com)
- including graphics on home and fix ie bugs (sgoodwin@redhat.com)

* Wed Mar 14 2012 Dan McPherson <dmcphers@redhat.com> 0.88.11-1
- Simple header should not have text, move content (ccoleman@redhat.com)
- Minor cleanup to the getting started content - Flex is bare enough that we
  should axe it (ccoleman@redhat.com)
- Minor routes cleanup (ccoleman@redhat.com)

* Wed Mar 14 2012 Dan McPherson <dmcphers@redhat.com> 0.88.10-1
- Fixed minLength for validations (fotios@redhat.com)
- Updated overview with new style commands and python package
  (ccoleman@redhat.com)
- Videos expand outside their boundaries when on a small device, temporary
  hac^Hfix (ccoleman@redhat.com)
- Added form validations (fotios@redhat.com)

* Wed Mar 14 2012 Dan McPherson <dmcphers@redhat.com> 0.88.9-1
- 

* Wed Mar 14 2012 Dan McPherson <dmcphers@redhat.com> 0.88.8-1
- add requires and conflicts data to cart types and display (johnp@redhat.com)
- fix the phpmyadmin descriptor (johnp@redhat.com)

* Wed Mar 14 2012 Dan McPherson <dmcphers@redhat.com> 0.88.7-1
- Added an inspector to watch an intermittent test failure (ffranz@redhat.com)
- Removed placeholder for application type image (fotios@redhat.com)
- Merge branch 'master' of git1.ops.rhcloud.com:/srv/git/li (ffranz@redhat.com)
- Merge branch 'devwed' (sgoodwin@redhat.com)
- new and improved header logo now with vitamin d (sgoodwin@redhat.com)
- Fixed streamline tests (ffranz@redhat.com)
- Fixes 803232 (ffranz@redhat.com)
- Merge branch 'master' of git1.ops.rhcloud.com:/srv/git/li (ffranz@redhat.com)
- Fixes 803232; added new getting started pages; conditional take_action
  according to existing session (ffranz@redhat.com)
- Bug 802709 - some links on homepage broken (ccoleman@redhat.com)
- Added haproxy application_type so scaled apps show up (fotios@redhat.com)
- Add text comments from yesterday (ccoleman@redhat.com)
- Fixes 803223 - added proper captcha error messages (ffranz@redhat.com)
- site/site.spec: Fixed permissions not taking (whearn@redhat.com)
- Bug 803189 - using wrong layout when change password fails
  (ccoleman@redhat.com)
- Bug 803229, fixup email confirm page with new styles (ccoleman@redhat.com)
- Merge branch 'master' of git1.ops.rhcloud.com:/srv/git/li (ffranz@redhat.com)
- Fixes 802658 (ffranz@redhat.com)
- Need to force the URL for aliases (fotios@redhat.com)
- Fixed login_ajax_path missing (fotios@redhat.com)
- Moved jQuery to use CDN and commented on JS usage (fotios@redhat.com)
- Fixed broken unit tests (ccoleman@redhat.com)
- Fixes 803212: added more error messages on signup (ffranz@redhat.com)
- Improvements to login flow. Time to go to sleep. (ffranz@redhat.com)
- Fixed error messages on signin (ffranz@redhat.com)
- Merge branch 'master' of git1.ops.rhcloud.com:/srv/git/li (ffranz@redhat.com)
- Fixed error messages on signin, signup and recover screens; added ribbon
  content support for the simple layout (ffranz@redhat.com)

* Wed Mar 14 2012 Dan McPherson <dmcphers@redhat.com> 0.88.6-1
- Fixed box layout to simple layout on user and login controllers
  (ffranz@redhat.com)

* Tue Mar 13 2012 Dan McPherson <dmcphers@redhat.com> 0.88.5-1
- Had to switch away from 'span-wrapper' to 'grid-wrapper' to get the proper
  ordering.  Responsive is updated to take into account.  Community styles
  updated (ccoleman@redhat.com)
- Fix navigation bar styles for thick underlines, make clickable area larger.
  (ccoleman@redhat.com)
- Give tiny highlight behavior to take action (ccoleman@redhat.com)
- Show openshift tweets until we have recommendation content For login page
  show a button that is not btn-primary (allow form to override btn-primary)
  (ccoleman@redhat.com)
- Switch to grid based column layout, fix problems with offset* and span-
  wrapper in various scenarios (ccoleman@redhat.com)
- More tweaks to layout and controllers (ccoleman@redhat.com)
- Stylesheets (ccoleman@redhat.com)
- Clean up references (ccoleman@redhat.com)
- Rename 'box' layout to 'simple', collapse references to both Add
  SiteController as a parent controller for controllers that are specific to a
  specific side of the site (ccoleman@redhat.com)
- Merge branch 'master' of git1.ops.rhcloud.com:/srv/git/li (ffranz@redhat.com)
- Fixes login flow bugs (ffranz@redhat.com)
- Change multi-element ribbon headers to single element headers
  (edirsh@redhat.com)
- Add styling for single-element ribbonw (edirsh@redhat.com)
- home callout styling (sgoodwin@redhat.com)
- Detect currently active tab in header navigation (fotios@redhat.com)
- Reverse order of buttons in the ui (ccoleman@redhat.com)
- Failing unit test caused by change in logout logic (ccoleman@redhat.com)
- Bug 802732 - was not merging errors correctly in applications_controller.
  Added some debug logging for future. (ccoleman@redhat.com)
- Temporarily fix stylesheet issues with help-block being turned to a color
  (and thus confusing users about whether the help is an error).
  (ccoleman@redhat.com)
- Allow aliased errors to be reported correctly for their originating attribute
  (ccoleman@redhat.com)
- Remove comments for now, no confusion (ccoleman@redhat.com)
- Add better logging to certain filters (ccoleman@redhat.com)
- Unit test updates (ccoleman@redhat.com)
- Merge branch 'devtues' (sgoodwin@redhat.com)
- detailing buzz section and other minor things home related
  (sgoodwin@redhat.com)
- add unit test for cartridges model (johnp@redhat.com)
- Various login tweaks to work around limitations from RHN
  (ccoleman@redhat.com)
- Make ID based rules class based (ccoleman@redhat.com)
- fine tuning navbar (sgoodwin@redhat.com)
- Merge branch 'master' of git1.ops.rhcloud.com:/srv/git/li (ffranz@redhat.com)
- Fixes login flows tests (ffranz@redhat.com)

* Mon Mar 12 2012 Dan McPherson <dmcphers@redhat.com> 0.88.4-1
- Removed login flow tests, starting to integrate with the new login flow
  (ffranz@redhat.com)
- Fixes old control_panel test (ffranz@redhat.com)
- Fixes some test failures on login flows (ffranz@redhat.com)
- Fixed user_controller tests that requires create.html.haml
  (ffranz@redhat.com)
- Fixes signup success page (ffranz@redhat.com)
- Branding: old control_panel and dashboard routes redirects to /console
  (ffranz@redhat.com)
- Branding: removed the temporary /new controller route (ffranz@redhat.com)
- Fixed signup redirect bug (ffranz@redhat.com)
- Fixed login redirect bug (ffranz@redhat.com)
- Merge branch 'master' of git1.ops.rhcloud.com:/srv/git/li (ffranz@redhat.com)
- Fixed login redirect bug (ffranz@redhat.com)
- focus states for primary nav (sgoodwin@redhat.com)
- Branding: fixed broken images, adjust routes for the good of SEO
  (ffranz@redhat.com)
- Branding: improved login page (ffranz@redhat.com)
- Branding: improved login page (ffranz@redhat.com)
- Overview typo, remove max-height (ccoleman@redhat.com)
- Merge branch 'master' of git1.ops.rhcloud.com:/srv/git/li (ffranz@redhat.com)
- Branding: links on signin, signup, recover pages (ffranz@redhat.com)
- Fixed workflow for signup form (fotios@redhat.com)
- updated comment thread styles (sgoodwin@redhat.com)
- Branding: improved Express and Flex pages (ffranz@redhat.com)
- Branding: merged header (ffranz@redhat.com)
- section-top color changes (sgoodwin@redhat.com)
- Fix links in between overview and content (ccoleman@redhat.com)
- Integrate overview site (ccoleman@redhat.com)
- Regeneration of home/common with merges (ccoleman@redhat.com)
- Reenable btn-primary for commit buttons (ccoleman@redhat.com)
- Update cartridge landing page styles (ccoleman@redhat.com)
- Styleguide example of landing page (ccoleman@redhat.com)
- Branding: getting started page (ffranz@redhat.com)
- Merge branch 'master' of git1.ops.rhcloud.com:/srv/git/li (ffranz@redhat.com)
- Branding: partners pages (ffranz@redhat.com)
- add cartridge_types functional tests (johnp@redhat.com)
- add bridge styling for simple page (edirsh@redhat.com)
- Merge branch 'master' of git1.ops.rhcloud.com:/srv/git/li (ffranz@redhat.com)
- Branding: videos pages (ffranz@redhat.com)
- make sure we have a leading slash when concatting rest urls
  (johnp@redhat.com)
- cartridges functional test (johnp@redhat.com)
- Branding: Flex page (ffranz@redhat.com)
- Branding: legal pages (ffranz@redhat.com)
- Merge branch 'master' of git1.ops.rhcloud.com:/srv/git/li (ffranz@redhat.com)
- Merge branch 'devmon' (sgoodwin@redhat.com)
- Merge branch 'master' of git1.ops.rhcloud.com:/srv/git/li (ffranz@redhat.com)
- Branding: integrating everything into current site (hold on your seat)
  (ffranz@redhat.com)
- checking in compiled stylesheet (edirsh@redhat.com)
- Further tweaks to large backgrounds (edirsh@redhat.com)
- cleanup odds and ends (sgoodwin@redhat.com)
- Update help link to app cli management (ccoleman@redhat.com)
- Make create app a button (ccoleman@redhat.com)
- Comment out videos for this sprint, will deal with in a follow up
  (ccoleman@redhat.com)
- Merge branch 'master' of git1.ops.rhcloud.com:/srv/git/li (ffranz@redhat.com)
- Branding: signup confirmation page (ffranz@redhat.com)
- Regen CSS after merge (ccoleman@redhat.com)
- New logo for status site, some minor css tweaks for now.
  (ccoleman@redhat.com)
- Update font family to match global variable (ccoleman@redhat.com)
- section-top bar mods (sgoodwin@redhat.com)
- newletter signup edit (sgoodwin@redhat.com)
- ui tweaks (sgoodwin@redhat.com)
- Merge branch 'master' of git1.ops.rhcloud.com:/srv/git/li (ffranz@redhat.com)
- Branding: recover password workflow (ffranz@redhat.com)
- touch icons (sgoodwin@redhat.com)
- Update logo for console site to match branding guidelines (roughly), still
  needs lots of love. (ccoleman@redhat.com)

* Fri Mar 09 2012 Dan McPherson <dmcphers@redhat.com> 0.88.3-1
- Merge branch 'master' of git1.ops.rhcloud.com:/srv/git/li (ffranz@redhat.com)
- Branding: signin, signup and recover pwd now on smaller boxes and dedicated
  pages (ffranz@redhat.com)

* Fri Mar 09 2012 Dan McPherson <dmcphers@redhat.com> 0.88.2-1
- Branding: signin, signup and recover pwd now on smaller boxes and dedicated
  pages (ffranz@redhat.com)
- Changed background styling for small screens (edirsh@redhat.com)
- Tweaked background styles for home page; added bg styles for interior and
  community pages (edirsh@redhat.com)
- Updated #search-field to use a marker class, added styles for votes, videos,
  and rudimentary KB articles. (ccoleman@redhat.com)
- Merge branch 'dev/kraman/US1972' (kraman@gmail.com)
- Moved font code to its own CSS for better loading (fotios@redhat.com)
- Rename 'take-action' to 'action-call' and add 'action-more' for secondary
  links.  Update styles for blog to match. (ccoleman@redhat.com)
- Branding: styling signup page (ffranz@redhat.com)
- Updates for getting devenv running (kraman@gmail.com)
- Renaming Cloud-SDK -> StickShift (kraman@gmail.com)
- Branding: signin page (ffranz@redhat.com)
- Mark old partials as obsolete (ccoleman@redhat.com)
- Mark style.scss as out of date so it is no longer generated, and ignore any
  .sass-cache directories created (ccoleman@redhat.com)
- Site css files (ccoleman@redhat.com)
- font size tweaks (sgoodwin@redhat.com)
- Merge branch 'dev309' (sgoodwin@redhat.com)
- avatar and type edits (sgoodwin@redhat.com)
- Added Overview and Flex sections to homepage header (ffranz@redhat.com)
- Fixed Firefox desaturation of the logo by removing the color profile from the
  PNG (ccoleman@redhat.com)
- sprite change (sgoodwin@redhat.com)
- Merge branch 'dev308' (sgoodwin@redhat.com)
- secondary navigation modifications (sgoodwin@redhat.com)
- Reorganization of navbar styles for console, minor hacks to get an
  approximate look for the old console.  More to come (ccoleman@redhat.com)
- when listing available carts show installed carts but disable selection
  (johnp@redhat.com)
- Chrome/webkit prefixed properties, fix minor bugs with gradients
  (ccoleman@redhat.com)
- Add rdiscount markdown support (ccoleman@redhat.com)
- Add more metadata to the cartridges in the CartridgeType model
  (johnp@redhat.com)
- Branding: added Express and Flex sections (ffranz@redhat.com)
- fix up the next steps page for carts wizard (johnp@redhat.com)
- next steps template file (johnp@redhat.com)
- next_steps wizard page for successful cart creation (johnp@redhat.com)
- Fix for getting hostname on prod/stg servers (fotios@redhat.com)
- Merge branch 'responsive' (ccoleman@redhat.com)
- Fix some responsive bugs at 768px (exactly), balance messaging font sizes in
  portrait mode, keep refining code (ccoleman@redhat.com)
- Fixes user controller missing routes (ffranz@redhat.com)
- Branding: added site controller, adjusted missing layout on legacy pages
  (ffranz@redhat.com)
- Branding: signin page and conditional headers according to existing session
  (ffranz@redhat.com)
- Branding: new signup page (ffranz@redhat.com)
- Integrate backgrounds directly, work around lack of compass for now by
  inlining after generation. Fix header colors Fix fonts to let Helvetica
  override Liberation Sans Letter spacing on check the buzz
  (ccoleman@redhat.com)
- Start abstracting colors into variables (ccoleman@redhat.com)
- Sign in link and header color (ccoleman@redhat.com)
- Allow views to pass classes to nav header for lifting (ccoleman@redhat.com)
- Give sections bottom margin, left align take-action in responsive mode, magic
  (ccoleman@redhat.com)
- Simplify take-action section, allow it to be used in nav and in content body,
  provide helper method, fix problems with responsive layout
  (ccoleman@redhat.com)
- Merge branch 'master' of git1.ops.rhcloud.com:/srv/git/li (ffranz@redhat.com)
- Branding: basic signup content, home header styling (ffranz@redhat.com)
- Add styles and images for homepage buzz section (edirsh@redhat.com)
- Add styling and images for new branding homepage header (edirsh@redhat.com)
- redirect on successful addition of cart (johnp@redhat.com)
- workarounds to using 'type' as a model field in the rest api
  (johnp@redhat.com)
- Branding: styling background images (ffranz@redhat.com)
- Branding new home CSS styling (ffranz@redhat.com)
- Branding new home CSS styling (ffranz@redhat.com)
- More responsive tweaks to take action bar (ccoleman@redhat.com)
- Favicons, headers, grid fixes for iphone and small devices, restore a minor
  merge conflict (ccoleman@redhat.com)
- New branding on homepage, added twitter buzz (ffranz@redhat.com)
- fixed cartridge model encoding issue (johnp@redhat.com)
- list style edit (sgoodwin@redhat.com)
- add the bones around adding a cart to an application (johnp@redhat.com)
- New branding for the home page (ffranz@redhat.com)
- Accidentally reenabled markdown too early (ccoleman@redhat.com)
- Add wrapper node for left column to give it a margin (Gnhhh, so many
  wrappers.  Damn you grid) Poll styles Images for expand collapse Comment
  style cleanup Simplification of links (ccoleman@redhat.com)
- overview page, fixes to header, minus markdown requirements.
  (ccoleman@redhat.com)
- Add headline marker class to primary messaging (ccoleman@redhat.com)
- Community tweaks (ccoleman@redhat.com)
- Add badges and some generic cleanup to comments (ccoleman@redhat.com)
- search block modifications (sgoodwin@redhat.com)
- revert an errant commit to development config file (johnp@redhat.com)
- Update tabs, update header (ccoleman@redhat.com)
- Minor tweaks to header to accomodate possible animation, fix problems at
  smaller resolutions (ccoleman@redhat.com)
- add show template for cartridge types (johnp@redhat.com)
- Add subheadings and some minor style tweaks to the help page
  (ccoleman@redhat.com)
- hook up the show cartridge_type action for adding cartridges
  (johnp@redhat.com)
- get cart list from rest api but fill in details in the model
  (johnp@redhat.com)
- Merge branch 'dev/clayton/help' (ccoleman@redhat.com)
- Marker class for styles (ccoleman@redhat.com)
- More fixup of help links (ccoleman@redhat.com)
- Proto help page (ccoleman@redhat.com)
- add links to add a cartridge (johnp@redhat.com)
- add initial page for cartridge selection (johnp@redhat.com)
- move wizard_create helper to app_wizard_create and add cartridge wizard
  (johnp@redhat.com)
- Fixes 799188: will remove Node.JS from the list of available cartridges in
  production (ffranz@redhat.com)
- Fixes 799188: will remove Node.JS from the list of available cartridges in
  production (ffranz@redhat.com)
- Merge branch 'master' of ssh://git1.ops.rhcloud.com/srv/git/li
  (mpatel@redhat.com)
- Changes to rename raw to diy. (mpatel@redhat.com)
- Layout with header content (ccoleman@redhat.com)
- Remove unused stylesheet, unused controller bit (ccoleman@redhat.com)
- Use relative links in CSS (ccoleman@redhat.com)
- sprite additions (sgoodwin@redhat.com)
- Logo integration (ccoleman@redhat.com)
- Merge branch 'master' of git:/srv/git/li (ccoleman@redhat.com)
- Add active colors for menu, ensure submenus have the right margins enter the
  commit message for your changes. Lines starting (ccoleman@redhat.com)
- Fix for BZ799561: rhc-outage now correctly identifies sync failures
  (fotios@redhat.com)
- Reenable node.js (ccoleman@redhat.com)
- Fix ordering of stylesheets on examples (ccoleman@redhat.com)
- Merge branch 'master' into dev/clayton/home (ccoleman@redhat.com)
- Merge branch 'master' into dev/clayton/home (ccoleman@redhat.com)
- Right facing arrow (ccoleman@redhat.com)
- Start on creating a layout for the new styles (ccoleman@redhat.com)
- Rename constants (ccoleman@redhat.com)
- Fix up menu padding (ccoleman@redhat.com)
- Begin reorganizing site.scss into partials (ccoleman@redhat.com)
- More tweaks to navigation and headers (ccoleman@redhat.com)
- Signup (ccoleman@redhat.com)
- Much simpler solution for grid filling (introduction of row-flush-right and
  span-wrapper) to allow backgrounds to fit content more cleanly
  (ccoleman@redhat.com)

* Fri Mar 02 2012 Dan McPherson <dmcphers@redhat.com> 0.88.1-1
- bump spec numbers (dmcphers@redhat.com)
- Had to fix the view too (fotios@redhat.com)
- Fixed static routes in status app (fotios@redhat.com)
- Refactored status_app to work with different Rails app_scopes
  (fotios@redhat.com)
- Reword text to match recommendations from dblado (ccoleman@redhat.com)
- Fixes 799503 (ffranz@redhat.com)
- Adjust base_domain configuration for stg and prod (ffranz@redhat.com)
- Merge branch 'master' into dev/clayton/home (ccoleman@redhat.com)
- Disable node.js 799188 (ccoleman@redhat.com)
- More comment tweaks (ccoleman@redhat.com)
- Minor tweaks to comments (ccoleman@redhat.com)
- Reorder try it out to be better (ccoleman@redhat.com)
- Pixel-perfect layout adjustments (ffranz@redhat.com)
- Fixed gutters to be more accurate within various resolutions, lines up
  exactly with ipad screen. (ccoleman@redhat.com)
- Fixes 798142, major app list style improvements (ffranz@redhat.com)
- sprite img (sgoodwin@redhat.com)
- Merge branch 'master' of git1.ops.rhcloud.com:/srv/git/li (ffranz@redhat.com)
- Fixes 798502: added links to docs (ffranz@redhat.com)
- Removed switch to use attr in %%files instead of chmod Mark hosts.yml as
  config(noreplace) (whearn@redhat.com)
- More changes to styling of community (ccoleman@redhat.com)
- Comments, various small tweaks to community CSS (ccoleman@redhat.com)
- Tweets, block quotes, some padding adjustments, default link colors, and
  background with repeating gradient. (ccoleman@redhat.com)
- Merge branch 'master' into dev/clayton/home (ccoleman@redhat.com)
- Merge of bootstrap (ccoleman@redhat.com)
- Styles for homepage (ccoleman@redhat.com)

* Thu Mar 01 2012 Dan McPherson <dmcphers@redhat.com> 0.87.13-1
- Fixed link for user guide to point to html version (fotios@redhat.com)

* Thu Mar 01 2012 Dan McPherson <dmcphers@redhat.com> 0.87.12-1
- Bug 798854 - some error messages were eaten because each block didn't return
  the same value for the block. (ccoleman@redhat.com)

* Wed Feb 29 2012 Dan McPherson <dmcphers@redhat.com> 0.87.11-1
- move to application layout since simple isn't ready (johnp@redhat.com)
- Add mthompso@redhat.com to promo mailing list (ccoleman@redhat.com)
- switch to simple layout for password reset (johnp@redhat.com)
- show errors (johnp@redhat.com)
- make sure streamline return the correct result when resetting password
  (johnp@redhat.com)
- render password reset with the correct layout (johnp@redhat.com)
- Another fix for BZ796075 (fotios@redhat.com)
- Fix for BZ796075. Moved _console.scss -> console.scss to reduce confusion,
  since its not a partial. Removed left over import in _responsive.scss to
  unbreak (fotios@redhat.com)
- styles to force word-wrap when needed (sgoodwin@redhat.com)
- fix wrong cased OpenShift (dmcphers@redhat.com)
- Merge branch 'master' of git:/srv/git/li (ccoleman@redhat.com)
- Loading icon not being displayed on staging (bad URL), and overly aggressive
  string aggregation in error messages leads to bad text.  Bug 797747
  (ccoleman@redhat.com)
- Breadcrumbs matching style (ccoleman@redhat.com)

* Tue Feb 28 2012 Dan McPherson <dmcphers@redhat.com> 0.87.10-1
- add an id to the control group so sauce can check for error conditions
  (johnp@redhat.com)
- Merge branch 'master' of git1.ops.rhcloud.com:/srv/git/li (lnader@redhat.com)
- Integrated app details page to new console markup and css (ffranz@redhat.com)
- Merge branch 'master' of git1.ops.rhcloud.com:/srv/git/li (lnader@redhat.com)
- Bug 797296 - [REST API] API allowed creation of key with 8000 character name
  (lnader@redhat.com)
- Merge branch 'master' of git1.ops.rhcloud.com:/srv/git/li (ffranz@redhat.com)
- add class and id markup so sauce tests can easily find elements
  (johnp@redhat.com)
- Integrated app details page to new console markup and css (ffranz@redhat.com)
- Bug 797296 - [REST API] API allowed creation of key with 8000 character name
  (lnader@redhat.com)
- Bug 797296 - [REST API] API allowed creation of key with 8000 character name
  (lnader@redhat.com)
- Integrated app details page to new console markup and css (ffranz@redhat.com)
- bug 798128 fix (sgoodwin@redhat.com)
- console css edit (sgoodwin@redhat.com)
- console updates (sgoodwin@redhat.com)
- Integrating markup and style for the new console (ffranz@redhat.com)
- Check in change to bootstrap (ccoleman@redhat.com)

* Mon Feb 27 2012 Dan McPherson <dmcphers@redhat.com> 0.87.9-1
- Added correct permissions for status site (fotios@redhat.com)

* Mon Feb 27 2012 Dan McPherson <dmcphers@redhat.com> 0.87.8-1
- Fixing site unit test to account for Bugz 797307 (kraman@gmail.com)
- make errors show up on the domain edit account page (johnp@redhat.com)

* Mon Feb 27 2012 Dan McPherson <dmcphers@redhat.com> 0.87.7-1
- start selenium tests for new console (johnp@redhat.com)
- Merge branch 'master' of git1.ops.rhcloud.com:/srv/git/li (ffranz@redhat.com)
- Added cartridge related Rails stuff (ffranz@redhat.com)
- Test failure on def argument (ccoleman@redhat.com)
- Can't create keys until domain exists (ccoleman@redhat.com)
- Merge branch 'dev0227' (sgoodwin@redhat.com)
- new console specific styles (sgoodwin@redhat.com)
- Bug 795538 - not copying :content errors to :raw_content, hidden by bad unit
  tests (ccoleman@redhat.com)
- Keys controller test was building content incorrectly (ccoleman@redhat.com)
- changes addressing default list margin issues and moved a couple things from
  type to custom (sgoodwin@redhat.com)
- Use old layout for reset password, bug 797749 (ccoleman@redhat.com)
- cleanup all the old command usage in help and messages (dmcphers@redhat.com)

* Sun Feb 26 2012 Dan McPherson <dmcphers@redhat.com> 0.87.6-1
- 

* Sun Feb 26 2012 Dan McPherson <dmcphers@redhat.com> 0.87.5-1
- Add ribbon magic, start pulling variables out, realized that $gridGutterWidth
  is not constant in all responsive layouts. (ccoleman@redhat.com)
- Start using bootstrap styles, quick example of community markup from drupal
  (which can be changed), convert to SASS for navigation elements
  (ccoleman@redhat.com)
- Get ribbon perfected (ccoleman@redhat.com)
- Working prototype of community blog page (ccoleman@redhat.com)
- Merge branch 'dev/clayton/branding1' (ccoleman@redhat.com)
- More changes to community (ccoleman@redhat.com)
- Start prepping markup for community site (ccoleman@redhat.com)

* Sat Feb 25 2012 Dan McPherson <dmcphers@redhat.com> 0.87.4-1
- Log errors on test failure (ccoleman@redhat.com)
- Allow users to access new console in preview state (ccoleman@redhat.com)
- Fix tc_console failures, revert tc_signup.rb to see if we can trigger the
  failure again (ccoleman@redhat.com)
- Use absolute path on logo (ccoleman@redhat.com)
- Integrate sass-twitter-bootstrap temporarily (should be gem'd), begin moving
  override code out of _custom.scss and into variables and sections that mimic
  their origin (ccoleman@redhat.com)
- Bug 797270 is on Q/A.  Fix the test. (rmillner@redhat.com)
- Indentation was off by one space, causing build errors. (rmillner@redhat.com)
- Add preview message and links for the Management Console
  (ccoleman@redhat.com)
- Fixed location of applications partial (fotios@redhat.com)
- Merge branch 'master' into dev/clayton/app_tests (ccoleman@redhat.com)
- Added ability to status site to sync upon starting up (fotios@redhat.com)
- Functionals are running, errors are being returned, specific exceptions
  arechecked and thrown. (ccoleman@redhat.com)
- add obsoletes of old package (dmcphers@redhat.com)
- renaming jbossas7 (dmcphers@redhat.com)
- Handing application list over to ffranz (fotios@redhat.com)
- Helper to create shared domain object for test suite (ccoleman@redhat.com)
- Prevent infinite loop on bad server response - try rename only once
  (ccoleman@redhat.com)
- Removed RH proxy from the rest client source (ffranz@redhat.com)
- Added basic cartridge information to the app details page (ffranz@redhat.com)
- Merge branch 'master' of git1.ops.rhcloud.com:/srv/git/li (ffranz@redhat.com)
- Merge branch 'master' into dev/clayton/app_tests (ccoleman@redhat.com)
- Server side validations (ccoleman@redhat.com)
- Merge branch 'master' of git1.ops.rhcloud.com:/srv/git/li (ffranz@redhat.com)
- Merge branch 'master' into dev/clayton/validation (ccoleman@redhat.com)
- Creation flow and key flow tests (ccoleman@redhat.com)
- minor style edits (sgoodwin@redhat.com)
- Update for jboss-as-7.1.0.Final (starksm64@gmail.com)
- Temporary commit to build (ffranz@redhat.com)
- Fixed several interface bugs (style and markup) (ffranz@redhat.com)
- Tests on server validation, local error handling (ccoleman@redhat.com)
- Removed that message from hell, embedded model of the rest api client
  (ffranz@redhat.com)
- Reverted production.rb (ffranz@redhat.com)
- Created ActiveResource structure for cartridges and embedded
  (ffranz@redhat.com)
- Add validation logic from server (ccoleman@redhat.com)
- Created ActiveResource structure for cartridges and embedded
  (ffranz@redhat.com)
- Temporary commit to build (ffranz@redhat.com)
- Added sqlite3 to Gemfile to correspond with site.spec (fotios@redhat.com)
- work with applications details page layout (johnp@redhat.com)
- Fix for BZ796812 (fotios@redhat.com)
- Revert Gemfile change (ccoleman@redhat.com)
- make the application title look better (johnp@redhat.com)
- Added top level content id (ccoleman@redhat.com)
- Fixed misaligned toolbar (ccoleman@redhat.com)
- Merge branch 'dev/clayton/loading' (ccoleman@redhat.com)
- Toolbar loading icon, correct styles in various forms (ccoleman@redhat.com)
- Add back button to application details page (ccoleman@redhat.com)
- Merge branch 'master' into dev/clayton/loading (ccoleman@redhat.com)
- Loading tweaks (ccoleman@redhat.com)
- loader and styles for config app form (sgoodwin@redhat.com)
- Forms with loading, use form-inline where possible, disable form submit while
  submitting (ccoleman@redhat.com)
- Add sqlite-ruby to gemfile (ccoleman@redhat.com)
- make cancel button go back to the refering page (johnp@redhat.com)
- fix up application list layout a bit (johnp@redhat.com)
- revert to claytons styles (sgoodwin@redhat.com)
- Merge branch 'master' into dev/clayton/loading (ccoleman@redhat.com)
- Display loading content when form submit occurs (ccoleman@redhat.com)
- revert jboss 7.1 changes (dmcphers@redhat.com)
- quick fix to CSRF security bug (johnp@redhat.com)
- Merge branch 'master' of git1.ops.rhcloud.com:/srv/git/li (lnader@redhat.com)
- bug fixes (lnader@redhat.com)
- merge with my latest edits (sgoodwin@redhat.com)
- Update for jboss-as-7.1.0.Final (starksm64@gmail.com)
- Merge branch 'dev/clayton/header' (ccoleman@redhat.com)
- Make utility-nav drop below application list on small screens
  (ccoleman@redhat.com)
- Fix small device issues with footer (ccoleman@redhat.com)
- US1736: OpenShift status page (fotios@redhat.com)
- Reorder button in namespace section (ccoleman@redhat.com)
- More header tweaks via steve, fix not found error on Domain#edit
  (ccoleman@redhat.com)
- Removal of remaining :simple => true flags (ccoleman@redhat.com)
- Round one, transition console header (ccoleman@redhat.com)
- Update forms with back buttons, move :simple flag up into bootstrap form
  builder (ccoleman@redhat.com)
- Updates to forms to have better layout (ccoleman@redhat.com)
- Preparation for transitional styles, integrate fonts, fix weight to be normal
  (ccoleman@redhat.com)
- footer styles (sgoodwin@redhat.com)
- moved styleguide only styles to page level (sgoodwin@redhat.com)
- error thumbnail and defaul button edits (sgoodwin@redhat.com)
- Better unit tests for error handling, throw and log more detailed exception
  when server response is unexpected, and properly display composite errors on
  application creation page. (ccoleman@redhat.com)

* Wed Feb 22 2012 Dan McPherson <dmcphers@redhat.com> 0.87.3-1
- add tests for the show application page (johnp@redhat.com)
- add tests for the applications list page (johnp@redhat.com)
- Text cleanup and form help (ccoleman@redhat.com)
- Use btn-mini, remove unused partial (ccoleman@redhat.com)
- Fix and update raw_content to be cleaner and fix bugs, some almost final
  styles (ccoleman@redhat.com)
- Saving with validation clears update_id (ccoleman@redhat.com)
- Add domains controller (ccoleman@redhat.com)
- Bug 795628 (ccoleman@redhat.com)
- set jboss version back for now (dmcphers@redhat.com)
- update jboss version (dmcphers@redhat.com)
- Cleanup of spacing, elements, names, and page titles (ccoleman@redhat.com)
- Merge branch 'dev/clayton/keys' (ccoleman@redhat.com)
- Fixup failing test (ccoleman@redhat.com)
- Overhaul of keys to work around existing defects (ccoleman@redhat.com)

* Mon Feb 20 2012 Dan McPherson <dmcphers@redhat.com> 0.87.2-1
- Styleguide should use split files (ccoleman@redhat.com)
- Pull out help links into their own helper URLs to minimize changes
  (ccoleman@redhat.com)
- Update my account with lost changes (ccoleman@redhat.com)
- Switch to split CSS files (ccoleman@redhat.com)
- Merge branch 'dev/clayton/units' (ccoleman@redhat.com)
- Split unit and integration tests for rest_api_test.rb (ccoleman@redhat.com)
- default bootstrap css (sgoodwin@redhat.com)
- customizations to bootstrap.css (sgoodwin@redhat.com)
- Unit test for 794764 (ccoleman@redhat.com)
- Fixes 794764: added Node.js to the list of standalone cartridges on website
  (ffranz@redhat.com)
- changes for US1797 (abhgupta@redhat.com)
- Remove puts (ccoleman@redhat.com)
- Update references to @application_type to work around issue with
  ActiveResource serialization for now (ccoleman@redhat.com)
- Use 'console' layout on User.show (ccoleman@redhat.com)
- Fixed bug 794643 by temporarily removing application_type getter
  (ccoleman@redhat.com)
- Merge branch 'master' into dev/clayton/layouts (ccoleman@redhat.com)
- Fixes 794539: staging and production routes was redirecting the account
  creation to the control panel (ffranz@redhat.com)
- Tweak text (ccoleman@redhat.com)
- Add Node.js, remove version label and website (for now), and add :new marker
  (ccoleman@redhat.com)
- Add more aggressive guard to logging exceptions (ccoleman@redhat.com)
- Merge branch 'master' into dev/clayton/layouts (ccoleman@redhat.com)
- <model>.first returns null if no items Fix domain name link for bug 790695
  (ccoleman@redhat.com)
- Add in more extensive key unit tests, fix a connection allocation bug, make
  unit tests reuse same user and teardown domain, fix layout of simple semantic
  forms, implement simple ssh key form for use within get_started
  (ccoleman@redhat.com)

* Thu Feb 16 2012 Dan McPherson <dmcphers@redhat.com> 0.87.1-1
- bump spec numbers (dmcphers@redhat.com)
- Added contextual help on the app details page for the new console
  (ffranz@redhat.com)
- Added contextual help on the app details page for the new console
  (ffranz@redhat.com)
- Merge branch 'master' of git1.ops.rhcloud.com:/srv/git/li (ffranz@redhat.com)
- Fixed errors that caused Sauce tests failures (ffranz@redhat.com)
- label style edits (sgoodwin@redhat.com)
- Merge branch 'dev2' (sgoodwin@redhat.com)
- edits for get started and other page styles (sgoodwin@redhat.com)

* Thu Feb 16 2012 Dan McPherson <dmcphers@redhat.com> 0.86.9-1
- add style change to My Applications (johnp@redhat.com)
- allow mutable attrs to be added one at a time (johnp@redhat.com)

* Wed Feb 15 2012 Dan McPherson <dmcphers@redhat.com> 0.86.8-1
- restyle application list to new boostrap styles (johnp@redhat.com)
- bug 790635 (wdecoste@localhost.localdomain)
- add the config.base_domain var to all config files (johnp@redhat.com)
- Merge branch 'dev' (sgoodwin@redhat.com)
- style addtions for code pre and append-prepend (sgoodwin@redhat.com)

* Tue Feb 14 2012 Dan McPherson <dmcphers@redhat.com> 0.86.7-1
- Developer fails at understanding core principles of coding
  (ccoleman@redhat.com)
- have rest api ActiveResource implement ActiveModel::Dirty (johnp@redhat.com)

* Tue Feb 14 2012 Dan McPherson <dmcphers@redhat.com> 0.86.6-1
- Minor wording tweaks (ccoleman@redhat.com)
- Tweak rendering of domain name to make it more accurate (ccoleman@redhat.com)
- Merge branch 'master' into dev/clayton/nextsteps (ccoleman@redhat.com)
- Flushed out getting started content (ccoleman@redhat.com)
- Merge branch 'dev' (sgoodwin@redhat.com)
- styleguide additions (sgoodwin@redhat.com)
- Merge branch 'master' into dev/clayton/nextsteps (ccoleman@redhat.com)
- Merge branch 'master' of ssh://git1.ops.rhcloud.com/srv/git/li
  (ccoleman@redhat.com)
- Next steps page round #1 (ccoleman@redhat.com)
- .reload required to refresh .applications list (ccoleman@redhat.com)
- Improved app details page looking (ffranz@redhat.com)
- Merge branch 'dev0213' (sgoodwin@redhat.com)
- updates for create app fow (sgoodwin@redhat.com)
- Move types around (ccoleman@redhat.com)
- Further iteration on index views and confirm views, more railsisms and
  simplifications (ccoleman@redhat.com)
- Bug 790323 - consistent display of framework value (ccoleman@redhat.com)
- Merge branch 'master' of git1.ops.rhcloud.com:/srv/git/li (ffranz@redhat.com)
- New console: added some more information to app details page
  (ffranz@redhat.com)

* Mon Feb 13 2012 Dan McPherson <dmcphers@redhat.com> 0.86.5-1
- Disable broken tests for new REST API/Applications controller
  (aboone@redhat.com)

* Mon Feb 13 2012 Dan McPherson <dmcphers@redhat.com> 0.86.4-1
- Replace print with Rails.logger.debug in PromoCodeMailer
  (ccoleman@redhat.com)
- Merge branch 'dev/clayton/wizards' (ccoleman@redhat.com)
- Make framework_name safer, throw ApplicationType::NotFound on errors
  (ccoleman@redhat.com)
- Fix a typo in site unit tests (aboone@redhat.com)
- Use bootstrap styles for select boxes Refactor filtering logic to be simpler
  and extract a model objec t Some railisms for naming of partials Added
  Application.framework_name which does a lookup on Applicat ionType to get the
  pretty name (ccoleman@redhat.com)
- hook up app filtering again and modify for rest api (johnp@redhat.com)
- Merge branch 'master' of git1.ops.rhcloud.com:/srv/git/li (ffranz@redhat.com)
- New console: shows basic application info, dedicated application details page
  (ffranz@redhat.com)
- fix domain_delete test since we can't have more than one domain right now
  (johnp@redhat.com)
- messages doesn't exist on the application object anymore (johnp@redhat.com)
- fix custom_id for both nonmutable and mutable ids and add tests
  (johnp@redhat.com)
- add the destroy code for app deletion (johnp@redhat.com)
- Active state for clicking on the type elements (ccoleman@redhat.com)
- Move to 'wizard_steps' styles, fix chrome link clicking (with window.location
  = <> instead of jquery.trigger/click()) (ccoleman@redhat.com)

* Mon Feb 13 2012 Dan McPherson <dmcphers@redhat.com> 0.86.3-1
- Allow application list to be shown with no domain (ccoleman@redhat.com)
- Merge branch 'master' of ssh://git1.ops.rhcloud.com/srv/git/li
  (ccoleman@redhat.com)
- When dynamic loading occurs, exception for ActiveResource isn't loaded. In
  staging and production, the console/* and account/* urls should redirect to
  the control panel (ccoleman@redhat.com)
- Rescue ActiveResource errors and put their info in the rack env, also ensure
  no_info.html.haml is properly accessed (ccoleman@redhat.com)
- Merge branch 'dev/clayton/activeresource_clean' (ccoleman@redhat.com)
- Return after rendering (ccoleman@redhat.com)
- Flush out applications_controller#save (ccoleman@redhat.com)
- Flatten model structure for better Railsisms, rename unit test modules.
  (ccoleman@redhat.com)
- Unit tests pass, assignment is working (ccoleman@redhat.com)
- Refactoring out RestApi to have autoloading work for rails
  (ccoleman@redhat.com)
- Improve rendering and details of applications (ccoleman@redhat.com)

* Mon Feb 13 2012 Dan McPherson <dmcphers@redhat.com> 0.86.2-1
- Fix for bug 788691 - show app deletion errors in the right place
  (aboone@redhat.com)
- Fix bug 789826 - restrict size of twitter avatars (aboone@redhat.com)
- Revert "require rest_api" - it seems this is reaking havok with tests
  (johnp@redhat.com)
- have the applications controller use the get_application API
  (johnp@redhat.com)
- add get_application convinience method to Domain (johnp@redhat.com)
- pass in options when instantiating a connection in find_single
  (johnp@redhat.com)
- require rest_api (johnp@redhat.com)
- hook up delete app again and port to active resources API (johnp@redhat.com)
- revamp styleguide (sgoodwin@redhat.com)
- Fix break in tests - no need for explicit requrie, and unit tests shouldn't
  be run from non-comand line includes (ccoleman@redhat.com)
- update to use new activecontroller APIs for showing data (johnp@redhat.com)
- add helper functions to the app model for getting the app's URLs
  (johnp@redhat.com)
- Bug 789281 - Explicitly set EXECJS_RUNTIME and disable barista autocompile
  (ccoleman@redhat.com)
- Tomporarily commenting out REST api tests on site (kraman@gmail.com)
- Create a new console controller which will route to applications (eventually
  we will have more complex flow here) (ccoleman@redhat.com)
- Integrate app creation workflow into new console (ccoleman@redhat.com)
- Merge branch 'master' into dev/clayton/createapp (ccoleman@redhat.com)
- Update navigation with new application controller (ccoleman@redhat.com)
- Remove fixed position header CSS, handled flash[:success] messages correctly
  (ccoleman@redhat.com)
- Merge branch 'master' into dev/clayton/bootstrap (ccoleman@redhat.com)
- Formtastic bootstrap markup is only enabled when before_filter :new_forms is
  defined Simple layout updated to be roughly consistent for now
  (ccoleman@redhat.com)
- Updated formtastic to get close to bootstrap (ccoleman@redhat.com)
- ordered list unstyled (sgoodwin@redhat.com)
- add the add an application link (johnp@redhat.com)
- Active Resource - allow toggling between integrated tests and mock tests
  (aboone@redhat.com)
- ActiveResource - fix create/update, other fixes (aboone@redhat.com)
- Reenable create link until it can be contextual (ccoleman@redhat.com)
- add application (johnp@redhat.com)
- implement delete app (johnp@redhat.com)
- add a delete button and confirm page (johnp@redhat.com)
- commit the filter template and add a flash message to index
  (johnp@redhat.com)
- make filters work (johnp@redhat.com)
- handle nil values (johnp@redhat.com)
- further filter additions (johnp@redhat.com)
- initial filter support (johnp@redhat.com)
- fix typo - point to app_list not app_info (johnp@redhat.com)
- make sure ApplicationsController is correctly defined (johnp@redhat.com)
- add the app list and info templates (johnp@redhat.com)
- added controller and route for console/applications (johnp@redhat.com)
- updated styleguide to use bootstrap (sgoodwin@redhat.com)
- General cleanup and refactoring of My Account and related forms to match new
  console layout Clean up flash presentation Begin investigating formtastic
  layout (ccoleman@redhat.com)
- Merge branch 'dev/sgoodwin/bootstrap' (sgoodwin@redhat.com)
- incorporate bootstrap (sgoodwin@redhat.com)
- Simple application type controller, layout, and default type population
  (ccoleman@redhat.com)
- Creating models for descriptor Fixing manifest files Added command to list
  installed cartridges and get descriptors (kraman@gmail.com)
- Revert "Added status subsite" (fotios@redhat.com)
- Merge branch 'master' of ssh://git1.ops.rhcloud.com/srv/git/li
  (ccoleman@redhat.com)
- Fix streamline test (ccoleman@redhat.com)
- Removed test status db (fotios@redhat.com)
- Added status subsite (fotios@redhat.com)
- Merge branch 'dev/clayton/activeresource' (ccoleman@redhat.com)
- Comment out failing unit tests until bugs are fixed (ccoleman@redhat.com)
- Deserialize remote errors on 422 ResourceInvalid Delete properly passes
  requests down Expose 'login' as an alias to 'rhlogin' (ccoleman@redhat.com)
- Also use the SSH key display name in the edit form (aboone@redhat.com)
- Cleanup of names, better formatting, and inline doc (ccoleman@redhat.com)
- Add application, domain, and a backport of an activeresource association
  framework (ccoleman@redhat.com)
- fix bug 787079 with long ssh key names, also create and use @ssh_key.to_s
  method (aboone@redhat.com)
- Infrastructure for new layouts (ccoleman@redhat.com)
- Changed bootstrap css: responsive design improvements (ffranz@redhat.com)
- Initial support for retrieving user info (ccoleman@redhat.com)
- Remove openshift.rb, moved to rest_api.rb but bungled the merge
  (ccoleman@redhat.com)
- Merge branch 'dev/clayton/activeresource' of
  ssh://git1.ops.rhcloud.com/srv/git/li into dev/clayton/activeresource
  (ccoleman@redhat.com)
- More tests, make :as required, pass :as through, merge changes from upstream
  that simplify how the get{} connection method works (ccoleman@redhat.com)
- Add timeout of 3s for simple cases (ccoleman@redhat.com)
- Clarified names of SSH key attributes to match server (ccoleman@redhat.com)
- Able to make requests to server, next steps are serialization deserialization
  mapping for wierd backends (ccoleman@redhat.com)
- Expand authentication (ccoleman@redhat.com)
- More tests, able to hit server (ccoleman@redhat.com)
- Set cookie based on user object, pass user object to find / delete
  (ccoleman@redhat.com)
- Getting user aware connections working (ccoleman@redhat.com)
- Simple active resource ssh keys (ccoleman@redhat.com)
- Fix four failing unit tests (ccoleman@redhat.com)
- Merge branch 'dev/clayton/bootstrap' (ccoleman@redhat.com)
- Merge branch 'master' into dev/clayton/my_account_latest
  (ccoleman@redhat.com)
- Clarified names of SSH key attributes to match server (ccoleman@redhat.com)
- Able to make requests to server, next steps are serialization deserialization
  mapping for wierd backends (ccoleman@redhat.com)
- Expand authentication (ccoleman@redhat.com)
- More tests, able to hit server (ccoleman@redhat.com)
- Set cookie based on user object, pass user object to find / delete
  (ccoleman@redhat.com)
- Getting user aware connections working (ccoleman@redhat.com)
- Simple active resource ssh keys (ccoleman@redhat.com)
- Updated to use styleguide instead of bootstrap for clarity, available via
  /app/styleguide (ccoleman@redhat.com)
- Workaround removed method (ccoleman@redhat.com)
- add a ssh success message to the en locale (johnp@redhat.com)
- display ssh key or edit box depending if it is set (johnp@redhat.com)
- correctly update ssh key (johnp@redhat.com)
- initial addition of sshkey updating (johnp@redhat.com)
- make work if ssh key is not yet set (johnp@redhat.com)
- keep sshkey if set when updating namespace, add start of ssh update
  (johnp@redhat.com)
- refactor edit to point to edit_namespace since we are adding edit_ssh
  (johnp@redhat.com)
- render flash messages on account page (johnp@redhat.com)
- use partial to render both create and update keys (johnp@redhat.com)
- [namespace update] stay on edit page on error and flash error message
  (johnp@redhat.com)
- make updating domains from accounts page work (johnp@redhat.com)
- initial edit namespace from accounts (johnp@redhat.com)
- Help link is correct Moved reset password to change password form
  (ccoleman@redhat.com)
- My account in mostly final form (ccoleman@redhat.com)
- All password behavior is functional (ccoleman@redhat.com)
- Use semantic_form_for on new password Provide ActiveModel like
  request_password_reset models Allow validation for :change_password and
  :reset_password scopes (ccoleman@redhat.com)
- Enable user model based change_password method in streamline Use
  semantic_form_tag in change password (ccoleman@redhat.com)
- Comment out path for now (ccoleman@redhat.com)
- More tweaking (ccoleman@redhat.com)
- Update routes to match older paths (ccoleman@redhat.com)
- Password controller unit tests (ccoleman@redhat.com)
- Remove warning in view (ccoleman@redhat.com)
- Tweaking layout of ssh_key to use semantic_form_tag (ccoleman@redhat.com)
- More experimentation with users (ccoleman@redhat.com)
- Restored changes for UserController.reset / request_reset
  (ccoleman@redhat.com)
- Changes to templates to experiment with help (ccoleman@redhat.com)
- Create new password controller, create new /account structure, add some
  simple helper forms for inline domain display.  Needs lots more testing but
  represents a simple my account.  Access via /app/account while authenticated.
  (ccoleman@redhat.com)
- Bootstrap controller (ccoleman@redhat.com)

* Fri Feb 03 2012 Dan McPherson <dmcphers@redhat.com> 0.86.1-1
- bump spec numbers (dmcphers@redhat.com)

* Thu Feb 02 2012 Dan McPherson <dmcphers@redhat.com> 0.85.15-1
- Properly pass ticket when adding/updating/deleting SSH keys
  (aboone@redhat.com)

* Wed Feb 01 2012 Dan McPherson <dmcphers@redhat.com> 0.85.14-1
- Merge branch 'master' of git1.ops.rhcloud.com:/srv/git/li (ffranz@redhat.com)
- Fixes 785654: added horizontal scroll with overflow-x (ffranz@redhat.com)
- Fix an issue w/ SSH key deletion (aboone@redhat.com)
- Ensure additional SSH key is valid before attempting to persist (BZ 785867)
  (aboone@redhat.com)
- Fix display of SSH keys with long names (bugzilla 786382) (aboone@redhat.com)
- More agressively shorten invalid SSH key so it fits in error message
  (aboone@redhat.com)

* Tue Jan 31 2012 Dan McPherson <dmcphers@redhat.com> 0.85.13-1
- Adding a selenium test for SSH keys and a couple of markup tweaks to support
  it (aboone@redhat.com)
- Show default key as "default" instead of "Primary" on site (BZ 785953)
  (aboone@redhat.com)

* Mon Jan 30 2012 Dan McPherson <dmcphers@redhat.com> 0.85.12-1
- update json version (dmcphers@redhat.com)

* Mon Jan 30 2012 Dan McPherson <dmcphers@redhat.com> 0.85.11-1
- update treetop refs (dmcphers@redhat.com)

* Mon Jan 30 2012 Dan McPherson <dmcphers@redhat.com> 0.85.10-1
- Revert changes to development.log in site,broker,devenv spec
  (aboone@redhat.com)
- Reduce number of rubygem dependencies in site build (aboone@redhat.com)

* Sat Jan 28 2012 Dan McPherson <dmcphers@redhat.com> 0.85.9-1
- 

* Sat Jan 28 2012 Alex Boone <aboone@redhat.com> 0.85.8-1
- Site build - don't use bundler, install all gems via RPM (aboone@redhat.com)

* Fri Jan 27 2012 Dan McPherson <dmcphers@redhat.com> 0.85.7-1
- POST to delete SSH keys instead of DELETE - browser compatibility
  (aboone@redhat.com)
- manage multiple SSH keys via the site control panel (aboone@redhat.com)
- Refactor ExpressApi to expose a class-level http_post method
  (aboone@redhat.com)
- Add a helper to generate URLs to the user guide for future topics
  (ccoleman@redhat.com)
- Another fix for build issue created in 532e0e8 (aboone@redhat.com)
- Fix for 532e0e8, also properly set permissions on logs (aboone@redhat.com)
- Remove therubyracer gem dependency, "js" is already being used
  (aboone@redhat.com)
- Unit tests all pass (ccoleman@redhat.com)
- Make streamline_mock support newer api methods (ccoleman@redhat.com)
- Streamline library changes (ccoleman@redhat.com)
- Provide barista dependencies at site build time (aboone@redhat.com)
- Add BuildRequires: rubygem-crack for site spec (aboone@redhat.com)
- remove old obsoletes (dmcphers@redhat.com)
- Consistently link to the Express Console via /app/control_panel
  (aboone@redhat.com)
- Allow app names up to 32 chars (fix BZ 784454) (aboone@redhat.com)
- remove generated javascript from git; generate during build
  (johnp@redhat.com)
- reflow popups if they are clipped by the document viewport (johnp@redhat.com)
- Fixed JS error 'body not defined' caused by previous commit
  (ccoleman@redhat.com)
- cleanup (dmcphers@redhat.com)

* Tue Jan 25 2012 John (J5) Palmieri <johnp@redhat.com> 0.85.6-1
- remove generated javascript and use rake to generate
  javascript during the build

* Tue Jan 24 2012 Dan McPherson <dmcphers@redhat.com> 0.85.5-1
- Remove floating header to reduce problems on iPad/iPhone
  (ccoleman@redhat.com)

* Fri Jan 20 2012 Mike McGrath <mmcgrath@redhat.com> 0.85.4-1
- merge and ruby-1.8 prep (mmcgrath@redhat.com)

* Wed Jan 18 2012 Dan McPherson <dmcphers@redhat.com> 0.85.3-1
- Fix documentation links (aboone@redhat.com)

* Tue Jan 17 2012 Dan McPherson <dmcphers@redhat.com> 0.85.2-1
- Adding Flex Monitoring and Scaling video for Chinese viewers
  (aboone@redhat.com)

* Fri Jan 13 2012 Dan McPherson <dmcphers@redhat.com> 0.85.1-1
- bump spec numbers (dmcphers@redhat.com)
- Adding China-hosted Flex - Deploying Seam video (BZ 773191)
  (aboone@redhat.com)
