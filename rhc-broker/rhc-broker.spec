%define htmldir %{_var}/www/html
%define brokerdir %{_var}/www/openshift/broker

Summary:   Li broker components
Name:      rhc-broker
Version: 1.10.5
Release:   1%{?dist}
Group:     Network/Daemons
License:   GPLv2
URL:       http://openshift.redhat.com
Source0:   rhc-broker-%{version}.tar.gz

BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
Requires:  rhc-common
Requires:  rhc-server-common
Requires:  httpd
Requires:  mod_ssl
Requires:  ruby193-mod_passenger
Requires:  ruby193
Requires:  ruby193-rubygem-json
Requires:  ruby193-rubygem-parseconfig
Requires:  rubygem-passenger-native-libs
Requires:  ruby193-rubygem-rails
Requires:  ruby193-rubygem-xml-simple
Requires:  rubygem-openshift-origin-controller
Requires:  ruby193-rubygem-bson_ext
Requires:  ruby193-rubygem-rest-client
Requires:  rubygem-openshift-origin-auth-streamline
Requires:  rubygem-openshift-origin-dns-dynect
Requires:  rubygem-openshift-origin-billing-aria
Requires:  rubygem-openshift-origin-msg-broker-mcollective
Requires:  ruby193-rubygem-mongo_mapper
Requires:  ruby193-rubygem-mongoid
Requires:  ruby193-rubygem-wddx
Requires:  ruby193-rubygem-pony
# As broker admin scripts are opensourced they are placed into this package
Requires:  openshift-origin-broker-util
Provides:  openshift-origin-broker
Provides:  openshift-broker
Requires:  ruby193-rubygem-simplecov
#Requires:  ruby193-rubygem-mongoid
Requires:  ruby193-rubygem-stomp
Requires:  ruby193-rubygem-open4
Requires:  ruby193-rubygem-regin
Requires:  ruby193-rubygem-ruby-prof
Requires:  ruby193-rubygem-systemu
Requires:  ruby193-rubygem-dnsruby
Requires:  ruby193-rubygem-bigdecimal
Requires:  ruby193-rubygem-state_machine
Requires:  ruby193-rubygem-minitest
Requires:  ruby193-rubygem-dalli
Requires:  ruby193-rubygem-uuidtools

BuildArch: noarch

%description
This contains the broker 'controlling' components of OpenShift.
This includes the public APIs for the client tools.

%prep
%setup -q

%build

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{htmldir}
mkdir -p %{buildroot}%{brokerdir}
mkdir -p %{buildroot}%{brokerdir}/httpd/conf
mkdir -p %{buildroot}%{brokerdir}/httpd/run
mkdir -p %{buildroot}/usr/lib/openshift/broker
mkdir -p %{buildroot}/etc/openshift/plugins.d/

cp -r . %{buildroot}%{brokerdir}
ln -s %{brokerdir}/public %{buildroot}%{htmldir}/broker
ln -sf /etc/httpd/conf/magic %{buildroot}%{brokerdir}/httpd/conf/magic

mkdir -p %{buildroot}%{brokerdir}/run
mkdir -p %{buildroot}%{_var}/log/openshift/broker/
mkdir -m 770 %{buildroot}%{_var}/log/openshift/broker/httpd/
mkdir -p -m 770 %{buildroot}%{brokerdir}/tmp/cache
mkdir -p -m 770 %{buildroot}%{brokerdir}/tmp/pids
mkdir -p -m 770 %{buildroot}%{brokerdir}/tmp/sessions
mkdir -p -m 770 %{buildroot}%{brokerdir}/tmp/sockets

mv %{buildroot}%{brokerdir}/script/rhc-admin-migrate %{buildroot}/%{_bindir}
mv %{buildroot}%{brokerdir}/script/rhc-admin-ctl-plan %{buildroot}/%{_bindir}
mv %{buildroot}%{brokerdir}/script/rhc-admin-stale-dns %{buildroot}/%{_bindir}

cp conf/broker.conf %{buildroot}/etc/openshift/
cp conf/broker-dev.conf %{buildroot}/etc/openshift/
cp conf/openshift-origin-msg-broker-mcollective-dev.conf %{buildroot}/etc/openshift/plugins.d/
cp conf/openshift-origin-msg-broker-mcollective.conf %{buildroot}/etc/openshift/plugins.d/
cp conf/quickstarts.json %{buildroot}/etc/openshift/

%clean
rm -rf $RPM_BUILD_ROOT

%files
%attr(0770,root,libra_user) %{brokerdir}/tmp
%defattr(0640,root,libra_user,0750)
%config(noreplace) %{brokerdir}/config/keys/public.pem
%config(noreplace) %{brokerdir}/config/keys/private.pem
%attr(0600,-,-) %config(noreplace) %{brokerdir}/config/keys/rsync_id_rsa
%config(noreplace) %{brokerdir}/config/keys/rsync_id_rsa.pub
%attr(0750,-,-) %{brokerdir}/config/keys/generate_rsa_keys
%attr(0750,-,-) %{brokerdir}/config/keys/generate_rsync_rsa_keys
%attr(0750,-,-) %{brokerdir}/script
%attr(0770,root,libra_user) %{_var}/log/openshift/broker/
%ghost %attr(0660,root,libra_user) %{_var}/log/openshift/user_action.log
%ghost %attr(0660,root,libra_user) %{_var}/log/openshift/broker/production.log
%ghost %attr(0660,root,libra_user) %{_var}/log/openshift/broker/development.log
%ghost %attr(0660,root,libra_user) %{_var}/log/openshift/broker/usage.log
%ghost %attr(0660,root,libra_user) %{_var}/log/openshift/broker/user_action.log
%{brokerdir}
%{htmldir}/broker
%attr(0750,-,-) %{_bindir}/rhc-admin-migrate
%attr(0750,-,-) %{_bindir}/rhc-admin-ctl-plan
%attr(0750,-,-) %{_bindir}/rhc-admin-stale-dns

