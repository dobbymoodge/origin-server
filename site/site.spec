%if 0%{?fedora}%{?rhel} <= 6
    %global scl ruby193
    %global scl_prefix ruby193-
%endif
%global rubyabi 1.9.1
%define htmldir %{_var}/www/html
%define sitedir %{_var}/www/openshift/site

Summary:   OpenShift Site Rails application
Name:      rhc-site
Version: 1.9.13
Release:   2%{?dist}
Group:     Network/Daemons
License:   ASL 2.0
URL:       http://openshift.redhat.com
Source0:   rhc-site-%{version}.tar.gz
BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
Requires:       %{?scl:%scl_prefix}ruby(abi) = %{rubyabi}
Requires:       %{?scl:%scl_prefix}ruby
Requires:       %{?scl:%scl_prefix}rubygems
Requires:       %{?scl:%scl_prefix}mod_passenger
Requires:       %{?scl:%scl_prefix}rubygem-passenger-native-libs
Requires:       rubygem(openshift-origin-console)
Requires:       %{?scl:%scl_prefix}rubygem(recaptcha)
Requires:       %{?scl:%scl_prefix}rubygem(wddx)
Requires:       %{?scl:%scl_prefix}rubygem(sinatra)
Requires:       %{?scl:%scl_prefix}rubygem(sqlite3)
Requires:       %{?scl:%scl_prefix}rubygem(httparty)
Requires:       rhc-site-static
Requires:       openshift-origin-util-scl
Requires:       %{?scl:%scl_prefix}rubygem(angular-rails)
Requires:       %{?scl:%scl_prefix}rubygem(ci_reporter)
Requires:       %{?scl:%scl_prefix}rubygem(coffee-rails)
Requires:       %{?scl:%scl_prefix}rubygem(compass-rails)
Requires:       %{?scl:%scl_prefix}rubygem(jquery-rails)
Requires:       %{?scl:%scl_prefix}rubygem(mocha)
Requires:       %{?scl:%scl_prefix}rubygem(sass-rails)
Requires:       %{?scl:%scl_prefix}rubygem(simplecov)
Requires:       %{?scl:%scl_prefix}rubygem(test-unit)
Requires:       %{?scl:%scl_prefix}rubygem(uglifier)
Requires:       %{?scl:%scl_prefix}rubygem(webmock)
Requires:       %{?scl:%scl_prefix}rubygem(therubyracer)
Requires:       %{?scl:%scl_prefix}rubygem(rack-recaptcha)
Requires:       %{?scl:%scl_prefix}rubygem(rack-picatcha)
Requires:       %{?scl:%scl_prefix}rubygem(dalli)
Requires:       %{?scl:%scl_prefix}rubygem(countries)
Requires:       %{?scl:%scl_prefix}rubygem(poltergeist)
Requires:       %{?scl:%scl_prefix}rubygem(konacha)
Requires:       %{?scl:%scl_prefix}rubygem(minitest)
Requires:       %{?scl:%scl_prefix}rubygem(rspec-core)

%if 0%{?fedora}%{?rhel} <= 6
BuildRequires:  ruby193-build
BuildRequires:  scl-utils-build
%endif

