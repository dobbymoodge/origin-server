%if 0%{?fedora}
    %global mco_agent_root /usr/libexec/mcollective/mcollective/agent/
%endif
%if 0%{?rhel}
    %global mco_agent_root /opt/rh/ruby193/root/usr/libexec/mcollective/mcollective/agent/
%endif

Summary:   Common dependencies of the libra server and node
Name:      rhc-common
Version: 1.5.3
Release:   1%{?dist}
Group:     Network/Daemons
License:   GPLv2
URL:       http://openshift.redhat.com
Source0:   rhc-common-%{version}.tar.gz

BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
Requires:  mcollective-client
Requires:  ruby193-mcollective-common
Requires:  qpid-cpp-client
Requires:  qpid-cpp-client-ssl
Requires:  ruby-qmf
Requires(pre):  shadow-utils

BuildArch: noarch

%description
Provides the common dependencies for the OpenShift server and nodes

%prep
%setup -q

%build

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_sysconfdir}/mcollective
mkdir -p %{buildroot}%{_libexecdir}/mcollective/mcollective/connector
mkdir -p %{buildroot}%{mco_agent_root}
cp mcollective/connector/amqp.rb %{buildroot}%{_libexecdir}/mcollective/mcollective/connector
touch %{buildroot}%{_sysconfdir}/mcollective/client.cfg
cp mcollective/agent/* %{buildroot}%{mco_agent_root}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%ghost %attr(0640,-,libra_user) %{_sysconfdir}/mcollective/client.cfg
%{_libexecdir}/mcollective/mcollective/connector/amqp.rb
%attr(0640,-,-) %{mco_agent_root}*

%pre
getent group libra_user >/dev/null || groupadd -r libra_user

%post
/bin/chgrp libra_user /etc/mcollective/client.cfg

%changelog
* Mon Jun 10 2013 Dan McPherson <dmcphers@redhat.com> 1.5.3-1
- Migration issues (dmcphers@redhat.com)

* Wed May 22 2013 Adam Miller <admiller@redhat.com> 1.5.2-1
- WIP Cartridge Refactor - V2 to V2 Migrations (jhonce@redhat.com)

* Wed May 08 2013 Adam Miller <admiller@redhat.com> 1.5.1-1
- bump_minor_versions for sprint 28 (admiller@redhat.com)

* Thu Apr 25 2013 Adam Miller <admiller@redhat.com> 1.4.2-1
- WIP: V2 Migrations (pmorie@gmail.com)

* Thu Mar 07 2013 Adam Miller <admiller@redhat.com> 1.4.1-1
- bump_minor_versions for sprint 25 (admiller@redhat.com)

* Thu Feb 28 2013 Adam Miller <admiller@redhat.com> 1.3.2-1
- Bug 901424 - client.cfg should have same perms as on int/stg/prod.
  (rmillner@redhat.com)

* Wed Dec 12 2012 Adam Miller <admiller@redhat.com> 1.3.1-1
- bump_minor_versions for sprint 22 (admiller@redhat.com)

* Tue Dec 04 2012 Adam Miller <admiller@redhat.com> 1.2.2-1
- Repacking for mco 2.2 (dmcphers@redhat.com)

* Sat Nov 17 2012 Adam Miller <admiller@redhat.com> 1.2.1-1
- bump_minor_versions for sprint 21 (admiller@redhat.com)

* Wed Nov 14 2012 Adam Miller <admiller@redhat.com> 1.1.2-1
- sclizing gems (dmcphers@redhat.com)

* Thu Nov 08 2012 Adam Miller <admiller@redhat.com> 1.1.1-1
- Bumping specs to at least 1.1 (dmcphers@redhat.com)

* Tue Oct 30 2012 Adam Miller <admiller@redhat.com> 1.0.1-1
- bumping specs to at least 1.0.0 (dmcphers@redhat.com)

* Mon Oct 15 2012 Adam Miller <admiller@redhat.com> 0.81.3-1
- Migrate to using OpenShift::Config.new (miciah.masters@gmail.com)

* Mon Oct 08 2012 Adam Miller <admiller@redhat.com> 0.81.2-1
- Fixing renames, paths, configs and cleaning up old packages. Adding
  obsoletes. (kraman@gmail.com)

* Wed Jul 11 2012 Adam Miller <admiller@redhat.com> 0.81.1-1
- bump_minor_versions for sprint 15 (admiller@redhat.com)

* Tue Jul 03 2012 Adam Miller <admiller@redhat.com> 0.80.3-1
- WIP changes to support mcollective 2.0. (mpatel@redhat.com)

* Sat Jun 23 2012 Dan McPherson <dmcphers@redhat.com> 0.80.2-1
- new package built with tito

* Fri Jun 01 2012 Adam Miller <admiller@redhat.com> 0.80.1-1
- bumping spec versions (admiller@redhat.com)

* Tue May 29 2012 Adam Miller <admiller@redhat.com> 0.79.3-1
- Bug 820223 820338 820325 (dmcphers@redhat.com)

* Tue May 22 2012 Adam Miller <admiller@redhat.com> 0.79.2-1
- EPEL updated mcollective and broke the build! forcing mcollective 1.1.2
  (admiller@redhat.com)

* Thu May 10 2012 Adam Miller <admiller@redhat.com> 0.79.1-1
- bumping spec versions (admiller@redhat.com)

* Mon May 07 2012 Adam Miller <admiller@redhat.com> 0.78.2-1
- Work with version 14.4 of qpid (dmcphers@redhat.com)

* Thu Apr 26 2012 Adam Miller <admiller@redhat.com> 0.78.1-1
- bumping spec versions (admiller@redhat.com)

* Thu Apr 12 2012 Mike McGrath <mmcgrath@redhat.com> 0.77.2-1
- release bump for tag uniqueness (mmcgrath@redhat.com)

* Fri Jan 13 2012 Dan McPherson <dmcphers@redhat.com> 0.76.1-1
- bump spec numbers (dmcphers@redhat.com)

* Wed Jan 11 2012 Dan McPherson <dmcphers@redhat.com> 0.75.2-1
- 

* Wed Dec 14 2011 Dan McPherson <dmcphers@redhat.com> 0.75.1-1
- bump spec numbers (dmcphers@redhat.com)

* Wed Dec 14 2011 Dan McPherson <dmcphers@redhat.com> 0.74.2-1
- 

* Thu Dec 01 2011 Dan McPherson <dmcphers@redhat.com> 0.74.1-1
- bump spec numbers (dmcphers@redhat.com)

* Fri Nov 18 2011 Dan McPherson <dmcphers@redhat.com> 0.73.3-1
- more php settings + mirage devenv additions (dmcphers@redhat.com)

* Mon Jun 27 2011 Dan McPherson <dmcphers@redhat.com> 0.73.2-1
- 

* Mon Jun 27 2011 Dan McPherson <dmcphers@redhat.com> 0.73.1-1
- bump spec numbers (dmcphers@redhat.com)

* Thu Jun 09 2011 Matt Hicks <mhicks@redhat.com> 0.72.3-1
- Reformatting and cleanup (mhicks@redhat.com)
- Retrying on initial connection failure (mhicks@redhat.com)

* Mon Jun 06 2011 Dan McPherson <dmcphers@redhat.com> 0.72.2-1
- move client.cfg update to the right place (dmcphers@redhat.com)

* Wed May 25 2011 Matt Hicks <mhicks@redhat.com> 0.72.1-2
- Fixing build root dirs

* Tue May 25 2011 Matt Hicks <mhicks@redhat.com> 0.72.1-1
- Initial refactoring