%config(noreplace) /etc/openshift/quickstarts.json
%config(noreplace) /etc/openshift/plugins.d/openshift-origin-msg-broker-mcollective.conf
%config(noreplace) /etc/openshift/broker.conf
/etc/openshift/plugins.d/openshift-origin-msg-broker-mcollective-dev.conf
/etc/openshift/broker-dev.conf

%post
if [ ! -f %{_var}/log/openshift/broker/production.log ]; then
  /bin/touch %{_var}/log/openshift/broker/production.log
  chown root:libra_user %{_var}/log/openshift/broker/production.log
  chmod 660 %{_var}/log/openshift/broker/production.log
fi

if [ ! -f %{_var}/log/openshift/broker/development.log ]; then
  /bin/touch %{_var}/log/openshift/broker/development.log
  chown root:libra_user %{_var}/log/openshift/broker/development.log
  chmod 660 %{_var}/log/openshift/broker/development.log
fi

if [ ! -f %{_var}/log/openshift/broker/user_action.log ]; then
  /bin/touch %{_var}/log/openshift/broker/user_action.log
  chown root:libra_user %{_var}/log/openshift/broker/user_action.log
  chmod 660 %{_var}/log/openshift/broker/user_action.log
fi

if [ ! -f %{_var}/log/openshift/broker/usage.log ]; then
  /bin/touch %{_var}/log/openshift/broker/usage.log
  chown root:libra_user %{_var}/log/openshift/broker/usage.log
  chmod 660 %{_var}/log/openshift/broker/usage.log
fi

%changelog
* Mon Jul 01 2013 Adam Miller <admiller@redhat.com> 1.10.5-1
- handle gears in flight during migration (dmcphers@redhat.com)

* Thu Jun 20 2013 Adam Miller <admiller@redhat.com> 1.10.4-1
- Merge pull request #1650 from rajatchopra/master
  (dmcphers+openshiftbot@redhat.com)
- refix test.rb env - use direct values (rchopra@redhat.com)
- env changes for download cartridge options (rchopra@redhat.com)

* Tue Jun 18 2013 Adam Miller <admiller@redhat.com> 1.10.3-1
- Fix ignore cartridge version for rhc-admin-migrate (dmcphers@redhat.com)
- Merge pull request #1645 from pravisankar/dev/ravi/bug974925
  (dmcphers+openshiftbot@redhat.com)
- Merge pull request #1640 from rajatchopra/master
  (dmcphers+openshiftbot@redhat.com)
- Bug 974925 - Typo fix (rpenta@redhat.com)
- Various cleanup (dmcphers@redhat.com)
- bz969696 - download cart settings (rchopra@redhat.com)

* Mon Jun 17 2013 Adam Miller <admiller@redhat.com> 1.10.2-1
- Migration fixes (dmcphers@redhat.com)
- Merge pull request #1556 from pravisankar/dev/ravi/user-plan-update-changes
  (dmcphers+openshiftbot@redhat.com)
- origin_runtime_138 - Add SSL_ENDPOINT variable and filter whether carts use
  ssl_to_gear. (rmillner@redhat.com)
- Add links for plans REST api (rpenta@redhat.com)
- return HTTP Status code 200 from DELETE instead of 204 (lnader@redhat.com)
- WIP Cartridge Refactor - Add ignore_cartridge_version to V2->V2 migration
  (jhonce@redhat.com)
- Fixing alias system tests (abhgupta@redhat.com)

* Thu May 30 2013 Adam Miller <admiller@redhat.com> 1.10.1-1
- bump_minor_versions for sprint 29 (admiller@redhat.com)

* Wed May 22 2013 Adam Miller <admiller@redhat.com> 1.9.4-1
- enable downloadable cartridges by default (rchopra@redhat.com)

* Mon May 20 2013 Dan McPherson <dmcphers@redhat.com> 1.9.3-1
- Fix billing events controller (rpenta@redhat.com)

* Thu May 16 2013 Adam Miller <admiller@redhat.com> 1.9.2-1
- match node timeouts (dmcphers@redhat.com)
- fix builds (dmcphers@redhat.com)
- Merge pull request #1385 from danmcp/master
  (dmcphers+openshiftbot@redhat.com)
- Merge pull request #1351 from smarterclayton/upgrade_to_mocha_0_13_3
  (admiller@redhat.com)
- adding update in progress at the gear level (dmcphers@redhat.com)
- move v2 migration into standard migration (dmcphers@redhat.com)
- Upgrade to mocha 0.13.3 (compatible with Rails 3.2.12) (ccoleman@redhat.com)
- Fix Broker extended usage tests (rpenta@redhat.com)

* Wed May 08 2013 Adam Miller <admiller@redhat.com> 1.9.1-1
- bump_minor_versions for sprint 28 (admiller@redhat.com)

* Thu May 02 2013 Adam Miller <admiller@redhat.com> 1.8.4-1
- Merge pull request #1288 from pmorie/dev/v2_migrations
  (dmcphers+openshiftbot@redhat.com)
- Merge pull request #1256 from smarterclayton/support_external_cartridges
  (dmcphers+openshiftbot@redhat.com)
- Add post-migration validation step (pmorie@gmail.com)
- Merge remote-tracking branch 'origin/master' into support_external_cartridges
  (ccoleman@redhat.com)
