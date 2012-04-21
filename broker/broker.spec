%define htmldir %{_localstatedir}/www/html
%define brokerdir %{_localstatedir}/www/stickshift/broker

Summary:   Li broker components
Name:      rhc-broker
Version:   0.91.8
Release:   1%{?dist}
Group:     Network/Daemons
License:   GPLv2
URL:       http://openshift.redhat.com
Source0:   rhc-broker-%{version}.tar.gz

BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
Requires:  rhc-server-common
Requires:  httpd
Requires:  mod_ssl
Requires:  mod_passenger
Requires:  rubygem-json
Requires:  rubygem-parseconfig
Requires:  rubygem-passenger-native-libs
Requires:  rubygem-rails
Requires:  rubygem-xml-simple
Requires:  rubygem-stickshift-controller
Requires:  rubygem-bson_ext
Requires:  rubygem-rest-client
Requires:  rubygem-thread-dump
Requires:  rubygem-swingshift-streamline-plugin
Requires:  rubygem-uplift-dynect-plugin
Requires:  rubygem-gearchanger-m-collective-plugin
Requires:  rubygem-crankcase-mongo-plugin
#Requires:  rubygem-term-ansicolor
#Requires:  rubygem-trollop
#Requires:  rubygem-cucumber
#Requires:  rubygem-gherkin
Requires:  rubygem(ruby-prof)
Requires:  rubygem-ruby-prof


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
cp -r . %{buildroot}%{brokerdir}
ln -s %{brokerdir}/public %{buildroot}%{htmldir}/broker

mkdir -p %{buildroot}%{brokerdir}/run
mkdir -p %{buildroot}%{brokerdir}/log
touch %{buildroot}%{brokerdir}/log/production.log
mv %{buildroot}%{brokerdir}/script/rhc-admin-ctl-domain %{buildroot}/%{_bindir}
mv %{buildroot}%{brokerdir}/script/rhc-admin-ctl-app %{buildroot}/%{_bindir}
mv %{buildroot}%{brokerdir}/script/rhc-admin-cartridge-do %{buildroot}/%{_bindir}
mv %{buildroot}%{brokerdir}/script/rhc-admin-move %{buildroot}/%{_bindir}
mv %{buildroot}%{brokerdir}/script/rhc-admin-ctl-district %{buildroot}/%{_bindir}
mv %{buildroot}%{brokerdir}/script/rhc-admin-ctl-template %{buildroot}/%{_bindir}
mv %{buildroot}%{brokerdir}/script/rhc-admin-user-vip %{buildroot}/%{_bindir}
mv %{buildroot}%{brokerdir}/script/rhc-admin-ctl-user %{buildroot}/%{_bindir}
mv %{buildroot}%{brokerdir}/script/rhc-admin-chk %{buildroot}/%{_bindir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(0640,root,libra_user,0750)
%attr(0666,-,-) %{brokerdir}/log/production.log
%config(noreplace) %{brokerdir}/config/environments/production.rb
%config(noreplace) %{brokerdir}/config/keys/public.pem
%config(noreplace) %{brokerdir}/config/keys/private.pem
%attr(0600,-,-) %config(noreplace) %{brokerdir}/config/keys/rsync_id_rsa
%config(noreplace) %{brokerdir}/config/keys/rsync_id_rsa.pub
%attr(0750,-,-) %{brokerdir}/config/keys/generate_rsa_keys
%attr(0750,-,-) %{brokerdir}/config/keys/generate_rsync_rsa_keys
%attr(0750,-,-) %{brokerdir}/script
%{brokerdir}
%{htmldir}/broker
%attr(0750,-,-) %{_bindir}/rhc-admin-ctl-domain
%attr(0750,-,-) %{_bindir}/rhc-admin-chk
%attr(0750,-,-) %{_bindir}/rhc-admin-ctl-app
%attr(0750,-,-) %{_bindir}/rhc-admin-cartridge-do
%attr(0750,-,-) %{_bindir}/rhc-admin-move
%attr(0750,-,-) %{_bindir}/rhc-admin-ctl-district
%attr(0750,-,-) %{_bindir}/rhc-admin-ctl-template
%attr(0750,-,-) %{_bindir}/rhc-admin-user-vip
%attr(0750,-,-) %{_bindir}/rhc-admin-ctl-user

%post
/bin/touch %{brokerdir}/log/production.log

%changelog
* Sat Apr 21 2012 Dan McPherson <dmcphers@redhat.com> 0.91.8-1
- Updating gem versions (dmcphers@redhat.com)
- Updating gem versions (dmcphers@redhat.com)
- Add profiler to test rails configuration. (rmillner@redhat.com)
- Also scrub out http auth header from REST calls. (rmillner@redhat.com)
- Clean up the info output.  Gzip the output files since they are huge.
  (rmillner@redhat.com)
- We only have perms to write into /tmp.  Still had a reference to outfile.
  (rmillner@redhat.com)
- Add info file with request and timestamp information. (rmillner@redhat.com)

* Wed Apr 18 2012 Dan McPherson <dmcphers@redhat.com> 0.91.7-1
- fixing controller Gemfile.lock in build/release (admiller@redhat.com)

* Wed Apr 18 2012 Adam Miller <admiller@redhat.com> 0.91.6-1
- 1) removing cucumber gem dependency from express broker. 2) moved ruby
  related cucumber tests back into express. 3) fixed issue with broker
  Gemfile.lock file where ruby-prof was not specified in the dependency
  section. 4) copying cucumber features into li-test/tests automatically within
  the devenv script. 5) fixing ctl status script that used ps to list running
  processes to specify the user. 6) fixed tidy.sh script to not display error
  on fedora stickshift. (abhgupta@redhat.com)
