%define ruby_sitelibdir            %(ruby -rrbconfig -e "puts Config::CONFIG['sitelibdir']")

Summary:       Common dependencies of the OpenShift broker and site
Name:          rhc-server-common
Version:       0.72.8
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