- Rename "external cartridge" to "downloaded cartridge".  UI should call them
  "personal" cartridges (ccoleman@redhat.com)
- Use standard name for boolean (ccoleman@redhat.com)
- Merge remote-tracking branch 'origin/master' into support_external_cartridges
  (ccoleman@redhat.com)
- Conf not available in rhc-broker test (ccoleman@redhat.com)
- Add broker config for external cartridges (ccoleman@redhat.com)

* Wed May 01 2013 Adam Miller <admiller@redhat.com> 1.8.3-1
- update dynect customer name (blentz@redhat.com)

* Tue Apr 30 2013 Adam Miller <admiller@redhat.com> 1.8.2-1
- Removed 'max_storage_per_gear' capability for Silver plan Added
  'max_untracked_addtl_storage_per_gear=5' and
  'max_tracked_addtl_storage_per_gear=0' capabilities for Silver plan. Fixed
  unit tests and models to accommodate the above change. Added migration script
  for existing users Fixed devenv spec Fix migration script (rpenta@redhat.com)

* Thu Apr 25 2013 Adam Miller <admiller@redhat.com> 1.8.1-1
- Merge pull request #1252 from pmorie/dev/v2_migrations
  (dmcphers+openshiftbot@redhat.com)
- WIP: V2 Migrations (pmorie@gmail.com)
- rest api improvements (lnader@redhat.com)
- eventual consistency is alright for some cases in migration
  (rchopra@redhat.com)
- Bug 953263 - Use ANSI color codes only in development (ccoleman@redhat.com)
- bump_minor_versions for sprint XX (tdawson@redhat.com)

* Tue Apr 16 2013 Troy Dawson <tdawson@redhat.com> 1.7.5-1
- Merge pull request #1193 from smarterclayton/move_to_minitest
  (dmcphers+openshiftbot@redhat.com)
- Move to using minitest 3.5, webmock 1.8.11, and mocha 0.12.10
  (ccoleman@redhat.com)
- Billing email notification changes: -Added generic Counter mongoid model that
  will provide atomic sequence numbers -Added GSS sku for plans -Separate email
  config params for assign entitelement, revoke entitlement and account-
  modications -'Effective Date' field will show calendar date instead of
  'Immediate/End of month' string -Generate billing transaction id for plan
  changes and write a comment with this id for the corresponding account in
  aria. (rpenta@redhat.com)

* Thu Apr 11 2013 Adam Miller <admiller@redhat.com> 1.7.4-1
- Merge pull request #1158 from liggitt/currency_display3
  (dmcphers+openshiftbot@redhat.com)
- Merge pull request #1155 from pravisankar/dev/ravi/card526
  (dmcphers@redhat.com)
- Add CAD to broker aria config (jliggitt@redhat.com)
- Report usage to the correct plan: - Populate plan history in case of any plan
  changes. - During dowgrade, set old plan end time as end of the month. -
  Split usage between plan changes so that usage report time matches the plan.
  - For safer side, use mid time between begin and end record time as usage
  report time to aria. - Use usage record begin time as
  qualifier_4/sync_identifier to record_usage/bulk_record_usage() aria api
  instead of created_at time to uniquely determine the record in case of
  partial syncs (i.e. sync succeeded in aria but failed to persist in mongo).
  (rpenta@redhat.com)

* Wed Apr 10 2013 Adam Miller <admiller@redhat.com> 1.7.3-1
- Remove CAD rates from broker config (jliggitt@redhat.com)
- Currency display story number_to_user_currency helper method Make CSV export
  async, refactor csv to view Add tests for eur display Cache currency_cd in
  session (jliggitt@redhat.com)

* Mon Apr 08 2013 Adam Miller <admiller@redhat.com> 1.7.2-1
- Card 536 (lnader@redhat.com)
- Fix user plan update: To handle old existing users, while acquiring the lock
  check plan_sate to be nil or active. (rpenta@redhat.com)
- Billing entitlement email notification changes:  - Don't capture all events
  from aria  - Plan change (upgrade/downgrade) will send revoke/assign
  entitlement email without depending on aria events.  - Only handle aria
  events in case of account status changes due to dunning or account
  supplemental field changes.  - Don't send revoke/assign entitlements if the
  modified plan is free plan.  - Fetch account contact address by querying
  streamline  - Don't use 'RHLogin' supplemental field for login, instead query
  mongo with aria acct_no to fetch login.    Reason: Any special chars in
  RHLogin is not properly escaped by aria.  - Bug fixes  - Cleanup
  (rpenta@redhat.com)
- Fixing extended broker tests (abhgupta@redhat.com)
- Merge pull request #1103 from rajatchopra/master
  (dmcphers+openshiftbot@redhat.com)
- fixed broker extended test (lnader@redhat.com)
- default read should be from primary (rchopra@redhat.com)
- Merge pull request #1087 from lnader/improve_test_coverage
  (dmcphers+openshiftbot@redhat.com)
- improve test coverage (lnader@redhat.com)

* Thu Mar 28 2013 Adam Miller <admiller@redhat.com> 1.7.1-1
- bump_minor_versions for sprint 26 (admiller@redhat.com)
- Merge pull request #1083 from pravisankar/dev/ravi/bug928205_917961_aria-
  sync-fix (dmcphers@redhat.com)
- Bug 928205 - Fix rhc-admin-ctl-plan typo/checks (rpenta@redhat.com)

* Wed Mar 27 2013 Adam Miller <admiller@redhat.com> 1.6.6-1
- Merge remote-tracking branch 'origin/master' into update_to_new_plan_values
  (ccoleman@redhat.com)
- Merge pull request #1065 from liggitt/bug/924791
  (dmcphers+openshiftbot@redhat.com)