- rhc-admin-ctl-user: added ability to set vip status (twiest@redhat.com)
- rhc-admin-ctl-user: updated to be able to set consumed gears as well.
  (twiest@redhat.com)
- typos (rmillner@redhat.com)
- Clean up some of the help text. (rmillner@redhat.com)
- Had to move profiler to ActionController::Base (rmillner@redhat.com)
- Add range to runtime squash (rmillner@redhat.com)
- Add measurement type to file name. (rmillner@redhat.com)
- Add measurement type and description in config (rmillner@redhat.com)
- It seems like most of our threads come in during processing.  Delete them
  after the fact from the report. (rmillner@redhat.com)
- Just print the thread IDs (rmillner@redhat.com)
- Add log for thread handling.  Fix config entry. (rmillner@redhat.com)
- Dont pack nils into the exclude_threads array. (rmillner@redhat.com)
- Clean up methods. Add thread squash. Pass whole cfg to printer.
  (rmillner@redhat.com)
- Profiler moved into the app controller. (rmillner@redhat.com)
- Move profiling into the controller filter. (rmillner@redhat.com)
- Used the wrong variable (rmillner@redhat.com)
- Variable was being defined lower in the code. (rmillner@redhat.com)
- Use double quotes for var expansion (rmillner@redhat.com)
- Catch nomethod in case theres no profiler config. (rmillner@redhat.com)
- Add debug logging to the profiler calls (rmillner@redhat.com)
- Add an instance of the profiler to the broker startup (rmillner@redhat.com)
- The rubygem(foo) dependency is missing from ruby-prof. (rmillner@redhat.com)
- changed configuration block for profiler. (rmillner@redhat.com)
- Add observer for profiling of specific events. (rmillner@redhat.com)
- Merge branch 'master' of ssh://git1.ops.rhcloud.com/srv/git/li
  (rchopra@redhat.com)
- admin chk script to check mismatch between consumed_gears and actual gears
  for each user (rchopra@redhat.com)

* Thu Apr 12 2012 Mike McGrath <mmcgrath@redhat.com> 0.91.5-1
- release bump for mongo (mmcgrath@redhat.com)

* Thu Apr 12 2012 Mike McGrath <mmcgrath@redhat.com> 0.91.4-1
- test commit (mmcgrath@redhat.com)

