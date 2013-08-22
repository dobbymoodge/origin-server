%define htmldir %{_var}/www/html
%define brokerdir %{_var}/www/openshift/broker

Summary:   Li broker components
Name:      rhc-broker
Version: 1.13.9
Release:   1%{?dist}
Group:     Network/Daemons
License:   GPLv2
URL:       http://openshift.redhat.com
Source0:   rhc-broker-%{version}.tar.gz

BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
Requires:  rhc-common
Requires:  rhc-server-common
Requires:  ruby193-ruby-wrapper
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

mv %{buildroot}%{brokerdir}/script/rhc-admin-ctl-plan %{buildroot}/%{_bindir}
mv %{buildroot}%{brokerdir}/script/rhc-admin-stale-dns %{buildroot}/%{_bindir}
mv %{buildroot}%{brokerdir}/script/rhc-admin-delete-subaccounts %{buildroot}/%{_bindir}
mv %{buildroot}%{brokerdir}/script/rhc-admin-migrate-datastore %{buildroot}/%{_bindir}

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
%attr(0750,-,-) %{_bindir}/rhc-admin-ctl-plan
%attr(0750,-,-) %{_bindir}/rhc-admin-stale-dns
%attr(0750,-,-) %{_bindir}/rhc-admin-delete-subaccounts
%attr(0750,-,-) %{_bindir}/rhc-admin-migrate-datastore

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
* Thu Aug 22 2013 Adam Miller <admiller@redhat.com> 1.13.9-1
- Script to delete all subaccounts that has no activity for at least a week and
  has no applications for a given parent login or for all parent logins.
  (rpenta@redhat.com)

* Tue Aug 20 2013 Adam Miller <admiller@redhat.com> 1.13.8-1
- Merge pull request #1839 from rajatchopra/master (dmcphers@redhat.com)
- add postrelease mode for datastore migration (rchopra@redhat.com)

* Tue Aug 20 2013 Adam Miller <admiller@redhat.com> 1.13.7-1
- Merge pull request #1831 from abhgupta/abhgupta-dev
  (dmcphers+openshiftbot@redhat.com)
- Fix for bug 995034 (abhgupta@redhat.com)

* Mon Aug 19 2013 Adam Miller <admiller@redhat.com> 1.13.6-1
- Merge pull request #1833 from abhgupta/bug_998368 (dmcphers@redhat.com)
- Fix for bug 998368 (abhgupta@redhat.com)

* Mon Aug 19 2013 Adam Miller <admiller@redhat.com> 1.13.5-1
- fix bz998404 (rchopra@redhat.com)
- Merge pull request #1825 from dobbymoodge/fix_tests_card219
  (dmcphers+openshiftbot@redhat.com)
- Fixing premium cartridge version from usage (abhgupta@redhat.com)
- <cartridge versions> origin_runtime_219, Update references to changed cart
  versions https://trello.com/c/evcTYKdn/219-3-adjust-out-of-date-cartridge-
  versions (jolamb@redhat.com)

* Fri Aug 16 2013 Adam Miller <admiller@redhat.com> 1.13.4-1
- Bug 997831 - Domain scope not in config (ccoleman@redhat.com)
- Merge pull request #1817 from rajatchopra/master
  (dmcphers+openshiftbot@redhat.com)
- migration for updating port interfaces on all gears (rchopra@redhat.com)

* Wed Aug 14 2013 Adam Miller <admiller@redhat.com> 1.13.3-1
- Default to membership off in development mode (ccoleman@redhat.com)
- Merge remote-tracking branch 'origin/master' into
  origin_ui_73_membership_model (ccoleman@redhat.com)
- Update domain allowed_gear_sizes during migration (ccoleman@redhat.com)
- * Support changes for membership in OpenShift Online (ccoleman@redhat.com)

* Fri Aug 09 2013 Adam Miller <admiller@redhat.com> 1.13.2-1
- Merge pull request #1810 from abhgupta/abhgupta-dev (dmcphers@redhat.com)
- Fixing cartridge version for migration script (abhgupta@redhat.com)

* Thu Aug 08 2013 Adam Miller <admiller@redhat.com> 1.13.1-1
- Migration script for updating cartridge/component versions in their name
  (abhgupta@redhat.com)
- added test for results returned from node (lnader@redhat.com)
- bump_minor_versions for sprint 32 (admiller@redhat.com)

* Wed Jul 31 2013 Adam Miller <admiller@redhat.com> 1.12.7-1
- Formalize datastore migration (dmcphers@redhat.com)

* Wed Jul 31 2013 Adam Miller <admiller@redhat.com> 1.12.6-1
- Bug 956859 (dmcphers@redhat.com)

* Mon Jul 29 2013 Adam Miller <admiller@redhat.com> 1.12.5-1
- Merge pull request #1753 from smarterclayton/changes_for_membership
  (dmcphers+openshiftbot@redhat.com)
- changing dynect user (dmcphers@redhat.com)
- Merge remote-tracking branch 'origin/master' into changes_for_membership
  (ccoleman@redhat.com)
- Merge remote-tracking branch 'origin/master' into changes_for_membership
  (ccoleman@redhat.com)
- Merge remote-tracking branch 'origin/master' into changes_for_membership
  (ccoleman@redhat.com)
- Make capabilities behave more like a regular model object
  (ccoleman@redhat.com)

* Fri Jul 26 2013 Adam Miller <admiller@redhat.com> 1.12.4-1
- Revert "Card 57 - provide simple visual branding to the admin console"
  (lmeyer@redhat.com)
- Merge pull request #1761 from pravisankar/dev/ravi/aria-fixes
  (dmcphers+openshiftbot@redhat.com)
- Fix broker extended tests (rpenta@redhat.com)

* Thu Jul 25 2013 Adam Miller <admiller@redhat.com> 1.12.3-1
- Merge pull request #1759 from jwforres/card_57_admin_console_styling
  (dmcphers+openshiftbot@redhat.com)
- make everything shell safe (dmcphers@redhat.com)
- Card 57 - provide simple visual branding to the admin console
  (jforrest@redhat.com)