- Remove test default config, billing config loaded in dev/test env
  (ccoleman@redhat.com)
- Fix bug 924791 - Use aria virtual datetime when reporting usage
  (jliggitt@redhat.com)
- Merge remote-tracking branch 'origin/master' into update_to_new_plan_values
  (ccoleman@redhat.com)
- Rename freeshift/megashift to free/silver everywhere (ccoleman@redhat.com)

* Tue Mar 26 2013 Adam Miller <admiller@redhat.com> 1.6.5-1
- Fix bug 927893 - calculate is_premium? by checking for usage rates
  (jliggitt@redhat.com)
- Bug 924666 (lnader@redhat.com)
- Bug 923801 - add unit tests and cancel queued plan changes
  (jliggitt@redhat.com)

* Thu Mar 21 2013 Adam Miller <admiller@redhat.com> 1.6.4-1
- fixed bz924308 (admiller@redhat.com)
- Merge pull request #1048 from abhgupta/abhgupta-dev
  (dmcphers+openshiftbot@redhat.com)
- Bug 923801 - Update user plan will also look at queued plans and decides
  whether to cancel queued plan or/and update the master plan.
  (rpenta@redhat.com)
- Fixing randomize app/gear uuid to ensure they are the same for the first gear
  (abhgupta@redhat.com)
- Merge pull request #1039 from rmillner/fix_proxy
  (dmcphers+openshiftbot@redhat.com)
- Fixes frontend httpd proxy rebuild. (rmillner@redhat.com)
- Randomize the uuid in test and dev environments. This helps simulate the
  environment in production and facilitates testing those scenarios
  (abhgupta@redhat.com)
- US436: When broker receives final dunning event/cancel acct status, mark plan
  state as 'canceled' for the corresponding user in mongo. (rpenta@redhat.com)
- Merge pull request #1034 from pravisankar/dev/ravi/us506
  (dmcphers+openshiftbot@redhat.com)
- fix migration script for 2.0.24 (rchopra@redhat.com)
- fixing migration (dmcphers@redhat.com)
- update migration to current release (dmcphers@redhat.com)
- get the migrate script running (dmcphers@redhat.com)
- fixed broker extended test (lnader@redhat.com)
- US506 : Broker rails flag to enable/disable broker in maintenance mode
  (rpenta@redhat.com)

* Mon Mar 18 2013 Adam Miller <admiller@redhat.com> 1.6.3-1
- Merge pull request #1028 from abhgupta/abhgupta-dev
  (dmcphers+openshiftbot@redhat.com)
- Merge pull request #1002 from lnader/revert_pull_request_944
  (dmcphers+openshiftbot@redhat.com)
- Merge pull request #1027 from pravisankar/dev/ravi/fix_broker_extended_tests
  (dmcphers+openshiftbot@redhat.com)
- Merge pull request #1026 from rajatchopra/master
  (dmcphers+openshiftbot@redhat.com)
- Removing keys resources since its covered in the origin-server
  (abhgupta@redhat.com)
- Fix broker extended usage tests (rpenta@redhat.com)
- last_access and git_push in analytics (rchopra@redhat.com)
- Bug 921337 (lnader@redhat.com)
- Implement memcached on devenv (ccoleman@redhat.com)
- Changed private_certificate to private_ssl_certificate (lnader@redhat.com)
- Add SNI upload support to API (lnader@redhat.com)

* Thu Mar 14 2013 Adam Miller <admiller@redhat.com> 1.6.2-1
- Bug 921277 - User plan update api change: For upgrade, set assign_directive
  to 2 and for downgrade set assign_directive to 1 (rpenta@redhat.com)
- Fix Aria event notification format (rpenta@redhat.com)

* Thu Mar 07 2013 Adam Miller <admiller@redhat.com> 1.6.1-1
- bump_minor_versions for sprint 25 (admiller@redhat.com)

* Wed Mar 06 2013 Adam Miller <admiller@redhat.com> 1.5.13-1
- Merge pull request #980 from abhgupta/abhgupta-dev
  (dmcphers+openshiftbot@redhat.com)
- Add testing for cartridge properties in application and cartridge rest
  response (abhgupta@redhat.com)

* Wed Mar 06 2013 Adam Miller <admiller@redhat.com> 1.5.12-1
- Merge pull request #971 from smarterclayton/stop_caching_rh_sso_ticket
  (dmcphers@redhat.com)
- Remove test case (ccoleman@redhat.com)

* Tue Mar 05 2013 Adam Miller <admiller@redhat.com> 1.5.11-1
- Merge pull request #956 from pravisankar/dev/ravi/us3409-migration
  (dmcphers+openshiftbot@redhat.com)
- Migrate script: Add 'begin' usage records for all existing apps.
  (rpenta@redhat.com)
- usage rates unit test (rchopra@redhat.com)
- Merge pull request #961 from rajatchopra/master
  (dmcphers+openshiftbot@redhat.com)
- remove redundant observer - coverage tests for rhc-broker
  (rchopra@redhat.com)

* Mon Mar 04 2013 Adam Miller <admiller@redhat.com> 1.5.10-1
- Fix restart for migrate (dmcphers@redhat.com)

* Fri Mar 01 2013 Adam Miller <admiller@redhat.com> 1.5.9-1
- Removing mcollective qpid plugin and adding some doc (dmcphers@redhat.com)
- fix rhc-admin-migrate so that it restarts jenkins (rchopra@redhat.com)

* Thu Feb 28 2013 Adam Miller <admiller@redhat.com> 1.5.8-1
- Merge pull request #919 from pravisankar/dev/ravi/us3409
  (dmcphers+openshiftbot@redhat.com)