* Thu Apr 12 2012 Mike McGrath <mmcgrath@redhat.com> 0.91.3-1
- gemfile bumps (mmcgrath@redhat.com)

* Thu Apr 12 2012 Mike McGrath <mmcgrath@redhat.com> 0.91.2-1
- Updating gem versions (mmcgrath@redhat.com)
- release bump for tag uniqueness (mmcgrath@redhat.com)

* Thu Apr 12 2012 Mike McGrath <mmcgrath@redhat.com> 0.90.21-1
- Updating gem versions (mmcgrath@redhat.com)
- added additional required rubygems (mmcgrath@redhat.com)
- added rubygem-term-ansicolor dep (mmcgrath@redhat.com)

* Wed Apr 11 2012 Adam Miller <admiller@redhat.com> 0.90.20-1
- Merge branch 'master' of ssh://git1.ops.rhcloud.com/srv/git/li
  (mmcgrath@redhat.com)
- test commit (mmcgrath@redhat.com)

* Wed Apr 11 2012 Adam Miller <admiller@redhat.com> 0.90.19-1
- fixing gemfile.lock (mmcgrath@redhat.com)

* Wed Apr 11 2012 Adam Miller <admiller@redhat.com> 0.90.18-1
- Updating gem versions (admiller@redhat.com)

* Tue Apr 10 2012 Mike McGrath <mmcgrath@redhat.com> 0.90.17-1
- Updating gem versions (mmcgrath@redhat.com)

* Tue Apr 10 2012 Mike McGrath <mmcgrath@redhat.com> 0.90.16-1
- removed test commits (mmcgrath@redhat.com)

* Tue Apr 10 2012 Mike McGrath <mmcgrath@redhat.com> 0.90.15-1
- Test commit (mmcgrath@redhat.com)

* Tue Apr 10 2012 Mike McGrath <mmcgrath@redhat.com> 0.90.14-1
- 

* Tue Apr 10 2012 Mike McGrath <mmcgrath@redhat.com> 0.90.13-1
- test commits (mmcgrath@redhat.com)

* Tue Apr 10 2012 Adam Miller <admiller@redhat.com> 0.90.12-1
- Updating gem versions (admiller@redhat.com)

* Tue Apr 10 2012 Adam Miller <admiller@redhat.com> 0.90.11-1
- Updating gem versions (admiller@redhat.com)
- Updating gem versions (admiller@redhat.com)

* Tue Apr 10 2012 Mike McGrath <mmcgrath@redhat.com> 0.90.10-1
- updating gemfile.lock (mmcgrath@redhat.com)

* Tue Apr 10 2012 Mike McGrath <mmcgrath@redhat.com> 0.90.9-1
- Updating gem versions (mmcgrath@redhat.com)

* Tue Apr 10 2012 Mike McGrath <mmcgrath@redhat.com> 0.90.8-1
- Updating gem versions (mmcgrath@redhat.com)

* Tue Apr 10 2012 Mike McGrath <mmcgrath@redhat.com> 0.90.7-1
- Updating gem versions (mmcgrath@redhat.com)

* Mon Apr 09 2012 Mike McGrath <mmcgrath@redhat.com> 0.90.6-1
- Updating gem versions (mmcgrath@redhat.com)
- Updating gem versions (kraman@gmail.com)

* Mon Apr 09 2012 Mike McGrath <mmcgrath@redhat.com> 0.90.5-1
- Updating gem versions (mmcgrath@redhat.com)
- cleaning up location of datatstore configuration (kraman@gmail.com)
- Updating gemfile.lock (kraman@gmail.com)
- Merge remote-tracking branch 'origin/master' into dev/kraman/US2048
  (kraman@gmail.com)
- Bunping gem version in Gemfile.lock Fix rename issue in application container
  proxy (kraman@gmail.com)
- moving bulk of the cucumber tests under stickshift and making changes so that
  tests can be run both on devenv with express  as well as with opensource
  pieces on the fedora image (abhgupta@redhat.com)
