%if 0%{?fedora}%{?rhel} <= 6
    %global scl ruby193
    %global scl_prefix ruby193-
%endif
%global rubyabi 1.9.1
%define htmldir %{_var}/www/html
%define sitedir %{_var}/www/openshift/site

Summary:   OpenShift Site Rails application
Name:      rhc-site
Version: 1.7.13
Release:   1%{?dist}
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

RAILS_ENV=production RAILS_RELATIVE_URL_ROOT=/app \
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
%attr(0770,root,libra_user) %{sitedir}/tmp
%attr(0770,root,libra_user) %{sitedir}/tmp/cache
%attr(0770,root,libra_user) %{sitedir}/tmp/cache/assets
%attr(0770,root,libra_user) %{_var}/log/openshift/site/
%ghost %attr(0660,root,libra_user) %{_var}/log/openshift/site/production.log
%ghost %attr(0660,root,libra_user) %{_var}/log/openshift/site/development.log

%defattr(0640,root,libra_user,0750)
%{sitedir}
%{htmldir}/app
%config(noreplace) %{sitedir}/config/environments/production.rb
%config(noreplace) %{sitedir}/app/subsites/status/config/hosts.yml
%config(noreplace) /etc/openshift/console.conf
%exclude %{sitedir}/public

%files static
%defattr(0640,root,libra_user,0750)
%{sitedir}/public

%changelog
* Fri Apr 19 2013 Dan McPherson <dmcphers@redhat.com> 1.7.13-1
- 

* Fri Apr 19 2013 Dan McPherson <dmcphers@redhat.com> 1.7.12-1
- Fix bug 953725 - don't do required element validation in contact_info
  (jliggitt@redhat.com)
- Fix bug 953176 - recognize tax line items correctly, use Aria-provided usage
  total amount (jliggitt@redhat.com)

* Thu Apr 18 2013 Dan McPherson <dmcphers@redhat.com> 1.7.11-1
- Fix bug 953549 to add address.js to production build (jliggitt@redhat.com)

* Wed Apr 17 2013 Dan McPherson <dmcphers@redhat.com> 1.7.10-1
- Looking current group ID (hripps@redhat.com)
- Fixed test cases for dummy invoice tmpl ID & coll group (hripps@redhat.com)
- Set collections group default during acct creation (hripps@redhat.com)
- Updated to validate invoice template ID assignment (hripps@redhat.com)
- Updated to include workaround for Streamline bug (hripps@redhat.com)
- Aria models now require and validate country plus other tweaks
  (hripps@redhat.com)
- Modified based on review feedback (hripps@redhat.com)
- Billing currency now auto-selected per config file mapping
  (hripps@redhat.com)

* Tue Apr 16 2013 Dan McPherson <dmcphers@redhat.com> 1.7.9-1
- Add buildrequires for new test packages (ccoleman@redhat.com)

* Tue Apr 16 2013 Dan McPherson <dmcphers@redhat.com> 1.7.8-1
- 

* Tue Apr 16 2013 Troy Dawson <tdawson@redhat.com> 1.7.7-1
- Fix bug 952371 - make first and last name required in billing info
  (jliggitt@redhat.com)
- Move to using minitest 3.5, webmock 1.8.11, and mocha 0.12.10
  (ccoleman@redhat.com)

* Mon Apr 15 2013 Adam Miller <admiller@redhat.com> 1.7.6-1
- Merge pull request #1188 from liggitt/bug/951671 (dmcphers@redhat.com)
- Merge pull request #1186 from liggitt/bug/952145
  (dmcphers+openshiftbot@redhat.com)
- Fix bug 951671 - allow unsetting address2, address3 in Aria
  (jliggitt@redhat.com)
- Fix bug 952145 - show prices in new currency as soon as user chooses it
  (jliggitt@redhat.com)
- Fix Bug 952140, use C$ for CAD (jliggitt@redhat.com)
- Set BillingInfo.persisted? correctly (jliggitt@redhat.com)
- Fix validation on billing info form (jliggitt@redhat.com)
- Merge pull request #1180 from
  smarterclayton/bug_951492_some_status_urls_wrong (dmcphers@redhat.com)
- Remove old references to the site theme from potential error pages
  (ccoleman@redhat.com)
- Development mode shouldn't have integrated true (ccoleman@redhat.com)
- Merge pull request #1178 from jtharris/features/Card6 (dmcphers@redhat.com)
- Merge pull request #1175 from nhr/BZ950867 (dmcphers@redhat.com)
- Bug 951492 - Some status URLs should be using relative paths
  (ccoleman@redhat.com)
- Merge pull request #1177 from nhr/BZ951158 (dmcphers@redhat.com)
- Fix for test output. (jharris@redhat.com)
- Add js tests to denenv. (jharris@redhat.com)
- Cannot clear comments in older versions of rake. (jharris@redhat.com)
- Only create js test tasks if konacha is available. (jharris@redhat.com)
- Bumping konacha version. (jharris@redhat.com)
- Add js testing gem dependencies. (jharris@redhat.com)
- Only use konacha in dev and test groups. (jharris@redhat.com)
- Slim down rspec requirement. (jharris@redhat.com)
- Fix up rake tasks for js test reporting. (jharris@redhat.com)
- Removing phantomjs gem. (jharris@redhat.com)
- Javascript unit testing. (jharris@redhat.com)
- Bug 951158 Wrapped dynamic portion of payment info form for aria-live
  attribute (hripps@redhat.com)
- Bug 950867 Phone number field max length corrected to 30 (hripps@redhat.com)

* Fri Apr 12 2013 Adam Miller <admiller@redhat.com> 1.7.5-1
- Merge pull request #1166 from liggitt/currency_test
  (dmcphers+openshiftbot@redhat.com)
- Bug 929178 Remove duplicate error messages for payment info
  (hripps@redhat.com)
- Add tests for premium indicator in correct currency on application types page
  (jliggitt@redhat.com)
- Merge pull request #1164 from smarterclayton/origin_ui_37_error_pages
  (dmcphers+openshiftbot@redhat.com)
- Merge pull request #1169 from smarterclayton/bug_950875_hit_console_first
  (dmcphers@redhat.com)
- Ensure login flows tests redirect to getting_started_path
  (ccoleman@redhat.com)
- Bug 950875 - After account confirm, redirect user to console first then get-
  started (ccoleman@redhat.com)
- Merge pull request #1160 from liggitt/accessibility
  (dmcphers+openshiftbot@redhat.com)
- Merge pull request #1161 from nhr/plan_currency (dmcphers@redhat.com)
- Add two additional pages for app unavailable and app installing
  (ccoleman@redhat.com)
- Add generic error pages to the product. (ccoleman@redhat.com)
- Add form labels (jliggitt@redhat.com)
- Add alt_template_msg_no to expected fields in Aria call (hripps@redhat.com)
- Clean up aria config settings (hripps@redhat.com)
- Users in unsupported countries cannot upgrade to Silver plan
  (hripps@redhat.com)
- Aria account main address set on account create (hripps@redhat.com)
- Lookup and apply functional account groups in Aria (hripps@redhat.com)
- Update plan upgrade page to match design spec (hripps@redhat.com)
- Fix async and controller logic for before_filter (hripps@redhat.com)
- Fix some views (fotios@redhat.com)
- Fix for process_async (fotios@redhat.com)
- plan id search (fotios@redhat.com)
- Added async aria stuff to all controllers (fotios@redhat.com)
- Better async (fotios@redhat.com)
- More before_filter (fotios@redhat.com)
- User info in before_filters (fotios@redhat.com)
- Added more supported countries (fotios@redhat.com)
- Fixing unit tests (fotios@redhat.com)
- Exclude better_errors gems during testing (fotios@redhat.com)
- Fixing unit tests (fotios@redhat.com)
- Add test for billing address update (hripps@redhat.com)
- Prevent currency change on billing info update (hripps@redhat.com)
- Added aside for billing info (fotios@redhat.com)
- Fixing workflow (fotios@redhat.com)
- Correct functional tests for new billing and payment configuration
  (hripps@redhat.com)
- Force user to select a currency (fotios@redhat.com)
- Billing info partial (fotios@redhat.com)
- Fixed partials for payment and billing info summaries (fotios@redhat.com)
- Fix view looking for credit cards in Rails configuration (fotios@redhat.com)
- Rebase Aria::BillingInfo to use class method overrides (hripps@redhat.com)
- billing_info link (fotios@redhat.com)
- Removed add_validations helper (fotios@redhat.com)
- Fixing countries config and helper (fotios@redhat.com)
- Change loading debug libs in Gemfile (fotios@redhat.com)
- Remove validation for previously removed atrribute (hripps@redhat.com)
- Removed styleguide changes (fotios@redhat.com)
- Removed plan pricing css (fotios@redhat.com)
- This was also in another helper, messed up during rebase (fotios@redhat.com)
- Changed payment_method css (fotios@redhat.com)
- section.row (fotios@redhat.com)
- Turn address.coffee into it's own function (fotios@redhat.com)
- Moved account form back (fotios@redhat.com)
- Moved credit card stuff to it's own helper (fotios@redhat.com)
- Moved country_helper to app/helpers (fotios@redhat.com)
- Refactored credit card JS (fotios@redhat.com)
- Fixed autocomplete helpers (fotios@redhat.com)
- Fixed Gemfile (fotios@redhat.com)
- Changes to plan upgrade forms https://trello.com/c/s6W4Sxd3 This allows users
  to create/update their account/billing/payment information in the upgrade
  workflow. (fotios@redhat.com)
- Extened billing info to support intl. addresses (hripps@redhat.com)

* Thu Apr 11 2013 Adam Miller <admiller@redhat.com> 1.7.4-1
- Merge pull request #1158 from liggitt/currency_display3
  (dmcphers+openshiftbot@redhat.com)
- Fix test data for CAD, always parse CAD, USD, EUR from plan descriptions
  (jliggitt@redhat.com)
- Merge pull request #1150 from smarterclayton/tweaks_to_quickstarts
  (dmcphers@redhat.com)
- Merge pull request #1153 from
  smarterclayton/bug_929056_send_community_help_to_console_help
  (dmcphers+openshiftbot@redhat.com)
- Add CAD, add tests for plan page listing (jliggitt@redhat.com)
- Final styling tweaks, allegedly fix facebook (ccoleman@redhat.com)
- Bug 929056 - Send community help to console help for now
  (ccoleman@redhat.com)
- Social sharing links, cleanup, styling fixes (ccoleman@redhat.com)
- Update quickstarts with correct icon sizes, fix typos and spelling errors.
  (ccoleman@redhat.com)

* Wed Apr 10 2013 Adam Miller <admiller@redhat.com> 1.7.3-1
- Merge pull request #1147 from
  smarterclayton/redirect_new_users_to_get_started
  (dmcphers+openshiftbot@redhat.com)
- Merge pull request #1151 from
  smarterclayton/bug_948371_fix_flash_to_be_now_only (dmcphers@redhat.com)
- Merge pull request #1146 from smarterclayton/set_no_default_community_url
  (dmcphers@redhat.com)
- Bug 948371 - Fixes to settings page (ccoleman@redhat.com)
- Do not set a default community URL (ccoleman@redhat.com)
- Add currency filtering to plan feature descriptions (jliggitt@redhat.com)
- Signup takes users to the get-started page (ccoleman@redhat.com)
- Merge pull request #1140 from liggitt/currency_display (dmcphers@redhat.com)
- Fix test failure caused by including Secured in BillingAware
  (jliggitt@redhat.com)
- Currency display story number_to_user_currency helper method Make CSV export
  async, refactor csv to view Add tests for eur display Cache currency_cd in
  session (jliggitt@redhat.com)
- Add picatcha to asset compilation (ccoleman@redhat.com)

* Mon Apr 08 2013 Adam Miller <admiller@redhat.com> 1.7.2-1
- Stop using Date.yesterday, move aria unit tests back into test:base
  (jliggitt@redhat.com)
- Move aria unit test to site_extended temporarily (jliggitt@redhat.com)
- Merge pull request #1126 from fabianofranz/master
  (dmcphers+openshiftbot@redhat.com)
- OpenShift and Shadowman logos for the invoice (ffranz@redhat.com)
- OpenShift and Shadowman logos for the invoice (ffranz@redhat.com)
- Move bills controller test to extended (jliggitt@redhat.com)
- Fix bug 948328 - stub remaining network calls to aria for
  billing_controller_test (jliggitt@redhat.com)
- Adding explicit injection annotations for uglifier (jharris@redhat.com)
- Merge pull request #1093 from liggitt/aria_functional_tests
  (dmcphers+openshiftbot@redhat.com)
- Enable advancing virtual time (jliggitt@redhat.com)
- Tolerate missing plans in RecurringLineItem (jliggitt@redhat.com)
- Fixing captcha test (fotios@redhat.com)
- Add bills and account controllers to aria:test (jliggitt@redhat.com)
- Refactor user transactions, add advance_virtual_datetime, make Account tab
  active, add current_period_end_date, use last_arrears_bill_thru_date to
  compute starting date (jliggitt@redhat.com)
- Add aria functional tests, test user generation, current period start date,
  forwarded balance (jliggitt@redhat.com)
- Fix for picatcha not being submitted properly (fotios@redhat.com)
- Merge branch 'master' of github.com:openshift/li into 401dev
  (sgoodwin@redhat.com)
- Removed the openshift-icon inclusion in stylesheet since it's not included
  through common Updates to iconfont usage styleguide Remove openshift-icon
  from config/environments/production.rb (sgoodwin@redhat.com)
- Fix bug 947081 - display dashboard for accounts with payment info and no next
  bill (jliggitt@redhat.com)
- Make forum login to post links buttons so they are recognizable/standout,
  since it's a key path to submitting questions. (sgoodwin@redhat.com)
- Merge pull request #1091 from liggitt/bug/928821 (dmcphers@redhat.com)
- Merge pull request #1090 from smarterclayton/line_item_plan_name_wrong
  (dmcphers@redhat.com)
- Merge pull request #1088 from liggitt/aria_test
  (dmcphers+openshiftbot@redhat.com)
- Fix bug 928821 - tweak signup success message for new plan name
  (jliggitt@redhat.com)
- Line item plan names say "Plan: Recurring" instead of "Plan: {{plan_name}}"
  (ccoleman@redhat.com)
- Fix bug 928793 - Billing page does not tolerate missing bills or plan items
  (jliggitt@redhat.com)
- Fix bug 928793 - &nbsp; shows in bill column (jliggitt@redhat.com)

* Thu Mar 28 2013 Adam Miller <admiller@redhat.com> 1.7.1-1
- bump_minor_versions for sprint 26 (admiller@redhat.com)
- Merge pull request #1077 from fotioslindiakos/picatcha_fix
  (dmcphers+openshiftbot@redhat.com)
- Restyle refresh link based on CSS (fotios@redhat.com)
- Client side picatcha checking (fotios@redhat.com)

* Wed Mar 27 2013 Adam Miller <admiller@redhat.com> 1.6.8-1
- Added fixtures for certificate tests (ffranz@redhat.com)
- Fix bug 924589 - dashboard cannot show when aria_enabled=false
  (jliggitt@redhat.com)
- Merge remote-tracking branch 'origin/master' into update_to_new_plan_values
  (ccoleman@redhat.com)
- Merge pull request #1076 from liggitt/invoice_styleguide
  (dmcphers@redhat.com)
- Merge pull request #1075 from jtharris/bugs/BZ923170 (dmcphers@redhat.com)
- Merge pull request #1074 from liggitt/bug/927628 (dmcphers@redhat.com)
- Add an invoice styleguide page (jliggitt@redhat.com)
- Account/help responsive support. (jharris@redhat.com)
- Fix bug 927628 - collapse identical usage line items (jliggitt@redhat.com)
- Bug 923746 - Fix tax exemption link (ccoleman@redhat.com)
- Alter usage line item reporting for free line items (ccoleman@redhat.com)
- Merge remote-tracking branch 'origin/master' into update_to_new_plan_values
  (ccoleman@redhat.com)
- Rename freeshift/megashift to free/silver everywhere (ccoleman@redhat.com)
- Show free rate total (ccoleman@redhat.com)
- Allow broker plan values to be configured.  Change devenv defaults to match
  new 'Free' and 'Silver' plans. (ccoleman@redhat.com)

* Tue Mar 26 2013 Adam Miller <admiller@redhat.com> 1.6.7-1
- Merge pull request #1064 from liggitt/bug/927187
  (dmcphers+openshiftbot@redhat.com)
- Fix bug 927187 - show dashboard correctly if aria_enabled=false
  (jliggitt@redhat.com)

* Mon Mar 25 2013 Adam Miller <admiller@redhat.com> 1.6.6-1
- Clean up premium cart indicators (ccoleman@redhat.com)
- Remove deep partials, expose trust provider from quickstart api
  (ccoleman@redhat.com)
- Merge pull request #1055 from fabianofranz/dev/ffranz/ssl
  (dmcphers+openshiftbot@redhat.com)
- Merge pull request #1057 from smarterclayton/aria_dashboard
  (dmcphers+openshiftbot@redhat.com)
- Merge pull request #1060 from smarterclayton/dont_logout_on_login
  (dmcphers+openshiftbot@redhat.com)
- Merge pull request #1061 from spurtell/spurtell/analytics
  (dmcphers@redhat.com)
- Merge pull request #1059 from sg00dwin/0315dev
  (dmcphers+openshiftbot@redhat.com)
- Eloqua integration,Omniture updates,AdWords Conversion Tracker Update
  (spurtell@redhat.com)
- Stop resetting the auth token when the login page is visited
  (ccoleman@redhat.com)
- Default to the localhost url for resources (ccoleman@redhat.com)
- Merge branch 'aria_dashboard' of github.com:smarterclayton/li into
  aria_dashboard (ccoleman@redhat.com)
- Additional fixes for accounts with unpaid usage items in an invoice
  (ccoleman@redhat.com)
- Add rules for displaying icons within definition list (sgoodwin@redhat.com)
- Fix bug 924664 - validate max lengths on billing info fields
  (jliggitt@redhat.com)
- Merge pull request #18 from liggitt/bug/924539 (ccoleman@redhat.com)
- Add .span12 (jliggitt@redhat.com)
- Fix bug 924539 - make dashboard header layout work better on iPhone
  (jliggitt@redhat.com)
- Card #239: Added support to alias creation and deletion and SSL certificate
  upload to the web console (ffranz@redhat.com)
- Fix typo in dashboard display, skip usage checks if there is no next bill
  (jliggitt@redhat.com)
- Merge branch 'master' of github.com:openshift/li into 0315dev
  (sgoodwin@redhat.com)