- Merge pull request #943 from
  smarterclayton/bug_916093_restore_broker_controller (dmcphers@redhat.com)
- reverted US2448 (lnader@redhat.com)
- ignore errors in teardown (lnader@redhat.com)
- Bug 916093 - Restore broker_controller (ccoleman@redhat.com)
- More than 80%% of the code is rewritten to improve rhc-admin-ctl-usage script
  Added bulk_record_usage to billing api. Used light weight Moped session
  instead of Mongoid model for read/write to mongo. Leverages
  bulk_record_usage() aria api to report usage in bulk that reduces #calls to
  aria. Query cloud_users collection for billing account# instead of aria api
  (mongo op is cheaper than external aria api). Process users by 'login'
  (created index on this field in UsageRecord model) and cache user->billing
  account# After some experimentation, setting chunk size for bulk_record_usage
  as 30 (conservative). We can go upto 50, anything above 50 records we may run
  into URL too long error. Set/Unset sync_time in one mongo call. If
  bulk_record_usage fails, we don't know which records has failed and so we
  can't unset sync_time. This should happen rarely and if it happens, try
  processing the records again one at a time. Added option 'enable-logger' to
  log errors and warning to /var/broker/openshift/usage.log file which helps
  during investigation in prod environment. Handle incorrect records that can
  ariase due to some hidden bug in broker. Try to fix the records or delete the
  records that are no longer needed. Fix and add ctl_usage test cases Use
  account# in record_usage/bulk_record_usage, we don't need to compute billing
  user id. Make list/sync/remove-sync-lock to be used in conjunction. For users
  with no aria a/c, sync option will delete ended records from usage_records
  collection. Check usage and usage_record collection consistency only during
  usage record deletion. Handle exceptions gracefully. Enable usage tracking in
  production mode. (rpenta@redhat.com)
- Merge pull request #938 from rmillner/US3143 (dmcphers@redhat.com)
- Migrate all cart types. (rmillner@redhat.com)
- Bug 916335 Split out config (dmcphers@redhat.com)

* Wed Feb 27 2013 Adam Miller <admiller@redhat.com> 1.5.7-1
- Merge pull request #934 from lnader/master (dmcphers+openshiftbot@redhat.com)
- Merge pull request #935 from smarterclayton/scope_changes_to_production.rb
  (dmcphers+openshiftbot@redhat.com)
- Default values missing for scopes in production.rb (ccoleman@redhat.com)
- US2448 (lnader@redhat.com)
- send domain creates and updates to nuture (dmcphers@redhat.com)

* Tue Feb 26 2013 Adam Miller <admiller@redhat.com> 1.5.6-1
- update migration to current release (dmcphers@redhat.com)
- Merge pull request #925 from smarterclayton/session_auth_support_2
  (dmcphers+openshiftbot@redhat.com)
- Merge remote-tracking branch 'origin/master' into session_auth_support_2
  (ccoleman@redhat.com)
- Merge remote-tracking branch 'origin/master' into session_auth_support_2
  (ccoleman@redhat.com)
- Tweak the log change so that is optional for developers running Rails
  directly, has same behavior on devenv, and allows more control over the path
  (ccoleman@redhat.com)
- Merge remote-tracking branch 'origin/master' into session_auth_support_2
  (ccoleman@redhat.com)
- Merge remote-tracking branch 'origin/master' into session_auth_support_2
  (ccoleman@redhat.com)
- Add the read scope.  Curl insecure doesn't create extra storage test.
  (ccoleman@redhat.com)
- Merge remote-tracking branch 'origin/master' into session_auth_support_2
  (ccoleman@redhat.com)
- Merge branch 'isolate_api_behavior_from_base_controller' into
  session_auth_support_2 (ccoleman@redhat.com)
- Move configuration parsing to a separate class (ccoleman@redhat.com)
- Config changes for scope support (ccoleman@redhat.com)
- Streamline auth tests pass (ccoleman@redhat.com)
- Changes to the broker to match session auth support in the origin
  (ccoleman@redhat.com)

* Mon Feb 25 2013 Adam Miller <admiller@redhat.com> 1.5.5-2
- bump Release for fixed build target rebuild (admiller@redhat.com)

* Mon Feb 25 2013 Adam Miller <admiller@redhat.com> 1.5.5-1
- Revert to original RAILS_LOG_PATH behavior (ccoleman@redhat.com)
- Merge pull request #920 from
  smarterclayton/bug_913816_work_around_bad_logtailer
  (dmcphers+openshiftbot@redhat.com)
- Bug 913816 - Fix log tailer to pick up the correct config
  (ccoleman@redhat.com)
- Merge pull request #918 from
  smarterclayton/bug_912286_cleanup_robots_misc_for_split
  (dmcphers+openshiftbot@redhat.com)
- Bug 912286 - Cleanup robots.txt and others for split (ccoleman@redhat.com)
- Tweak the log change so that is optional for developers running Rails
  directly, has same behavior on devenv, and allows more control over the path
  (ccoleman@redhat.com)

* Wed Feb 20 2013 Adam Miller <admiller@redhat.com> 1.5.4-1
- open source rhc-admin-clear-pending-ops to oo-admin-clear-pending-ops
  (rchopra@redhat.com)
- Merge pull request #906 from rajatchopra/master
  (dmcphers+openshiftbot@redhat.com)
- fix framework field for nurture send (rchopra@redhat.com)

* Tue Feb 19 2013 Adam Miller <admiller@redhat.com> 1.5.3-1
- make the clear pending ops script report what its doing (rchopra@redhat.com)
- fix rhc-admin-clear-pending-ops (rchopra@redhat.com)
- nurture send should use uuid for all events as is done with destroy
  (rchopra@redhat.com)
