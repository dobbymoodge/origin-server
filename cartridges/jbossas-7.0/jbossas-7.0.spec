%define cartridgedir %{_libexecdir}/li/cartridges/jbossas-7.0

Summary:   Provides JBossAS7 support
Name:      rhc-cartridge-jbossas-7.0
Version:   0.78.2
Release:   1%{?dist}
Group:     Development/Languages
License:   GPLv2
URL:       http://openshift.redhat.com
Source0:   %{name}-%{version}.tar.gz

BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
BuildRequires:  git
BuildRequires:  java-devel >= 1:1.6.0 
BuildRequires:  jpackage-utils
Requires:  rhc-node
Requires: jboss-as7 = 7.0.1.Final
Requires:  maven3

BuildArch: noarch

%description
Provides JBossAS7 support to OpenShift

%prep
%setup -q

%build

#mkdir -p template/src/main/webapp/WEB-INF/classes
#pushd template/src/main/java > /dev/null
#/usr/bin/javac *.java -d ../webapp/WEB-INF/classes 
#popd

mkdir -p info/data
pushd template/src/main/webapp > /dev/null 
/usr/bin/jar -cvf ../../../../info/data/ROOT.war -C . .
popd

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{cartridgedir}
mkdir -p %{buildroot}/%{_sysconfdir}/libra/cartridges
ln -s %{cartridgedir}/info/configuration/ %{buildroot}/%{_sysconfdir}/libra/cartridges/%{name}
cp -r info %{buildroot}%{cartridgedir}/
cp -r template %{buildroot}%{cartridgedir}/
cp README %{buildroot}%{cartridgedir}/
ln -s %{cartridgedir}/../abstract-httpd/info/hooks/add-module %{buildroot}%{cartridgedir}/info/hooks/add-module
ln -s %{cartridgedir}/../abstract-httpd/info/hooks/info %{buildroot}%{cartridgedir}/info/hooks/info
ln -s %{cartridgedir}/../abstract-httpd/info/hooks/post-install %{buildroot}%{cartridgedir}/info/hooks/post-install
ln -s %{cartridgedir}/../abstract-httpd/info/hooks/post-remove %{buildroot}%{cartridgedir}/info/hooks/post-remove
ln -s %{cartridgedir}/../abstract-httpd/info/hooks/reload %{buildroot}%{cartridgedir}/info/hooks/reload
ln -s %{cartridgedir}/../abstract-httpd/info/hooks/remove-module %{buildroot}%{cartridgedir}/info/hooks/remove-module
ln -s %{cartridgedir}/../abstract-httpd/info/hooks/restart %{buildroot}%{cartridgedir}/info/hooks/restart
ln -s %{cartridgedir}/../abstract-httpd/info/hooks/start %{buildroot}%{cartridgedir}/info/hooks/start
ln -s %{cartridgedir}/../abstract-httpd/info/hooks/stop %{buildroot}%{cartridgedir}/info/hooks/stop
ln -s %{cartridgedir}/../abstract-httpd/info/hooks/update_namespace %{buildroot}%{cartridgedir}/info/hooks/update_namespace

%post
#maven
alternatives --install /etc/alternatives/maven-3.0 maven-3.0 /usr/share/java/apache-maven-3.0.3 100


%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%attr(0750,-,-) %{cartridgedir}/info/hooks/
%attr(0640,-,-) %{cartridgedir}/info/data/
%attr(0755,-,-) %{cartridgedir}/info/bin/
%{cartridgedir}/template/
%config(noreplace) %{cartridgedir}/info/configuration/
%{_sysconfdir}/libra/cartridges/%{name}
%{cartridgedir}/info/changelog
%{cartridgedir}/info/control
%{cartridgedir}/README

%changelog
* Fri Sep 09 2011 Matt Hicks <mhicks@redhat.com> 0.78.2-1
- Adding switchyard proxy pass setup in JBoss (mhicks@redhat.com)

* Thu Sep 01 2011 Dan McPherson <dmcphers@redhat.com> 0.78.1-1
- bump spec numbers (dmcphers@redhat.com)