- Fix bug 924550 - unpaid invoices with usage line items don't work
  (jliggitt@redhat.com)
- Show tax blurb if there are tax line items (jliggitt@redhat.com)
- Merge branch 'aria_dashboard' of github.com:smarterclayton/li into
  aria_dashboard (ccoleman@redhat.com)
- Fix unit tests, ensure that users are correctly notified when they are in a
  downgrade situation, as well as when there are no charges.
  (ccoleman@redhat.com)
- Add virtual time indicator, add tax help blurb (jliggitt@redhat.com)
- Merge branch 'master' of github.com:openshift/li into 0315dev
  (sgoodwin@redhat.com)
- Merge remote-tracking branch 'origin/master' into aria_dashboard
  (ccoleman@redhat.com)
- Next plan is "false" if current and future == free, empty? otherwise
  (ccoleman@redhat.com)
- Plan arrow was missing (ccoleman@redhat.com)
- Unit test should pass (ccoleman@redhat.com)
- Implement CSV export (jliggitt@redhat.com)
- Refactor bills controller (jliggitt@redhat.com)
- Refactor bills controller, add error handling for invoices not found
  (jliggitt@redhat.com)
- Add print support to billing (jliggitt@redhat.com)
- add usage rules for alert headings w/ icons (sgoodwin@redhat.com)
- Reuse usage items from next bill (jliggitt@redhat.com)
- Expand usage graphs, add warning message for test users, render empty layout
  if no bills (jliggitt@redhat.com)
- Warn users if they are a test user. (ccoleman@redhat.com)
- Be clearer about what charges are pending.  Stop checking for invoices in the
  future. (ccoleman@redhat.com)
- Remove bill_day hack, update test case (jliggitt@redhat.com)
- Bill controller and layout (jliggitt@redhat.com)
- Broken helper, clear instance variables, include plan details link
  (ccoleman@redhat.com)
- Integrate and cleanup the application dashboard (ccoleman@redhat.com)
- Merge remote-tracking branch 'jtharris/ta3668' into aria_dashboard
  (ccoleman@redhat.com)
- Add methods for getting invoice payments (jliggitt@redhat.com)
- Fix bug 921276 - manually set bill_day after creating user
  (jliggitt@redhat.com)
- Fix tests (jliggitt@redhat.com)
- Tests are passing (ccoleman@redhat.com)
- Use helper for forums URL (asari.ruby@gmail.com)
- Implement memcached on devenv (ccoleman@redhat.com)
- Provide an easier path to upgrade (asari.ruby@gmail.com)
- Merge remote-tracking branch 'origin/master' into aria_dashboard
  (ccoleman@redhat.com)
- Fixing up test cases (ccoleman@redhat.com)
- FAQ search UI tweaks. (jharris@redhat.com)
- Tolerate short bills (ccoleman@redhat.com)
- Merge pull request #1012 from liggitt/bug/921276_master (ccoleman@redhat.com)
- Add correct breadcrumbs, make tabs active when users are on subpages, make
  settings page flows go back to settings page (ccoleman@redhat.com)
- More tweaks towards final account page (ccoleman@redhat.com)
- Make dashboard accessible to unpaid users (ccoleman@redhat.com)
- Add test for bill date of day 1, use month name for billing period, default
  to bill on day 1 (jliggitt@redhat.com)
- Make graph styles generic, avoid using usage names as class names
  (jliggitt@redhat.com)
- Handle user without account (ccoleman@redhat.com)
- Usage graph work (jliggitt@redhat.com)
- Add account summary information to the account dashboard
  (ccoleman@redhat.com)
- Model line items on a plan (ccoleman@redhat.com)
- Add billing info retrieval to aria helpers (ccoleman@redhat.com)
- Rearrange elements based on discussion with Clayton (asari.ruby@gmail.com)
- No use in specifying :to here. (asari.ruby@gmail.com)
- @user was not intialized. (asari.ruby@gmail.com)
- Merge remote-tracking branch 'upstream/master' into ta3668
  (jharris@redhat.com)
- FAQ search matches body. (jharris@redhat.com)
- Merge pull request #9 from sg00dwin/account-help (jharris@redhat.com)
- why upgrade text (sgoodwin@redhat.com)
- UI styling for account/help (sgoodwin@redhat.com)
- Merge pull request #7 from BanzaiMan/ta3668 (jharris@redhat.com)
- Use plain text email instead of HTML (asari.ruby@gmail.com)
- Adding angular-rails to site spec. (jharris@redhat.com)
- Merge remote-tracking branch 'upstream/master' into ta3668
  (jharris@redhat.com)
- Making faq service call relative. (jharris@redhat.com)
- Merge remote-tracking branch 'upstream/master' into ta3668
  (jharris@redhat.com)
- Reworking community api models. (jharris@redhat.com)
- UI adjustments for account/help page (sgoodwin@redhat.com)
- contact_support test (asari.ruby@gmail.com)
- AccountSupportContactMailer tests (asari.ruby@gmail.com)
- Tabs to spaces (asari.ruby@gmail.com)
- Clean up form handling (asari.ruby@gmail.com)
- Bare minimum email form support, along with necessary routing support.
  (asari.ruby@gmail.com)
- Add plan upgrade blurb for free plan users (asari.ruby@gmail.com)
- Make FAQ endpoint configurable. (asari.ruby@gmail.com)
- Adding in FAQ rails proxy and additional tests. (jharris@redhat.com)
- Adding in jasmine tests using testem. (jharris@redhat.com)
- Make plan information available to views (asari.ruby@gmail.com)
- Killing the scrolled div. (jharris@redhat.com)
- More angular refactoring and rendering default no-js content.
  (jharris@redhat.com)
- Getting bare bones faq search in place (jharris@redhat.com)
- Add tooltip with Bootstrap (asari.ruby@gmail.com)
- Tidy up FAQ items into a list (asari.ruby@gmail.com)
- Skeleton of FAQ display (asari.ruby@gmail.com)
- Correct help nav bar position (asari.ruby@gmail.com)
- Go partial-happy and start styling (asari.ruby@gmail.com)
- Hard-wiring 'account/help'. (asari.ruby@gmail.com)

* Fri Mar 22 2013 Adam Miller <admiller@redhat.com> 1.6.5-1
- Merge pull request #1052 from smarterclayton/quickstarts_in_community
  (dmcphers+openshiftbot@redhat.com)
- Merge remote-tracking branch 'origin/master' into quickstarts_in_community
  (ccoleman@redhat.com)
- Style fixes from rob (ccoleman@redhat.com)
- Switch to div based layout, lock taxonomies.  Follow Rob's changes to views
  and remove excess output. (ccoleman@redhat.com)
- US3113:  presentational tweaks to quickstarts lists (rhamilto@redhat.com)
- US3113:  detabbing _community.scss, addressing .links.inline a { } bug, and
  first cut at styling of a quick start page (rhamilto@redhat.com)
- Add quickstart features, simplify markup for blogs and quickstarts to be
  consistent (ccoleman@redhat.com)
- Implement a quickstart content view with popular and recent results
  (ccoleman@redhat.com)

* Thu Mar 21 2013 Adam Miller <admiller@redhat.com> 1.6.4-1
- updated account inclusion regex (spurtell@redhat.com)
- Bug 921508 - Fix link to Create Application page (hripps@redhat.com)

* Mon Mar 18 2013 Adam Miller <admiller@redhat.com> 1.6.3-1
- Implement memcached on devenv (ccoleman@redhat.com)
- Revise signup test to expect account upgrade view (hripps@redhat.com)
- Merge pull request #1017 from sg00dwin/various-work (dmcphers@redhat.com)
- set legend color that was accidently removed with previous css refactor
  (sgoodwin@redhat.com)

* Thu Mar 14 2013 Adam Miller <admiller@redhat.com> 1.6.2-1
- Merge pull request #1012 from liggitt/bug/921276_master
  (dmcphers+openshiftbot@redhat.com)
- Fix bug 921276 - default bill_day to 1 for new aria accounts
  (jliggitt@redhat.com)
- Revoved reference to missing partial /site/type (sgoodwin@redhat.com)
- Merge branch 'master' of github.com:openshift/li into misc-dev
  (sgoodwin@redhat.com)
- Merge pull request #997 from nhr/US2461_upgrade_confirmation_page
  (dmcphers+openshiftbot@redhat.com)
- Merge pull request #991 from jtharris/features/US2627
  (dmcphers+openshiftbot@redhat.com)
- US2461 - Upgrade confirmation page (hripps@redhat.com)
- moving to console for inclusion in origin.css (sgoodwin@redhat.com)
- %%div is redundant (jharris@redhat.com)
- Console heading color variable used (sgoodwin@redhat.com)
- Revert to single _type partial And add usage cases in styleguide font page
  (sgoodwin@redhat.com)
- Updated styleguide page for iconfont usage (sgoodwin@redhat.com)
- Merge branch 'master' of github.com:openshift/li into misc-dev
  (sgoodwin@redhat.com)
- Merge pull request #986 from liggitt/aria_landmarks
  (dmcphers+openshiftbot@redhat.com)
- Small tweak to usage costs message. (jharris@redhat.com)
- Remove whitespace around premium decorator to avoid orphan wrapping
  (jliggitt@redhat.com)
- Adding partial overrides for premium messaging. (jharris@redhat.com)
- Separate _type partials for console and site move h1,h2,h3...
  (sgoodwin@redhat.com)
- Scope table cell and row headers, add role=main landmarks, add 'Skip to
  content' links (jliggitt@redhat.com)

* Thu Mar 07 2013 Adam Miller <admiller@redhat.com> 1.6.1-1
- bump_minor_versions for sprint 25 (admiller@redhat.com)

* Thu Mar 07 2013 Adam Miller 1.5.12-2
- Bump spec for mass drupal rebuild

* Wed Mar 06 2013 Adam Miller <admiller@redhat.com> 1.5.12-1
- Merge pull request #981 from maxamillion/dev/admiller/fix_site_gemfile
  (admiller@redhat.com)
- Merge pull request #979 from smarterclayton/fix_default_config
  (dmcphers@redhat.com)
- modify site Gemfile to not require specific version (admiller@redhat.com)
- Add a trailing slash to the default COMMUNITY_URL (ccoleman@redhat.com)

* Wed Mar 06 2013 Adam Miller <admiller@redhat.com> 1.5.11-1
- Merge pull request #978 from spurtell/spurtell/analytics
  (dmcphers+openshiftbot@redhat.com)
- Tracking updates for domain split and enterprise (spurtell@redhat.com)
- Merge pull request #975 from smarterclayton/bug_917946_do_not_rh_sso_on_login
  (dmcphers@redhat.com)
- Merge pull request #966 from sg00dwin/icon-changes
  (dmcphers+openshiftbot@redhat.com)
- Revert "Tracking code updates for domain split and enterprise"
  (spurtell@redhat.com)
- Tracking code updates for domain split and enterprise (spurtell@redhat.com)
- Bug 917946 - Do not set rh_sso during login (ccoleman@redhat.com)
- Merge pull request #972 from liggitt/alt_text (dmcphers@redhat.com)
- Merge pull request #970 from smarterclayton/remove_old_pry_reference
  (dmcphers+openshiftbot@redhat.com)
- Add alt text to styleguide and twitter avatars (jliggitt@redhat.com)
- Merge pull request #968 from smarterclayton/update_to_robots
  (dmcphers+openshiftbot@redhat.com)
- Remove old pry reference (ccoleman@redhat.com)
- Update to robots (ccoleman@redhat.com)
- Merge branch 'master' of github.com:openshift/li into icon-changes
  (sgoodwin@redhat.com)
- Add usage scenarios to icon styleguide (sgoodwin@redhat.com)

* Tue Mar 05 2013 Adam Miller <admiller@redhat.com> 1.5.10-1
- Merge pull request #958 from sg00dwin/general-dev
  (dmcphers+openshiftbot@redhat.com)
- Merge pull request #953 from nhr/BZ910091_enable_streamline_user_retrieval
  (dmcphers@redhat.com)
- Merge pull request #959 from
  smarterclayton/bug_916495_relative_urls_in_community_still
  (dmcphers@redhat.com)
- Revised mock web user to better override the promote behavior
  (hripps@redhat.com)
- Bug 916495 - Fix more broken relative URLs (ccoleman@redhat.com)
- revert link change (sgoodwin@redhat.com)
- fix Bug 916564 content layout changes, minor (sgoodwin@redhat.com)
- Bug 910091 - Corrected http_post call that was not returning JSON response
  (hripps@redhat.com)

* Fri Mar 01 2013 Adam Miller <admiller@redhat.com> 1.5.9-1
- Merge pull request #936 from sg00dwin/iconfont
  (dmcphers+openshiftbot@redhat.com)
- Merge pull request #911 from fotioslindiakos/plan_upgrade
  (dmcphers+openshiftbot@redhat.com)
- Merge branch 'master' of github.com:openshift/li into blog-img
  (sgoodwin@redhat.com)
- Fix Bug 915523 - blog teaser img (sgoodwin@redhat.com)
- addition of openshift-icon.css to config (sgoodwin@redhat.com)
- Plan stuff (fotios@redhat.com)
- include note for implementation (sgoodwin@redhat.com)
- moving font files (sgoodwin@redhat.com)
- change icon name in svg metadata (sgoodwin@redhat.com)
- Iconfont modifications for styleguide and correct font name
  (sgoodwin@redhat.com)

* Thu Feb 28 2013 Adam Miller <admiller@redhat.com> 1.5.8-1
- Add a test case for upgrading a user, allow session state to be reset during
  promotion (ccoleman@redhat.com)

* Wed Feb 27 2013 Adam Miller <admiller@redhat.com> 1.5.7-1
- Merge pull request #886 from nhr/BZ910091_enable_streamline_user_retrieval
  (dmcphers+openshiftbot@redhat.com)
- Merge pull request #930 from smarterclayton/aria_direct_post_tweaks
  (dmcphers+openshiftbot@redhat.com)
- Tweak direct post production.rb example (ccoleman@redhat.com)
- Additional check to ensure persistant account upgrade (hripps@redhat.com)
- Bug 910091 - Users that exist in streamline are now populated from the
  streamline API (hripps@redhat.com)

* Tue Feb 26 2013 Adam Miller <admiller@redhat.com> 1.5.6-1
- Bug 915602 - Unable to signup (ccoleman@redhat.com)
- Merge pull request #924 from smarterclayton/community_url_not_available
  (dmcphers+openshiftbot@redhat.com)
- Merge pull request #925 from smarterclayton/session_auth_support_2
  (dmcphers+openshiftbot@redhat.com)
- The community URL is not available for some operations - use the default
  config if that is true (ccoleman@redhat.com)
- Bug 915253 - Eagerly load referenced model classes in development mode
  (ccoleman@redhat.com)
- Merge remote-tracking branch 'origin/master' into session_auth_support_2
  (ccoleman@redhat.com)
- Merge remote-tracking branch 'origin/master' into session_auth_support_2
  (ccoleman@redhat.com)
- Cleanup auth token pages (ccoleman@redhat.com)
- Tweak the log change so that is optional for developers running Rails
  directly, has same behavior on devenv, and allows more control over the path
  (ccoleman@redhat.com)
- Improvements to authorization pages and the extended dashboard
  (ccoleman@redhat.com)
- Allow auth token access from site console, show specific message when
  expired. (ccoleman@redhat.com)
- Merge remote-tracking branch 'origin/master' into session_auth_support_2
  (ccoleman@redhat.com)
- Support console authorization management (ccoleman@redhat.com)
- Merge remote-tracking branch 'origin/master' into session_auth_support_2
  (ccoleman@redhat.com)
- Merge remote-tracking branch 'origin/master' into session_auth_support_2
  (ccoleman@redhat.com)
- Merge branch 'isolate_api_behavior_from_base_controller' into
  session_auth_support_2 (ccoleman@redhat.com)
- Changes to the broker to match session auth support in the origin
  (ccoleman@redhat.com)

* Mon Feb 25 2013 Adam Miller <admiller@redhat.com> 1.5.5-1
- Merge pull request #922 from smarterclayton/bug_909992_more_community_fixes
  (dmcphers+openshiftbot@redhat.com)
- Bug 909992 - Fix login errors outside of login (ccoleman@redhat.com)
- Revert to original RAILS_LOG_PATH behavior (ccoleman@redhat.com)
- Merge pull request #920 from
  smarterclayton/bug_913816_work_around_bad_logtailer
  (dmcphers+openshiftbot@redhat.com)
- Bug 913816 - Fix log tailer to pick up the correct config
  (ccoleman@redhat.com)
- Merge pull request #918 from
  smarterclayton/bug_912286_cleanup_robots_misc_for_split
  (dmcphers+openshiftbot@redhat.com)
- Asset pages need community_aware (ccoleman@redhat.com)
- Use a more generic redirect to old content, integrate new URL
  (ccoleman@redhat.com)
- Set icon sizes class names to correspond to pixels. I believe this is the
  most sensible path for the time being. (sgoodwin@redhat.com)
- rename OSicon to openshift-icon (sgoodwin@redhat.com)
- Bug 912286 - Cleanup robots.txt and others for split (ccoleman@redhat.com)
- Introduction of OSicon font set includes: - Four font type files -
  OSicon.dev.svg master file generated from http://icomoon.io/app which will be
  used for further modifications to the set. - OSicon.css contains core styles
  - iconfont.css custom styles - inclusion of css within _stylesheets.html.haml
  for both console and site - New styleguide file for showing entire set
  (sgoodwin@redhat.com)
- Tweak the log change so that is optional for developers running Rails
  directly, has same behavior on devenv, and allows more control over the path
  (ccoleman@redhat.com)

* Wed Feb 20 2013 Adam Miller <admiller@redhat.com> 1.5.4-2
- Bump spec for rebuild

* Tue Feb 19 2013 Adam Miller <admiller@redhat.com> 1.5.4-1
- bump site for chainbuild (admiller@redhat.com)

* Tue Feb 19 2013 Adam Miller <admiller@redhat.com> - 1.5.3-2
- Bump for chainbuild

* Tue Feb 19 2013 Adam Miller <admiller@redhat.com> 1.5.3-1
- Merge pull request #891 from smarterclayton/bug_907647_remove_calls_to_extend
  (dmcphers+openshiftbot@redhat.com)
- Fix remaining unit test (ccoleman@redhat.com)
- Bug 907647 - Remove calls to Object#extend from Streamline, use delegator
  instead (ccoleman@redhat.com)
- Remove test case usage of Object#extend (ccoleman@redhat.com)
- Bug 909995 - Add logout link to log user out of community and console Bug
  873918 - When accessing a protected resource in community, take user to login
  page (ccoleman@redhat.com)