- stop passing extra app object (dmcphers@redhat.com)
- initial git url for nurture (rchopra@redhat.com)
- Merge pull request #888 from abhgupta/abhgupta-dev
  (dmcphers+openshiftbot@redhat.com)
- changes for US3402 - we are returning cartridge rates for all  plans
  (abhgupta@redhat.com)
- Remove Auth filter for billing controller (rpenta@redhat.com)
- minor changes to usage_ext (abhgupta@redhat.com)
- overriding get_usage_rate method in the usage class (abhgupta@redhat.com)
- Bug 910076 Split out aria config from production.rb (dmcphers@redhat.com)

* Fri Feb 08 2013 Adam Miller <admiller@redhat.com> 1.5.2-1
- Merge pull request #873 from pravisankar/dev/ravi/fix-billevent-minor
  (dmcphers+openshiftbot@redhat.com)
- Fix: send billing events to correct email addr (rpenta@redhat.com)
- Merge pull request #843 from smarterclayton/improve_action_logging
  (dmcphers+openshiftbot@redhat.com)
- Merge remote-tracking branch 'origin/master' into
  isolate_api_behavior_from_base_controller (ccoleman@redhat.com)
- Missed redundant filters (ccoleman@redhat.com)
- Remove legacy controllers and helpers.  Fix API controller reference in
  billing. (ccoleman@redhat.com)
- Match origin-server refactor (ccoleman@redhat.com)

* Thu Feb 07 2013 Adam Miller <admiller@redhat.com> 1.5.1-1
- Modifying tests to only set namespace and not the canonical_namespace
  (abhgupta@redhat.com)
- bump_minor_versions for sprint 24 (admiller@redhat.com)

* Wed Feb 06 2013 Adam Miller <admiller@redhat.com> 1.4.9-1
- Merge pull request #864 from danmcp/master (dmcphers@redhat.com)
- Merge pull request #862 from pravisankar/dev/ravi/us2626-config-fix
  (dmcphers@redhat.com)
- more renames express -> online (dmcphers@redhat.com)
- -Change usage rates from cents to dollars and add 'duration' field for each
  usage type. (rpenta@redhat.com)
- Merge pull request #858 from danmcp/master (dmcphers@redhat.com)
- Bug 884934 (asari.ruby@gmail.com)
- express -> online (dmcphers@redhat.com)
- more coverage adjustments (dmcphers@redhat.com)

* Tue Feb 05 2013 Adam Miller <admiller@redhat.com> 1.4.8-1
- Improving coverage tooling (dmcphers@redhat.com)
- Merge pull request #849 from rajatchopra/master (dmcphers@redhat.com)
- cleanup script for ops to clear pending op groups (rchopra@redhat.com)

* Tue Feb 05 2013 Adam Miller <admiller@redhat.com> 1.4.7-1
- Fix for bug 907683 - reading the distributed lock from the primary
  (abhgupta@redhat.com)
- Fixing broker extended tests (abhgupta@redhat.com)

* Mon Feb 04 2013 Adam Miller <admiller@redhat.com> 1.4.6-1
- Merge pull request #812 from maxamillion/dev/admiller/move_logs
  (dmcphers+openshiftbot@redhat.com)
- move all logs to /var/log/openshift/ so we can logrotate properly
  (admiller@redhat.com)

* Mon Feb 04 2013 Adam Miller <admiller@redhat.com> 1.4.5-1
- working on testing coverage (dmcphers@redhat.com)
- handle numbers for users and passwords (dmcphers@redhat.com)
- Merge pull request #834 from lnader/improve-test-coverage
  (dmcphers+openshiftbot@redhat.com)
- Better naming (dmcphers@redhat.com)
- Added simplecov to rhc broker tests (lnader@redhat.com)
- share db connection logic (dmcphers@redhat.com)

* Fri Feb 01 2013 Adam Miller <admiller@redhat.com> 1.4.4-1
- Bug 906669 (dmcphers@redhat.com)
- Merge pull request #828 from pravisankar/dev/ravi/us2626-feedback
  (dmcphers+openshiftbot@redhat.com)
- Merge pull request #822 from
  smarterclayton/us3350_establish_plan_upgrade_capability
  (dmcphers+openshiftbot@redhat.com)
- US2626 changes based on feedback - Store usage_rates for different currencies
  (currently only have usd) in broker rails configuration (rpenta@redhat.com)
- Review - remove old lines (ccoleman@redhat.com)
- US3350 - Expose a plan_upgrade_enabled capability (ccoleman@redhat.com)

* Thu Jan 31 2013 Adam Miller <admiller@redhat.com> 1.4.3-1
- fix rhc-admin-migrate (rchopra@redhat.com)
- Bug 906496: Repair ownership of app Git repo objects (ironcladlou@gmail.com)
- Merge pull request #820 from pravisankar/dev/ravi/us2626-unit-tests
  (dmcphers+openshiftbot@redhat.com)
- Merge pull request #816 from pravisankar/dev/ravi/us2626
  (dmcphers+openshiftbot@redhat.com)
- Premium cartridge usage unit tests (rpenta@redhat.com)
- Collect/Sync Usage data for EAP cart (rpenta@redhat.com)
- Making sure logins and domains left behind from earlier tests  are not
  accidentally reused (abhgupta@redhat.com)
- Merge pull request #814 from pravisankar/dev/ravi/fix-test
  (dmcphers+openshiftbot@redhat.com)
- Fix ctl_usage test (rpenta@redhat.com)
- Fix for broker extended tests (abhgupta@redhat.com)