* Tue Aug 30 2011 Dan McPherson <dmcphers@redhat.com> 0.77.6-1
- bugid=734380, remove stale links from the standalone/configuration dir
  (starksm64@gmail.com)

* Mon Aug 29 2011 Dan McPherson <dmcphers@redhat.com> 0.77.5-1
- update jboss version (dmcphers@redhat.com)

* Mon Aug 29 2011 Dan McPherson <dmcphers@redhat.com> 0.77.4-1
- Bug 734028 (dmcphers@redhat.com)

* Thu Aug 25 2011 Matt Hicks <mhicks@redhat.com> 0.77.3-1
- Fix some merge errors (starksm64@gmail.com)
- Merge branch 'master' of ssh://git1.ops.rhcloud.com/srv/git/li
  (starksm64@gmail.com)
- US495, US1013, add support for extending the server modules and allow users
  to add configuration directory content. (starksm64@gmail.com)

* Fri Aug 19 2011 Dan McPherson <dmcphers@redhat.com> 0.77.2-1
- fix internals tests (dmcphers@redhat.com)

* Fri Aug 19 2011 Matt Hicks <mhicks@redhat.com> 0.77.1-1
- bump spec numbers (dmcphers@redhat.com)
- splitting app_ctl.sh out (dmcphers@redhat.com)

* Wed Aug 17 2011 Matt Hicks <mhicks@redhat.com> 0.76.11-1
- Bugzilla 731238 (mhicks@redhat.com)

* Wed Aug 17 2011 Dan McPherson <dmcphers@redhat.com> 0.76.10-1
- use new env var (dmcphers@redhat.com)
- add app type and db type and migration restart (dmcphers@redhat.com)

* Tue Aug 16 2011 Dan McPherson <dmcphers@redhat.com> 0.76.9-1
- cleanup (dmcphers@redhat.com)

* Tue Aug 16 2011 Dan McPherson <dmcphers@redhat.com> 0.76.8-1
- redo the start/stop changes (dmcphers@redhat.com)
- only restore m2 when git is restored (dmcphers@redhat.com)
- split out post and pre receive from the apps (dmcphers@redhat.com)

* Tue Aug 16 2011 Matt Hicks <mhicks@redhat.com> 0.76.7-1
- JBoss cgroup and container tuning (mhicks@redhat.com)
- Merge branch 'master' of ssh://git1.ops.rhcloud.com/srv/git/li
  (mmcgrath@redhat.com)
- Fixing chcon to include git (mmcgrath@redhat.com)
- splitting out stop/start, changing snapshot to use stop start and bug 730890
  (dmcphers@redhat.com)
- Appending / to dir names (mmcgrath@redhat.com)
- ensuring /tmp ends with a / (mmcgrath@redhat.com)

* Mon Aug 15 2011 Dan McPherson <dmcphers@redhat.com> 0.76.6-1
- adding migration for snapshot/restore (dmcphers@redhat.com)
- snapshot and restore using path (dmcphers@redhat.com)

* Sun Aug 14 2011 Dan McPherson <dmcphers@redhat.com> 0.76.5-1
- get jboss working again (dmcphers@redhat.com)
- Added new scripted snapshot (mmcgrath@redhat.com)
- Adding custom snapshot (mmcgrath@redhat.com)
- reducing output for restore (mmcgrath@redhat.com)
- Added rhcsh, as well as _RESTORE functionality (mmcgrath@redhat.com)
- Adding additional output, also running pre and post hooks of git
  (mmcgrath@redhat.com)
- add source based samples to jboss index page (dmcphers@redhat.com)
- restore error handling (dmcphers@redhat.com)
- add stop deploy start to restore (dmcphers@redhat.com)
- functional restore (dmcphers@redhat.com)

* Fri Aug 12 2011 Matt Hicks <mhicks@redhat.com> 0.76.4-1
- remvove skip maven build keep (dmcphers@redhat.com)

* Thu Aug 11 2011 Matt Hicks <mhicks@redhat.com> 0.76.3-1
- bug729751, fix the failure return value of the ishttpup() function
  (starksm64@gmail.com)
- change default db name to app_name (dmcphers@redhat.com)