- Merge remote-tracking branch 'origin/master' (kraman@gmail.com)
- Merge remote-tracking branch 'origin/master' (kraman@gmail.com)
- Bug fixes after initial merge of OSS packages (kraman@gmail.com)
- Automatic commit of package [rhc-broker] release [0.90.2-1].
  (kraman@gmail.com)
- Updating dependencies to match new package names (kraman@gmail.com)
- Merge remote-tracking branch 'origin/dev/kraman/US2048' (kraman@gmail.com)
- Adding m-collective and oddjob gearchanger plugins (kraman@gmail.com)
- Added mongo and streamline swingshift plugins (kraman@gmail.com)
- Creating dynect plugin (kraman@gmail.com)

* Wed Apr 04 2012 Mike McGrath <mmcgrath@redhat.com> 0.90.4-1
- Updating gem versions (mmcgrath@redhat.com)

* Wed Apr 04 2012 Mike McGrath <mmcgrath@redhat.com> 0.90.3-1
- test commit (mmcgrath@redhat.com)

* Tue Apr 03 2012 Mike McGrath <mmcgrath@redhat.com> 0.90.2-1
- Updating gem versions (mmcgrath@redhat.com)
- custom request does not take multiple nodes very well, fix for bug#806375
  (rchopra@redhat.com)
- added rhc-admin-ctl-user (twiest@redhat.com)

* Mon Apr 02 2012 Krishna Raman <kraman@gmail.com> 0.90.2-1
- Updating dependencies to match new package names (kraman@gmail.com)
- Merge remote-tracking branch 'origin/dev/kraman/US2048' (kraman@gmail.com)
- added rhc-admin-ctl-user (twiest@redhat.com)
- Adding m-collective and oddjob gearchanger plugins (kraman@gmail.com)
- Added mongo and streamline swingshift plugins (kraman@gmail.com)
- Creating dynect plugin (kraman@gmail.com)

* Sat Mar 31 2012 Dan McPherson <dmcphers@redhat.com> 0.90.1-1
- Updating gem versions (dmcphers@redhat.com)
- bump spec numbers (dmcphers@redhat.com)

* Fri Mar 30 2012 Dan McPherson <dmcphers@redhat.com> 0.89.8-1
- Bug 807568 (dmcphers@redhat.com)

* Thu Mar 29 2012 Dan McPherson <dmcphers@redhat.com> 0.89.7-1
- Updating gem versions (dmcphers@redhat.com)

* Wed Mar 28 2012 Dan McPherson <dmcphers@redhat.com> 0.89.6-1
- Updating gem versions (dmcphers@redhat.com)

* Wed Mar 28 2012 Dan McPherson <dmcphers@redhat.com> 0.89.5-1
- Updating gem versions (dmcphers@redhat.com)
- cosmetics in debug statement; fix for broken cartridge configure not getting
  a deconfigure but two destroys instead (rchopra@redhat.com)
- Bug 807654 (dmcphers@redhat.com)

* Tue Mar 27 2012 Dan McPherson <dmcphers@redhat.com> 0.89.4-1
- Updating gem versions (dmcphers@redhat.com)
- fixed refs to user.namespace (lnader@redhat.com)
- change default max gears to 3 (dmcphers@redhat.com)
- BugzID 806298 (kraman@gmail.com)

* Mon Mar 26 2012 Dan McPherson <dmcphers@redhat.com> 0.89.3-1
- Updating gem versions (dmcphers@redhat.com)

* Mon Mar 26 2012 Dan McPherson <dmcphers@redhat.com> 0.89.2-1
- Updating gem versions (dmcphers@redhat.com)
- 806473 (dmcphers@redhat.com)
- Merge branch 'master' of git1.ops.rhcloud.com:/srv/git/li (lnader@redhat.com)
- parallelize mcollective calls for parallel jobs (dmcphers@redhat.com)
- Merge branch 'master' of git1.ops.rhcloud.com:/srv/git/li (lnader@redhat.com)
- Merge branch 'compass', removed conflicting JS file (ccoleman@redhat.com)
- Broker and site in devenv should use RackBaseURI and be relative to content
  Remove broker/site app_scope (ccoleman@redhat.com)
