%define ruby_sitelibdir            %(ruby -rrbconfig -e "puts Config::CONFIG['sitelibdir']")

Summary:       Common dependencies of the OpenShift broker and site
Name:          rhc-server-common
Version:       0.80.0
Release:       1%{?dist}
Group:         Network/Daemons
License:       GPLv2
URL:           http://openshift.redhat.com
Source0:       rhc-server-common-%{version}.tar.gz

BuildRoot:     %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
BuildRequires: ruby
Requires:      ruby >= 1.8.7
Requires:      rubygem-parseconfig
Requires:      rubygem-json

BuildArch: noarch

%description
Provides the common dependencies for the OpenShift broker and site

%prep
%setup -q

%build
for f in openshift/*.rb
do
  ruby -c $f
done

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{ruby_sitelibdir}
cp -r openshift %{buildroot}%{ruby_sitelibdir}
cp openshift.rb %{buildroot}%{ruby_sitelibdir}
mkdir -p %{buildroot}%{_sysconfdir}/libra
cp conf/libra/* %{buildroot}%{_sysconfdir}/libra/

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{ruby_sitelibdir}/openshift
%{ruby_sitelibdir}/openshift.rb
%attr(0640,root,libra_user) %config(noreplace) %{_sysconfdir}/libra/controller.conf

%pre
/usr/sbin/groupadd -r libra_user 2>&1 || :
/usr/sbin/useradd libra_passenger -g libra_user \
                                  -d /var/lib/passenger \
                                  -r \
                                  -s /sbin/nologin 2>&1 > /dev/null || :

%changelog
* Tue Oct 11 2011 Dan McPherson <dmcphers@redhat.com> 0.79.9-1
- fix get_cart_framework to handle multiple - (dmcphers@redhat.com)

* Mon Oct 10 2011 Dan McPherson <dmcphers@redhat.com> 0.79.8-1
- require only 1 jenkins per account (dmcphers@redhat.com)

* Wed Oct 05 2011 Dan McPherson <dmcphers@redhat.com> 0.79.7-1
- add concept of CLIENT_ERROR and use from phpmyadmin (dmcphers@redhat.com)

* Wed Oct 05 2011 Dan McPherson <dmcphers@redhat.com> 0.79.6-1
- better logging (dmcphers@redhat.com)

* Tue Oct 04 2011 Dan McPherson <dmcphers@redhat.com> 0.79.5-1
- Added streamline timing to HTTP requests (fotios@redhat.com)

* Mon Oct 03 2011 Dan McPherson <dmcphers@redhat.com> 0.79.4-1
- Reverting DRYed up streamline configs for now (fotios@redhat.com)

* Mon Oct 03 2011 Dan McPherson <dmcphers@redhat.com> 0.79.3-1
- Fixed Rails missing for cucumber tests (fotios@redhat.com)
- DRYed up streamline configuration variables (fotios@redhat.com)

* Thu Sep 29 2011 Dan McPherson <dmcphers@redhat.com> 0.79.2-1
- turn on cnames and some status work (dmcphers@redhat.com)

* Thu Sep 29 2011 Dan McPherson <dmcphers@redhat.com> 0.79.1-1
- bump spec numbers (dmcphers@redhat.com)
- env var add/remove (dmcphers@redhat.com)

* Wed Sep 28 2011 Dan McPherson <dmcphers@redhat.com> 0.78.13-1
- add preconfigure for jenkins to split out auth key gen (dmcphers@redhat.com)

* Mon Sep 26 2011 Dan McPherson <dmcphers@redhat.com> 0.78.12-1
- Added password change functionality (fotios@redhat.com)

* Mon Sep 26 2011 Dan McPherson <dmcphers@redhat.com> 0.78.11-1
- separate streamline secrets (dmcphers@redhat.com)
- Validate the login resolves before registering a domain (mhicks@redhat.com)

* Fri Sep 23 2011 Dan McPherson <dmcphers@redhat.com> 0.78.10-1
- remove check for rhlogin length >= 6 (dmcphers@redhat.com)

* Thu Sep 22 2011 Dan McPherson <dmcphers@redhat.com> 0.78.9-1
- rename ssh_keys to system_ssh_keys (dmcphers@redhat.com)

* Tue Sep 20 2011 Dan McPherson <dmcphers@redhat.com> 0.78.8-1
- Added node profile to broker configs (mmcgrath@redhat.com)
- updating to use dynamic node profile (mmcgrath@redhat.com)
- Merge branch 'master' of ssh://git1.ops.rhcloud.com/srv/git/li
  (mmcgrath@redhat.com)
- Changing default find_all to use capacity instead of git_repos
  (mmcgrath@redhat.com)
- add broker auth key when jenkins is created (dmcphers@redhat.com)
- add auth keys when a new app is added (dmcphers@redhat.com)
- call add and remove ssh keys from jenkins configure and deconfigure
  (dmcphers@redhat.com)

* Thu Sep 15 2011 Dan McPherson <dmcphers@redhat.com> 0.78.7-1
- adding iv encryption (dmcphers@redhat.com)
- broker auth fixes - functional for adding token (dmcphers@redhat.com)
- fix typo (dmcphers@redhat.com)
- move broker_auth_secret to controller.conf (dmcphers@redhat.com)

* Wed Sep 14 2011 Dan McPherson <dmcphers@redhat.com> 0.78.6-1
- disable client gem release (temp) beginnings of broker auth adding barista to
  spec (dmcphers@redhat.com)

* Tue Sep 13 2011 Dan McPherson <dmcphers@redhat.com> 0.78.5-1
- Changed Rails.configuration.streamline to be a hash. Changed references to
  build URIs from that hash (fotios@redhat.com)

* Mon Sep 12 2011 Dan McPherson <dmcphers@redhat.com> 0.78.4-1
- better error checking (dmcphers@redhat.com)

* Mon Sep 12 2011 Dan McPherson <dmcphers@redhat.com> 0.78.3-1
- allow 1 system ssh key per app (dmcphers@redhat.com)

* Fri Sep 09 2011 Matt Hicks <mhicks@redhat.com> 0.78.2-1
- have mcollective use capacity instead of git_repos (mmcgrath@redhat.com)

* Thu Sep 01 2011 Dan McPherson <dmcphers@redhat.com> 0.78.1-1
- bump spec numbers (dmcphers@redhat.com)
- add system ssh key support along with the beginning of multiple ssh key
  support (dmcphers@redhat.com)

* Mon Aug 29 2011 Dan McPherson <dmcphers@redhat.com> 0.77.5-1
- better error handling (dmcphers@redhat.com)

* Mon Aug 29 2011 Dan McPherson <dmcphers@redhat.com> 0.77.4-1
- 734009 (dmcphers@redhat.com)

* Thu Aug 25 2011 Dan McPherson <dmcphers@redhat.com> 0.77.3-1
- add CNAME support (turned off) (dmcphers@redhat.com)
- add method for cname (dmcphers@redhat.com)
- add logging (dmcphers@redhat.com)

* Thu Aug 25 2011 Matt Hicks <mhicks@redhat.com> 0.77.2-1
- Adding protection for a directory entry in S3 (mhicks@redhat.com)

* Fri Aug 19 2011 Matt Hicks <mhicks@redhat.com> 0.77.1-1
- bump spec numbers (dmcphers@redhat.com)

* Mon Aug 15 2011 Matt Hicks <mhicks@redhat.com> 0.76.4-1
- rename li-controller-0.1 to li-controller (dmcphers@redhat.com)

* Tue Aug 09 2011 Dan McPherson <dmcphers@redhat.com> 0.76.3-1
- Some prelim API and broker versioning (jimjag@redhat.com)

* Mon Aug 08 2011 Matt Hicks <mhicks@redhat.com> 0.76.2-1
- Apptegic Integration (mhicks@redhat.com)
- fix tests (dmcphers@redhat.com)
- enable remainder of selenium tests (dmcphers@redhat.com)

* Fri Aug 05 2011 Dan McPherson <dmcphers@redhat.com> 0.76.1-1
- bump spec numbers (dmcphers@redhat.com)

* Tue Jul 26 2011 Dan McPherson <dmcphers@redhat.com> 0.75.4-1
- test case fix (dmcphers@redhat.com)

* Tue Jul 26 2011 Dan McPherson <dmcphers@redhat.com> 0.75.3-1
- better error handling (dmcphers@redhat.com)
- fail on no json from streamline (dmcphers@redhat.com)

* Mon Jul 25 2011 Dan McPherson <dmcphers@redhat.com> 0.75.2-1
- remove aws account number from flex request access (dmcphers@redhat.com)

* Thu Jul 21 2011 Dan McPherson <dmcphers@redhat.com> 0.75.1-1
- dns call cleanup (dmcphers@redhat.com)
- refactor some common code (dmcphers@redhat.com)
- handle destroy with auto identity update (dmcphers@redhat.com)
- bump spec numbers (dmcphers@redhat.com)
- add server identity and namespace auto migrate (dmcphers@redhat.com)

* Fri Jul 15 2011 Dan McPherson <dmcphers@redhat.com> 0.74.4-1
- Merge branch 'master' of ssh://libragit/srv/git/li (edirsh@redhat.com)
- Changed streamline_mock so selenium tests will run (edirsh@redhat.com)

* Fri Jul 15 2011 Dan McPherson <dmcphers@redhat.com> 0.74.3-1
- Added more test coverage for access/exress controller (edirsh@redhat.com)

* Tue Jul 12 2011 Dan McPherson <dmcphers@redhat.com> 0.74.2-1
- Automatic commit of package [rhc-server-common] release [0.74.1-1].
  (dmcphers@redhat.com)
- bumping spec numbers (dmcphers@redhat.com)
- Automatic commit of package [rhc-server-common] release [0.73.17-1].
  (dmcphers@redhat.com)
- handle errors from controller and properly delete failed app creations
  (dmcphers@redhat.com)
- Automatic commit of package [rhc-server-common] release [0.73.16-1].
  (dmcphers@redhat.com)
- add retries to login/logout and doc updates (dmcphers@redhat.com)
- Automatic commit of package [rhc-server-common] release [0.73.15-1].
  (dmcphers@redhat.com)
- remove embed param passing to broker and doc updates (dmcphers@redhat.com)
- Automatic commit of package [rhc-server-common] release [0.73.14-1].
  (dmcphers@redhat.com)
- rework dyn retries (dmcphers@redhat.com)
- Automatic commit of package [rhc-server-common] release [0.73.13-1].
  (dmcphers@redhat.com)
- rework dyn retries (dmcphers@redhat.com)
- Automatic commit of package [rhc-server-common] release [0.73.12-1].
  (dmcphers@redhat.com)
- cleanup client messages (dmcphers@redhat.com)
- fix typo causing build break (dmcphers@redhat.com)
- add dyn retries (dmcphers@redhat.com)
- moving debug line so it produces output (mmcgrath@redhat.com)
- Automatic commit of package [rhc-server-common] release [0.73.11-1].
  (edirsh@redhat.com)
- consistent names (dmcphers@redhat.com)
- Hide the "type" logic (jimjag@redhat.com)
- Automatic commit of package [rhc-server-common] release [0.73.10-1].
  (dmcphers@redhat.com)
- fixup embedded cart remove (dmcphers@redhat.com)
- Automatic commit of package [rhc-server-common] release [0.73.9-1].
  (dmcphers@redhat.com)
- wrong message for invalid cart type (dmcphers@redhat.com)
- Automatic commit of package [rhc-server-common] release [0.73.8-1].
  (dmcphers@redhat.com)
- cleanup (dmcphers@redhat.com)
- perf improvements for how/when we look up the valid cart types on the server
  (dmcphers@redhat.com)
- Merge branch 'master' of ssh://git1.ops.rhcloud.com/srv/git/li
  (mmcgrath@redhat.com)
- fixing embedded call and adding debug (mmcgrath@redhat.com)
- handle nil output (dmcphers@redhat.com)
- Automatic commit of package [rhc-server-common] release [0.73.7-1].
  (dmcphers@redhat.com)
- fix error message when havent requested access yet (dmcphers@redhat.com)
- sso support for broker (dmcphers@redhat.com)
- cleanup unused vars (dmcphers@redhat.com)
- Automatic commit of package [rhc-server-common] release [0.73.6-1].
  (dmcphers@redhat.com)
- undo passing rhlogin to cart (dmcphers@redhat.com)
- Merge branch 'master' of ssh://git1.ops.rhcloud.com/srv/git/li
  (mmcgrath@redhat.com)
- add nurture call for git push (dmcphers@redhat.com)
- Added mysql (mmcgrath@redhat.com)
- Correcting framework operations (mmcgrath@redhat.com)
- fixing merge from Dan (mmcgrath@redhat.com)
- proper error handling for embedded cases (mmcgrath@redhat.com)
- share common code (dmcphers@redhat.com)
- better message on app exists (dmcphers@redhat.com)
- Automatic commit of package [rhc-server-common] release [0.73.5-1].
  (dmcphers@redhat.com)
- Added initial S3 bits (mmcgrath@redhat.com)
- share code (dmcphers@redhat.com)
- Automatic commit of package [rhc-server-common] release [0.73.4-1].
  (mhicks@redhat.com)
- allow messsages from cart to client (dmcphers@redhat.com)
- Added support to call embedded cartridges (mmcgrath@redhat.com)
- Added embedded list (mmcgrath@redhat.com)

* Mon Jul 11 2011 Dan McPherson <dmcphers@redhat.com> 0.74.1-1
- bumping spec numbers (dmcphers@redhat.com)

* Sat Jul 09 2011 Dan McPherson <dmcphers@redhat.com> 0.73.17-1
- handle errors from controller and properly delete failed app creations
  (dmcphers@redhat.com)

* Thu Jul 07 2011 Dan McPherson <dmcphers@redhat.com> 0.73.16-1
- add retries to login/logout and doc updates (dmcphers@redhat.com)

* Thu Jul 07 2011 Dan McPherson <dmcphers@redhat.com> 0.73.15-1
- remove embed param passing to broker and doc updates (dmcphers@redhat.com)

* Wed Jul 06 2011 Dan McPherson <dmcphers@redhat.com> 0.73.14-1
- rework dyn retries (dmcphers@redhat.com)

* Wed Jul 06 2011 Dan McPherson <dmcphers@redhat.com> 0.73.13-1
- rework dyn retries (dmcphers@redhat.com)

* Wed Jul 06 2011 Dan McPherson <dmcphers@redhat.com> 0.73.12-1
- cleanup client messages (dmcphers@redhat.com)
- fix typo causing build break (dmcphers@redhat.com)
- add dyn retries (dmcphers@redhat.com)
- moving debug line so it produces output (mmcgrath@redhat.com)

* Fri Jul 01 2011 Emily Dirsh <edirsh@redhat.com> 0.73.11-1
- consistent names (dmcphers@redhat.com)
- Hide the "type" logic (jimjag@redhat.com)

* Fri Jul 01 2011 Dan McPherson <dmcphers@redhat.com> 0.73.10-1
- fixup embedded cart remove (dmcphers@redhat.com)

* Thu Jun 30 2011 Dan McPherson <dmcphers@redhat.com> 0.73.9-1
- wrong message for invalid cart type (dmcphers@redhat.com)

* Thu Jun 30 2011 Dan McPherson <dmcphers@redhat.com> 0.73.8-1
- cleanup (dmcphers@redhat.com)
- perf improvements for how/when we look up the valid cart types on the server
  (dmcphers@redhat.com)
- Merge branch 'master' of ssh://git1.ops.rhcloud.com/srv/git/li
  (mmcgrath@redhat.com)
- fixing embedded call and adding debug (mmcgrath@redhat.com)
- handle nil output (dmcphers@redhat.com)

* Thu Jun 30 2011 Dan McPherson <dmcphers@redhat.com> 0.73.7-1
- fix error message when havent requested access yet (dmcphers@redhat.com)
- sso support for broker (dmcphers@redhat.com)
- cleanup unused vars (dmcphers@redhat.com)

* Wed Jun 29 2011 Dan McPherson <dmcphers@redhat.com> 0.73.6-1
- undo passing rhlogin to cart (dmcphers@redhat.com)
- Merge branch 'master' of ssh://git1.ops.rhcloud.com/srv/git/li
  (mmcgrath@redhat.com)
- add nurture call for git push (dmcphers@redhat.com)
- Added mysql (mmcgrath@redhat.com)
- Correcting framework operations (mmcgrath@redhat.com)
- fixing merge from Dan (mmcgrath@redhat.com)
- proper error handling for embedded cases (mmcgrath@redhat.com)
- share common code (dmcphers@redhat.com)
- better message on app exists (dmcphers@redhat.com)
- Added initial S3 bits (mmcgrath@redhat.com)

* Wed Jun 29 2011 Dan McPherson <dmcphers@redhat.com> 0.73.5-1
- share code (dmcphers@redhat.com)

* Tue Jun 28 2011 Matt Hicks <mhicks@redhat.com> 0.73.4-1
- allow messsages from cart to client (dmcphers@redhat.com)
- Added support to call embedded cartridges (mmcgrath@redhat.com)
- Added embedded list (mmcgrath@redhat.com)

* Mon Jun 27 2011 Dan McPherson <dmcphers@redhat.com> 0.73.3-1
- set default apps to 5 (mmcgrath@redhat.com)

* Mon Jun 27 2011 Dan McPherson <dmcphers@redhat.com> 0.73.2-1
- 

* Mon Jun 27 2011 Dan McPherson <dmcphers@redhat.com> 0.73.1-1
- Merge branch 'master' of ssh://git1.ops.rhcloud.com/srv/git/li
  (jimjag@redhat.com)
- bump spec numbers (dmcphers@redhat.com)
- User.servers not used... clean up factor customer_* and git_cnt_* (US554)
  (jimjag@redhat.com)
- change how we would get email address (dmcphers@redhat.com)
- better message when running create app before create domain
  (dmcphers@redhat.com)

* Wed Jun 22 2011 Dan McPherson <dmcphers@redhat.com> 0.72.18-1
- changing require back to right_http_connection (dmcphers@redhat.com)

* Wed Jun 22 2011 Dan McPherson <dmcphers@redhat.com> 0.72.17-1
- right_http_connection -> http_connection (dmcphers@redhat.com)

* Sat Jun 18 2011 Dan McPherson <dmcphers@redhat.com> 0.72.16-1
- nurture updates, namespace + action (dmcphers@redhat.com)

* Fri Jun 17 2011 Dan McPherson <dmcphers@redhat.com> 0.72.15-1
- get tests running again (dmcphers@redhat.com)

* Thu Jun 16 2011 Matt Hicks <mhicks@redhat.com> 0.72.14-1
- Merge branch 'master' into streamline (mhicks@redhat.com)
- Gracefully handling Rails dep (mhicks@redhat.com)
- Refactoring the streamline modules (mhicks@redhat.com)

* Thu Jun 16 2011 Matt Hicks <mhicks@redhat.com> 0.72.13-1
- add error if invalid cart sent to server (dmcphers@redhat.com)

* Tue Jun 14 2011 Matt Hicks <mhicks@redhat.com> 0.72.12-1
- rename to make more sense... (jimjag@redhat.com)
- minor fixes (dmcphers@redhat.com)
- minor fixes (dmcphers@redhat.com)
- Force list to be a string... xfer to array when conv (jimjag@redhat.com)
- cart_list factor returns a string now, with cartridges sep by '|'
  (jimjag@redhat.com)
- /usr/lib/ruby/site_ruby/1.8/facter/libra.rb:86:in `+': can't convert String
  into Array (TypeError) (jimjag@redhat.com)
- Force check each time (jimjag@redhat.com)
- Don't use '<<' (which should work) (jimjag@redhat.com)
- nil is an error... but no idea how we are getting it (at the worst, we should
  get an empty list) (jimjag@redhat.com)
- force usage of blacklist (jimjag@redhat.com)
- revert... I am stumped. (jimjag@redhat.com)
- force usage of dummy arg (jimjag@redhat.com)
- simple name change (jimjag@redhat.com)
- until (jimjag@redhat.com)
- use class (jimjag@redhat.com)
- weird... why can't the server find this? (jimjag@redhat.com)
- 'self.get_cartridges' not found?? (jimjag@redhat.com)
- Adjust for permissions (jimjag@redhat.com)
- debug devenv (jimjag@redhat.com)
- Init to nil (jimjag@redhat.com)

* Fri Jun 10 2011 Matt Hicks <mhicks@redhat.com> 0.72.11-1
- Move along to more dynamic using :carts factor (jimjag@redhat.com)

* Thu Jun 09 2011 Matt Hicks <mhicks@redhat.com> 0.72.10-1
- fixup minor issues with refactor plus debugging (dmcphers@redhat.com)
- refactored logic of Libra.execute for clarity (markllama@redhat.com)

* Wed Jun 08 2011 Matt Hicks <mhicks@redhat.com> 0.72.9-1
- move migration to separate file (dmcphers@redhat.com)

* Wed Jun 08 2011 Dan McPherson <dmcphers@redhat.com> 0.72.8-1
- moved account and S3 record delete to the right places in Libra.execute
  (markllama@redhat.com)
- added a server method to delete and account, and call it when deleting an app
  (markllama@redhat.com)
- migration progress (dmcphers@redhat.com)

* Mon Jun 06 2011 Dan McPherson <dmcphers@redhat.com> 0.72.7-1
- 

* Mon Jun 06 2011 Dan McPherson <dmcphers@redhat.com> 0.72.6-1
- move client.cfg update to the right place (dmcphers@redhat.com)

* Mon Jun 06 2011 Dan McPherson <dmcphers@redhat.com> 0.72.5-1
- build fixes (dmcphers@redhat.com)
- Bug 706329 (dmcphers@redhat.com)

* Fri Jun 03 2011 Matt Hicks <mhicks@redhat.com> 0.72.4-1
- using app_uuid instead of user uuid, making user_uuid more obvious
  (mmcgrath@redhat.com)
- remove redirects on login to broker thx to streamline change
  (dmcphers@redhat.com)
- migration updates (dmcphers@redhat.com)
- controller.conf install fixup (dmcphers@redhat.com)
- remove to_sym from appname (dmcphers@redhat.com)

* Wed Jun 01 2011 Dan McPherson <dmcphers@redhat.com> 0.72.3-1
- app-uuid patch from dev/markllama/app-uuid
  69b077104e3227a73cbf101def9279fe1131025e (markllama@gmail.com)

* Tue May 31 2011 Matt Hicks <mhicks@redhat.com> 0.72.2-1
- Bug 707108 (dmcphers@redhat.com)
- get site and broker working on restructure (dmcphers@redhat.com)

* Wed May 25 2011 Matt Hicks <mhicks@redhat.com> 0.72.1-3
- Fixing ruby build requirement

* Wed May 25 2011 Matt Hicks <mhicks@redhat.com> 0.72.1-2
- Fixing ruby version

* Wed May 25 2011 Matt Hicks <mhicks@redhat.com> 0.72.1-1
- Initial refactoring