* Tue Aug 09 2011 Dan McPherson <dmcphers@redhat.com> 0.76.2-1
- Minor cleanup of echo statement (mhicks@redhat.com)

* Fri Aug 05 2011 Dan McPherson <dmcphers@redhat.com> 0.76.1-1
- bump spec numbers (dmcphers@redhat.com)

* Fri Aug 05 2011 Dan McPherson <dmcphers@redhat.com> 0.75.16-1
- 

* Fri Aug 05 2011 Dan McPherson <dmcphers@redhat.com> 0.75.15-1
- Adding DNS name for reference (mmcgrath@redhat.com)

* Wed Aug 03 2011 Dan McPherson <dmcphers@redhat.com> 0.75.14-1
- IE fixes (dmcphers@redhat.com)

* Tue Aug 02 2011 Dan McPherson <dmcphers@redhat.com> 0.75.13-1
- Update the README with the jboss-as7 brew rpm build info and steps, and add
  the mysql jdbc driver archive to the cartridge data. (starksm64@gmail.com)

* Sun Jul 31 2011 Dan McPherson <dmcphers@redhat.com> 0.75.12-1
- fix jboss version (dmcphers@redhat.com)

* Sun Jul 31 2011 Dan McPherson <dmcphers@redhat.com> 0.75.11-1
- Update to jboss-as-web-7.0.0.FinalOS to reduce the number of msc threads
  (scott.stark@jboss.org)
- remove maven repository when deconfiguring jboss (markllama@redhat.com)
- removed -x from jbossas configure script to reduce noise
  (markllama@redhat.com)

* Thu Jul 28 2011 Dan McPherson <dmcphers@redhat.com> 0.75.10-1
- logic rework (dmcphers@redhat.com)

* Thu Jul 28 2011 Dan McPherson <dmcphers@redhat.com> 0.75.9-1
- README update (dmcphers@redhat.com)

* Thu Jul 28 2011 Dan McPherson <dmcphers@redhat.com> 0.75.8-1
- adding skip build and markers (dmcphers@redhat.com)
- added some sample env variables (mmcgrath@redhat.com)
- removing restrictive permissions for the template" (mmcgrath@redhat.com)

* Tue Jul 26 2011 Dan McPherson <dmcphers@redhat.com> 0.75.7-1
- Adding README (mmcgrath@redhat.com)
- added build scripts to jboss, perl, rack and wsgi (mmcgrath@redhat.com)
- Merge branch 'master' of ssh://git1.ops.rhcloud.com/srv/git/li
  (mmcgrath@redhat.com)
- import environment variables as part of the git hooks (mmcgrath@redhat.com)

* Tue Jul 26 2011 Dan McPherson <dmcphers@redhat.com> 0.75.6-1
- Adding environment variables to jboss (mmcgrath@redhat.com)

* Mon Jul 25 2011 Dan McPherson <dmcphers@redhat.com> 0.75.5-1
- adding commented out dep to pom.xml (dmcphers@redhat.com)

* Fri Jul 22 2011 Dan McPherson <dmcphers@redhat.com> 0.75.4-1
- Bug 724026 (dmcphers@redhat.com)

* Thu Jul 21 2011 Dan McPherson <dmcphers@redhat.com> 0.75.3-1
- perms cleanup (dmcphers@redhat.com)

* Thu Jul 21 2011 Dan McPherson <dmcphers@redhat.com> 0.75.2-1
- move .config -> .openshift/config (dmcphers@redhat.com)

* Thu Jul 21 2011 Dan McPherson <dmcphers@redhat.com> 0.75.1-1
- pom improvements (dmcphers@redhat.com)
- bump spec numbers (dmcphers@redhat.com)
- add server identity and namespace auto migrate (dmcphers@redhat.com)
- half the jca workmanager thread counts (scott.stark@jboss.org)

* Mon Jul 18 2011 Dan McPherson <dmcphers@redhat.com> 0.74.8-1
- change default mysql ds db name (dmcphers@redhat.com)
- doc update (dmcphers@redhat.com)
- doc updates (dmcphers@redhat.com)
- doc updates (dmcphers@redhat.com)
- adding disabled mysql ds to jboss cart (dmcphers@redhat.com)
- adding standalone.xml to git repo (dmcphers@redhat.com)
- 722836 (dmcphers@redhat.com)
- Bug 720898, update the weld-translator ejb injection to work with jboss-as-
  web-7.0.0.Final (scott.stark@jboss.org)