- merged conflicts with master (lnader@redhat.com)
- group mcollective calls (dmcphers@redhat.com)
- Merge branch 'master' of git1.ops.rhcloud.com:/srv/git/li (lnader@redhat.com)
- US1876 (lnader@redhat.com)
- Fix for bug# 804029 (rpenta@redhat.com)
- Update stickshift gemfiles to new rack versions, remove multimap which is no
  longer required by rack (versions before .7 had a dependency, it has since
  been inlined) (ccoleman@redhat.com)
- Merge branch 'rack' (ccoleman@redhat.com)
- code cleanup checkpoint for US2091. scalable apps may not work right now.
  (rchopra@redhat.com)
- Update rack dependencies (ccoleman@redhat.com)
- Update rack to 1.3 (ccoleman@redhat.com)
- keep around OPENSHIFT_APP_DNS (dmcphers@redhat.com)

* Sat Mar 17 2012 Dan McPherson <dmcphers@redhat.com> 0.89.1-1
- Updating gem versions (dmcphers@redhat.com)
- bump spec numbers (dmcphers@redhat.com)

* Thu Mar 15 2012 Dan McPherson <dmcphers@redhat.com> 0.88.8-1
- Updating gem versions (dmcphers@redhat.com)

* Wed Mar 14 2012 Dan McPherson <dmcphers@redhat.com> 0.88.7-1
- Updating gem versions (dmcphers@redhat.com)

* Wed Mar 14 2012 Dan McPherson <dmcphers@redhat.com> 0.88.6-1
- Updating gem versions (dmcphers@redhat.com)
- Merge branch 'master' of git1.ops.rhcloud.com:/srv/git/li (rpenta@redhat.com)
- Fix for bug# 800095 (rpenta@redhat.com)

* Tue Mar 13 2012 Dan McPherson <dmcphers@redhat.com> 0.88.5-1
- Updating gem versions (dmcphers@redhat.com)
- make sure remove httpd proxy gets run on move failure (dmcphers@redhat.com)
- move error handling messaging (dmcphers@redhat.com)
- give a better retry success message on move (dmcphers@redhat.com)

* Mon Mar 12 2012 Dan McPherson <dmcphers@redhat.com> 0.88.4-1
- Updating gem versions (dmcphers@redhat.com)
- merging admin scripts to add/remove template into a single control script
  (abhgupta@redhat.com)
- fix for case when server_identity changes; switch to flip mcollective
  optimizations on/off (rchopra@redhat.com)
- spec file fix so that rhc-admin-chk is available in bin (rchopra@redhat.com)

* Sat Mar 10 2012 Dan McPherson <dmcphers@redhat.com> 0.88.3-1
- Updating gem versions (dmcphers@redhat.com)
- rhc-admin-chk (rchopra@redhat.com)
- checkpoint - rhc-admin-chk script - incomplete (rchopra@redhat.com)
- Fixing a couple of missed Cloud::Sdk references (kraman@gmail.com)

* Fri Mar 09 2012 Dan McPherson <dmcphers@redhat.com> 0.88.2-1
- Updating gem versions (dmcphers@redhat.com)
- Merge branch 'master' of ssh://git1.ops.rhcloud.com/srv/git/li
  (rchopra@redhat.com)
- Updating gem versions (dmcphers@redhat.com)
- finally ...iv/token working (rchopra@redhat.com)
- Fix factor code to read node config properly Fix rhc-admin-add-template to
  store yaml for descriptor (kraman@gmail.com)
- Making access to mongo config info consistent across broker and controller
  (kraman@gmail.com)
- Updating tests (kraman@gmail.com)
- Updates for getting devenv running (kraman@gmail.com)
- Changes to MongoDatastore: - Enabled creation of new mongodb instances with
  different config parameters. - Re-organized mongo rails configuration
  (rpenta@redhat.com)