- Merge pull request #878 from sg00dwin/misc-bugs
  (dmcphers+openshiftbot@redhat.com)
- Bug 905859: fix picatcha at mobile resolution (sgoodwin@redhat.com)

* Fri Feb 08 2013 Adam Miller <admiller@redhat.com> 1.5.2-2
- bump for chainbuild

* Fri Feb 08 2013 Adam Miller <admiller@redhat.com> 1.5.2-1
- Merge pull request #869 from sg00dwin/bug-fixes (ccoleman@redhat.com)
- Merge pull request #871 from
  smarterclayton/us3292_us3293_us3291_split_community_to_openshift_com
  (dmcphers+openshiftbot@redhat.com)
- US3291 US3292 US3293 - Move community to www.openshift.com
  (ccoleman@redhat.com)
- Bug 885194 - Fixed and activated upgrade form validations (hripps@redhat.com)
- Add function for placehold on signin page include jquery_placeholder for ie9
  and older (sgoodwin@redhat.com)

* Thu Feb 07 2013 Adam Miller <admiller@redhat.com> 1.5.1-2
- bump for chainbuild

* Thu Feb 07 2013 Adam Miller <admiller@redhat.com> 1.5.1-1
- bump_minor_versions for sprint 24 (admiller@redhat.com)

* Wed Feb 06 2013 Adam Miller <admiller@redhat.com> 1.4.9-2
- bump for chainbuild

* Wed Feb 06 2013 Adam Miller <admiller@redhat.com> 1.4.9-1
- Merge pull request #861 from rhamilto/master (dmcphers@redhat.com)
- Merge pull request #854 from fotioslindiakos/BZ907570 (dmcphers@redhat.com)
- Tweaks to improve upon the rotate on hover effect of the logo.
  (rhamilto@redhat.com)
- Missing an alias for plan_upgrade_enabled? (ccoleman@redhat.com)
- Bug 908171 - My account page throws an error when aria disabled
  (ccoleman@redhat.com)
- Bug 907570: Also change message for increasing user storage
  (fotios@redhat.com)

* Tue Feb 05 2013 Adam Miller <admiller@redhat.com> 1.4.8-2
- bump for chainbuild

* Tue Feb 05 2013 Adam Miller <admiller@redhat.com> 1.4.8-1
- Improving coverage tooling (dmcphers@redhat.com)
- Merge pull request #851 from smarterclayton/improve_capability_extension
  (dmcphers+openshiftbot@redhat.com)
- Use string id instead of symbol id for plans (ccoleman@redhat.com)
- Ensure that billing code cannot be reached without the appropriate plan
  attribute (ccoleman@redhat.com)

* Tue Feb 05 2013 Adam Miller <admiller@redhat.com> 1.4.7-2
- bump for chainbuild

* Tue Feb 05 2013 Adam Miller <admiller@redhat.com> 1.4.7-1
- Merge pull request #848 from smarterclayton/fix_firesass_support
  (dmcphers+openshiftbot@redhat.com)
- Fix FireSass support in site (ccoleman@redhat.com)

* Mon Feb 04 2013 Adam Miller <admiller@redhat.com> 1.4.6-2
- bump for chainbuild

* Mon Feb 04 2013 Adam Miller <admiller@redhat.com> 1.4.6-1
- Merge pull request #827 from fotioslindiakos/storage
  (dmcphers+openshiftbot@redhat.com)
- Merge pull request #812 from maxamillion/dev/admiller/move_logs
  (dmcphers+openshiftbot@redhat.com)
- Changed message if the user wants to upgrade storage (fotios@redhat.com)
- Added wrapper for storage_controller tests from console (fotios@redhat.com)
- US2441: View for storage (fotios@redhat.com)
- move all logs to /var/log/openshift/ so we can logrotate properly
  (admiller@redhat.com)

* Mon Feb 04 2013 Adam Miller <admiller@redhat.com> 1.4.5-1
- working on testing coverage (dmcphers@redhat.com)
- Merge pull request #838 from sg00dwin/partnerslink
  (dmcphers+openshiftbot@redhat.com)
- add partners link in footer (sgoodwin@redhat.com)

* Fri Feb 01 2013 Adam Miller <admiller@redhat.com> 1.4.4-2
- bump spec for chainbuild (admiller@redhat.com)

* Fri Feb 01 2013 Adam Miller <admiller@redhat.com> - 1.4.4-2
- bump spec for chain build

* Fri Feb 01 2013 Adam Miller <admiller@redhat.com> 1.4.4-1
- Merge pull request #822 from
  smarterclayton/us3350_establish_plan_upgrade_capability
  (dmcphers+openshiftbot@redhat.com)
- US3350 - Expose a plan_upgrade_enabled capability (ccoleman@redhat.com)

* Thu Jan 31 2013 Adam Miller <admiller@redhat.com> 1.4.3-1
- Login controller doesn't rescue correctly (ccoleman@redhat.com)
- Merge pull request #793 from jtharris/features/US3205
  (dmcphers+openshiftbot@redhat.com)
- Merge pull request #785 from sg00dwin/misc-dev
  (dmcphers+openshiftbot@redhat.com)
- CSS fixes for Bug 902173 - Events page /community/calendar is out of bounds
  on Safari Iphone4S (sgoodwin@redhat.com)
- set outline color to currentColor ftw (sgoodwin@redhat.com)
- make focus outline light gray color (sgoodwin@redhat.com)
- setting tab focus outline to be more visible (sgoodwin@redhat.com)
- Adding call to console/_popover (sgoodwin@redhat.com)
- Introduce classes img-captcha img-recaptcha; Set border-color with variable;
  Move .ie specific class to _core (sgoodwin@redhat.com)
- switch :plain html to haml (sgoodwin@redhat.com)
- _account.scss  - move body, label styles to _base  - condense style rules  -
  remove duplicate form-actions rule  - move bg to body.simple  - control
  reCaptcha widths at mobile portrait and tablet (sgoodwin@redhat.com)
- add bullets for consistency with signup (sgoodwin@redhat.com)
- change default event calendar view style (sgoodwin@redhat.com)

* Wed Jan 30 2013 Adam Miller <admiller@redhat.com> - 1.4.2-2
- bump for chainbuild

* Tue Jan 29 2013 Adam Miller <admiller@redhat.com> 1.4.2-2
- Fixed dependency loading for libs (fotios@redhat.com)
- Fixed tracking.js for captcha story (fotios@redhat.com)
- Fixed tests (fotios@redhat.com)
- View changes for captcha (fotios@redhat.com)
- Controllers changes and helper for captcha (fotios@redhat.com)
- Added tracking code for Google Analytics to track captcha status
  (fotios@redhat.com)
- Added modular captcha libraries (fotios@redhat.com)
- US2709: Captcha replacement (fotios@redhat.com)
- Bug 892821 (dmcphers@redhat.com)
- Bug 888692 (dmcphers@redhat.com)
- fix references to rhc app cartridge (dmcphers@redhat.com)

* Wed Jan 23 2013 Adam Miller <admiller@redhat.com> 1.4.1-1
- bump_minor_versions for sprint 23 (admiller@redhat.com)

* Wed Jan 23 2013 Adam Miller <admiller@redhat.com> 1.3.10-1
- Merge remote-tracking branch 'upstream/master' (ffranz@redhat.com)
- Bug 901949 - improved Twitter tests, now just mocking nonce and timestamp
  instead of the whole OAuth (ffranz@redhat.com)

* Tue Jan 22 2013 Adam Miller <admiller@redhat.com> 1.3.9-1
- Merge pull request #776 from fabianofranz/master
  (dmcphers+openshiftbot@redhat.com)
- Ref bug 901949, Twitter tests removed to make sanity pass (ffranz@redhat.com)
- Fix bug 901342 (ffranz@redhat.com)
- Fix bug 901949, now mocking oauth timestamp and nonce instead of oauth itself
  to provide better tests (ffranz@redhat.com)
- Merge remote-tracking branch 'upstream/master' (ffranz@redhat.com)

* Mon Jan 21 2013 Adam Miller <admiller@redhat.com> 1.3.8-1
- Merge pull request #770 from
  smarterclayton/bug_887522_handle_service_failure_from_streamline
  (dmcphers+openshiftbot@redhat.com)
- Fix mock test (ccoleman@redhat.com)
- Merge pull request #769 from smarterclayton/streamline_spec_tests_pass
  (dmcphers+openshiftbot@redhat.com)
- Properly cleanup and recover from streamline errors, fix the error page in
  the console related to HAML parsing, add unit tests (ccoleman@redhat.com)
- Merge pull request #768 from fabianofranz/master
  (dmcphers+openshiftbot@redhat.com)
- Streamline tests pass (ccoleman@redhat.com)
- Errors from streamline should result in a failure of the operation IF
  queueing is disabled. (ccoleman@redhat.com)
- Added logging to help troubleshoot bug 901342 (ffranz@redhat.com)

* Fri Jan 18 2013 Dan McPherson <dmcphers@redhat.com> 1.3.7-1
- 

* Thu Jan 17 2013 Adam Miller <admiller@redhat.com> 1.3.6-1
- Add test cases for streamline terms acceptance and the expected roles after
  signin (ccoleman@redhat.com)

* Wed Jan 16 2013 Adam Miller <admiller@redhat.com> 1.3.5-1
- Additional method is not needed here (ffranz@redhat.com)
- Fixes Bug 888383 (ffranz@redhat.com)
- Fixes Bug 887887 (ffranz@redhat.com)
- Merge pull request #754 from fabianofranz/dev/ffranz/twitter1.1
  (dmcphers+openshiftbot@redhat.com)
- Increased the Twitter cache timeout to 30 minutes (ffranz@redhat.com)
- Fixed tests for fetching tweets with the new Twitter API (ffranz@redhat.com)
- Added Twitter API development (read-only) keys (ffranz@redhat.com)
- Removed unused artifacts (ffranz@redhat.com)
- Fetching tweets using the new Twitter API (1.1) (ffranz@redhat.com)
- Updating our Twitter clients to use the REST API 1.1 (ffranz@redhat.com)

* Mon Jan 14 2013 Adam Miller <admiller@redhat.com> 1.3.4-1
- Merge pull request #752 from smarterclayton/move_email_confirm_to_extended
  (dmcphers+openshiftbot@redhat.com)
- Move email_confirm tests to extended (it hits Streamline)
  (ccoleman@redhat.com)

* Thu Jan 10 2013 Adam Miller <admiller@redhat.com> 1.3.3-2
- bump site.spec Release: for fake chain-build with console
  (admiller@redhat.com)

* Thu Jan 10 2013 Adam Miller <admiller@redhat.com> 1.3.3-1
- Merge pull request #745 from smarterclayton/bug_892232_show_recent_issues
  (dmcphers+openshiftbot@redhat.com)
- Merge pull request #742 from smarterclayton/add_robots_for_john
  (dmcphers+openshiftbot@redhat.com)
- Bug 892232 - Show any resolved issues from the last 3 months
  (ccoleman@redhat.com)
- Update site robots.txt (ccoleman@redhat.com)
- Introduce classes img-captcha img-recaptcha; Set border-color with variable;
  Move .ie specific class to _core (sgoodwin@redhat.com)
- switch :plain html to haml (sgoodwin@redhat.com)
- _account.scss  - move body, label styles to _base  - condense style rules  -
  remove duplicate form-actions rule  - move bg to body.simple  - control
  reCaptcha widths at mobile portrait and tablet (sgoodwin@redhat.com)
- add bullets for consistency with signup (sgoodwin@redhat.com)
- change default event calendar view style (sgoodwin@redhat.com)
- Merge pull request #726 from
  smarterclayton/run_external_code_tests_in_extended (openshift+bot@redhat.com)
- Merge pull request #685 from EmilyDirsh/master (openshift+bot@redhat.com)
- Run all external integration test cases in the extended suite
  (ccoleman@redhat.com)
- Make enterprise banner responsive (edirsh@redhat.com)
- Replace "speed" icon with "enterprise" icon on home page (edirsh@redhat.com)

* Tue Dec 18 2012 Adam Miller <admiller@redhat.com> 1.3.2-2
- bump site.spec Release: for fake chain-build with console
  (admiller@redhat.com)

* Tue Dec 18 2012 Adam Miller <admiller@redhat.com> 1.3.2-1
- Merge pull request #720 from sg00dwin/failed-login-inputs
  (openshift+bot@redhat.com)
- include class on when error state (sgoodwin@redhat.com)
- Hide the outage box in the login page when there are no messages to display
  (ffranz@redhat.com)

* Wed Dec 12 2012 Adam Miller <admiller@redhat.com> 1.3.1-2
- bump site.spec Release: for fake chain-build with console
  (admiller@redhat.com)

* Wed Dec 12 2012 Adam Miller <admiller@redhat.com> 1.3.1-1
- bump_minor_versions for sprint 22 (admiller@redhat.com)

* Wed Dec 12 2012 Adam Miller <admiller@redhat.com> 1.2.7-2
- bump site.spec Release: for fake chain-build with console
  (admiller@redhat.com)

* Wed Dec 12 2012 Adam Miller <admiller@redhat.com> 1.2.7-1
- Merge remote-tracking branch 'upstream/master' (ffranz@redhat.com)
- Improved styling for outage messages in the login page (ffranz@redhat.com)
- Fix for Bug 883334. Addition of class to sigin and signup buttons.
  (sgoodwin@redhat.com)
- Fixes Bug 886451 by properly displaying multiple outage messages in the login
  page (ffranz@redhat.com)
- Merge pull request #708 from sg00dwin/dev-release-notes
  (openshift+bot@redhat.com)
- add style for release list (sgoodwin@redhat.com)

* Tue Dec 11 2012 Adam Miller <admiller@redhat.com> 1.2.6-2
- bump site.spec Release: for fake chain-build with console
  (admiller@redhat.com)

* Tue Dec 11 2012 Adam Miller <admiller@redhat.com> 1.2.6-1
- Fixes rhc-outage date and time display in the login page (ffranz@redhat.com)
- Fixes Bug 884508, improved URI encoding (ffranz@redhat.com)
- Fixes Bug 884508 (ffranz@redhat.com)
- edit width (sgoodwin@redhat.com)
- bug 884414 fix signup page width at mobile portrait view
  (sgoodwin@redhat.com)
- Added suppress ribbon support to haml pages (ffranz@redhat.com)
- Now displaying release notes info in the login pages, styling improvements
  (ffranz@redhat.com)
- Adjusted some images path on css styles (ffranz@redhat.com)
- Improved simple theme (sign in, sign up, remember password and other pages),
  added outage issues and news to login page (ffranz@redhat.com)
- New css for account (sgoodwin@redhat.com)
- switch background-position from 4 value to 2 value syntax since to appease
  Chrome & Safari (sgoodwin@redhat.com)
- switch text hover to be underline (sgoodwin@redhat.com)
- Updates to simple template including css/design changes. New mixin for
  account_background. (sgoodwin@redhat.com)

* Fri Dec 07 2012 Adam Miller <admiller@redhat.com> 1.2.5-2
- bump site.spec Release: for fake chain-build with console
  (admiller@redhat.com)

* Fri Dec 07 2012 Adam Miller <admiller@redhat.com> 1.2.5-1
- Merge pull request #697 from
  smarterclayton/sitemap_and_updates_to_quickstart_permissions
  (dmcphers@redhat.com)
- Merge pull request #695 from
  smarterclayton/bug_884747_be_resilient_to_bad_json_data (dmcphers@redhat.com)
- Updated streamline handling to match API changes (nhr@redhat.com)
- Sitemap and updates to application quickstarts (ccoleman@redhat.com)
- Bug 884747 - Be resilient to bad JSON data from the community
  (ccoleman@redhat.com)

* Thu Dec 06 2012 Adam Miller <admiller@redhat.com> 1.2.4-2
- bump site.spec Release: for fake chain-build with console
  (admiller@redhat.com)

* Wed Dec 05 2012 Adam Miller <admiller@redhat.com> 1.2.4-1
- fix mobile portrait view of enterprise message bz 879501
  (sgoodwin@redhat.com)

* Tue Dec 04 2012 Adam Miller <admiller@redhat.com> 1.2.3-2
- bump site.spec Release: for fake chain-build with console
  (admiller@redhat.com)

* Tue Dec 04 2012 Adam Miller <admiller@redhat.com> 1.2.3-1
- Revised test case to match revisions in underlying code (nhr@redhat.com)
- Improved test case based on feedback (nhr@redhat.com)
- Added test to insure propoagation of multiple errors on same element
  (nhr@redhat.com)
- Updated based on review feedback (nhr@redhat.com)
- Revised promote flow and fixed error handling (hripps@redhat.com)
- Added blanket Aria omit checks for plans_controller tests (nhr@redhat.com)
- Suppressing Aria-related tests based on test.rb setting (nhr@redhat.com)

* Thu Nov 29 2012 Adam Miller <admiller@redhat.com> 1.2.2-2
- bump site.spec Release: for fake chain-build with console
  (admiller@redhat.com)

* Thu Nov 29 2012 Adam Miller <admiller@redhat.com>
- 

* Thu Nov 29 2012 Adam Miller <admiller@redhat.com> 1.2.2-1
- Corrected missing field for streamline promotion; fixed mock integration data
  to match current form structures. (hripps@redhat.com)
- Corrected streamline proxy URL (hripps@redhat.com)
- Inline context not necessary for lone checkbox (hripps@redhat.com)
- Refactored based on code review (hripps@redhat.com)
- Refactored to accomodate streamline full-user promote and formtastic mods
  (hripps@redhat.com)
- Updated based on code review (hripps@redhat.com)
- Added integration test for promoteUser API (hripps@redhat.com)
- Added unit tests for promote_user (hripps@redhat.com)
- Modified streamline / account upgrades to handle user promotions
  (hripps@redhat.com)
- Bug 879501 - Outage message too wide at mobile resolutions
  (ccoleman@redhat.com)
- Merge pull request #655 from
  smarterclayton/us3055_enterprise_content_for_launch_to_stage
  (openshift+bot@redhat.com)
- US3055 - Enterprise content for stage (ccoleman@redhat.com)
- using oo-ruby (dmcphers@redhat.com)
- Merge pull request #653 from sg00dwin/master (ccoleman@redhat.com)
- images in correct dir, change to masthead-div (sgoodwin@redhat.com)
- Merge pull request #652 from sg00dwin/master (ccoleman@redhat.com)
- masthead div hidden by default (sgoodwin@redhat.com)
- Addition of masthead for homepage, banner files, enterprise files, swap
  pricing and plans link for enterprise link (sgoodwin@redhat.com)