- Update standalone.xml to be closer to the 7.0.0.Final version. Update default
  index.hmtl to refer to README for more deployment options.
  (scott.stark@jboss.org)

* Fri Jul 15 2011 Dan McPherson <dmcphers@redhat.com> 0.74.7-1
- Make the start action syncd with the caller (scott.stark@jboss.org)
- Bug 719800 instead of removing stop_lock, simply indicate the start is
  skipped due to lock (scott.stark@jboss.org)
- Bug 719800, remove stop_lock during git push (scott.stark@jboss.org)
- Merge branch 'master' of ssh://git1.ops.rhcloud.com/srv/git/li
  (scott.stark@jboss.org)
- Bug 720882 (dmcphers@redhat.com)
- Merge branch 'master' of ssh://git1.ops.rhcloud.com/srv/git/li
  (scott.stark@jboss.org)
- Bug 717552, Remove the lock file on restart (scott.stark@jboss.org)

* Wed Jul 13 2011 Dan McPherson <dmcphers@redhat.com> 0.74.6-1
- Merge branch 'master' of ssh://git1.ops.rhcloud.com/srv/git/li
  (scott.stark@jboss.org)
- Bug 720474 - Update jbossas server to be based on 7.0.0.GA with mysql jdbc
  driver (scott.stark@jboss.org)

* Wed Jul 13 2011 Dan McPherson <dmcphers@redhat.com> 0.74.5-1
- stop using fake tmp for maven build (dmcphers@redhat.com)

* Wed Jul 13 2011 Dan McPherson <dmcphers@redhat.com> 0.74.4-1
- Typo fix (mhicks@redhat.com)
- mvn env settings (dmcphers@redhat.com)

* Tue Jul 12 2011 Dan McPherson <dmcphers@redhat.com> 0.74.3-1
- jboss readme updates (dmcphers@redhat.com)

* Tue Jul 12 2011 Dan McPherson <dmcphers@redhat.com> 0.74.2-1
- seeding maven repository (dmcphers@redhat.com)
- Update DataSource name, bug 717187 (scott.stark@jboss.org)
- Automatic commit of package [rhc-cartridge-jbossas-7.0] release [0.74.1-1].
  (dmcphers@redhat.com)
- bumping spec numbers (dmcphers@redhat.com)
- move jboss template creation to instantiation (dmcphers@redhat.com)
- use maven war plugin rather than ant by default (dmcphers@redhat.com)
- Automatic commit of package [rhc-cartridge-jbossas-7.0] release [0.73.23-1].
  (dmcphers@redhat.com)
- adjust heap sizes (dmcphers@redhat.com)
- changing to lsof method (mmcgrath@redhat.com)
- Update MaxPermSize to 128m (scott.stark@jboss.org)
- Automatic commit of package [rhc-cartridge-jbossas-7.0] release [0.73.22-1].
  (dmcphers@redhat.com)
- doc updates (dmcphers@redhat.com)
- Automatic commit of package [rhc-cartridge-jbossas-7.0] release [0.73.21-1].
  (dmcphers@redhat.com)
- Update to jboss-as-7.0.0.CR1OS to address AS7-1225 (scott.stark@jboss.org)
- Automatic commit of package [rhc-cartridge-jbossas-7.0] release [0.73.20-1].
  (dmcphers@redhat.com)
- remove .doploy file for packaged war for now (dmcphers@redhat.com)
- Automatic commit of package [rhc-cartridge-jbossas-7.0] release [0.73.19-1].
  (dmcphers@redhat.com)
- readme update (dmcphers@redhat.com)
- add data dir to jboss (dmcphers@redhat.com)
- Automatic commit of package [rhc-cartridge-jbossas-7.0] release [0.73.18-1].
  (dmcphers@redhat.com)
- change groupid to be mynamespace by default (dmcphers@redhat.com)
- Automatic commit of package [rhc-cartridge-jbossas-7.0] release [0.73.17-1].
  (dmcphers@redhat.com)