- Renaming Cloud-SDK -> StickShift (kraman@gmail.com)
- missed a help message on the new gear sizes (rmillner@redhat.com)
- Add new env var *_USER_APP_NAME (need to rename this once the *_APP_NAME is
  switched over to *_GEAR_NAME). (ramr@redhat.com)
- Merge branch 'master' of li-master:/srv/git/li (ramr@redhat.com)
- checkpoint 3 - mcollective parallelized calls working - not integrated yet
  (rchopra@redhat.com)
- Increase timeouts to 60 secs. (ramr@redhat.com)
- Broker defaults to small gear size (rmillner@redhat.com)
- Fixed rhc-admin-add-template to properly parse YAML and JSON files
  (fotios@redhat.com)
- checkpoint 2 - parallel execution over mcollective - not integrated yet
  (rchopra@redhat.com)
- checkpoint - half the setup for parallel mcollective calls - not integrated
  (rchopra@redhat.com)
- fix issue with move changing nodes half way through (dmcphers@redhat.com)
- fix a couple comments (dmcphers@redhat.com)
- remove double URL encoding (lnader@redhat.com)

* Fri Mar 02 2012 Dan McPherson <dmcphers@redhat.com> 0.88.1-1
- Updating gem versions (dmcphers@redhat.com)
- bump spec numbers (dmcphers@redhat.com)
- fail if you dont get a result from rpc_exec (dmcphers@redhat.com)
- make help pages fast on admin tools and sync output from migrate
  (dmcphers@redhat.com)
- rolling back changes for raising exceptions when component is not found on
  gear (rchopra@redhat.com)
- do not consider deconfigure benign if a component is not found on the node
  (rchopra@redhat.com)

* Thu Mar 01 2012 Dan McPherson <dmcphers@redhat.com> 0.87.11-1
- Adding admin script to set user VIP status (kraman@gmail.com)

* Wed Feb 29 2012 Dan McPherson <dmcphers@redhat.com> 0.87.10-1
- Updating gem versions (dmcphers@redhat.com)

* Tue Feb 28 2012 Dan McPherson <dmcphers@redhat.com> 0.87.9-1
- Updating gem versions (dmcphers@redhat.com)
- Fix for Bugz 798256 Consolidating user lookup (kraman@gmail.com)
- dont pre/post move for same uid (dmcphers@redhat.com)

* Mon Feb 27 2012 Dan McPherson <dmcphers@redhat.com> 0.87.8-1
- Updating gem versions (dmcphers@redhat.com)

* Mon Feb 27 2012 Dan McPherson <dmcphers@redhat.com> 0.87.7-1
- 

* Mon Feb 27 2012 Dan McPherson <dmcphers@redhat.com> 0.87.6-1
- Updating gem versions (dmcphers@redhat.com)
- Merge branch 'master' of git1.ops.rhcloud.com:/srv/git/li (rpenta@redhat.com)
- gear info REST api call fix (rpenta@redhat.com)

* Mon Feb 27 2012 Dan McPherson <dmcphers@redhat.com> 0.87.5-1
- Updating gem versions (dmcphers@redhat.com)
- BugzID# 797098, 796088. Application validation (kraman@gmail.com)
- Adding config for template collection to all environments (kraman@gmail.com)
- Bigfix. App creation was failing for non vip users. (kraman@gmail.com)
- US1908: Allow only vip users to create gears that are larger than medium
  (std) (kraman@gmail.com)

* Sat Feb 25 2012 Dan McPherson <dmcphers@redhat.com> 0.87.4-1
- Updating gem versions (dmcphers@redhat.com)
- get rid of debug log messages in libra_check (lnader@redhat.com)
- adding back Gemfile.lock assuming it was deleted by accident
  (dmcphers@redhat.com)
- Temporary commit to build (ffranz@redhat.com)
- Update cartridge configure hooks to load git repo from remote URL Add REST
  API to create application from template Moved application template
  models/controller to cloud-sdk (kraman@gmail.com)