* Tue Jan 29 2013 Adam Miller <admiller@redhat.com> 1.4.2-1
- Merge pull request #804 from rajatchopra/master
  (dmcphers+openshiftbot@redhat.com)
- Merge pull request #801 from pravisankar/dev/ravi/fix-broker-extended-tests
  (dmcphers+openshiftbot@redhat.com)
- restore mongo cursor and discard pagination (rchopra@redhat.com)
- Bug 892821 (dmcphers@redhat.com)
- Fix Broker Extended tests (rpenta@redhat.com)
- Bug 888692 (dmcphers@redhat.com)
- Bug 888692 (dmcphers@redhat.com)
- Bug 902286 (dmcphers@redhat.com)
- Bug 873180 (dmcphers@redhat.com)
- refactored admin scripts (rchopra@redhat.com)
- fix references to rhc app cartridge (dmcphers@redhat.com)
- half done - rhc-admin-migrate refactorization (rchopra@redhat.com)
- - Add SSL option to Rails config.datastore and to mongoid.yml
  (rpenta@redhat.com)
- - Use deep_copy() for copying user capabilities - Fix usage integration test
  (rpenta@redhat.com)
- more fixes (rpenta@redhat.com)
- Fix usage integration tests (rpenta@redhat.com)
- fix li-cleanup-util script, delete old mongo datastore tests
  (rpenta@redhat.com)
- model-refactor unit tests cleanup (rpenta@redhat.com)
- Model-refactor changes:  - Remove MongoMapper references  - Move systems
  tests, subuser tests and usage tests from li/rhc-broker to origin-
  server/broker  - Remove stale files: mongo_data_store.rb, old
  distributed_lock.rb  - Fix rhc-admin-ctl-plan (rpenta@redhat.com)
- Added Distributed Lock using mongoid model + unit testcase
  (rpenta@redhat.com)
- rhc-admin-ctl-usage script rework (rpenta@redhat.com)
- Populate mongoid.yml config from Rails datastore configuration
  (rpenta@redhat.com)
- fix nurture agent so that it sends correct app id for older apps
  (rchopra@redhat.com)
- fix nurture deconfigure event - send for app destroy only
  (rchopra@redhat.com)
- Fix for bug 892115 (abhgupta@redhat.com)
- fix rhc-admin-ctl-plan (rpenta@redhat.com)
- Bug 892132 (dmcphers@redhat.com)
- Fixing extended broker tests (abhgupta@redhat.com)
- Bug# 889957: part 2 (rpenta@redhat.com)
- fixing mongoid.yml for broker tests (abhgupta@redhat.com)
- fix mongoid.yml (dmcphers@redhat.com)
- add dynect migration (dmcphers@redhat.com)
- removing txt records (dmcphers@redhat.com)
- refactoring to use getter/setter for user capabilities (abhgupta@redhat.com)
- removed show-port from test (lnader@redhat.com)
- removing app templates and other fixes (dmcphers@redhat.com)
- fix all the cloud_user.find passing login falls (dmcphers@redhat.com)
- test case fixes (dmcphers@redhat.com)
- fix tests (dmcphers@redhat.com)
- fix rhc broker tests (dmcphers@redhat.com)
- fix broker functional tests (dmcphers@redhat.com)
- fixing cloud user tests (dmcphers@redhat.com)
- Updates for model refactor (dmcphers@redhat.com)
- Removing usage model from li (moved to origin-server) (kraman@gmail.com)
- fixup accept node and several cloud user usages (dmcphers@redhat.com)
- test case fixes (dmcphers@redhat.com)
- Fixing nurture call on app deletion (kraman@gmail.com)
- changed app.uuid to app._id.to_s (lnader@redhat.com)
- Add mongoid rpm as dependency (kraman@gmail.com)
- Updates for model refactor (dmcphers@redhat.com)

* Wed Jan 23 2013 Adam Miller <admiller@redhat.com> 1.4.1-1
- bump_minor_versions for sprint 23 (admiller@redhat.com)
- dont add to the config on every call (dmcphers@redhat.com)

* Wed Jan 23 2013 Adam Miller <admiller@redhat.com> 1.3.6-1
- Merge pull request #783 from ironcladlou/bz/903152 (dmcphers@redhat.com)
- Reset app git repo file permissions to gear user/group
  (ironcladlou@gmail.com)
- remove mod_passenger req from broker (dmcphers@redhat.com)

* Fri Jan 18 2013 Dan McPherson <dmcphers@redhat.com> 1.3.5-1
- Fix BZ895843: migrate postgresql cartridges (pmorie@gmail.com)

* Mon Jan 14 2013 Adam Miller <admiller@redhat.com> 1.3.4-1
- Bug 889017 (rchopra@redhat.com)

* Thu Jan 10 2013 Adam Miller <admiller@redhat.com> 1.3.3-1
- add missing loop for migrate (dmcphers@redhat.com)

* Tue Dec 18 2012 Adam Miller <admiller@redhat.com> 1.3.2-1
- fix for bug#886245 (rchopra@redhat.com)

* Wed Dec 12 2012 Adam Miller <admiller@redhat.com> 1.3.1-1
- bump_minor_versions for sprint 22 (admiller@redhat.com)

* Wed Dec 12 2012 Adam Miller <admiller@redhat.com> 1.2.5-1
- adding Provides:  openshift-origin-broker (tdawson@redhat.com)

* Wed Dec 05 2012 Adam Miller <admiller@redhat.com> 1.2.4-1
- Merge pull request #681 from sosiouxme/BZ872415 (openshift+bot@redhat.com)
- rhc-server-common should not depend on rhc-common - they are independant.
  (ccoleman@redhat.com)
- rhc conf files changes to add :default_gear_capabilities BZ872415
  (lmeyer@redhat.com)