- remove unnecessary chown (dmcphers@redhat.com)
- Automatic commit of package [rhc-cartridge-jbossas-7.0] release [0.73.16-1].
  (dmcphers@redhat.com)
- doc update (dmcphers@redhat.com)
- doc update (dmcphers@redhat.com)
- README updates (dmcphers@redhat.com)
- Automatic commit of package [rhc-cartridge-jbossas-7.0] release [0.73.15-1].
  (dmcphers@redhat.com)
- use different tmp dir for maven (dmcphers@redhat.com)
- moving jboss README and adding details (dmcphers@redhat.com)
- add mkdir for deployments just in case (dmcphers@redhat.com)
- Automatic commit of package [rhc-cartridge-jbossas-7.0] release [0.73.14-1].
  (dmcphers@redhat.com)
- up jboss.version file (dmcphers@redhat.com)
- fixup terminology in index.html (dmcphers@redhat.com)
- Automatic commit of package [rhc-cartridge-jbossas-7.0] release [0.73.13-1].
  (dmcphers@redhat.com)
- change jboss as7 dep (dmcphers@redhat.com)
- Automatic commit of package [rhc-cartridge-jbossas-7.0] release [0.73.12-1].
  (dmcphers@redhat.com)
- trying different java requires (dmcphers@redhat.com)
- Automatic commit of package [rhc-cartridge-jbossas-7.0] release [0.73.11-1].
  (dmcphers@redhat.com)
- trying full jar path in build (dmcphers@redhat.com)
- Automatic commit of package [rhc-cartridge-jbossas-7.0] release [0.73.10-1].
  (dmcphers@redhat.com)
- move ROOT.war out of repo (dmcphers@redhat.com)
- Automatic commit of package [rhc-cartridge-jbossas-7.0] release [0.73.9-1].
  (dmcphers@redhat.com)
- moving default template to be maven based (dmcphers@redhat.com)
- Automatic commit of package [rhc-cartridge-jbossas-7.0] release [0.73.8-1].
  (dmcphers@redhat.com)
- make jboss like other carts for when untar happens (dmcphers@redhat.com)
- back off on calling post receive for now (dmcphers@redhat.com)
- Automatic commit of package [rhc-cartridge-jbossas-7.0] release [0.73.7-1].
  (edirsh@redhat.com)
- call post-receive from configure instead of start (dmcphers@redhat.com)
- Automatic commit of package [rhc-cartridge-jbossas-7.0] release [0.73.6-1].
  (dmcphers@redhat.com)
- undo passing rhlogin to cart (dmcphers@redhat.com)
- add nurture call for git push (dmcphers@redhat.com)
- fix formatting in README (dmcphers@redhat.com)
- Automatic commit of package [rhc-cartridge-jbossas-7.0] release [0.73.5-1].
  (dmcphers@redhat.com)
- handle embed or command not passed (dmcphers@redhat.com)
- fix typo in README (dmcphers@redhat.com)
- fix skip tests (dmcphers@redhat.com)
- use alternative for maven-3.0 (dmcphers@redhat.com)
- Automatic commit of package [rhc-cartridge-jbossas-7.0] release [0.73.4-1].
  (mhicks@redhat.com)
- switch to use rpm for maven (dmcphers@redhat.com)
- Automatic commit of package [rhc-cartridge-jbossas-7.0] release [0.73.3-1].
  (dmcphers@redhat.com)
- Automatic commit of package [rhc-broker] release [0.73.3-1].
  (dmcphers@redhat.com)

* Mon Jul 11 2011 Dan McPherson <dmcphers@redhat.com> 0.74.1-1
- bumping spec numbers (dmcphers@redhat.com)
- move jboss template creation to instantiation (dmcphers@redhat.com)
- use maven war plugin rather than ant by default (dmcphers@redhat.com)

* Sat Jul 09 2011 Dan McPherson <dmcphers@redhat.com> 0.73.23-1
- adjust heap sizes (dmcphers@redhat.com)
- changing to lsof method (mmcgrath@redhat.com)
- Update MaxPermSize to 128m (scott.stark@jboss.org)