- Merge branch 'master' of git1.ops.rhcloud.com:/srv/git/li (rpenta@redhat.com)
- bind dns service bug fixes and cleanup (rpenta@redhat.com)
- fix validate args for mcollective calls as we are sending json strings over
  now (rchopra@redhat.com)
- jsonify connector output from multiple gears for consumption by subscriber
  connectors (rchopra@redhat.com)

* Wed Feb 22 2012 Dan McPherson <dmcphers@redhat.com> 0.87.3-1
- Updating gem versions (dmcphers@redhat.com)
- trying to fix the build... continued (dmcphers@redhat.com)
- fixing gemfile.lock for open4/dnsruby dependencies (rchopra@redhat.com)
- Merge branch 'master' of ssh://git1.ops.rhcloud.com/srv/git/li
  (rchopra@redhat.com)
- checkpoint 3 - horizontal scaling, minor fixes, connector hook for haproxy
  not complete (rchopra@redhat.com)
- Adding template management tests (kraman@gmail.com)
- Merge branch 'master' of ssh://git1.ops.rhcloud.com/srv/git/li
  (rchopra@redhat.com)
- Add show-proxy call. (rmillner@redhat.com)
- Adding admin scripts to manage templates Adding REST API for creatig
  applications given a template GUID (kraman@gmail.com)
- checkpoint 2 - option to create scalable type of app, scaleup/scaledown apis
  added, group minimum requirements get fulfilled (rchopra@redhat.com)
- Merge branch 'master' of ssh://git1.ops.rhcloud.com/srv/git/li
  (rchopra@redhat.com)
- checkpoint 1 - horizontal scaling broker support (rchopra@redhat.com)
- Adding admin scripts to manage templates (kraman@gmail.com)
- Added ability to list and retrieve application template data
  (kraman@gmail.com)

* Mon Feb 20 2012 Dan McPherson <dmcphers@redhat.com> 0.87.2-1
- Updating gem versions (dmcphers@redhat.com)
- Revert "Updating gem versions" (ramr@redhat.com)
- Updating gem versions (ramr@redhat.com)

* Thu Feb 16 2012 Dan McPherson <dmcphers@redhat.com> 0.87.1-1
- Updating gem versions (dmcphers@redhat.com)
- bump spec numbers (dmcphers@redhat.com)

* Thu Feb 16 2012 Dan McPherson <dmcphers@redhat.com> 0.86.8-1
- Updating gem versions (dmcphers@redhat.com)

* Wed Feb 15 2012 Dan McPherson <dmcphers@redhat.com> 0.86.7-1
- Updating gem versions (dmcphers@redhat.com)
- Bugzid# 789916 (kraman@gmail.com)

* Tue Feb 14 2012 Dan McPherson <dmcphers@redhat.com> 0.86.6-1
- Updating gem versions (dmcphers@redhat.com)

* Tue Feb 14 2012 Dan McPherson <dmcphers@redhat.com> 0.86.5-1
- Updating gem versions (dmcphers@redhat.com)
- add find_one capability (dmcphers@redhat.com)
- Supressing debug output for cartridge-list to make logs legible Turning on
  rails caching for streamline-aws configuration (kraman@gmail.com)
- try a different order with the embedded feature (dmcphers@redhat.com)
- cleaning up version reqs (dmcphers@redhat.com)

* Mon Feb 13 2012 Dan McPherson <dmcphers@redhat.com> 0.86.4-1
- Updating gem versions (dmcphers@redhat.com)
- share common move logic (dmcphers@redhat.com)
- Rolling back my changes to expose targetted proxy. Revert "Add calls to
  backend for proxy." (rmillner@redhat.com)

* Mon Feb 13 2012 Dan McPherson <dmcphers@redhat.com> 0.86.3-1
- Updating gem versions (dmcphers@redhat.com)
- cleaning up specs to force a build (dmcphers@redhat.com)
- add back capacity and restrict remove node to 0 capacity nodes
  (dmcphers@redhat.com)