BuildRequires:  %{?scl:%scl_prefix}ruby(abi) = %{rubyabi}
BuildRequires:  %{?scl:%scl_prefix}ruby
BuildRequires:  %{?scl:%scl_prefix}rubygems
BuildRequires:  %{?scl:%scl_prefix}rubygems-devel
BuildRequires:  %{?scl:%scl_prefix}rubygem(angular-rails)
BuildRequires:  %{?scl:%scl_prefix}rubygem(rails)
BuildRequires:  %{?scl:%scl_prefix}rubygem(compass-rails)
BuildRequires:  %{?scl:%scl_prefix}rubygem(mocha)
BuildRequires:  %{?scl:%scl_prefix}rubygem(simplecov)
BuildRequires:  %{?scl:%scl_prefix}rubygem(test-unit)
BuildRequires:  %{?scl:%scl_prefix}rubygem(ci_reporter)
BuildRequires:  %{?scl:%scl_prefix}rubygem(webmock)
BuildRequires:  %{?scl:%scl_prefix}rubygem(sprockets)
BuildRequires:  %{?scl:%scl_prefix}rubygem(rdiscount)
BuildRequires:  %{?scl:%scl_prefix}rubygem(formtastic)
BuildRequires:  %{?scl:%scl_prefix}rubygem(net-http-persistent)
BuildRequires:  %{?scl:%scl_prefix}rubygem(haml)
BuildRequires:  rubygem(openshift-origin-console)
BuildRequires:  %{?scl:%scl_prefix}rubygem(recaptcha)
BuildRequires:  %{?scl:%scl_prefix}rubygem(wddx)
BuildRequires:  %{?scl:%scl_prefix}rubygem(sinatra)
BuildRequires:  %{?scl:%scl_prefix}rubygem(sqlite3)
BuildRequires:  %{?scl:%scl_prefix}rubygem(httparty)
BuildRequires:  %{?scl:%scl_prefix}rubygem(therubyracer)
BuildRequires:  %{?scl:%scl_prefix}rubygem(rack-recaptcha)
BuildRequires:  %{?scl:%scl_prefix}rubygem(rack-picatcha)
BuildRequires:  %{?scl:%scl_prefix}rubygem(dalli)
BuildRequires:  %{?scl:%scl_prefix}rubygem(countries)
BuildRequires:  %{?scl:%scl_prefix}rubygem(poltergeist)
BuildRequires:  %{?scl:%scl_prefix}rubygem(konacha)
BuildRequires:  %{?scl:%scl_prefix}rubygem(minitest)
BuildRequires:  %{?scl:%scl_prefix}rubygem(rspec-core)

BuildArch:      noarch

%description
This contains the OpenShift website which manages user authentication,
authorization and also the workflows to request access.  It requires
the OpenShift Origin management console and specializes some of its
behavior.

%package static
Summary:   The static content for the OpenShift website
Requires: rhc-server-common

%description static
Static files that can be used even if the OpenShift site is not installed,
such as images, CSS, JavaScript, and HTML.

%prep
%setup -q

%build
%{?scl:scl enable %scl - << \EOF}

set -e

mkdir -p %{buildroot}%{_var}/log/openshift/site/
mkdir -m 770 %{buildroot}%{_var}/log/openshift/site/httpd/
touch %{buildroot}%{_var}/log/openshift/site/httpd/production.log
chmod 0666 %{buildroot}%{_var}/log/openshift/site/httpd/production.log

rm -f Gemfile.lock
bundle install --local

RAILS_ENV=production RAILS_HOST=openshift.redhat.com RAILS_RELATIVE_URL_ROOT=/app \
  RAILS_LOG_PATH=%{buildroot}%{_var}/log/openshift/site/httpd/production.log \
  CONSOLE_CONFIG_FILE=conf/console.conf \
  bundle exec rake assets:precompile assets:public_pages assets:generic_error_pages