- Reverted  conditional based on feedback (hripps@redhat.com)
- Refactored Aria-related tests to omit if Aria isn't available
  (hripps@redhat.com)
- Fixes BZ876027 (ffranz@redhat.com)

* Sat Nov 17 2012 Adam Miller <admiller@redhat.com> 1.2.1-1
- bump_minor_versions for sprint 21 (admiller@redhat.com)

* Fri Nov 16 2012 Adam Miller <admiller@redhat.com> 1.1.8-2
- bump site.spec Release: for fake chain-build with console
  (admiller@redhat.com)

* Fri Nov 16 2012 Adam Miller <admiller@redhat.com> 1.1.8-1
- Merge pull request #630 from smarterclayton/slightly_extend_match_spec
  (openshift+bot@redhat.com)
- Merge pull request #624 from
  smarterclayton/better_gear_limit_message_on_create (ccoleman@redhat.com)
- Ensure cartridge type test runs from li/site tests (ccoleman@redhat.com)
- Stop overlaying our message on top of the broker's message, now that it is
  better. (ccoleman@redhat.com)

* Thu Nov 15 2012 Adam Miller <admiller@redhat.com> 1.1.7-2
- bump site.spec Release: for fake chain-build with console
  (admiller@redhat.com)

* Thu Nov 15 2012 Adam Miller <admiller@redhat.com> 1.1.7-1
- Can't search community content from the 404 page, no form action or input
  name (ccoleman@redhat.com)
- Merge pull request #604 from
  smarterclayton/deliver_content_to_mainpage_from_community
  (openshift+bot@redhat.com)
- Handle test failures due to twitter rate limits (ccoleman@redhat.com)
- Mock twitter so as to prevent rate limit test failures (ccoleman@redhat.com)
- Content should be loaded from the community for the blogs section on the
  site, and tweets should be loaded via a better caching mechanism
  (ccoleman@redhat.com)

* Wed Nov 14 2012 Adam Miller <admiller@redhat.com> 1.1.6-2
- bump site.spec Release: for fake chain-build with console
  (admiller@redhat.com)

* Wed Nov 14 2012 Adam Miller <admiller@redhat.com> 1.1.6-1
- Merge pull request #612 from smarterclayton/us3046_quickstarts_and_app_types
  (openshift+bot@redhat.com)
- Merge remote-tracking branch 'origin/master' into
  us3046_quickstarts_and_app_types (ccoleman@redhat.com)
- Plan capabilities were not decaching correctly (ccoleman@redhat.com)
- Attempt to resolve issues with test race conditions (ccoleman@redhat.com)
- US3046 - Implement quickstarts in drupal and react to changes in console
  (ccoleman@redhat.com)

* Wed Nov 14 2012 Adam Miller <admiller@redhat.com> 1.1.5-1
- Merge pull request #606 from smarterclayton/bug_874916_bad_url_helpers
  (dmcphers@redhat.com)
- Add account helper back (ccoleman@redhat.com)
- Bug 874916 - A number of community URL helpers were duplicated
  (ccoleman@redhat.com)
- Bug 876017 - Mark rh_sso httponly (ccoleman@redhat.com)

* Tue Nov 13 2012 Adam Miller <admiller@redhat.com> 1.1.4-1
- Styled the events list by country, sync date and country views, ical feed
  improvements (ffranz@redhat.com)
- Improved styling for events list (ffranz@redhat.com)
- Added more data to the iCal feed, added iCal link, improved tabs styling in
  the events list page (ffranz@redhat.com)
- Improved Events page with better styles, logo upload, venue info, etc
  (ffranz@redhat.com)
- New Events section styles, added event detail page (ffranz@redhat.com)

* Mon Nov 12 2012 Adam Miller <admiller@redhat.com> 1.1.3-2
- bump site.spec Release: for fake chain-build with console
  (admiller@redhat.com)

* Mon Nov 12 2012 Adam Miller <admiller@redhat.com> 1.1.3-1
- Merge pull request #589 from
  smarterclayton/bug_874944_prevent_session_fixation (openshift+bot@redhat.com)
- Merge pull request #590 from
  smarterclayton/bug_874896_redirect_allows_bad_paths
  (openshift+bot@redhat.com)
- Bug 874896 - Redirection after login allows paths without a leading slash,
  which creates dangerous URLs (ccoleman@redhat.com)
- Bug 874944 - Prevent session fixation in site (ccoleman@redhat.com)

* Thu Nov 08 2012 Adam Miller <admiller@redhat.com> 1.1.2-2
- bump site.spec Release: for fake chain-build with console
  (admiller@redhat.com)

* Thu Nov 08 2012 Adam Miller <admiller@redhat.com> 1.1.2-1
- The status link is not present on OpenShift production when we deployed to
  production (ccoleman@redhat.com)
- Merge pull request #561 from sg00dwin/master (openshift+bot@redhat.com)
- placeholder color fix (sgoodwin@redhat.com)

* Thu Nov 01 2012 Adam Miller <admiller@redhat.com> 1.1.1-1
- bump_minor_versions for sprint 20 (admiller@redhat.com)

* Thu Nov 01 2012 Adam Miller <admiller@redhat.com> 1.0.3-2
- bump site.spec Release: for fake chain-build with console
  (admiller@redhat.com)

* Thu Nov 01 2012 Adam Miller <admiller@redhat.com> 1.0.3-1
- Bug 872054 - When a user enters the wrong email in their confirmation link,
  Streamline invalidates the token and then rejects the request.  We can
  display a better message in that scenario. (ccoleman@redhat.com)

* Wed Oct 31 2012 Adam Miller <admiller@redhat.com> 1.0.2-2
- bump site.spec Release: for fake chain-build with console
  (admiller@redhat.com)

* Wed Oct 31 2012 Adam Miller <admiller@redhat.com> 1.0.2-1
- Omit streamline failure in staging until it can be resolved
  (ccoleman@redhat.com)

* Tue Oct 30 2012 Adam Miller <admiller@redhat.com> 1.0.1-2
- bump site.spec Release: for fake chain-build with console
  (admiller@redhat.com)

* Tue Oct 30 2012 Adam Miller <admiller@redhat.com> 1.0.1-1
- bumping specs to at least 1.0.0 (dmcphers@redhat.com)

* Mon Oct 29 2012 Adam Miller <admiller@redhat.com> 0.99.15-2
- bump site.spec Release: for fake chain-build with console
  (admiller@redhat.com)

* Mon Oct 29 2012 Adam Miller <admiller@redhat.com> 0.99.15-1
- Merge pull request #518 from smarterclayton/console_remote_user
  (openshift+bot@redhat.com)
- Bug 869590 - Infinite redirect on visit to /unauthorized
  (ccoleman@redhat.com)
- Update site to accomodate new console config settings and implement
  console_access_denied exception handler. (ccoleman@redhat.com)

* Fri Oct 26 2012 Adam Miller <admiller@redhat.com> 0.99.14-3
- bump site.spec Release: for fake chain-build with console
  (admiller@redhat.com)

* Wed Oct 24 2012 Adam Miller <admiller@redhat.com> 0.99.14-2
- bump site.spec Release: for fake chain-build with console
  (admiller@redhat.com)

* Wed Oct 24 2012 Adam Miller <admiller@redhat.com> 0.99.14-1
- Merge pull request #492 from nhr/specify_gear_size (openshift+bot@redhat.com)
- Fixing a test case to pre-authenticate (nhr@redhat.com)
- fix bz 864777 (sgoodwin@redhat.com)

* Fri Oct 19 2012 Adam Miller <admiller@redhat.com> 0.99.13-3
- bump site Release for quasi chain build (admiller@redhat.com)

* Fri Oct 19 2012 Adam Miller <admiller@redhat.com> 0.99.13-2
- bump site Release for quasi chain build (admiller@redhat.com)

* Fri Oct 19 2012 Adam Miller <admiller@redhat.com> 0.99.13-1
- Merge pull request #499 from fabianofranz/master (dmcphers@redhat.com)
- Added TOC limit support to site styles (ffranz@redhat.com)

* Thu Oct 18 2012 Adam Miller <admiller@redhat.com> 0.99.12-2
- bump site Release for quasi chain build (admiller@redhat.com)

* Thu Oct 18 2012 Adam Miller <admiller@redhat.com> 0.99.12-1
- Merge pull request #482 from sg00dwin/master (openshift+bot@redhat.com)
- Adjust linear gradient degree to account for rendering change introduced in
  FF16 more info here https://hacks.mozilla.org/2012/07/aurora-16-is-out/
  (sgoodwin@redhat.com)
- Merge branch 'master' of github.com:openshift/li (sgoodwin@redhat.com)
- Merge branch 'master' of github.com:openshift/li (sgoodwin@redhat.com)
- fix bz816372 (sgoodwin@redhat.com)

* Tue Oct 16 2012 Adam Miller <admiller@redhat.com> 0.99.11-2
- bump spec file for chain build 

* Tue Oct 16 2012 Adam Miller <admiller@redhat.com> 0.99.11-1
- Allow streamline tests to fail, fixup auth to match latest changes
  (ccoleman@redhat.com)

* Mon Oct 15 2012 Adam Miller <admiller@redhat.com> 0.99.10-2
- Bump Release of site for quasi chain-build (admiller@redhat.com)

* Mon Oct 15 2012 Adam Miller <admiller@redhat.com> 0.99.10-1
- removing addressable dep, not needed. (admiller@redhat.com)
- Changed blurb in the website home (ffranz@redhat.com)

* Mon Oct 08 2012 Adam Miller <admiller@redhat.com> 0.99.9-1
- US2912 - Site should customize error pages to use site layout
  (ccoleman@redhat.com)
- Merge pull request #448 from smarterclayton/preserve_old_content
  (openshift+bot@redhat.com)
- Merge pull request #451 from smarterclayton/production_assets_broken
  (openshift+bot@redhat.com)
- Merge pull request #439 from nhr/BZ849627 (openshift+bot@redhat.com)
- Merge pull request #449 from sg00dwin/master (openshift+bot@redhat.com)
- renaming crankcase -> origin-server (dmcphers@redhat.com)
- Fixing renames, paths, configs and cleaning up old packages. Adding
  obsoletes. (kraman@gmail.com)
- Revert to Shawns' changes (ccoleman@redhat.com)
- Use application.js in console in production, rather than console.js
  (ccoleman@redhat.com)
- Asset compilation in production should be disabled without digests, but a
  Rails issue is preventing page rendering when digests are off.  Patch Rails,
  then ensure the correct compile = false flags are present.
  (ccoleman@redhat.com)
- Corrected error handling for inlined selects (hripps@redhat.com)
- Merge branch 'master' of github.com:openshift/li (sgoodwin@redhat.com)
- css fix for bz 849077 Include link to overpass.css for styleguide
  (sgoodwin@redhat.com)
- Re-added semantic_errors calls to handle general form errors.
  (hripps@redhat.com)
- Merge branch 'master' of github.com:openshift/li (admiller@redhat.com)
- Explicitly calling for error strings on customized selects
  (hripps@redhat.com)
- Removed explicit error inclusion; happens automatically (hripps@redhat.com)
- Add generated versions of site and console CSS/JS for N-1 compatibility
  (ccoleman@redhat.com)
- Temporarily preserve asset files that were moved for N-1 sprint
  compatability.  This commit should be undone later. (ccoleman@redhat.com)
- Ignore gemfile.lock always during builds (ccoleman@redhat.com)
- Allow variable extension. (ccoleman@redhat.com)
- Isolate site specific variables (ccoleman@redhat.com)
- Transparent noise image should not be inlined for size reasons
  (ccoleman@redhat.com)
- Revised inlined form elements to use revised error capture method
  (hripps@redhat.com)
- Removed month names to avoid I18N complications (hripps@redhat.com)
- BZ849627 Revised forms to correctly use new formtastic inline presentation
  (hripps@redhat.com)
- Merge branch 'master' of github.com:openshift/li (sgoodwin@redhat.com)

* Thu Oct 04 2012 Adam Miller <admiller@redhat.com> 0.99.8-2
- bump site.spec Release: for fake chain-build with console
  (admiller@redhat.com)

* Thu Oct 04 2012 Adam Miller <admiller@redhat.com> 0.99.8-1
- Merge pull request #441 from
  smarterclayton/not_found_and_error_pages_for_drupal
  (openshift+bot@redhat.com)
- Merge pull request #440 from sg00dwin/master (openshift+bot@redhat.com)
- Merge pull request #435 from
  smarterclayton/bug862362_move_remaining_js_to_assets
  (openshift+bot@redhat.com)
- Add not found and error pages for drupal (ccoleman@redhat.com)
- horizontal logo for aws marketplace (sgoodwin@redhat.com)
- Bug 862362 Move remaining js to assets to avoid errors and simplify links
  (ccoleman@redhat.com)

* Wed Oct 03 2012 Adam Miller <admiller@redhat.com> 0.99.7-1
- Merge pull request #395 from nhr/specify_gear_size (openshift+bot@redhat.com)
- Merge pull request #434 from
  smarterclayton/bug862065_additional_faq_on_signup (openshift+bot@redhat.com)
- Merge pull request #430 from
  smarterclayton/bug862298_add_passenger_to_site_rpm (openshift+bot@redhat.com)
- US1375 Created multi-gear user for test; moved URLs to helpers
  (hripps@redhat.com)
- Bug 862065 - Add some additional info to signup complete page.
  (ccoleman@redhat.com)
- Bug 862298 - Add passenger dependencies to RPM (ccoleman@redhat.com)
- Merge pull request #426 from danmcp/master (openshift+bot@redhat.com)
- Merge pull request #422 from smarterclayton/favicon_misplaced
  (openshift+bot@redhat.com)
- Favicon-32 should be in the assets directory (ccoleman@redhat.com)
- Overpass was missing from site (ccoleman@redhat.com)
- Removing Gemfile.locks (dmcphers@redhat.com)

* Sat Sep 29 2012 Adam Miller <admiller@redhat.com> 0.99.6-4
- fix typo in Requires ... its late (admiller@redhat.com)

* Sat Sep 29 2012 Adam Miller <admiller@redhat.com> 0.99.6-3
- Fixed -Release -- added missing Requires: from Gemfile to spec
  (admiller@redhat.com)
- added missing Requires: from Gemfile to spec (admiller@redhat.com)

* Sat Sep 29 2012 Adam Miller <admiller@redhat.com>
- added missing Requires: from Gemfile to spec (admiller@redhat.com)

* Sat Sep 29 2012 Adam Miller <admiller@redhat.com> 0.99.6-2
- Release bump to build against newer origin console 

* Sat Sep 29 2012 Adam Miller <admiller@redhat.com> 0.99.6-2
- Release bump to build against newer version of origin console

* Sat Sep 29 2012 Adam Miller <admiller@redhat.com> 0.99.6-1
- add addressable gem dep to site (admiller@redhat.com)

* Fri Sep 28 2012 Adam Miller <admiller@redhat.com> 0.99.5-1
- Merge pull request #417 from smarterclayton/add_therubyracer
  (openshift+bot@redhat.com)
- Add therubyracer for RPM builds (ccoleman@redhat.com)
- Merge pull request #416 from
  smarterclayton/bug861184_confirmation_on_password_change
  (openshift+bot@redhat.com)
- Merge pull request #415 from smarterclayton/bug861317_typo_in_error
  (openshift+bot@redhat.com)
- Bug 861184 - Confirmation on password change (ccoleman@redhat.com)
- Bug 861317 - Typo in error message for key creation (ccoleman@redhat.com)

* Fri Sep 28 2012 Adam Miller <admiller@redhat.com> 0.99.4-1
- Merge pull request #413 from smarterclayton/remove_execjs_dependency
  (openshift+bot@redhat.com)
- Merge pull request #412 from smarterclayton/more_asset_images
  (openshift+bot@redhat.com)
- Remove dependency on SpiderMonkey for ExecJS (ccoleman@redhat.com)
- Credit card images should be assets (ccoleman@redhat.com)
- Merge pull request #411 from
  smarterclayton/bug860892_drupal_needs_to_use_new_assets_paths
  (openshift+bot@redhat.com)
- Bug 860892 - No CSS or JS in drupal, need to update theme to point to new
  directories (ccoleman@redhat.com)

* Wed Sep 26 2012 Adam Miller <admiller@redhat.com> 0.99.3-1
- Ensure key messages are the same from the engine and the site
  (ccoleman@redhat.com)
- Remove old unused test (preventing test:check:base from running)
  (ccoleman@redhat.com)
- Use a relative path for default Gemfile.lock for development mode
  (ccoleman@redhat.com)
- Bug 860223 - Load error when resetting password a second time
  (ccoleman@redhat.com)
- Add other tests, only update lock file for site and console
  (ccoleman@redhat.com)
- Httparty rpm available (ccoleman@redhat.com)
- Bug 860223 - Error when resetting password, a class was being reloaded
  (ccoleman@redhat.com)
- Merge branch 'opensource_console_final' of github.com:smarterclayton/li into
  dev0924 (sgoodwin@redhat.com)
- Add default bottom margin to h1, h2 Adjust various custom heading styles to
  offset change and addtion of smaller font to wiki/community default links
  (subscribe, flag, bookmark links) (sgoodwin@redhat.com)
- Handle generic exceptions more abstractly ConsoleController no longer
  rescues, that is calling applications responsibility Fix bug 859564 -
  newsletter signup (ccoleman@redhat.com)
- Remove Rails 3.0 workaround for bootstrap simple forms (ccoleman@redhat.com)
- Only load webmock in test env (ccoleman@redhat.com)
- Gemfile.lock should be more specific (ccoleman@redhat.com)
- Site is almost ready to build (ccoleman@redhat.com)
- Console builds in devenv/builder (ccoleman@redhat.com)
- Visibility of application_controller methods changed (ccoleman@redhat.com)
- Ensure application errors (not generic errors) are caught across the entire
  site (ccoleman@redhat.com)
- Ensure site properly respects error handlers (ccoleman@redhat.com)
- Fixup JS errors related to twitter and home js being loaded on all pages
  (ccoleman@redhat.com)
- Force bundle installation of site gems, make selinux enablement correct.  Set
  permissions on site_ruby (ccoleman@redhat.com)
- Do not create development.log (ccoleman@redhat.com)
- Merge remote-tracking branch 'origin/master' into opensource_console_final
  (ccoleman@redhat.com)
- Changes necessary to run site in devenv in Ruby 1.9 mode (selinux execmem
  hack, change order site.conf is loaded, and add site_ruby stub for
  LD_LOAD_PATH) (ccoleman@redhat.com)
- Fix asset building (incomplete task conversion) and prep site spec build
  requires (ccoleman@redhat.com)