* Sat Feb 11 2012 Dan McPherson <dmcphers@redhat.com> 0.86.2-1
- Updating gem versions (dmcphers@redhat.com)
- get move working again and add quota support (dmcphers@redhat.com)
- Add calls to backend for proxy. (rmillner@redhat.com)
- Fix broker auth service, bug# 787297 (rpenta@redhat.com)
- Minor fixes to export/conceal port functions (kraman@gmail.com)
- Bug 789225 (dmcphers@redhat.com)
- bug 722828 (wdecoste@localhost.localdomain)
- bug 722828 (wdecoste@localhost.localdomain)
- more move debug + test case simplifications (dmcphers@redhat.com)
- Fixing add/remove embedded cartridges Fixing domain info on legacy broker
  controller Fixing start/stop/etc app and cart. control calls for legacy
  broker (kraman@gmail.com)
- Update application_container_proxy to be able to distnguish between
  app,framework,embedded carts and perform config/start/etc hooks appropriately
  (kraman@gmail.com)
- Bug fixes for saving connection list Abstracting difference between
  framework/embedded cart in application_container_proxy and application
  (kraman@gmail.com)
- Renamed ApplicationContainer to Gear to avoid confusion Fixed gear
  creation/configuration/deconfiguration for framework cartridge Fixed
  save/load of group insatnce map Removed hacks where app was assuming one gear
  only Started changes to enable rollback if operation fails (kraman@gmail.com)
- Fixes for re-enabling cli tools. git url is not yet working.
  (kraman@gmail.com)
- Updated code to make it re-enterant. Adding/removing dependencies does not
  change location of dependencies that did not change.
  (rchopra@unused-32-159.sjc.redhat.com)
- Updating models to improove schems of descriptor in mongo Moved
  connection_endpoint to broker (kraman@gmail.com)
- Changes to re-enable app to be saved/retrieved to/from mongo Various bug
  fixes (kraman@gmail.com)
- Creating models for descriptor Fixing manifest files Added command to list
  installed cartridges and get descriptors (kraman@gmail.com)
- Merge branch 'master' into haproxy (mmcgrath@redhat.com)
- Adding expose-port and conceal-port (mmcgrath@redhat.com)
- change status to use normal client_result instead of special handling
  (dmcphers@redhat.com)
- add force stop to move (dmcphers@redhat.com)
- better messaging on move deconfigure failure (dmcphers@redhat.com)
- add warning about existing migration data (dmcphers@redhat.com)
- restrict ctl-district to allowed commands (dmcphers@redhat.com)
- Bug 787994 (dmcphers@redhat.com)
- move server_identities to array (dmcphers@redhat.com)
- make actions and cdk commands match (dmcphers@redhat.com)
- increase std and large gear restrictions (dmcphers@redhat.com)
- add app url lookup to move (dmcphers@redhat.com)
- always take the destination district uuid (dmcphers@redhat.com)
- keep apps stopped or idled on move (dmcphers@redhat.com)

* Fri Feb 03 2012 Dan McPherson <dmcphers@redhat.com> 0.86.1-1
- Updating gem versions (dmcphers@redhat.com)
- bump spec numbers (dmcphers@redhat.com)
- add move by uuid (dmcphers@redhat.com)
- Bug 786709 (dmcphers@redhat.com)
- fix comment (dmcphers@redhat.com)
- double url encode rhlogin for apptegic (lnader@dhcp-240-165.mad.redhat.com)
- Merge branch 'master' of ssh://git1.ops.rhcloud.com/srv/git/li
  (lnader@dhcp-240-165.mad.redhat.com)
- Removing specific version dependency for rest-client from gemfile
  (kraman@gmail.com)
- Removing specific version dependency for rest-client from gemfile
  (kraman@gmail.com)
- made changes to dns_service.rb so it can be imported and used outside rails
  (lnader@dhcp-240-165.mad.redhat.com)