* Thu Jul 07 2011 Dan McPherson <dmcphers@redhat.com> 0.73.22-1
- doc updates (dmcphers@redhat.com)

* Thu Jul 07 2011 Dan McPherson <dmcphers@redhat.com> 0.73.21-1
- Update to jboss-as-7.0.0.CR1OS to address AS7-1225 (scott.stark@jboss.org)

* Wed Jul 06 2011 Dan McPherson <dmcphers@redhat.com> 0.73.20-1
- remove .doploy file for packaged war for now (dmcphers@redhat.com)

* Wed Jul 06 2011 Dan McPherson <dmcphers@redhat.com> 0.73.19-1
- readme update (dmcphers@redhat.com)
- add data dir to jboss (dmcphers@redhat.com)

* Wed Jul 06 2011 Dan McPherson <dmcphers@redhat.com> 0.73.18-1
- change groupid to be mynamespace by default (dmcphers@redhat.com)

* Wed Jul 06 2011 Dan McPherson <dmcphers@redhat.com> 0.73.17-1
- remove unnecessary chown (dmcphers@redhat.com)

* Tue Jul 05 2011 Dan McPherson <dmcphers@redhat.com> 0.73.16-1
- doc update (dmcphers@redhat.com)
- doc update (dmcphers@redhat.com)
- README updates (dmcphers@redhat.com)

* Tue Jul 05 2011 Dan McPherson <dmcphers@redhat.com> 0.73.15-1
- use different tmp dir for maven (dmcphers@redhat.com)
- moving jboss README and adding details (dmcphers@redhat.com)
- add mkdir for deployments just in case (dmcphers@redhat.com)

* Fri Jul 01 2011 Dan McPherson <dmcphers@redhat.com> 0.73.14-1
- up jboss.version file (dmcphers@redhat.com)
- fixup terminology in index.html (dmcphers@redhat.com)

* Fri Jul 01 2011 Dan McPherson <dmcphers@redhat.com> 0.73.13-1
- change jboss as7 dep (dmcphers@redhat.com)

* Fri Jul 01 2011 Dan McPherson <dmcphers@redhat.com> 0.73.12-1
- trying different java requires (dmcphers@redhat.com)

* Fri Jul 01 2011 Dan McPherson <dmcphers@redhat.com> 0.73.11-1
- trying full jar path in build (dmcphers@redhat.com)

* Fri Jul 01 2011 Dan McPherson <dmcphers@redhat.com> 0.73.10-1
- move ROOT.war out of repo (dmcphers@redhat.com)

* Fri Jul 01 2011 Dan McPherson <dmcphers@redhat.com> 0.73.9-1
- moving default template to be maven based (dmcphers@redhat.com)

* Fri Jul 01 2011 Dan McPherson <dmcphers@redhat.com> 0.73.8-1
- make jboss like other carts for when untar happens (dmcphers@redhat.com)
- back off on calling post receive for now (dmcphers@redhat.com)

* Fri Jul 01 2011 Emily Dirsh <edirsh@redhat.com> 0.73.7-1
- call post-receive from configure instead of start (dmcphers@redhat.com)

* Wed Jun 29 2011 Dan McPherson <dmcphers@redhat.com> 0.73.6-1
- undo passing rhlogin to cart (dmcphers@redhat.com)
- add nurture call for git push (dmcphers@redhat.com)
- fix formatting in README (dmcphers@redhat.com)

* Wed Jun 29 2011 Dan McPherson <dmcphers@redhat.com> 0.73.5-1
- handle embed or command not passed (dmcphers@redhat.com)
- fix typo in README (dmcphers@redhat.com)
- fix skip tests (dmcphers@redhat.com)
- use alternative for maven-3.0 (dmcphers@redhat.com)

* Tue Jun 28 2011 Matt Hicks <mhicks@redhat.com> 0.73.4-1
- switch to use rpm for maven (dmcphers@redhat.com)

* Tue Jun 28 2011 Dan McPherson <dmcphers@redhat.com> 0.73.3-1
- maven support (dmcphers@redhat.com)

* Mon Jun 27 2011 Dan McPherson <dmcphers@redhat.com> 0.73.2-1
- make appl dir ref rel (dmcphers@redhat.com)