* Tue Dec 04 2012 Adam Miller <admiller@redhat.com> 1.2.3-1
- Additional fix for US3078 (abhgupta@redhat.com)

* Thu Nov 29 2012 Adam Miller <admiller@redhat.com> 1.2.2-1
- various mcollective changes getting ready for 2.2 (dmcphers@redhat.com)
- taking production.rb out of config (dmcphers@redhat.com)
- fix elif typos (dmcphers@redhat.com)
- fix desc (dmcphers@redhat.com)
- command cleanup (dmcphers@redhat.com)
- avoid timeouts on long running queries in a safe way (dmcphers@redhat.com)
- don't call status if already found stopped from bulk call
  (dmcphers@redhat.com)
- use a more reasonable large disctimeout (dmcphers@redhat.com)
- usage and exit code cleanup (dmcphers@redhat.com)
- use $? the right way (dmcphers@redhat.com)
- fix max-threads opt (dmcphers@redhat.com)
- increase disc timeout on admin ops (dmcphers@redhat.com)
- using oo-ruby (dmcphers@redhat.com)
- Merge pull request #649 from smarterclayton/bug_878328_add_instant_apps
  (openshift+bot@redhat.com)
- Bug 878328 - Wordpress and Drupal should be tagged "instant_app"
  (ccoleman@redhat.com)
- migrate all the active gears first (dmcphers@redhat.com)
- migrate active gears first (dmcphers@redhat.com)
- increment rather than assign addtl nodes (dmcphers@redhat.com)

* Sat Nov 17 2012 Adam Miller <admiller@redhat.com> 1.2.1-1
- bump_minor_versions for sprint 21 (admiller@redhat.com)

* Fri Nov 16 2012 Adam Miller <admiller@redhat.com> 1.1.9-1
- Finishing off bug 876447 (dmcphers@redhat.com)

* Thu Nov 15 2012 Adam Miller <admiller@redhat.com> 1.1.8-1
- take out test-unit (dmcphers@redhat.com)
- more ruby 1.9 changes (dmcphers@redhat.com)
- Merge pull request #621 from danmcp/master (dmcphers@redhat.com)
- added ruby193-rubygem-minitest to rhc-site (admiller@redhat.com)
- Merge pull request #615 from rajatchopra/us3069 (dmcphers@redhat.com)
- Merge pull request #619 from rmillner/BZ876712 (dmcphers@redhat.com)
- Bug 876459 (dmcphers@redhat.com)
- Add "git" to the list of blacklisted app names. (rmillner@redhat.com)
- process the timezone to pacific time for nurture last access stamps
  (rchopra@redhat.com)

* Wed Nov 14 2012 Adam Miller <admiller@redhat.com> 1.1.7-1
- Merge pull request #616 from danmcp/master (dmcphers@redhat.com)
- add additional gem deps (dmcphers@redhat.com)

* Wed Nov 14 2012 Adam Miller <admiller@redhat.com> 1.1.6-1
- Merge pull request #612 from smarterclayton/us3046_quickstarts_and_app_types
  (openshift+bot@redhat.com)
- Merge remote-tracking branch 'origin/master' into
  us3046_quickstarts_and_app_types (ccoleman@redhat.com)
- Add quickstarts to broker (ccoleman@redhat.com)
- Add Quickstart config to build (ccoleman@redhat.com)
- US3046 - Implement quickstarts in drupal and react to changes in console
  (ccoleman@redhat.com)

* Wed Nov 14 2012 Adam Miller <admiller@redhat.com> 1.1.5-1
- Merge pull request #614 from danmcp/master (openshift+bot@redhat.com)
- migration efficiency changes (dmcphers@redhat.com)
- fix aria tests (dmcphers@redhat.com)
- Fixing gemspecs (kraman@gmail.com)
- Moving plugins to Rails 3.2.8 engines (kraman@gmail.com)
- sclizing gems (dmcphers@redhat.com)
- Bug 873349 (dmcphers@redhat.com)

* Tue Nov 13 2012 Adam Miller <admiller@redhat.com> 1.1.4-1
- Merge pull request #599 from ramr/master (openshift+bot@redhat.com)
- add acceptable errors category (dmcphers@redhat.com)
- better strings (dmcphers@redhat.com)
- Change back mcollective timeout on rhc to 3 minutes. (ramr@redhat.com)
- reformat timestring and url for nurture (rchopra@redhat.com)
- Add additional timings for migrations (dmcphers@redhat.com)
- handle queues as available processors rather than preset lists
  (dmcphers@redhat.com)
- Merge pull request #595 from rajatchopra/us3069 (openshift+bot@redhat.com)
- last access time update to nurture (rchopra@redhat.com)

* Mon Nov 12 2012 Adam Miller <admiller@redhat.com> 1.1.3-1
- simplify migration logic (dmcphers@redhat.com)

* Thu Nov 08 2012 Adam Miller <admiller@redhat.com> 1.1.2-1
- Merge pull request #580 from bdecoste/master (openshift+bot@redhat.com)
- BZ873969 (bdecoste@gmail.com)
- Merge pull request #575 from bdecoste/master (openshift+bot@redhat.com)
- US2944 - CapeDwarf (bdecoste@gmail.com)
- US2944 - CapeDwarf (bdecoste@gmail.com)
- update migration to 2.0.20 (dmcphers@redhat.com)
- Fix system/app_events_test.rb (causing broker_extended to fail)
  (rpenta@redhat.com)

* Thu Nov 01 2012 Adam Miller <admiller@redhat.com> 1.1.1-1
- bump_minor_versions for sprint 20 (admiller@redhat.com)