find . -name .gitignore | xargs rm 
find . -name .gitkeep | xargs rm 
rm -rf tmp
rm -rf %{buildroot}%{_var}/log/openshift/*
rm -f Gemfile.lock

%{?scl:EOF}

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{htmldir}
mkdir -p %{buildroot}%{sitedir}
mkdir -p %{buildroot}%{sitedir}/run
mkdir -p %{buildroot}%{sitedir}/tmp/cache/assets
mkdir -p %{buildroot}/etc/openshift/

mkdir -p %{buildroot}%{_var}/log/openshift/site/
mkdir -m 770 %{buildroot}%{_var}/log/openshift/site/httpd/

mkdir -p %{buildroot}%{sitedir}/httpd/conf
mkdir -p %{buildroot}%{sitedir}/httpd/run

cp -r . %{buildroot}%{sitedir}
ln -s %{sitedir}/public %{buildroot}%{htmldir}/app
ln -sf /etc/httpd/conf/magic %{buildroot}%{sitedir}/httpd/conf/magic

cp conf/console.conf %{buildroot}/etc/openshift/
cp conf/console-devenv.conf %{buildroot}/etc/openshift/

%clean
rm -rf %{buildroot}

%post
if [ ! -f %{_var}/log/openshift/site/production.log ]; then
  /bin/touch %{_var}/log/openshift/site/production.log
  chown root:libra_user %{_var}/log/openshift/site/production.log
  chmod 660 %{_var}/log/openshift/site/production.log
fi

if [ ! -f %{_var}/log/openshift/site/development.log ]; then
  /bin/touch %{_var}/log/openshift/site/development.log
  chown root:libra_user %{_var}/log/openshift/site/development.log
  chmod 660 %{_var}/log/openshift/site/development.log
fi

%files
%attr(0770,root,libra_user) %{sitedir}/app/subsites/status/db
%attr(0660,root,libra_user) %config(noreplace) %{sitedir}/app/subsites/status/db/status.sqlite3
%attr(0740,root,libra_user) %{sitedir}/app/subsites/status/rhc-outage
%attr(0750,root,libra_user) %{sitedir}/script/site_ruby
%attr(0750,root,libra_user) %{sitedir}/script/enable-mini-profiler
%attr(0770,root,libra_user) %{sitedir}/tmp
%attr(0770,root,libra_user) %{sitedir}/tmp/cache
%attr(0770,root,libra_user) %{sitedir}/tmp/cache/assets
%attr(0770,root,libra_user) %{_var}/log/openshift/site/
%ghost %attr(0660,root,libra_user) %{_var}/log/openshift/site/production.log
%ghost %attr(0660,root,libra_user) %{_var}/log/openshift/site/development.log

%defattr(0640,root,libra_user,0750)
%{sitedir}
%{htmldir}/app
%config(noreplace) %{sitedir}/app/subsites/status/config/hosts.yml
%config(noreplace) /etc/openshift/console.conf
%config /etc/openshift/console-devenv.conf
%exclude %{sitedir}/public

%files static
%defattr(0640,root,libra_user,0750)
%{sitedir}/public

%changelog
* Sat Jun 08 2013 Adam Miller 1.9.13-2
- - Bump spec for site rebuild

* Fri Jun 07 2013 Adam Miller <admiller@redhat.com> 1.9.13-1
- Site summit changes, backported from bbe7f47f293c826be00ead46457377f475b810b7
  in master (ccoleman@redhat.com)
- Backport stage tests to stage now that packages are tagged
  (ccoleman@redhat.com)

* Sat Jun 01 2013 Dan McPherson <dmcphers@redhat.com> 1.9.12-1
- Merge pull request #1501 from nhr/STAGE_remove_tos_link
  (dmcphers+openshiftbot@redhat.com)
- Remove TOS link from site footer (hripps@redhat.com)
- Remove preview language (jliggitt@redhat.com)

* Thu May 30 2013 Adam Miller <admiller@redhat.com> 1.9.11-1
- Test signup flow more carefully (jliggitt@redhat.com)
- Fix bug 967746 - tolerate missing PROHIBITED_EMAIL_DOMAINS config value
  (jliggitt@redhat.com)
- Merge pull request #1455 from jtharris/email_blacklist
  (dmcphers+openshiftbot@redhat.com)
- Fix failing captcha test. (jharris@redhat.com)
- Code review suggestions. (jharris@redhat.com)
- Validation to reject prohibited email domains. (jharris@redhat.com)

* Wed May 29 2013 Adam Miller <admiller@redhat.com> 1.9.10-1
- Fix bug 966746 - remove unused legal controller and view content
  (jliggitt@redhat.com)
- Merge pull request #1474 from nhr/cancelled_status_handling
  (dmcphers+openshiftbot@redhat.com)
- Merge pull request #1476 from liggitt/help_page_beta_feedback
  (dmcphers+openshiftbot@redhat.com)
- Correct tests that now rely on #status_cd (hripps@redhat.com)
- Open support links in a new page, tolerate FAQ fetch failures
  (jliggitt@redhat.com)
- Merge pull request #1472 from liggitt/payment_collected_message
  (dmcphers+openshiftbot@redhat.com)
- Merge pull request #1471 from jtharris/analytics_logging
  (dmcphers+openshiftbot@redhat.com)
- Flip logic on account status check for readability (hripps@redhat.com)
- Revise tests for better coverage (hripps@redhat.com)
- Add My Account status messages for cancelled and pending cancelled accounts
  (hripps@redhat.com)
- Merge pull request #1470 from nhr/legal_statement_on_upgrade
  (dmcphers+openshiftbot@redhat.com)
- Show a message when payment will be collected (jliggitt@redhat.com)
- Log source entry from js analytics. (jharris@redhat.com)
- Added legal notice to upgrade confirmation page (hripps@redhat.com)

* Tue May 28 2013 Adam Miller <admiller@redhat.com> 1.9.9-1
- Merge pull request #1461 from liggitt/bug_966714_skip_content_link
  (dmcphers+openshiftbot@redhat.com)
- Merge pull request #1462 from
  liggitt/bug_966335_credit_card_images_at_narrow_width
  (dmcphers+openshiftbot@redhat.com)
- Fix bug 966335 - credit card images at narrow width (jliggitt@redhat.com)
- Fix bug 966714 - add style to hide 'skip to navigation' link in site pages
  (jliggitt@redhat.com)

* Fri May 24 2013 Adam Miller <admiller@redhat.com> 1.9.8-1
- Fix site extended test, tolerate missing error codes from Aria
  (jliggitt@redhat.com)
- Improve payment page errors (jliggitt@redhat.com)
- Merge pull request #1453 from
  smarterclayton/bug_966499_properly_rescue_auth_denied
  (dmcphers+openshiftbot@redhat.com)
- Merge branch 'master' of github.com:openshift/li (admiller@redhat.com)
- Merge pull request #1450 from spurtell/spurtell/analytics
  (dmcphers+openshiftbot@redhat.com)
- Bug 966499 - Properly handle REST API access revocation (ccoleman@redhat.com)
- Added source tracking to new account form (spurtell@redhat.com)

* Thu May 23 2013 Adam Miller <admiller@redhat.com> 1.9.7-1
- Merge pull request #1439 from liggitt/dashboard_layout
  (dmcphers+openshiftbot@redhat.com)
- Merge pull request #1442 from smarterclayton/better_mail_config
  (dmcphers+openshiftbot@redhat.com)
- Move debug code out of show method Update disclaimer to mention unbilled
  usage from other billing periods (jliggitt@redhat.com)
- Allow upgrade layout to be vertical or horizontal (jliggitt@redhat.com)
- Improve dashboard layout, add last_bill with tests (jliggitt@redhat.com)
- Merge pull request #1444 from smarterclayton/prevent_unrescued_errors
  (dmcphers+openshiftbot@redhat.com)
- The site should rescue exceptions and report reference IDs as much as
  possible (ccoleman@redhat.com)
- Better mail config, allow SMTP to be set by ops (ccoleman@redhat.com)

* Wed May 22 2013 Adam Miller <admiller@redhat.com> 1.9.6-1
- Merge pull request #1438 from liggitt/bug_963640_blank_state_allowed
  (dmcphers+openshiftbot@redhat.com)
- Fix bug 963640 - don't allow blank state in IE (jliggitt@redhat.com)

* Wed May 22 2013 Adam Miller <admiller@redhat.com> 1.9.5-1
- Merge pull request #1440 from smarterclayton/rescue_delivery_failures
  (dmcphers+openshiftbot@redhat.com)
- Merge pull request #1426 from jtharris/bugs/BZ961072
  (dmcphers+openshiftbot@redhat.com)
- Promo code delivery failures should not fail signup flow
  (ccoleman@redhat.com)
- Merge pull request #1429 from liggitt/extend_user_cache
  (dmcphers+openshiftbot@redhat.com)
- Merge pull request #1420 from
  smarterclayton/site_doesnt_preserve_parameters_through_login
  (dmcphers+openshiftbot@redhat.com)
- Bug 961072 (jharris@redhat.com)
- Extend user cache key timeout (jliggitt@redhat.com)
- Merge pull request #1423 from liggitt/nhr-direct_post_improvements
  (dmcphers+openshiftbot@redhat.com)
- Change aria_user to current_aria_user (jliggitt@redhat.com)
- Move @aria_user into helper method (jliggitt@redhat.com)
- Show message when account is in dunning, suspended, or terminated. Explicitly
  set all direct_post settings (jliggitt@redhat.com)
- Merge pull request #1421 from smarterclayton/hide_google_frame
  (dmcphers+openshiftbot@redhat.com)
- Hide the google frame in ads (ccoleman@redhat.com)
- During redirection from a protected page (via authenticate_user!) parameters
  on the URL are lost.  They should be preserved. (ccoleman@redhat.com)

* Mon May 20 2013 Dan McPherson <dmcphers@redhat.com> 1.9.4-1
- 

* Mon May 20 2013 Dan McPherson <dmcphers@redhat.com> 1.9.3-1
- Disable support email form in account help. (jharris@redhat.com)
- Merge pull request #1402 from jtharris/features/Card284
  (dmcphers+openshiftbot@redhat.com)
- Card online_ui_284 - OpenShift Online bugzilla url (jharris@redhat.com)

* Thu May 16 2013 Adam Miller <admiller@redhat.com> 1.9.2-1
- Rename log helper (jharris@redhat.com)
- fix builds (dmcphers@redhat.com)
- Merge pull request #1351 from smarterclayton/upgrade_to_mocha_0_13_3
  (admiller@redhat.com)
- Bug 961525 - Robots.txt change for crawling of account new
  (ccoleman@redhat.com)
- Code slipped in with failing tests, fix to handle nil users
  (ccoleman@redhat.com)
- Card online_ui_278 - User action logging (jharris@redhat.com)
- Merge pull request #1364 from fabianofranz/master (dmcphers@redhat.com)
- Moved Help Link Tests do extended (ffranz@redhat.com)
- Moved Help Link Tests do extended (ffranz@redhat.com)
- Merge pull request #1326 from sg00dwin/508dev
  (dmcphers+openshiftbot@redhat.com)
- Merge pull request #1349 from
  liggitt/bug_961672_tolerate_plans_with_no_service_rates
  (dmcphers+openshiftbot@redhat.com)
- Merge pull request #1350 from smarterclayton/bug_961671_remove_community_link
  (dmcphers+openshiftbot@redhat.com)
- Fix bug 961672 - tolerate users assigned plans with no service rates
  (jliggitt@redhat.com)
- Merge pull request #1352 from smarterclayton/simplify_blog_test
  (ccoleman@redhat.com)
- Allow test to pass cleanly (ccoleman@redhat.com)
- Bug 961671 - Remove the community link from the header (ccoleman@redhat.com)
- Upgrade to mocha 0.13.3 (compatible with Rails 3.2.12) (ccoleman@redhat.com)
- Merge pull request #1347 from liggitt/direct_post
  (dmcphers+openshiftbot@redhat.com)
- Collect on direct_post (jliggitt@redhat.com)
- Merge pull request #1335 from liggitt/line_item_text
  (dmcphers+openshiftbot@redhat.com)
- Merge pull request #1333 from nhr/Bug_961267
  (dmcphers+openshiftbot@redhat.com)
- Tweak usage line item display (jliggitt@redhat.com)
- Change storage max text from '30GB' to '6GB' (hripps@redhat.com)
- Add sequence functional group spec to create_acct_complete
  (hripps@redhat.com)
- Merge branch 'master' of github.com:openshift/li into 508dev
  (sgoodwin@redhat.com)
- body.admin-menu specific styles for mobile resolutions so they don't cover
  the top bar links (sgoodwin@redhat.com)
- Fix for Bug 902173 - Events page /community/calendar is out of bounds on
  Safari Iphone4S (sgoodwin@redhat.com)

* Wed May 08 2013 Adam Miller <admiller@redhat.com> 1.9.1-1
- bump_minor_versions for sprint 28 (admiller@redhat.com)

* Wed May 08 2013 Adam Miller <admiller@redhat.com> 1.8.9-1
- Merge pull request #1327 from liggitt/bug_959559_js_validation_errors
  (dmcphers+openshiftbot@redhat.com)
- Merge pull request #1325 from smarterclayton/disallow_external_referrers
  (dmcphers+openshiftbot@redhat.com)
- Merge pull request #1323 from nhr/Bug_961043
  (dmcphers+openshiftbot@redhat.com)
- Fix bug 959559 - add test for jquery validate (jliggitt@redhat.com)
- Bug 960018 - Disallow external redirection (ccoleman@redhat.com)
- Bug 961043 Update plan comparison logic to handle new field name
  (hripps@redhat.com)

* Wed May 08 2013 Adam Miller <admiller@redhat.com> 1.8.8-1
- Merge pull request #1324 from detiber/bz959162
  (dmcphers+openshiftbot@redhat.com)
- Merge pull request #1320 from liggitt/bug_959559_js_validation_errors
  (dmcphers+openshiftbot@redhat.com)
- Migrating some console base styling to origin-server/console
  (jdetiber@redhat.com)
- Fix bug 959559 - validate cc number on page load (jliggitt@redhat.com)
- Updated per PR feedback (hripps@redhat.com)
- Bug 960225 Add text to indicate that entitlements aren't instant.
  (hripps@redhat.com)

* Tue May 07 2013 Adam Miller <admiller@redhat.com> 1.8.7-1
- Revert drop-down title to "Bill date" on billing history page
  (jliggitt@redhat.com)
- Code review updates (jliggitt@redhat.com)
- Merge pull request #1312 from liggitt/bug_959555_beta_wording_tweaks
  (dmcphers+openshiftbot@redhat.com)
- Merge pull request #1311 from nhr/BZ960260 (dmcphers+openshiftbot@redhat.com)
- Fix bug 959555 - Beta wording tweaks (jliggitt@redhat.com)
- Merge pull request #1309 from nhr/functional_acct_groups
  (dmcphers+openshiftbot@redhat.com)
- Bug 960260 - Explcitily map @billing_info 'region' to @full_user 'state'
  (hripps@redhat.com)
- Updated per PR feedback (hripps@redhat.com)
- Add functional account group assignment to new Aria accounts
  (hripps@redhat.com)

* Mon May 06 2013 Adam Miller <admiller@redhat.com> 1.8.6-1
- Add authorization controller test (ccoleman@redhat.com)
- Merge pull request #1261 from nhr/aria_email_info
  (dmcphers+openshiftbot@redhat.com)
- Merge pull request #1306 from jwforres/Bug958525ResetPwdLoginLoop
  (dmcphers+openshiftbot@redhat.com)
- Merge pull request #1303 from jwforres/Bug959163TwitterLinksNotRendered
  (dmcphers+openshiftbot@redhat.com)
- Remove extraneous clear_cache (hripps@redhat.com)
- Bug 958525 - User enters infinite loop with Reset Password and login
  (jforrest@redhat.com)
- Merge remote-tracking branch 'upstream/master' into aria_email_info
  (hripps@redhat.com)
- Merge pull request #1300 from smarterclayton/merge_coverage_properly
  (dmcphers+openshiftbot@redhat.com)
- Merge pull request #1295 from liggitt/cache_aria
  (dmcphers+openshiftbot@redhat.com)
- Bug 959163 - Twitter links of "Check the buzz" not clickable
  (jforrest@redhat.com)
- Modify test address to use example.com (hripps@redhat.com)
- Remove before_filters that obfuscated model setup (hripps@redhat.com)
- Modified to cache & clear has_account? result as appropriate
  (hripps@redhat.com)
- Updated per Clayton's feedback (hripps@redhat.com)
- Updated per PR feedback (hripps@redhat.com)
- Add email attribute to BillingInfo and ContactInfo (hripps@redhat.com)
- Allow arbitrary commands to be merged by giving them different command names
  based on what is run (ccoleman@redhat.com)
- Put clear_cache in ensure, make clear_cache safer, use with_clean_cache
  (jliggitt@redhat.com)
- Cache Aria user methods (jliggitt@redhat.com)
- Fix bug calling cache_key_for (jliggitt@redhat.com)
- Use Aria.cached, clear cache appropriately, stop modifying arg options
  (jliggitt@redhat.com)
- Use HasWithIndifferentAccess (jliggitt@redhat.com)

* Thu May 02 2013 Adam Miller <admiller@redhat.com> 1.8.5-1
- Merge pull request #1293 from jwforres/Bug958596_CantAccessAccountHelp
  (dmcphers+openshiftbot@redhat.com)
- Bug 958596 - The Account Help page is not accessible. (jforrest@redhat.com)
- Fix site_extended tests (jliggitt@redhat.com)
- Merge pull request #1285 from liggitt/bug_958278_segfault_on_int_assetss
  (dmcphers+openshiftbot@redhat.com)
- Merge pull request #1256 from smarterclayton/support_external_cartridges
  (dmcphers+openshiftbot@redhat.com)
- Merge pull request #1277 from smarterclayton/add_customer_service_links
  (dmcphers+openshiftbot@redhat.com)
- Merge pull request #1282 from smarterclayton/add_request_denied_error
  (dmcphers+openshiftbot@redhat.com)
- Merge pull request #1273 from liggitt/bug_958219_direct_post_plan_id
  (dmcphers+openshiftbot@redhat.com)
- Review comments - adjust messages (ccoleman@redhat.com)
- Fix bug 958278 - only compress and precompile content in production build
  task (jliggitt@redhat.com)
- Introduce a request denied error (ccoleman@redhat.com)
- Merge remote-tracking branch 'origin/master' into support_external_cartridges
  (ccoleman@redhat.com)
- Minor tweaks to our text around customer service - use "Customer Service",
  link directly to the support link for contact info, and then remove
  unnecessary config from account_helper.rb (ccoleman@redhat.com)
- Fix bug 958219 - use plan id in direct_post config name (jliggitt@redhat.com)
- Site should include console coverage numbers (ccoleman@redhat.com)
- Improve test performance by skipping aria checks on most tests
  (ccoleman@redhat.com)

* Wed May 01 2013 Adam Miller <admiller@redhat.com> 1.8.4-1
- Merge pull request #1274 from
  smarterclayton/production_rb_not_a_config_any_longer
  (dmcphers+openshiftbot@redhat.com)
- production.rb should no longer be a config(noreplace), now that the config
  file is being used. (ccoleman@redhat.com)
- Merge pull request #1271 from jwforres/Bug955444_FAQRelativeLinks404
  (dmcphers+openshiftbot@redhat.com)
- Bug 955444 - Getting Started page link 404 on account help page
  (jforrest@redhat.com)

* Mon Apr 29 2013 Adam Miller <admiller@redhat.com> 1.8.3-1
- Merge pull request #1258 from smarterclayton/drupal_fixes
  (dmcphers+openshiftbot@redhat.com)
- Unformatted lists should write nothing (ccoleman@redhat.com)
- Base collections account group only on billing country (hripps@redhat.com)
- Merge pull request #1246 from fabianofranz/master
  (dmcphers+openshiftbot@redhat.com)
- Fixed tests for Maintenance mode (ffranz@redhat.com)
- Using a dedicated exception to handle server unavailable so we don't have to
  check status codes more than once (ffranz@redhat.com)
- Tests for Maintenance mode (ffranz@redhat.com)
- Tests for Maintenance mode (ffranz@redhat.com)
- Maintenance mode will now handle login/authorization properly
  (ffranz@redhat.com)
- Maintenance mode page, now handling nil responses on server error
  (ffranz@redhat.com)
- Maintenance mode for the web console (ffranz@redhat.com)