* Mon Jun 27 2011 Dan McPherson <dmcphers@redhat.com> 0.73.1-1
- bump spec numbers (dmcphers@redhat.com)

* Mon Jun 27 2011 Dan McPherson <dmcphers@redhat.com> 0.72.29-1
- fix jboss spec (dmcphers@redhat.com)
- Bug 716362, restore server stop/start hooks and update to
  jbossas-7.0.0Beta7OS to address app removal error (scott.stark@jboss.org)
- Bug 716362, don't restart server on git push as it is not needed
  (scott.stark@jboss.org)
- Version 0.72.27 (scott.stark@jboss.org)
- Merge branch 'master' of ssh://git1.ops.rhcloud.com/srv/git/li
  (scott.stark@jboss.org)
- 715135, fix multiple start/stop errors (scott.stark@jboss.org)

* Thu Jun 24 2011 Scott Stark <sstark@redhat.com> 0.72.28-1
- Bug 716362, don't restart server on git push as it is not needed

* Thu Jun 23 2011 Scott Stark <sstark@redhat.com> 0.72.27-1
- Bug 715135

* Thu Jun 23 2011 Dan McPherson <dmcphers@redhat.com> 0.72.26-1
- exiting 0 even on failure (mmcgrath@redhat.com)
- Disabling this, it's causing errors on git push (mmcgrath@redhat.com)

* Thu Jun 23 2011 Dan McPherson <dmcphers@redhat.com> 0.72.25-1
- Bug 715525 (dmcphers@redhat.com)

* Tue Jun 21 2011 Dan McPherson <dmcphers@redhat.com> 0.72.24-1
- Close stdout before calling app_ctl.sh start to fix git hang
  (scott.stark@jboss.org)
- remove dup / from jboss app dir (dmcphers@redhat.com)

* Tue Jun 21 2011 Dan McPherson <dmcphers@redhat.com> 0.72.23-1
- Bug 714868 (dmcphers@redhat.com)

* Mon Jun 20 2011 Dan McPherson <dmcphers@redhat.com> 0.72.22-1
- 

* Mon Jun 20 2011 Dan McPherson <dmcphers@redhat.com> 0.72.21-1
- install fixup (dmcphers@redhat.com)
- adding template files (dmcphers@redhat.com)
- Temporary commit to build client (dmcphers@redhat.com)
- move template out of repo (dmcphers@redhat.com)
- remove old comment (dmcphers@redhat.com)
- supressing timestamp warnings (mmcgrath@redhat.com)

* Fri Jun 17 2011 Dan McPherson <dmcphers@redhat.com> 0.72.20-1
- trying version again (dmcphers@redhat.com)

* Fri Jun 17 2011 Dan McPherson <dmcphers@redhat.com> 0.72.19-1
- fixup dep version (dmcphers@redhat.com)

* Thu Jun 16 2011 Dan McPherson <dmcphers@redhat.com> 0.72.18-1
- 

* Thu Jun 16 2011 Dan McPherson <dmcphers@redhat.com> 0.72.17-1
- Add comment about logs link (scott.stark@jboss.org)
- Create a link from the standalone/log directory to ${APP_DIR}/logs for rhc-
  tail-files (scott.stark@jboss.org)
- Explicity declare dependency on version jboss-7.0.0.Beta6OS of jboss-as7
  (scott.stark@jboss.org)

* Thu Jun 16 2011 Scott Stark <sstark@redhat.com> 0.72.16-1
- Explicity declare dependency on version jboss-7.0.0.Beta6OS of jboss-as7
- Create a link from the standalone/log directory to ${APP_DIR}/logs for rhc-tail-files

* Wed Jun 15 2011 Dan McPherson <dmcphers@redhat.com> 0.72.15-1
- server side bundling for rails 3 (dmcphers@redhat.com)
- Update to jboss-as7 7.0.0.Beta6OS, brew buildID=167639
  (scott.stark@jboss.org)
- add stop/start to git push (dmcphers@redhat.com)
- move context to libra service and configure Part 2 (dmcphers@redhat.com)
- move context to libra service and configure (dmcphers@redhat.com)