- Site spec update (ccoleman@redhat.com)
- Arrange content so that the same markup can be shown in the site and console
  (ccoleman@redhat.com)
- Error page and test (ccoleman@redhat.com)
- * Add simple Pry support * Add error page renderer * Fix test failures in
  domain/key due to new RestApi::ResourceNotFound exception
  (ccoleman@redhat.com)
- Billing info needs to_key implementation (ccoleman@redhat.com)
- Merge branch 'master' into rails32 (ccoleman@redhat.com)
- Merge branch 'master' into rails32 (ccoleman@redhat.com)
- Build site specs under Rails 3.2 (sort out asset issues, use bundler for now)
  (ccoleman@redhat.com)
- Add simplecov support to the site, remove some obvious unused and dead code
  (ccoleman@redhat.com)
- Fix some rails 32 issues in the account section (ccoleman@redhat.com)
- Include required images into the assets folder. (ccoleman@redhat.com)
- More purging and moves (ccoleman@redhat.com)
- Massive asset renaming spree (ccoleman@redhat.com)
- Make footer more opensource compatible. (ccoleman@redhat.com)
- Move console assets into place. (ccoleman@redhat.com)
- Abstract branding, begin moving images. (ccoleman@redhat.com)
- Remove SSH startup for li in rails server script (ccoleman@redhat.com)
- Update site to rails 3.2 gems.  Remove references to .length on
  ActiveModel::Errors.  Use ::SecureRandom instead of
  ActiveSupport::SecureRandom.  Other minor cleanup. (ccoleman@redhat.com)
- Remove upgrade_in_rails31 and fix 404 rendering in console app
  (ccoleman@redhat.com)
- Rails 3.2 testing.  Refactor active_resource overrides and remove old paths
  (some fixes merged upstream).  Change to use ActiveModel::Dirty more
  effectively.  Begin stubbing out and removing old 3.0 code - some code still
  stubs.  Handle cacheable resources correctly with to_partial_path
  (ccoleman@redhat.com)
- Merge error with logged_in (which has been removed) (ccoleman@redhat.com)
- filter_hash is implicitly loaded (ccoleman@redhat.com)
- Merge remote-tracking branch 'origin/master' into opensource
  (ccoleman@redhat.com)
- More 1.9 fixes in site (ccoleman@redhat.com)
- Ruby 1.9 support (ccoleman@redhat.com)
- Rename openshift_origin_console to openshift-origin-console to match overall
  openshift gem naming (extensions of openshift). (ccoleman@redhat.com)
- All tests should pass! (ccoleman@redhat.com)
- Separate streamline user tests (ccoleman@redhat.com)
- Ensure there are test stubs for all tests.  Fix failing unit tests in base.
  (ccoleman@redhat.com)
- Ensure console and site both have extended tests (ccoleman@redhat.com)
- Demonstrate relocatable test (ccoleman@redhat.com)
- Ensure devenv builds correctly with origin (ccoleman@redhat.com)
- Ensure version can be run without bundler. (ccoleman@redhat.com)
- Site spec needs to require openshift_origin_console (ccoleman@redhat.com)
- Gem builds, site can launch via gem or via path (ccoleman@redhat.com)
- Rename gemspecs and rpm (ccoleman@redhat.com)
- Allow tests in console to be executed in scope of current app.
  (ccoleman@redhat.com)
- Implement a root path, split coffee into appropriate files, and fix load
  errors in console tests. (ccoleman@redhat.com)
- Put videos in proper location, cleanup and fix issues in site helpers.  All
  site tests pass. (ccoleman@redhat.com)
- Scope helpers and provide config so that applications can include/override
  specific methods. (ccoleman@redhat.com)
- More tests running in site (ccoleman@redhat.com)
- Move stub footer and update source links to proposed destinations.
  (ccoleman@redhat.com)
- Clean up CSS and images (pure copy) (ccoleman@redhat.com)
- Get remaining javascript in the right place (ccoleman@redhat.com)
- Application templates pass (html5 boilerplate needs to come back as well)
  (ccoleman@redhat.com)
- Most tests pass, move stylesheets back to site. (ccoleman@redhat.com)
- Building, app, scaling, and cart controller tests pass (ccoleman@redhat.com)
- Account code split into console (ccoleman@redhat.com)
- Some functional tests pass (ccoleman@redhat.com)
- Move helpers to correct location (ccoleman@redhat.com)
- Move helpers and other code into the right locations (ccoleman@redhat.com)
- Rest API unit tests run, finish merging latest changes (ccoleman@redhat.com)
- Merge branch 'master' into opensource (ccoleman@redhat.com)
- Move javascript into console, remove dead javascript (ccoleman@redhat.com)
- Update root to redirect to /console Move app_redirector into console gem
  Update footer to point back to opensource on GitHub Update domain suffixes
  (ccoleman@redhat.com)
- CSS mostly working (ccoleman@redhat.com)
- Move footer back to preserve version history. (ccoleman@redhat.com)
- Merge branch 'master' into dev/clayton/opensource (ccoleman@redhat.com)
- Merge branch 'master' into dev/clayton/opensource (ccoleman@redhat.com)
- Setup locales in the gem (ccoleman@redhat.com)
- Add simple web_user.rb, add dependency on mocha in gemspec, move methods from
  application_helper.rb (ccoleman@redhat.com)
- Refactor user_controller to use the engine user_controller
  (ccoleman@redhat.com)
- Begin rearranging user_controller to be easily overriden
  (ccoleman@redhat.com)
- Copy routes, move initializers (ccoleman@redhat.com)
- Move /test and image resources into opensource (ccoleman@redhat.com)
- Move the rest /app for opensource (ccoleman@redhat.com)
- Move /lib directory contents out (ccoleman@redhat.com)
- Bad comments in opensource.sh (ccoleman@redhat.com)
- Move selenium into site (ccoleman@redhat.com)
- All contents documented (ccoleman@redhat.com)

* Thu Sep 20 2012 Adam Miller <admiller@redhat.com> 0.99.2-1
- Merge pull request #372 from nhr/formtastic_layout (openshift+bot@redhat.com)
- Fixed month/year selects per feedback (hripps@redhat.com)
- Temporarily suspended JS validation logic for inline form elements
  (hripps@redhat.com)
- Formtastic gymnastics - new control + CSS adoption (hripps@redhat.com)
- Change hard-coded references to mongodb-2.2 (rmillner@redhat.com)
- Make related logo background not be white (ccoleman@redhat.com)

* Wed Sep 12 2012 Adam Miller <admiller@redhat.com> 0.99.1-1
- bump_minor_versions for sprint 18 (admiller@redhat.com)

* Wed Sep 12 2012 Adam Miller <admiller@redhat.com> 0.98.9-1
- bug fixes - 835843, 828111 (sgoodwin@redhat.com)
- Revised Aria::MasterPlan::description() (hripps@redhat.com)
- Fixed test setup to match plans controller behavior (hripps@redhat.com)
- Updated with feedback from pull request discussion (hripps@redhat.com)
- Applied layout & CSS to plan confirmation page (hripps@redhat.com)
- Revised functional testing of account upgrade controller (hripps@redhat.com)
- ruby style refactor; corrected plan signup tests (hripps@redhat.com)
- Updated from feedback. (hripps@redhat.com)
- Fixed features parser to handle empty sets (hripps@redhat.com)
- Added end-to-end plans description and feature comparison (hripps@redhat.com)
- Merge pull request #359 from
  smarterclayton/bug849950_fix_priority_order_of_mongo_vs_diy
  (openshift+bot@redhat.com)
- Merge pull request #363 from smarterclayton/last_minute_zend_changes
  (openshift+bot@redhat.com)
- Ruby 1.8.7 can't sort symbols (ccoleman@redhat.com)
- Updates for Zend based on last minute feedback (ccoleman@redhat.com)
- bug 828111 fix (sgoodwin@redhat.com)
- Bug 849950 - DIY cart has lower priority, deeper bug in sort order
  (ccoleman@redhat.com)

* Tue Sep 11 2012 Troy Dawson <tdawson@redhat.com> 0.98.8-1
- Merge pull request #356 from sg00dwin/master (openshift+bot@redhat.com)
- Minor css updates (sgoodwin@redhat.com)
- Merge branch 'master' of github.com:openshift/li (sgoodwin@redhat.com)

* Mon Sep 10 2012 Troy Dawson <tdawson@redhat.com> 0.98.7-1
- 

* Mon Sep 10 2012 Troy Dawson <tdawson@redhat.com> 0.98.6-1
- Merge pull request #353 from
  smarterclayton/bug849950_ensure_cart_tags_properly_pulled_from_server
  (openshift+bot@redhat.com)
- Backport changes from the opensource branch that fix build issues
  (ccoleman@redhat.com)
- Bug 849950 - Respect server tags (ccoleman@redhat.com)
- Bug 849950 - Give Zend cart proper metadata and ensure sorting of cartridges
  on the cartridge page is working. (ccoleman@redhat.com)

* Fri Sep 07 2012 Adam Miller <admiller@redhat.com> 0.98.5-1
- Merge pull request #350 from sg00dwin/master (openshift+bot@redhat.com)
- Merge pull request #340 from pravisankar/dev/ravi/zend-fix-description
  (openshift+bot@redhat.com)
