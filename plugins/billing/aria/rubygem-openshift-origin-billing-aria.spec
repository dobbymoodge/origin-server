%if 0%{?fedora}%{?rhel} <= 6
    %global scl ruby193
    %global scl_prefix ruby193-
%endif
%{!?scl:%global pkg_name %{name}}
%{?scl:%scl_package rubygem-%{gem_name}}
%global gem_name openshift-origin-billing-aria
%global rubyabi 1.9.1

Summary:        OpenShift plugin for Aria Billing service

Name:           rubygem-%{gem_name}
Version: 1.5.6
Release:        1%{?dist}
Group:          Development/Languages
License:        ASL 2.0
URL:            http://openshift.redhat.com
Source0:        rubygem-%{gem_name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires:       %{?scl:%scl_prefix}ruby(abi) = %{rubyabi}
Requires:       %{?scl:%scl_prefix}ruby
Requires:       %{?scl:%scl_prefix}rubygems
Requires:       rubygem(openshift-origin-common)
Requires:       %{?scl:%scl_prefix}rubygem(json)

%if 0%{?fedora}%{?rhel} <= 6
BuildRequires:  ruby193-build
BuildRequires:  scl-utils-build
%endif
BuildRequires:  %{?scl:%scl_prefix}ruby(abi) = %{rubyabi}
BuildRequires:  %{?scl:%scl_prefix}ruby 
BuildRequires:  %{?scl:%scl_prefix}rubygems
BuildRequires:  %{?scl:%scl_prefix}rubygems-devel
BuildArch:      noarch
Provides:       rubygem(%{gem_name}) = %version

%description
Provides Aria Billing service based plugin

%prep
%setup -q

%build
%{?scl:scl enable %scl - << \EOF}
mkdir -p ./%{gem_dir}
# Create the gem as gem install only works on a gem file
gem build %{gem_name}.gemspec
export CONFIGURE_ARGS="--with-cflags='%{optflags}'"
# gem install compiles any C extensions and installs into a directory
# We set that to be a local directory so that we can move it into the
# buildroot in %%install
gem install -V \
        --local \
        --install-dir ./%{gem_dir} \
        --bindir ./%{_bindir} \
        --force \
        --rdoc \
        %{gem_name}-%{version}.gem
%{?scl:EOF}

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a ./%{gem_dir}/* %{buildroot}%{gem_dir}/

mkdir -p %{buildroot}/etc/openshift/plugins.d
cp conf/openshift-origin-billing-aria.conf %{buildroot}/etc/openshift/plugins.d/
cp conf/openshift-origin-billing-aria-dev.conf %{buildroot}/etc/openshift/plugins.d/

%clean
rm -rf %{buildroot}                                

%files
%defattr(-,root,root,-)
%doc %{gem_docdir}
%{gem_instdir}
%{gem_spec}
%{gem_cache}
%config(noreplace) /etc/openshift/plugins.d/openshift-origin-billing-aria.conf
/etc/openshift/plugins.d/openshift-origin-billing-aria-dev.conf

%changelog
* Fri Apr 26 2013 Adam Miller <admiller@redhat.com> 1.5.6-1
- Add 'Operating Unit' field to billing email notifications.
  (rpenta@redhat.com)

* Tue Apr 16 2013 Troy Dawson <tdawson@redhat.com> 1.5.5-1
- Billing email notification changes: -Added generic Counter mongoid model that
  will provide atomic sequence numbers -Added GSS sku for plans -Separate email
  config params for assign entitelement, revoke entitlement and account-
  modications -'Effective Date' field will show calendar date instead of
  'Immediate/End of month' string -Generate billing transaction id for plan
  changes and write a comment with this id for the corresponding account in
  aria. (rpenta@redhat.com)

* Thu Apr 11 2013 Adam Miller <admiller@redhat.com> 1.5.4-1
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

* Wed Apr 10 2013 Adam Miller <admiller@redhat.com> 1.5.3-1
- Remove CAD rates from broker config (jliggitt@redhat.com)
- Currency display story number_to_user_currency helper method Make CSV export
  async, refactor csv to view Add tests for eur display Cache currency_cd in
  session (jliggitt@redhat.com)

* Mon Apr 08 2013 Adam Miller <admiller@redhat.com> 1.5.2-1
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

* Thu Mar 28 2013 Adam Miller <admiller@redhat.com> 1.5.1-1
- bump_minor_versions for sprint 26 (admiller@redhat.com)
- Merge pull request #1083 from pravisankar/dev/ravi/bug928205_917961_aria-
  sync-fix (dmcphers@redhat.com)
- Fix conf variable in openshift-origin-billing-aria.rb (rpenta@redhat.com)
- Fix sync usage in Aria plugin: pass app_name as qualifier and added
  additional guards (rpenta@redhat.com)

* Wed Mar 27 2013 Adam Miller <admiller@redhat.com> 1.4.6-1
- Update plan # (ccoleman@redhat.com)
- Merge remote-tracking branch 'origin/master' into update_to_new_plan_values
  (ccoleman@redhat.com)
- Merge pull request #1065 from liggitt/bug/924791
  (dmcphers+openshiftbot@redhat.com)
- Bad initializer file (ccoleman@redhat.com)
- Remove test default config, billing config loaded in dev/test env
  (ccoleman@redhat.com)
- Fix bug 924791 - Use aria virtual datetime when reporting usage
  (jliggitt@redhat.com)
- Merge remote-tracking branch 'origin/master' into update_to_new_plan_values
  (ccoleman@redhat.com)
- Rename freeshift/megashift to free/silver everywhere (ccoleman@redhat.com)
- Allow broker plan values to be configured.  Change devenv defaults to match
  new 'Free' and 'Silver' plans. (ccoleman@redhat.com)

* Tue Mar 26 2013 Adam Miller <admiller@redhat.com> 1.4.5-1
- Bug 924666 (lnader@redhat.com)
- Bug 923801 - add unit tests and cancel queued plan changes
  (jliggitt@redhat.com)

* Thu Mar 21 2013 Adam Miller <admiller@redhat.com> 1.4.4-1
- Bug 923801 - Update user plan will also look at queued plans and decides
  whether to cancel queued plan or/and update the master plan.
  (rpenta@redhat.com)
- - Allow request to /broker/billing/rest/events only if auth_key, client_no
  matches and remote ip is within aria provisioning servers IP range. - Mark
  user as in 'canceled' plan state if aria event status code < 0 i.e.
  suspended, canceled or terminated. (rpenta@redhat.com)
- US436: When broker receives final dunning event/cancel acct status, mark plan
  state as 'canceled' for the corresponding user in mongo. (rpenta@redhat.com)

* Mon Mar 18 2013 Adam Miller <admiller@redhat.com> 1.4.3-1
- Changed private_certificate to private_ssl_certificate (lnader@redhat.com)
- Add SNI upload support to API (lnader@redhat.com)

* Thu Mar 14 2013 Adam Miller <admiller@redhat.com> 1.4.2-1
- Merge pull request #1006 from pravisankar/dev/ravi/bug920107
  (dmcphers+openshiftbot@redhat.com)
- Bug 920107 - Don't create usage records for subaccount users during migration
  (rpenta@redhat.com)
- Bug 921277 - User plan update api change: For upgrade, set assign_directive
  to 2 and for downgrade set assign_directive to 1 (rpenta@redhat.com)
- Bug 920107 - oo-admin-ctl-usage shouldn't throw errors in case of parent
  users with c9 gears (rpenta@redhat.com)
- Fix Aria event notification format (rpenta@redhat.com)

* Thu Mar 07 2013 Adam Miller <admiller@redhat.com> 1.4.1-1
- bump_minor_versions for sprint 25 (admiller@redhat.com)

* Wed Mar 06 2013 Adam Miller <admiller@redhat.com> 1.3.7-1
- Usage migration: show total #usage records created in the end
  (rpenta@redhat.com)

* Tue Mar 05 2013 Adam Miller <admiller@redhat.com> 1.3.6-1
- Migrate script: Add 'begin' usage records for all existing apps.
  (rpenta@redhat.com)

* Mon Mar 04 2013 Adam Miller <admiller@redhat.com> 1.3.5-1
- Aria plugin fixes (rpenta@redhat.com)

* Thu Feb 28 2013 Adam Miller <admiller@redhat.com> 1.3.4-1
- Fixing tags from merge of new package

* Wed Feb 27 2013 Ravi Sankar <rpenta@redhat.com> 1.3.3-1
- Re-organize aria plugin files (rpenta@redhat.com)
- Automatic commit of package [rubygem-openshift-origin-billing-aria] release
  [1.3.2-1]. (rpenta@redhat.com)
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

* Wed Feb 27 2013 Ravi Sankar <rpenta@redhat.com> 1.3.2-1
- new package built with tito