* Tue Jun 14 2011 Scott Stark <sstark@redhat.com> 0.72.15-1
- Update standalone.xml configuration for jbossas-7.0.0.Beta6OS

* Tue Jun 14 2011 Matt Hicks <mhicks@redhat.com> 0.72.14-1
- Spec cleanup (mhicks@redhat.com)
- Permanent jboss fix now in place (mmcgrath@redhat.com)
- Merge branch 'master' of ssh://git1.ops.rhcloud.com/srv/git/li
  (scott.stark@jboss.org)
- Improve the way the control script is generated and correct the output of the
  status command. (scott.stark@jboss.org)

* Fri Jun 10 2011 Matt Hicks <mhicks@redhat.com> 0.72.13-1
- Add link to sample source Update H2DS to have local file store under
  jboss.server.data.dir (scott.stark@jboss.org)

* Wed Jun 08 2011 Dan McPherson <dmcphers@redhat.com> 0.72.12-1
- fixing configuration dir (mmcgrath@redhat.com)

* Tue Jun 07 2011 Matt Hicks <mhicks@redhat.com> 0.72.11-1
- Fixing servername to remove the debug server (mmcgrath@redhat.com)

* Tue Jun 07 2011 Matt Hicks <mhicks@redhat.com> 0.72.9-1
- Fixing git clone to repack after cloning (mhicks@redhat.com)
- tracking symlink dir (mmcgrath@redhat.com)
- Changing config dir to an actual config.  Also symlinking changes into the
  /etc/libra dir (mmcgrath@redhat.com)
- adding node_ssl_template (mmcgrath@redhat.com)

* Mon Jun 06 2011 Dan McPherson <dmcphers@redhat.com> 0.72.8-1
- moving to sym links for actions (dmcphers@redhat.com)

* Mon Jun 06 2011 Mike McGrath <mmcgrath@redhat.com> 0.72.7-2
- Added config dir symlink and config(noreplace)

* Fri Jun 03 2011 Matt Hicks <mhicks@redhat.com> 0.72.7-1
- Fixing jboss selinux issues (mmcgrath@redhat.com)
- customer -> application rename in cartridges (dmcphers@redhat.com)

* Fri Jun 03 2011 Mike McGrath <mmcgrath@redhat.com> 0.72.6-2
- Added semanage bits

* Wed Jun 01 2011 Dan McPherson <dmcphers@redhat.com> 0.72.6-1
- 

* Wed Jun 01 2011 Dan McPherson <dmcphers@redhat.com> 0.72.5-1
- Automatic commit of package [rhc-cartridge-jbossas-7.0] release [0.72.4-1].
  (dmcphers@redhat.com)

* Wed Jun 01 2011 Dan McPherson <dmcphers@redhat.com> 0.72.4-1
- move common files to abstract httpd (dmcphers@redhat.com)
- remove apptype dir part 1 (dmcphers@redhat.com)
- missed 1 delete (dmcphers@redhat.com)
- app-uuid patch from dev/markllama/app-uuid
  69b077104e3227a73cbf101def9279fe1131025e (markllama@gmail.com)

* Tue May 31 2011 Matt Hicks <mhicks@redhat.com> 0.72.3-1
- Update the README with the new brew build task info for jboss-as7 rpm
  (scott.stark@jboss.org)
- Bug 707108 (dmcphers@redhat.com)
- Update the jboss cartridge to use jboss-as7-7.0.0.Beta5OS
  https://brewweb.devel.redhat.com//buildinfo?buildID=165385
  (scott.stark@jboss.org)
- fix issue after refactor with remote clone (dmcphers@redhat.com)
* Tue May 25 2011 Matt Hicks <mhicks@redhat.com> 0.72.2-1
- Another cartridge rename to include minor version

* Tue May 25 2011 Matt Hicks <mhicks@redhat.com> 0.72.1-2
- Minor spec cleanup

* Tue May 25 2011 Scott Stark sstark@redhat.com
- change cartridge location to cartridges/jbossas7

* Tue May 25 2011 Matt Hicks <mhicks@redhat.com> 0.72.1-1
- Initial refactoring