- Merge branch 'master' of github.com:openshift/li (sgoodwin@redhat.com)
- add table-fixed class for IE text-overflow bug on sshkey table. Include form
  field states back in _custom (not sure why they don't work in _forms)
  (sgoodwin@redhat.com)
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
- Modify Display-name/Description fields for all cartridges (rpenta@redhat.com)

* Thu Sep 06 2012 Adam Miller <admiller@redhat.com> 0.98.4-1
- Merge pull request #343 from spurtell/spurtell/analytics
  (openshift+bot@redhat.com)
- updated sitespeedsample rate, updated origin download tracking, updated
  kissinsights code (spurtell@redhat.com)
- Merge branch 'master' of github.com:openshift/li (sgoodwin@redhat.com)
- Chrome bug fix 851389. Target Chrome and adjust span-flush-right to allow for
  width variance at grid spans widths within 768-980 (sgoodwin@redhat.com)

* Tue Sep 04 2012 Adam Miller <admiller@redhat.com> 0.98.3-1
- Added some functional tests around plan upgrades (hripps@redhat.com)

* Thu Aug 30 2012 Adam Miller <admiller@redhat.com> 0.98.2-1
- TA2740 Added form validation for payment, billing & technical account info
  (hripps@redhat.com)
- Merge pull request #325 from nhr/TA2734 (openshift+bot@redhat.com)
- Bug 849627 - In development mode, the Enter payment method form would hide
  errors. (ccoleman@redhat.com)
- Cloned the console layout & theme for use with accounts (hripps@redhat.com)
- Move console scss completely into partials so that it can be reused.
  (ccoleman@redhat.com)
- Use .name because aria_plan is protected (ccoleman@redhat.com)
- Add thread timeout safety to the async_aware gem method, and a test.  This
  fixes intermittent test failures with account dashboard (5s join timeout
  before).  Default timeout is now 15s. Also fix cases with parallel test
  cleanup (domain is stomping on other domains). (ccoleman@redhat.com)
- Merge pull request #298 from sg00dwin/master (openshift+bot@redhat.com)
- 849902 fix pricing page to display example site boxes correctly at mobile
  sizes (sgoodwin@redhat.com)

* Wed Aug 22 2012 Adam Miller <admiller@redhat.com> 0.98.1-1
- bump_minor_versions for sprint 17 (admiller@redhat.com)

* Wed Aug 22 2012 Adam Miller <admiller@redhat.com> 0.97.12-1
- Un-refactoring overwrite_db (fotios@redhat.com)
- Moved dumping to JSON to its own function (fotios@redhat.com)
- Moved deletion to its own function (fotios@redhat.com)
- Refuse to push if there are no Issues on this host (fotios@redhat.com)
- Added function to clear current database (useful for testing)
  (fotios@redhat.com)
- Refuse to sync from a host with no issues (fotios@redhat.com)
- Renamed sync to push (fotios@redhat.com)
- Moved writing database to helper functions (fotios@redhat.com)
- Merge pull request #283 from
  smarterclayton/bug849939_plan_upgrade_fails_to_put (openshift+bot@redhat.com)
- Bug 849939 - Use POST instead of PUT when submitting an account upgrade.
  (ccoleman@redhat.com)

* Tue Aug 21 2012 Adam Miller <admiller@redhat.com> 0.97.11-1
- Merge pull request #279 from
  smarterclayton/bug849627_improve_error_message_handling_on_direct_post
  (openshift+bot@redhat.com)
- ctl usage tests (dmcphers@redhat.com)
- Bug 849627 When an error is encountered from direct post, redirect back to
  the form with the error keys and attributes. (ccoleman@redhat.com)
- Merge pull request #276 from nhr/US2457_revised_billing_plan_layout
  (openshift+bot@redhat.com)
- Revised plan-related CSS; moved to .haml file (hripps@redhat.com)
- US2457 Updated plan layout to match latest design (hripps@redhat.com)

* Mon Aug 20 2012 Adam Miller <admiller@redhat.com> 0.97.10-1
- Merge pull request #275 from
  smarterclayton/bug849631_downgrade_should_show_errors
  (openshift+bot@redhat.com)
- No wizard state on plan selection page. (ccoleman@redhat.com)
- Bug 849631 - Downgrade of user plan should display errors to user
  (ccoleman@redhat.com)
- Bug 849636 Account upgrade should display validation messages from forms
  (ccoleman@redhat.com)
- Bug 849356 - The first two segments of the raw content for an SSH key should
  be used as type and content. (ccoleman@redhat.com)
- Merge pull request #251 from smarterclayton/header_and_footer_updates
  (openshift+bot@redhat.com)
- Tests were looking for old link name.  Moved newsletter into footer.
  (ccoleman@redhat.com)
- Update header and footer to fix doc links, and begin simplification of the
  header. (ccoleman@redhat.com)

* Fri Aug 17 2012 Adam Miller <admiller@redhat.com> 0.97.9-1
- Merge pull request #255 from
  smarterclayton/bug849068_warn_about_account_change (openshift+bot@redhat.com)
- Merge pull request #253 from nhr/US2457_auth_changes
  (openshift+bot@redhat.com)
- Add left margin to blog author image to force H1 to wrap
  (ccoleman@redhat.com)
- Bug 849068 - Warn the user when they take an action that may result in them
  being authenticated as another person. (ccoleman@redhat.com)
- US2457 Relaxed auth for cartridge types and app templates (nhr@redhat.com)

* Fri Aug 17 2012 Adam Miller <admiller@redhat.com> 0.97.8-1
- Merge pull request #249 from smarterclayton/support_aria_feature_flag
  (openshift+bot@redhat.com)
- Merge pull request #248 from fabianofranz/master (openshift+bot@redhat.com)
- Forgot to add plan info page for disabled path (ccoleman@redhat.com)
- Provide Aria enabled and disabled modes in production. (ccoleman@redhat.com)
- US2592 and US2583 (ffranz@redhat.com)

* Thu Aug 16 2012 Adam Miller <admiller@redhat.com> 0.97.7-1
- Merge pull request #230 from nhr/plan_tests (openshift+bot@redhat.com)
- US2457 - Added tests for billing components (nhr@redhat.com)

* Thu Aug 16 2012 Adam Miller <admiller@redhat.com> 0.97.6-1
- Merge pull request #237 from smarterclayton/add_process_id_to_rails_logs
  (openshift+bot@redhat.com)
- Merge pull request #226 from smarterclayton/us2516_fill_out_billing_flow
  (openshift+bot@redhat.com)
- Merge pull request #238 from smarterclayton/use_aria_proxy_for_devenv
  (openshift+bot@redhat.com)
- Create a separate test configuration for direct post so it does not conflict
  with the real values. (ccoleman@redhat.com)
- Add process id output to Rails loggers in all modes.  Will need to be changed
  in Rails 3.2+ (ccoleman@redhat.com)
- Point site and broker development environments to the Aria API proxy machine
  (same as streamline) (ccoleman@redhat.com)
- MasterPlan is cached without loading aria_plan, but the cached object is
  frozen which prevents the plan from being loaded. (ccoleman@redhat.com)
- Bad merge (ccoleman@redhat.com)
- Tweak cache_method for Plan to work correctly (ccoleman@redhat.com)
- PlansController#show should be auth protected (ccoleman@redhat.com)
- Overlapping cache responses because of key generation (ccoleman@redhat.com)
- REST API models were not inheriting parent state, which prevented caching
  from working.  Add caching more aggressively to all static content.  Remove
  singleton on application template. (ccoleman@redhat.com)
- US2516 Flush out the billing flow, add prototypical dashboard for plans, and
  add Aria caching. (ccoleman@redhat.com)

* Wed Aug 15 2012 Adam Miller <admiller@redhat.com> 0.97.5-1
- Merge pull request #231 from sg00dwin/master (openshift+bot@redhat.com)
- Styles and images for the developers technology page; and fix search field
  img on console/help, set new app input width (sgoodwin@redhat.com)
- Merge branch 'master' of github.com:openshift/li (sgoodwin@redhat.com)

* Tue Aug 14 2012 Adam Miller <admiller@redhat.com> 0.97.4-1
- Bug 847147 - Change linking of help information about SSH to the developer
  center, also add some informative help to the ssh upload section.
  (ccoleman@redhat.com)
- Made some minor changes based on code review (nhr@redhat.com)
- Added conditional display hints to plans (nhr@redhat.com)
- Updated plan selection page (nhr@redhat.com)
- Updated from comments (nhr@redhat.com)
- Merge remote-tracking branch 'upstream/master' into aria (nhr@redhat.com)
- Merge pull request #211 from fabianofranz/master (openshift+bot@redhat.com)
- Updated Plan, added Aria::MasterPlan (nhr@redhat.com)
- US2583: added and adjusted tests (ffranz@redhat.com)
- US2583: changed footer links and added redirects for the Legal content
  (ffranz@redhat.com)

* Thu Aug 09 2012 Adam Miller <admiller@redhat.com> 0.97.3-1
- Merge pull request #206 from smarterclayton/us2583_move_learn_more_to_drupal
  (openshift+bot@redhat.com)
- Remove unused code, add tests to cover new redirections (ccoleman@redhat.com)
- Move remaining openshift content in drupal (ccoleman@redhat.com)
- Merge pull request #199 from sg00dwin/master (openshift+bot@redhat.com)
- Point learn more to community (ccoleman@redhat.com)
- Merge pull request #194 from smarterclayton/direct_post_config_tasks
  (openshift+bot@redhat.com)
- fix blog author photo 829774 (sgoodwin@redhat.com)
- Middle initial is not serialized identically between create/update account.
  (ccoleman@redhat.com)
- Check persistence in unit tests (ccoleman@redhat.com)
- Update account upgrade edit page to more closely resemble emily's mockups and
  to reuse data (ccoleman@redhat.com)
- The mother of all integration tests (ccoleman@redhat.com)
- Flush out payment methods (ccoleman@redhat.com)
- Adding feature request search field (sgoodwin@redhat.com)
- Add direct payment edit paths, simplify logic and flow (ccoleman@redhat.com)
- Provide rake tasks to set/clear direct post Aria configuration.
  (ccoleman@redhat.com)
- Remove ruby common code from rhc-server-common (ccoleman@redhat.com)

* Thu Aug 02 2012 Adam Miller <admiller@redhat.com> 0.97.2-1
- Merge pull request #162 from smarterclayton/use_ci_reporter_in_site
  (ccoleman@redhat.com)
- Bug 844845 - Parallelize site tests, add junit style XML output for reporting
  to Jenkins (ccoleman@redhat.com)

* Thu Aug 02 2012 Adam Miller <admiller@redhat.com> 0.97.1-1
- bump_minor_versions for sprint 16 (admiller@redhat.com)

* Wed Aug 01 2012 Adam Miller <admiller@redhat.com> 0.96.8-1
- css fix for 844916b (sgoodwin@redhat.com)
- fix 844891 (sgoodwin@redhat.com)

* Tue Jul 31 2012 Adam Miller <admiller@redhat.com> 0.96.7-1
- add custom forum only search; minor work of breadcrumb partials and spacing,
  headings at <480px get small line-height (sgoodwin@redhat.com)
- Merge pull request #151 from
  smarterclayton/bug844231_user_gets_error_on_signup (contact@fabianofranz.com)
- Merge pull request #150 from smarterclayton/captcha_can_be_nil
  (contact@fabianofranz.com)
- Merge pull request #145 from
  smarterclayton/us2531_add_user_agent_to_console_requests
  (ccoleman@redhat.com)
- Bug 844231 - During signup, a user who has confirmed his email sees an error
  message, instead of being taken to the signup confirm page.  This is because
  streamline has different behavior if the user has confirmed their email.
  (ccoleman@redhat.com)
- Allow captcha to be set to nil to disable it. (ccoleman@redhat.com)
- Fix functional tests (ccoleman@redhat.com)
- Send a consistent user agent from the console to Aria, Streamline, and
  broker. (ccoleman@redhat.com)

* Mon Jul 30 2012 Dan McPherson <dmcphers@redhat.com> 0.96.6-1
- Merge pull request #89 from smarterclayton/add_tax_exempt_model_attribute
  (ccoleman@redhat.com)
- Remove tax exemption for simplification of process. (ccoleman@redhat.com)
- Have account_upgrade completion post to itself to simplify creation, move
  some plan stuff, update tests to validate plan id from broker.
  (ccoleman@redhat.com)
- Ensure that the correct plan ID is pushed to the user object.
  (ccoleman@redhat.com)
- Add the necessary glue so that the checkbox for tax exemption shows up and
  sets values on creation.  Also ensure that user accounts are created with the
  default tax_exempt value of 0. (ccoleman@redhat.com)
- Add a tax_exempt supplemental attribute in Aria for use by Ops team.  Value 0
  means not tax exempt, value 1 means has requested exemption, value 2 means
  user has been confirmed exempt (ccoleman@redhat.com)

* Thu Jul 26 2012 Dan McPherson <dmcphers@redhat.com> 0.96.5-1
- site.spec: removing release changes (tdawson@redhat.com)
- site.spec: clean up the spec file (tdawson@redhat.com)
- add requires for rhc-site-static (dmcphers@redhat.com)

* Thu Jul 19 2012 Adam Miller <admiller@redhat.com> 0.96.4-1
- added rubygem-rcov to Build/Requires for site to fix brew build breakage
  (admiller@redhat.com)

* Thu Jul 19 2012 Adam Miller <admiller@redhat.com> 0.96.3-1
- Merge remote-tracking branch 'origin/master' into move_os-client-tools_to_rhc
  (ccoleman@redhat.com)
- Removed invalid puts (ccoleman@redhat.com)
- Move %%files static below %%post, give all static files the default
  permissions (ccoleman@redhat.com)
- Merge pull request #85 from smarterclayton/us2518_split_rpm_output_of_site
  (contact@fabianofranz.com)
- Merge pull request #68 from J5/master (ccoleman@redhat.com)
- Add console layout helpers for steve's story (ccoleman@redhat.com)
- Merge pull request #67 from sg00dwin/master (ccoleman@redhat.com)
- Provide a rake task to delete pregenerated content in a devenv.  Run rake
  assets:clean to make autogeneration work. (ccoleman@redhat.com)
- US2518 - Split the RPM output of the site into a static subpackage that can
  be installed and updated independently. (ccoleman@redhat.com)
- Merge pull request #77 from smarterclayton/add_test_suite_tasks
  (ccoleman@redhat.com)
- US2531 - Move os-client-tools to rhc (ccoleman@redhat.com)
- Fix remaining issue with mock reuse (wrapper class doesn't pass
  http_without_mock to nested connection) (ccoleman@redhat.com)
- Speed up tests by reswizzling http mock behavior (ccoleman@redhat.com)
- refactor "rcov" rake task to "coverage" (johnp@redhat.com)
- add rcov rake task for site (johnp@redhat.com)
- Add new rake test:streamline, test:aria, and test:restapi wrappers for more
  focused testing (ccoleman@redhat.com)
- switch margin to baseLineHeight variable (sgoodwin@redhat.com)
- Merge branch 'master' of github.com:openshift/li (sgoodwin@redhat.com)
- revert class placement (sgoodwin@redhat.com)
- switch to baseLineHeight (sgoodwin@redhat.com)
- Visual adjustments several places (sgoodwin@redhat.com)

* Fri Jul 13 2012 Adam Miller <admiller@redhat.com> 0.96.2-1
- Streamline fixed the confirm email bug in staging so that confirm can be done
  twice. (ccoleman@redhat.com)
- Merge pull request #65 from
  smarterclayton/bug_839545_duplicate_text_in_template (ccoleman@redhat.com)
- Bug 839545 - The provides element on a template should be coerced to an array
  (ccoleman@redhat.com)
- Merge pull request #60 from
  smarterclayton/bug_839127_update_client_install_docs (ccoleman@redhat.com)
- Merge pull request #59 from nhr/BZ838062r1 (ccoleman@redhat.com)
- Bug 839127 - Update the client getting started documentation to be more gem
  centric (cross platform) and link out to a new developer center page.
  (ccoleman@redhat.com)
- Building controller now differentiates between Jenkins server DNS delays and
  other Jenkins client cartridge creation errors. Also revised/streamlined
  cartridge save attempt logic (nhr@redhat.com)

* Wed Jul 11 2012 Adam Miller <admiller@redhat.com> 0.96.1-1
- bump_minor_versions for sprint 15 (admiller@redhat.com)

* Wed Jul 11 2012 Adam Miller <admiller@redhat.com> 0.95.13-1
- Add more tests to verify filtering and behavior of application template
  methods and make the filtering apply after the objects have been type
  converted (ccoleman@redhat.com)
- Allow templates to be added which do not show up in production (the
  :in_development / 'in_development' category/tag) (ccoleman@redhat.com)
- Add an integration test specifically for the Streamline confirm twice failure
  and rescue body errors so the ticket can be retrieved (ccoleman@redhat.com)
- Merge pull request #50 from sg00dwin/master (ccoleman@redhat.com)
- Merge branch 'master' of github.com:openshift/li (sgoodwin@redhat.com)
- Visual edits and bug fix (sgoodwin@redhat.com)
- merge into one file for _code.scss (sgoodwin@redhat.com)

* Tue Jul 10 2012 Adam Miller <admiller@redhat.com> 0.95.12-1
- Add tests to streamline to ensure parse failures are handled.
  (ccoleman@redhat.com)
- Merge pull request #51 from fabianofranz/master (ccoleman@redhat.com)
- Bug 838800 - Update streamline address in drupal, make no cookies the default
  (ccoleman@redhat.com)
- Updated links to pricing page to point to full url (contact@fabianofranz.com)
- Links to pricing page all over the website, related to BZ 837902
  (contact@fabianofranz.com)
- Merge pull request #46 from smarterclayton/aria_payment_methods
  (ccoleman@redhat.com)
- Get unit tests passing again (ccoleman@redhat.com)
- Implement account payment specification and full account creation flow
  (ccoleman@redhat.com)

* Mon Jul 09 2012 Adam Miller <admiller@redhat.com> 0.95.11-1
- Fix ordering test to be accurate with 1.8 ruby now lower.
  (ccoleman@redhat.com)
- Update Ruby 1.8.7 to fall further down the list, fix double HTML escaping of
  descriptions (ccoleman@redhat.com)
- Ensure cart metadata is not overwriting core values. (ccoleman@redhat.com)

* Mon Jul 09 2012 Dan McPherson <dmcphers@redhat.com> 0.95.10-1
- 

* Mon Jul 09 2012 Dan McPherson <dmcphers@redhat.com> 0.95.9-1
- Merge pull request #40 from
  smarterclayton/bugz_838428_users_intermittently_logged_out
  (ccoleman@redhat.com)
- Fix bug 838428 and random session logout issues caused by the session cookie
  being unencoded. (ccoleman@redhat.com)

* Mon Jul 09 2012 Dan McPherson <dmcphers@redhat.com> 0.95.8-1
- Merge pull request #36 from
  smarterclayton/bugz_814025_prevent_external_redirect (ccoleman@redhat.com)
- Merge branch 'sgoodwin-dev0506' (sgoodwin@redhat.com)
- Multiple style related changes to address bugs or other issue
  (sgoodwin@redhat.com)
- new pre.cli styles within console (sgoodwin@redhat.com)
- 838353 link fix (sgoodwin@redhat.com)
- Bug 814025 Prevent external redirects on login, logout, and a few other
  places (ccoleman@redhat.com)

* Mon Jul 09 2012 Dan McPherson <dmcphers@redhat.com> 0.95.7-1
- Add better debugging to session_trace in development mode, remove some
  unnecessary trace statements (ccoleman@redhat.com)
- Balance news and learn sections of the homepage with bottom margin
  (ccoleman@redhat.com)
- At Legal's request, change the footer link for 'Terms of Service' to point to
  the preview services agreement. (ccoleman@redhat.com)

* Thu Jul 05 2012 Adam Miller <admiller@redhat.com> 0.95.6-1
- Ensure rails cache is cleared before tests and fix incorrect cache entries
  (ccoleman@redhat.com)
- Update cartridge type (ccoleman@redhat.com)
- React to cartridge metadata by removing need for :framework category.
  (ccoleman@redhat.com)
- all css changes... align center footer when in mobile portrait display. set
  app name and app url on same line when space allows, and set max-width with
  text-overflow:ellipsis to address bz 832900 (sgoodwin@redhat.com)
- Merge branch 'master' of github.com:openshift/li (sgoodwin@redhat.com)
- Unable to log into site in devenv, changing mock implementation resulted in
  form parameters being wrong. (ccoleman@redhat.com)
- 834714 css fix (sgoodwin@redhat.com)
- US2361 - Allow user to be automatically logged in after signup, and allow
  redirect after signup back to originating page.  Add lots and lots and lots
  of testing. (ccoleman@redhat.com)

* Mon Jul 02 2012 Adam Miller <admiller@redhat.com> 0.95.5-1
- added rubygem-wddx to requires/buildrequires for site rpm
  (admiller@redhat.com)

* Mon Jul 02 2012 Adam Miller <admiller@redhat.com> 0.95.4-1
- Updated omniture script to send stg data to correct report suites
  (spurtell@redhat.com)
- US2500 - Prototype aria billing in the site, includes massive chunks of new
  code.  Adds aria client wrapper, config for connecting to aria, new
  controllers, test cases, and should handle when the current system doesn't
  have access to aria gracefully. (ccoleman@redhat.com)
- Add requires for transitions, fix build break (ccoleman@redhat.com)
- Bug 834727 - Use Compass helpers to get full browser support on rotating O
  (ccoleman@redhat.com)
- update streamline ip (dmcphers@redhat.com)

* Sat Jun 23 2012 Dan McPherson <dmcphers@redhat.com> 0.95.3-1
- new package built with tito

* Thu Jun 21 2012 Adam Miller <admiller@redhat.com> 0.95.2-1
- fix eap url (bdecoste@gmail.com)
- Bug 820760 - Background animated images don't work, copy hidden source image
  url (ccoleman@redhat.com)

* Wed Jun 20 2012 Adam Miller <admiller@redhat.com> 0.95.1-1
- bump_minor_versions for sprint 14 (admiller@redhat.com)

* Wed Jun 20 2012 Adam Miller <admiller@redhat.com> 0.94.16-1
- BZ833654: Removed extra flashes if the string is blank (fotios@redhat.com)
- Allow streamline to return login or emailAddress (as confirmation of email
  login) (ccoleman@redhat.com)
- Merge branch 'master' of git:/srv/git/li (sgoodwin@redhat.com)
- css edits - fix for 832900 (sgoodwin@redhat.com)
- Bug 830670 - Remove cartridge user guide link. (ccoleman@redhat.com)
- Bug 825094 - Prevent clickjacking through use of X-Frame-Options: SAMEORIGIN
  (ccoleman@redhat.com)

* Tue Jun 19 2012 Adam Miller <admiller@redhat.com> 0.94.15-1
- Update homepage with EAP6 info (ccoleman@redhat.com)
- BZ828116: Added logic for displaying credentials for applications created
  from templates (fotios@redhat.com)
- Update some of the cartridge text to be less verbose (ccoleman@redhat.com)

* Mon Jun 18 2012 Adam Miller <admiller@redhat.com> 0.94.14-1
- merge fix in pricing.scss (sgoodwin@redhat.com)
- fix layout issues for bug 832926 (sgoodwin@redhat.com)
- Minor wording of login placeholder (ccoleman@redhat.com)
- Update helpers to fix broken link on get_started page for JBoss tools
  (ccoleman@redhat.com)
- Merge branch 'master' of git1.ops.rhcloud.com:/srv/git/li (ffranz@redhat.com)
- Removed flexbox model styling form pricing page (spec still very unstable)
  (ffranz@redhat.com)
- Bug 819402 - Streamline sometimes returns 401 + specific service error, which
  is not an AccessDeniedException scenario. (ccoleman@redhat.com)
- minor spacing changes for lists and on the search input (sgoodwin@redhat.com)

* Fri Jun 15 2012 Adam Miller <admiller@redhat.com> 0.94.13-1
- Bug 832290 - Publish remote access page (ccoleman@redhat.com)
- Bug 827531 - Link to add cart page from getting started (ccoleman@redhat.com)

* Thu Jun 14 2012 Adam Miller <admiller@redhat.com> 0.94.12-1
- Add caching to drupal views and blocks for better performance.  Remove
  unnecessary sections from UI (ccoleman@redhat.com)
- Improved gears background images (ffranz@redhat.com)
- Merge branch 'master' of git1.ops.rhcloud.com:/srv/git/li (ffranz@redhat.com)
- Pricing page styles and images (ffranz@redhat.com)
- Add unit tests for and gracefully handle when cartridges are added without
  metadata Speed up application and cartridge tests by reusing existing apps
  (ccoleman@redhat.com)
- updated URL of pricing page for custom tracking variable
  (spurtell@redhat.com)
- fix typos (sgoodwin@redhat.com)
- Merge branch 'master' of git1.ops.rhcloud.com:/srv/git/li (ffranz@redhat.com)
- More pricing page styling, gears background images (ffranz@redhat.com)
- Show only a single error message when hit gear limit on creation.
  (ccoleman@redhat.com)
- Clean up cartridge layout at low resolutions (ccoleman@redhat.com)
- Minor pricing page style adjustments (ffranz@redhat.com)
- add test to make sure JBoss EAP comes befor JBoss AS (johnp@redhat.com)
- make sure JBoss EAP comes before JBoss AS (johnp@redhat.com)
- Added FAQ section content, styling (ffranz@redhat.com)
- New separated file for pricing styles (ffranz@redhat.com)
- remove space before parens in function call (johnp@redhat.com)
- functional tests for sshkey cache (johnp@redhat.com)
- make ssh urls and git show up only if the user has added their ssh key
  (johnp@redhat.com)
- add ssh_key caching (johnp@redhat.com)
- add ssh url to application overview (johnp@redhat.com)
- Merge branch 'master' of git:/srv/git/li (sgoodwin@redhat.com)
- mobile ui tuning (sgoodwin@redhat.com)
- Styling for the pricing page (ffranz@redhat.com)

* Wed Jun 13 2012 Adam Miller <admiller@redhat.com> 0.94.11-1
- add text to getting started application page for JBoss Dev Studio
  (johnp@redhat.com)
- Merge branch 'master' of git:/srv/git/li (sgoodwin@redhat.com)
- fix header spacing and such, change action-call on home (sgoodwin@redhat.com)

* Tue Jun 12 2012 Adam Miller <admiller@redhat.com> 0.94.10-1
- Modularize security helpers in application controller for better readability
  and consistency with other security solutions. Provide a session level cache
  for user domain info and listen for create/delete events.  Use the cache when
  viewing pages, but not on update pages. (ccoleman@redhat.com)
- Add :new tag to EAP (ccoleman@redhat.com)
- Gemfile.lock no longer has dependencies on a few extra modules
  (ccoleman@redhat.com)

* Tue Jun 12 2012 Adam Miller <admiller@redhat.com> 0.94.9-1
- explict height set on form fields and minor visual adjustment in console
  (sgoodwin@redhat.com)
- fix to force wrap long strings within table cells (sgoodwin@redhat.com)
- Merge branch 'master' of git:/srv/git/li into searchmod (sgoodwin@redhat.com)
- incorporate search field within header of site pages, reset headings to use
  line-height instead of margin-bottom, reset /stylesheets/_type.scss to
  bootstrap/_type.scss and merge customizations within so that we only use
  single _type file, minor tinkerings and condensing of styles
  (sgoodwin@redhat.com)
- Merge branch 'master' of git:/srv/git/li into searchmod (sgoodwin@redhat.com)
- Merge branch 'master' of git:/srv/git/li into searchmod (sgoodwin@redhat.com)
- modifications to search in header within drupal pages (sgoodwin@redhat.com)
- Initial incorporation of search within ui header (sgoodwin@redhat.com)

* Mon Jun 11 2012 Adam Miller <admiller@redhat.com> 0.94.8-1
- Update of spec file (admiller@redhat.com)
- Display the current scale multiplier in the UI and add feature enablement
  pages that allow users to understand how scaling is exposed. Add a build
  feature enabler into the application overview page that lets users easily add
  and remove Jenkins support to their application. (ccoleman@redhat.com)

* Mon Jun 11 2012 Adam Miller <admiller@redhat.com> - 0.94.7-1
- Display the current scale multiplier in the UI and add feature enablement
  pages that allow users to understand how scaling is exposed. Add a build
  feature enabler into the application overview page that lets users easily add
  and remove Jenkins support to their application. (ccoleman@redhat.com)

* Mon Jun 11 2012 Adam Miller <admiller@redhat.com> 0.94.6-1
- remove requires aws-sdk, these apparently don't actually need it
  (admiller@redhat.com)

* Mon Jun 11 2012 Adam Miller <admiller@redhat.com> 0.94.5-1
- need hard requires of rubygem-aws-sdk version for rhc-site spec file
  (admiller@redhat.com)

* Fri Jun 08 2012 Adam Miller <admiller@redhat.com> 0.94.3-1
- Remove black bar from simple layout (ccoleman@redhat.com)
- Updating jquery version to fix new bootstrap issue
  (fotioslindiakos@gmail.com)
- Fix JS error with reenabling the loading button (ccoleman@redhat.com)
- Update the help link for the getting_started page (ccoleman@redhat.com)
- Updated tracking.js with KissInsights integration, pricing page var, and
  Origin download tracking (spurtell@redhat.com)
- Made sure application_types index page works when no templates exist
  (fotioslindiakos@gmail.com)
- Add EAP metadata, clean up the creation pages a bit more, fix an empty box on
  app creation. (ccoleman@redhat.com)
- bz 827994 changes to next steps page, change experimental label to use just
  default label style, remove label hover, add spacing in btw p + heading
  (sgoodwin@redhat.com)
- Updated gem info for rails 3.0.13 (admiller@redhat.com)

* Mon Jun 04 2012 Adam Miller <admiller@redhat.com> 0.94.2-1
- Merge branch 'master' of git:/srv/git/li (sgoodwin@redhat.com)
- css updates for labels, breadcrumbs, help section in console, blogs
  (sgoodwin@redhat.com)
- Merge branch 'net_http_persistent' (ccoleman@redhat.com)
- Added detailed steps to the Getting Started page about installing cli on
  windows (ffranz@redhat.com)
- Reuse HTTP object more efficiently (ccoleman@redhat.com)
- Keep local copy of gear_groups until Application.reload (ccoleman@redhat.com)
- Merge branch 'master' into net_http_persistent (ccoleman@redhat.com)
- Update index (ccoleman@redhat.com)
- Update terminology to avoid "templates" being exposed to users.
  (ccoleman@redhat.com)
- Bug 826651 - Can't login to mock devenv with @ in login, use Base64 encoding
  instead of CGI double encoding (ccoleman@redhat.com)
- Pass all tests (ccoleman@redhat.com)
- Merge branch 'master' into net_http_persistent (ccoleman@redhat.com)
- Implement part of persistent local http connections (ccoleman@redhat.com)
- Add net-http-persistent to site. (ccoleman@redhat.com)
- Print a message when a user's cookie cannot be decoded (ccoleman@redhat.com)
- Bug 822018 - Remove JS validation on domain create/edit forms for simplicity
  (ccoleman@redhat.com)
- Bug 811391 - Users with '+' in them can't stay logged in under non-integrated
  environment (ccoleman@redhat.com)

* Fri Jun 01 2012 Adam Miller <admiller@redhat.com> 0.94.1-1
- bumping spec versions (admiller@redhat.com)
- Fixed minor typo (fotioslindiakos@gmail.com)

* Thu May 31 2012 Adam Miller <admiller@redhat.com> 0.93.12-1
- Removed experimental tag from DIY cart (fotioslindiakos@gmail.com)
- Added experimental label and adding spacing between multiple labels
  (fotioslindiakos@gmail.com)

* Thu May 31 2012 Adam Miller <admiller@redhat.com> 0.93.11-1
- 818653 (sgoodwin@redhat.com)
- Stylized template information in applications list
  (fotioslindiakos@gmail.com)
- BZ826972: Fixing application template link (fotioslindiakos@gmail.com)

* Wed May 30 2012 Adam Miller <admiller@redhat.com> 0.93.10-1
- Added application_templates to site (fotioslindiakos@gmail.com)
- Revert "Merge branch 'dev/fotios/descriptor'" (admiller@redhat.com)
- styling for application templates additions (sgoodwin@redhat.com)
- Moved templates to their own row in the view (fotioslindiakos@gmail.com)
- Added views for new application_templates (fotioslindiakos@gmail.com)
- Merge branch 'dev0530' (sgoodwin@redhat.com)
- fix for bz 820842 and enable outage status link display at view <768
  (sgoodwin@redhat.com)
- Fixes BZ 821103 (ffranz@redhat.com)
- mostly css changes - adjustments to breadcrumb, headings, collapsed nav
  order. haml change - add my account tab back into console default nav.
  (sgoodwin@redhat.com)

* Tue May 29 2012 Adam Miller <admiller@redhat.com> 0.93.9-1
- fine tuning position of ui at individual responsive breakpoints, correct
  utility nav drop menu and alert status message presentation and other ui
  tweaks (sgoodwin@redhat.com)

* Sun May 27 2012 Dan McPherson <dmcphers@redhat.com> 0.93.8-1
- add base package concept (dmcphers@redhat.com)

* Fri May 25 2012 Adam Miller <admiller@redhat.com> 0.93.7-1
- Bug 821103 - Send promo code to registration endpoint via streamline
  (ccoleman@redhat.com)
- Users were being logged in to the broker with the wrong rhlogin in non-
  integrated mode (ccoleman@redhat.com)
- Bug 811391 - Users with '+' in them can't stay logged in under non-integrated
  environment (ccoleman@redhat.com)
- Bug 822018 - Remove JS validation on domain create/edit forms for simplicity
  (ccoleman@redhat.com)
- Merge branch 'master' of git:/srv/git/li (sgoodwin@redhat.com)
- auto merge conflict fixes to console.scss and console/_ribbon.scss Merge
  branch 'mobileui' (sgoodwin@redhat.com)
- status alert header msg fix, minor spacing and font-type changes
  (sgoodwin@redhat.com)
- fix horizontal scroll at <767, and adjustment tuning (sgoodwin@redhat.com)
- css/markup to enable responsive nav for mobile views and lots of fine tuning
  of ui components in both site and console (sgoodwin@redhat.com)

* Thu May 24 2012 Adam Miller <admiller@redhat.com> 0.93.6-1
- Bug 824913 - Add helper code to filter certain parameter values from logged
  hashes (instead of using Rails helper code that wasn't working)
  (ccoleman@redhat.com)
- New installation instructions on Windows (ffranz@redhat.com)

* Wed May 23 2012 Adam Miller <admiller@redhat.com> 0.93.5-1
- Adding application template support (fotioslindiakos@gmail.com)

* Wed May 23 2012 Adam Miller <admiller@redhat.com> 0.93.4-1
- Blank flashes are duly ignored (ccoleman@redhat.com)
- Update cartridge link on getting started page to point to Platform Features
  page. (ccoleman@redhat.com)
- CSS cleanup of application header and application list, make headers share
  CSS and degrade gracefully, and make application lists flush with the left
  margin (ccoleman@redhat.com)
- Unit test for gear state output (ccoleman@redhat.com)

* Tue May 22 2012 Adam Miller <admiller@redhat.com> 0.93.3-1
- Add more information to the status app Update overview text with less
  hyperbolic descriptions (ccoleman@redhat.com)
- Bug 822936 - Remove old reference to express. (ccoleman@redhat.com)
- Cache streamline email address loading per user to speed up my account page
  (ccoleman@redhat.com)
- Provide a tiered application view that shows cartridges organized by what
  resources they share Expose Jenkins builds as an embedded component within a
  cartridge Implement a unified cartridge / application type model with caching
  (ccoleman@redhat.com)

* Thu May 17 2012 Adam Miller <admiller@redhat.com> 0.93.2-1
- Unit test now passes with bug 812060 fixed (ccoleman@redhat.com)
- Bug 804937 - Update to use the correct exit code for the message
  (ccoleman@redhat.com)
- Remove puts (ccoleman@redhat.com)
- Gear state (ccoleman@redhat.com)
- Basic gear group code (ccoleman@redhat.com)
- re enable mixin inputGridSystem-generate (sgoodwin@redhat.com)
- Merge branch 'dev0510' (sgoodwin@redhat.com)
- another tweak for search-query class (sgoodwin@redhat.com)
- update to tracking.js (spurtell@redhat.com)
- Merge branch 'master' of git:/srv/git/li (spurtell@redhat.com)
- community search field fix for ipad/chrome width issue (sgoodwin@redhat.com)
- More fixes for input field width sizing (sgoodwin@redhat.com)
- Merge branch 'master' of git:/srv/git/li into dev0510 (sgoodwin@redhat.com)
- Add helper to generate technologies page for dev center (ccoleman@redhat.com)
- Make username drop menu position absolute at mobile sizes to enable topmost
  position on open, Fix search field to use modified mixin inputGridSystem-
  inputColumns and set have it's width set appropriate to grid. And a few other
  minor visual mods... (sgoodwin@redhat.com)
- Merge branch 'master' of git:/srv/git/li (spurtell@redhat.com)
- Updated tracking.js with Google Analytcs and AdWords code
  (spurtell@redhat.com)

* Thu May 10 2012 Adam Miller <admiller@redhat.com> 0.93.1-1
- Merge branch 'master' of ssh://git1.ops.rhcloud.com/srv/git/li
  (admiller@redhat.com)
- bumping spec versions (admiller@redhat.com)
- Bug 818030 - Remove opensource disclaimer page (ccoleman@redhat.com)
- Fix username dropdown-menu at responsive sizes, tweak wizard styles
  (sgoodwin@redhat.com)

* Wed May 09 2012 Adam Miller <admiller@redhat.com> 0.92.6-1
- alignment issue fix on docs page (sgoodwin@redhat.com)
- add error-client class to correct state handling on form submits
  (johnp@redhat.com)
- Make forum thread list much simpler (ccoleman@redhat.com)
- Make status ribbon be a bit cleaner in console (ccoleman@redhat.com)
- Update logo invoice (ccoleman@redhat.com)
- Bug 817447 - Feedback from david about getting started page
  (ccoleman@redhat.com)
- Bug 817892 - Grammar police are out in force (ccoleman@redhat.com)
- CSS tweaks to bring content into better visual appearance, restore some minor
  problems (ccoleman@redhat.com)
- Cancel button on delete always returns user to application details page (more
  consistent), fix logging bug, and terms page should use simpler title style.
  (ccoleman@redhat.com)
- Bug 820151 - Show the account information for jenkins on app creation,
  refactor message passing on cart creation, remove layout/_flashes and replace
  with simpler helper, ensure pages are flashing in the right spot, add a new
  :info_pre flash type that renders with preformatted output (don't like the
  name, but eh) (ccoleman@redhat.com)
- Bug 819441 - Some account related paths should not be redirected back to
  (ccoleman@redhat.com)
- Bug 817907 - Really REALLY don't set cookies from status app.  Also fix
  issues with starting status app in failure mode. (ccoleman@redhat.com)
- Basic compact left navigation (ccoleman@redhat.com)
- Simplify how the dropdown link is generated, use a view helper
  (ccoleman@redhat.com)

* Tue May 08 2012 Adam Miller <admiller@redhat.com> 0.92.5-1
- Merge branch 'devcomm' (sgoodwin@redhat.com)
-  minor updates to the visual presentation of the forums threat list and blog
  details views (sgoodwin@redhat.com)

* Tue May 08 2012 Adam Miller <admiller@redhat.com> 0.92.4-1
- Make the delete button more subtle (ccoleman@redhat.com)
- Merge branch 'cleanupscss' (sgoodwin@redhat.com)
- button disabled/active changes (sgoodwin@redhat.com)
- Reenable Jenkins from the UI (ccoleman@redhat.com)
- Add an informational page on logout that informs the user that they have been
  logged out and why.  Currently just takes the user back to the account page.
  (ccoleman@redhat.com)

* Mon May 07 2012 Adam Miller <admiller@redhat.com> 0.92.3-1
- add navbar tests back and add unique classes to links (johnp@redhat.com)
- Fix bug 818391 - special code branch should have been removed when we fixed
  bug 789786 (ccoleman@redhat.com)
- shadowman icon for username association (sgoodwin@redhat.com)

* Mon May 07 2012 Adam Miller <admiller@redhat.com> 0.92.2-1
- Fix failing test from renaming red hat network identity (ccoleman@redhat.com)
- Update styles on terms controller, remove captcha there.
  (ccoleman@redhat.com)
- Change from 'red hat network' to 'red hat' terminology. (ccoleman@redhat.com)
- Remove extra role establish call on login. (ccoleman@redhat.com)
- Merge branch 'dev0430' (sgoodwin@redhat.com)
- separate console button styles out from site into their own partial scss
  (sgoodwin@redhat.com)
- Merge events recent changes and user profile into code. (ccoleman@redhat.com)
- pull duplicate style, add mixin box-shadow (sgoodwin@redhat.com)
- more scss cleanup. button work, username dropdown and ribbon polish
  (sgoodwin@redhat.com)
- Merge branch 'master' of git:/srv/git/li into dev0430 (sgoodwin@redhat.com)
- scss css cleanup (sgoodwin@redhat.com)
- Failure during cartridge creation, tests not as good as we thought.
  (ccoleman@redhat.com)
- Simplify how we handle cart type models Prevent bad custom_ids from being
  passed Fix bug with CartridgeType retrieval (ccoleman@redhat.com)
- Prefix mappings were screwed up and breaking unit tests.  Now use
  RestApi::Base.prefix everywhere (ccoleman@redhat.com)
- new _buttons and _dropdowns partials for console and color corrected logo
  (sgoodwin@redhat.com)
- Merge branch 'master' of git:/srv/git/li into dev0430 (sgoodwin@redhat.com)
- color scale added for console and change styleguide/console markup to bring
  into alignment with latest (sgoodwin@redhat.com)
- Remove duplicate slash from request URLs (ccoleman@redhat.com)
- Instrument ActiveResource to logs (ccoleman@redhat.com)
- Loading icon needs to be reinstated Update loading script
  (ccoleman@redhat.com)
- Add better association logic Allow objects to be passed to RestApi::Base
  initialize method to handle belongs_to Add more assignment unit tests Ensure
  change notifications are cleared by the save() command Remove unnecessary
  check in domain save Test changes? more thoroughly (ccoleman@redhat.com)
- Fix formatting of error messages when form is using input-prepends
  (ccoleman@redhat.com)
- Update community side nav-column font color/size and fix ipad search field
  issue. Adjust console colors, center nav, breadcrumb and other minor visual
  changes. (sgoodwin@redhat.com)
- Package rename python(3.2 -> 2.6), ruby(1.1 -> 1.8) (kraman@gmail.com)
- Merge branch 'dev/clayton/identity' (ccoleman@redhat.com)
- Add passing status_app_test for null issues (ccoleman@redhat.com)
- Use simple user to extract identity (ccoleman@redhat.com)
- Fix styleguide (ccoleman@redhat.com)
- Ensure exceptions are loaded optimistically for streamline
  (ccoleman@redhat.com)
- Ensure type is correctly loaded from session (ccoleman@redhat.com)
- Refactor streamline into multiple objects that cleanly define usage Make
  inheritance act normally Remove autoload of lib sub-directories (so that
  Rails autoloading picks up module namespaces) (ccoleman@redhat.com)
- Add a type attribute on streamline user (ccoleman@redhat.com)
- Move attributes to Streamline::Base for resharing (ccoleman@redhat.com)
- Merge branch 'master' into dev/clayton/identity (ccoleman@redhat.com)
- Ensure status app cannot set session cookies, add tests.
  (ccoleman@redhat.com)
- Get tests to passing with better abstraction of name change logic and role
  setting in streamline_test.rb (ccoleman@redhat.com)
- Unit tests for status (ccoleman@redhat.com)
- Ensure status app cannot set session cookies (ccoleman@redhat.com)
- Status app should not set cookies (ccoleman@redhat.com)
- Fix bugs with recording time of streamline calls (ccoleman@redhat.com)
- Add streamline time tracing (ccoleman@redhat.com)
- Make streamline attribute writers protected to prevent general access Prevent
  rhlogin from being updated except by Streamline code Allow captcha_secret to
  be provided on login URL for simpler login sequence in kiosks Change
  establish_email_address to load_email_address Fine tune identity display on
  account page to show link to RHN account page When access denied exception is
  thrown write backtrace (ccoleman@redhat.com)
- Fix unit test failure on nil test (ccoleman@redhat.com)
- Centralize roles load logic (ccoleman@redhat.com)
- Update identity to have better display name (ccoleman@redhat.com)
- Add identity display to ui (ccoleman@redhat.com)
- Bug 817627 - Prevent infinite redirect of users who have invalid rh_sso
  tokens (ccoleman@redhat.com)
- Add tests to handle infinite redirect bug (ccoleman@redhat.com)
- Move accessors (squash) (ccoleman@redhat.com)
- Refactor some of the establish scenarios to be cleaner (ccoleman@redhat.com)
- Adjust margin settings for console at >767 widths, remove inadvertant btn
  box-shadow default, center console nav per design, and a few other minor
  tweaks to spacing in the console (sgoodwin@redhat.com)
- Finish breadcrumb (ccoleman@redhat.com)
- Alter head ribbon to use a simpler style of wrapping (ccoleman@redhat.com)
- Start whittling console.scss down, fix ribbon to flush correctly
  (ccoleman@redhat.com)
- css tweeks (sgoodwin@redhat.com)
- Add FireSASS support (ccoleman@redhat.com)
- More aggressive gitignore (ccoleman@redhat.com)
- Write expanded CSS in dev mode (ccoleman@redhat.com)
- Rename to make a generic tracking file and tracking JS file Provide query
  parameters for promo_code on emails Remove warnings on test runs Add test
  cases for promo code redirect Make it so that a refresh is not required to
  enter a promo code. Fix failures in test env on mailer. (ccoleman@redhat.com)
- Community nav column is creating a white bar on iphone (ccoleman@redhat.com)
- Removed mirror.openshift.com tests until it goes public (ffranz@redhat.com)
- Fixes BZ 816797 (ffranz@redhat.com)
- Remove 'by Red Hat' from site (ccoleman@redhat.com)
- Updated requirements from legal regarding removal of opensource disclaimer
  page and changes to language on download page. (ccoleman@redhat.com)

* Thu Apr 26 2012 Adam Miller <admiller@redhat.com> 0.92.1-1
- new loader image for console and css (sgoodwin@redhat.com)
- bumping spec versions (admiller@redhat.com)
- Update logo-24-inside to not have improper color saturation on firefox
  (ccoleman@redhat.com)
- Origin SRPMs on download page (ccoleman@redhat.com)

* Wed Apr 25 2012 Adam Miller <admiller@redhat.com> 0.91.11-1
- Merge branch 'dev0425' (sgoodwin@redhat.com)
- event section styles added (sgoodwin@redhat.com)

* Wed Apr 25 2012 Adam Miller <admiller@redhat.com> 0.91.10-1
- Create a stub logo invoice (ccoleman@redhat.com)
- Bug 815173 - Set header in drupal to force IE edge mode in devenv.   Ensure
  that status messages won't be shown for N-1 compat with site   Update
  copyright colors to be black background   Update copyright date
  (ccoleman@redhat.com)
- Fixes #816081 (ffranz@redhat.com)

* Tue Apr 24 2012 Adam Miller <admiller@redhat.com> 0.91.9-1
- Links to live cd Navbar tweaks to fit in small spaces Remove "new" tag on
  node.js (ccoleman@redhat.com)
- Better wrapping of header on phone (ccoleman@redhat.com)
- Added warning color and some tweaks to content width (ccoleman@redhat.com)
- More button tweaks, some table fixes.  Will need to further pursue items next
  sprint. (ccoleman@redhat.com)
- Heavy refactoring of nav header code (ccoleman@redhat.com)
- Remove navbar-inner, not used (ccoleman@redhat.com)
- Move navbar code into _navbar (ccoleman@redhat.com)

* Tue Apr 24 2012 Adam Miller <admiller@redhat.com> 0.91.8-1
- Improved responsiveness for dropdown navbar (ffranz@redhat.com)
- Improved responsiveness for dropdown navbar (ffranz@redhat.com)
- Fixes #815261 (ffranz@redhat.com)
- Merge branch 'dev0424' (sgoodwin@redhat.com)
- Tighten up opensource download page (sgoodwin@redhat.com)
- Fixes #815698 by handling invalid constant names; rest api auto detects proxy
  (ffranz@redhat.com)
- Bug 814573 - Fix up lots of links to www.redhat.com/openshift/community
  (ccoleman@redhat.com)

* Tue Apr 24 2012 Adam Miller <admiller@redhat.com> 0.91.7-1
- sync error handling client side and server side (johnp@redhat.com)

* Mon Apr 23 2012 Adam Miller <admiller@redhat.com> 0.91.6-1
- Disable Jenkins because upstream bugs could not be fixed.
  (ccoleman@redhat.com)
- Merge branch 'dev0423' (sgoodwin@redhat.com)
- revised button styles, search field focus (sgoodwin@redhat.com)
- Mark's suggestions (ccoleman@redhat.com)
- Better opensource links and descriptions (ccoleman@redhat.com)
- Update to LiveCd with kraman's agreement (ccoleman@redhat.com)
- Reorder items in user_profile_box to work better with Steve's styling
  (ccoleman@redhat.com)
- Touch up blog theme prior to ship (ccoleman@redhat.com)

* Mon Apr 23 2012 Adam Miller <admiller@redhat.com> 0.91.5-1
- Change #console-head to .console-head for selectivity fix
  (ccoleman@redhat.com)
- Fix breadcrumbs on lots of console pages, add blue add cart button to app
  details page (ccoleman@redhat.com)
- max-widths off by one Replace console-panel with section-console (may change
  selectivity) (ccoleman@redhat.com)
- Fix warning on applications index page (ccoleman@redhat.com)
- Split out urls for git/opensource into their own file to reduce
  application_helper size Remove unused _pageheader file Switch order of page
  title - current page title comes first, then the generic 'Openshift by
  redhat' message Improve text on index.html.haml page Changes to opensource
  download page to reflect new structure of page (ccoleman@redhat.com)

* Sat Apr 21 2012 Dan McPherson <dmcphers@redhat.com> 0.91.4-1
- Added styles for the ToC of wiki pages (ffranz@redhat.com)
- minor spacing changes in community forum (sgoodwin@redhat.com)
- Tests mildly out of sync with controllers in bug 814835 (ccoleman@redhat.com)
- Merge branch 'dev0420' (sgoodwin@redhat.com)
- community pages - ui css changes (sgoodwin@redhat.com)
- Reads better this way (ccoleman@redhat.com)
- Bug 814835 - Password reset should not expose whether the user has an account
  (ccoleman@redhat.com)
- isolate column-content div only (sgoodwin@redhat.com)
- Merge branch 'dev0420' (sgoodwin@redhat.com)
- community comments changes (sgoodwin@redhat.com)
- Bug 808657 - Users who signup should be taken to the console after their
  first login (ccoleman@redhat.com)
- Merge branch 'master' of git1.ops.rhcloud.com:/srv/git/li (ffranz@redhat.com)
- Bug 814575 - Developers link is missing (ccoleman@redhat.com)
- minor edit to go along with forum changes (sgoodwin@redhat.com)
- Reformat forum thread and comments (sgoodwin@redhat.com)
- Added styles for the ToC of wiki pages (ffranz@redhat.com)
- Fix cartridge tests to use new assigns names (ccoleman@redhat.com)
- Merge branch 'dev/clayton/console-branding' (ccoleman@redhat.com)
- Added styles for the ToC of wiki pages (ffranz@redhat.com)
- Lots of cleanup of getting started and next steps (ccoleman@redhat.com)
- community forum layout changes and remove input box-shadow from console
  (sgoodwin@redhat.com)
- comment out visual blocks which we don't have any data for yet
  (johnp@redhat.com)
- [security] do not call html_safe on error messages (johnp@redhat.com)
- Prevent pictures in left nav from getting too big (ccoleman@redhat.com)
- Merge branch 'master' into dev/clayton/console-branding (ccoleman@redhat.com)
- Give Jenkins some info and a link to a help page (ccoleman@redhat.com)
- minor edits (sgoodwin@redhat.com)
- Help documents update (ccoleman@redhat.com)
- Tweaks to console help (ccoleman@redhat.com)
- Fixes duplicate arrows for external links on wiki (ffranz@redhat.com)
- more merge fixes (johnp@redhat.com)
- fix merge issues (johnp@redhat.com)
- update my applications page to dark console ui (johnp@redhat.com)
- Remove section help (ccoleman@redhat.com)
- Revert changes to console help, update footer sections to be cleaner
  (ccoleman@redhat.com)
- Unbreak layout for J5 (ccoleman@redhat.com)
- A few less styles, some slightly cleaner grid behavior for help
  (ccoleman@redhat.com)
- Other dark_layout page, a few color tweaks for readability on get started
  page.  Fix remaining styleguides (ccoleman@redhat.com)
- Alternate dark_layout implementation, change #console-panel to .section-
  console and .row-console to be consistent with site (ccoleman@redhat.com)
- Update links on homepage to new features this sprint (ccoleman@redhat.com)
- update cartridge_type selection and addition styles (johnp@redhat.com)
- style dark layout closer to mockups (johnp@redhat.com)
- style application details page (johnp@redhat.com)
- add dark_layout to console and have the applications::show controller use it
  (johnp@redhat.com)
- update breadcrumb helper to add delimiters and an active class
  (johnp@redhat.com)
- Restore color overrides on form errors that were lost during _custom.css
  normalization (ccoleman@redhat.com)
- add breadcrumbs helper and content_for block to the layout (johnp@redhat.com)
- fix styling on create app page (johnp@redhat.com)
- Abstract out messaging and handle navbar bottom margin a bit cleaner
  (ccoleman@redhat.com)
- fix link color and dropdown arrow position (johnp@redhat.com)
- fix up dropdown style a bit more (johnp@redhat.com)
- remove import to nonexitant file (johnp@redhat.com)
- minor position edits and class change on get started (sgoodwin@redhat.com)
- Remove console-transition (ccoleman@redhat.com)
- Some basic stuff to verify that the styles were properly merged
  (ccoleman@redhat.com)
- Merge branch 'dev/clayton/console-branding' of git:/srv/git/li into
  dev/clayton/console-branding (ccoleman@redhat.com)
- Switch to using common.scss for console, mostly refactored
  (ccoleman@redhat.com)
- Move stuff moved out of _custom.scss (ccoleman@redhat.com)
- make header more like mockups (johnp@redhat.com)
- Moving stuff out of custom.scss (ccoleman@redhat.com)
- Split out buttons (ccoleman@redhat.com)
- add dropdown user menu to user's login in header (johnp@redhat.com)
- upgrade to jquery-1.7.2 and add bootstrap-dropdown.js dropdown menu widget
  (johnp@redhat.com)

* Wed Apr 18 2012 Adam Miller <admiller@redhat.com> 0.91.3-1
- Status app now causing warning on redefinition in test - hack around it
  (ccoleman@redhat.com)
- Bug 813616 - Instruct users about the optional RHEL 6.2 channel for getting
  'rubygems' (ccoleman@redhat.com)
- Bug 813613 (ccoleman@redhat.com)
- Abstract out messaging and handle navbar bottom margin a bit cleaner
  (ccoleman@redhat.com)
- Fix domain controller failures, bonehead move. (ccoleman@redhat.com)
- new console prototype pages for reference (sgoodwin@redhat.com)
- Fixed image overflow at small sizes in product overview page.
  (edirsh@redhat.com)
- Update getting started page to be a "bit" prettier (ccoleman@redhat.com)
- Merge branch 'master' into dev/clayton/community_urls (ccoleman@redhat.com)
- Enable Jenkins as an app (ccoleman@redhat.com)
- Fix fake_before_filter_test, add pending/error access request pages
  (ccoleman@redhat.com)
- Merge remote-tracking branch 'origin/master' into dev/fotios/login
  (ccoleman@redhat.com)
- Add GitHub link to footer (ccoleman@redhat.com)
- Link the redhat image to https://www.redhat.com/ (ccoleman@redhat.com)
- Enable the opensource and download controllers for production
  (ccoleman@redhat.com)
- First stab at new navigation / footer layout (ccoleman@redhat.com)
- Remove old layout files (ccoleman@redhat.com)
- Merge branch 'master' into dev/clayton/community_urls (ccoleman@redhat.com)
- Fix two test changes (ccoleman@redhat.com)
- Merged some test improvements made upstream (ccoleman@redhat.com)
- Merge branch 'master' into dev/fotios/login (ccoleman@redhat.com)
- Get terms controller test passing (ccoleman@redhat.com)
- Center the signup terms to balance the page (ccoleman@redhat.com)
- Move AccessDeniedException to an appropriate place, ensure it is autoloaded,
  fix syntactical vagueness in unit test (ccoleman@redhat.com)
- Minor reorganization (ccoleman@redhat.com)
- Switch to a much cleaner recaptcha and give the promo code an extra few
  pixels. (ccoleman@redhat.com)
- Remove sso cookie reset from login page (ccoleman@redhat.com)
- Make promo code suggestion simpler (ccoleman@redhat.com)
- Simple pages are wasting too much vertical space on the header
  (ccoleman@redhat.com)
- Allow the community theme to return to the current location after logout
  (ccoleman@redhat.com)
- Allow streamline to be dynamically reloaded when it changes Fix logout flow
  to use standard streamline config (ccoleman@redhat.com)
- Updated test_helper.rb to match latest changes from master Merged
  application_controller (ccoleman@redhat.com)
- Automatic commit of package [rhc-site] release [0.90.6-1].
  (mmcgrath@redhat.com)
- Simplify some styles on the opensource page, correct some phone/tablet layout
  issues. (ccoleman@redhat.com)
- Attached images list removed from Community Wiki using CSS display none
  (ffranz@redhat.com)
- restrict opensource download routes to dev instance (johnp@redhat.com)
- add all cart links to page (johnp@redhat.com)
- Add timing and parent branch removal Better comments in the change section
  Branch pruning and empty merge filtering Add password controller to
  exclusion, begin tidying opensource.sh up for final status. Indicate how many
  files will be preserved (ccoleman@redhat.com)
- Create draft file for creating open source engine on console
  (ccoleman@redhat.com)
- Tweak headers down except on home page, change header to point to the
  developers link. (ccoleman@redhat.com)
- Update forum_list view with menu fix Make relative URLs work from menus Minor
  CSS tweaks to community. (ccoleman@redhat.com)
- Merged login changes (fotios@redhat.com)

* Thu Apr 12 2012 Mike McGrath <mmcgrath@redhat.com> 0.91.2-1
- release bump for tag uniqueness (mmcgrath@redhat.com)
- Merge branch '0412dev' (sgoodwin@redhat.com)
- include fallback background color for ie since it doesn't support css3 linear
  gradients (sgoodwin@redhat.com)
- Update preview agreement to remove flex (ccoleman@redhat.com)

* Thu Apr 12 2012 Mike McGrath <mmcgrath@redhat.com> 0.90.16-1
- Unit tests for domains controller   Remove old :namespace error output in
  form   Make errors on domain correct for case when an error exists
  (ccoleman@redhat.com)
- Bug 811847 - Bad refactor, domain :edit not showing up (ccoleman@redhat.com)
- Fixes 807565 (ffranz@redhat.com)
- Merge branch 'master' of git1.ops.rhcloud.com:/srv/git/li (ffranz@redhat.com)
- Fixes 807565 (ffranz@redhat.com)

* Wed Apr 11 2012 Adam Miller <admiller@redhat.com> 0.90.15-1
- fix for ie9 background-image bug and newsletter link lighten
  (sgoodwin@redhat.com)

* Wed Apr 11 2012 Adam Miller <admiller@redhat.com> 0.90.14-1
- Bug 804849; Improve styling of outage notification to match new branding
  (edirsh@redhat.com)
- Better integrate illustrations in overview page (edirsh@redhat.com)

* Wed Apr 11 2012 Adam Miller <admiller@redhat.com> 0.90.13-1
- Merge branch 'master' of ssh://git1.ops.rhcloud.com/srv/git/li
  (mmcgrath@redhat.com)
- Test commit (mmcgrath@redhat.com)

* Wed Apr 11 2012 Adam Miller <admiller@redhat.com> 0.90.12-1
- Remove debugging logic - it hath served its purpose (ccoleman@redhat.com)
- Merge branch 'dev/clayton/partners' (ccoleman@redhat.com)
- Reenable domain test (ccoleman@redhat.com)
- Remove partners from UI.  Footer in community as well (ccoleman@redhat.com)
- Bug 802634 - Improve the display of the search button on the Help page to
  make it clear it can be clicked, use styles from community.
  (ccoleman@redhat.com)

* Tue Apr 10 2012 Mike McGrath <mmcgrath@redhat.com> 0.90.11-1
- Temporarily disable test_domain_exists_error in domain_test.rb to allow AMI
  to build clean (ccoleman@redhat.com)

* Tue Apr 10 2012 Mike McGrath <mmcgrath@redhat.com> 0.90.10-1
- test commit (mmcgrath@redhat.com)

* Tue Apr 10 2012 Mike McGrath <mmcgrath@redhat.com> 0.90.9-1
- Change requires for all test/units so that 'ruby test/unit/xxx.rb' runs the
  test (ccoleman@redhat.com)
- Bug 804018 - display a proper 404 when resources are not found   Until
  multiple domain support lands we were using Domain.first - this returns nil
  when an item exists.  Most .find methods that load a specific resource throw
  an exception.  We should be doing the same until multidomain lands (and after
  multidomain lands we should be looking up domains via id).  For now, use
  Domain.find :one, which was created to throw if there is no domain.  Updated
  unit tests.  Added rescue_from to ApplicationController, and added a note
  about Rails 3.1 (which will allow render :status => 404 instead of a more
  complicated output).  Controller should handle exceptions before redirecting
  (ccoleman@redhat.com)

* Tue Apr 10 2012 Mike McGrath <mmcgrath@redhat.com> 0.90.8-1
- Revert "Merged login changes" (fotios@redhat.com)
- fix vars in opensource download view (johnp@redhat.com)
- css fix added for 802640, ie bug and rearrangement of font family order
  (sgoodwin@redhat.com)
- Merge branch 'master' of git1.ops.rhcloud.com:/srv/git/li (ffranz@redhat.com)
- Fixes 811146 (ffranz@redhat.com)
- refactor gear_size_profile and node profile to gear_profile
  (johnp@redhat.com)
- fix github urls to agreed upon path for OpenSource repos (johnp@redhat.com)

* Tue Apr 10 2012 Mike McGrath <mmcgrath@redhat.com> 0.90.7-1
- Merged login changes (fotios@redhat.com)

* Mon Apr 09 2012 Mike McGrath <mmcgrath@redhat.com> 0.90.6-1
- Simplify some styles on the opensource page, correct some phone/tablet layout
  issues. (ccoleman@redhat.com)
- Attached images list removed from Community Wiki using CSS display none
  (ffranz@redhat.com)
- restrict opensource download routes to dev instance (johnp@redhat.com)
- add all cart links to page (johnp@redhat.com)
- Add timing and parent branch removal Better comments in the change section
  Branch pruning and empty merge filtering Add password controller to
  exclusion, begin tidying opensource.sh up for final status. Indicate how many
  files will be preserved (ccoleman@redhat.com)
- Create draft file for creating open source engine on console
  (ccoleman@redhat.com)
- move generic css to site so everyone can use it (johnp@redhat.com)
- restyle opensource download page and add perliminary links (johnp@redhat.com)
- Fix infinite recursion in find_or_create_resource_for by inlining method
  React to changes from domain :name to domain :id   Remove legacy code
  referencing old :namespace attributes   Replace all references to domain
  :namespace with domain :name   Make custom_id in RestApi::Base override
  :to_param instead of :id     Clean up unit tests to reflect this change - .id
  and .name will now both show updates   Create new id alias methods to provide
  legacy support for the getter key.destroy works on the first key - update the
  test to check that (ccoleman@redhat.com)
- ActiveResource association support was not working, and when attributes with
  dashes are returned from REST API they throw a NameError.  Fix by sanitizing
  resource class names for ActiveResource autodeserialization before invoked
  (use a monkey patch on ActiveResource::Base) (ccoleman@redhat.com)
- better layout for opensource download page (johnp@redhat.com)
- tweak layout for download page (johnp@redhat.com)
- example of using the info-ribbon class (johnp@redhat.com)
- add a info-ribbon class to site.scss (johnp@redhat.com)

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
