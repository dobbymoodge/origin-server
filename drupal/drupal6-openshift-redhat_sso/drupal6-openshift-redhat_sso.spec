%global drupal_release      6
%global drupal_base         %{_datadir}/drupal%{drupal_release}
%global drupal_sites_all    %{drupal_base}/sites/all        
%global drupal_modules      %{drupal_sites_all}/modules/custom
%global modname             redhat_sso

Name:    drupal%{drupal_release}-openshift-%{modname}
Version: 1.6.3
Release: 1%{?dist}
Summary: Openshift Red Hat Custom SSO Module for Drupal6
Group:   Applications/Publishing
License: GPLv2+
Source0: %{name}-%{version}.tar.gz
BuildArch: noarch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires:  drupal6

%description
Openshift Red Hat Custom SSO Module for Drupal6


%prep
%setup -q
# Remove empty index.html and others
find -size 0 | xargs rm -f

%build


%install
rm -rf $RPM_BUILD_ROOT
%{__mkdir} -p $RPM_BUILD_ROOT/%{drupal_modules}/%{modname}
cp -pr . $RPM_BUILD_ROOT/%{drupal_modules}/%{modname}


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%{drupal_modules}/%{modname}

%changelog
* Fri Jun 07 2013 Adam Miller <admiller@redhat.com> 1.6.3-1
- Site summit changes, backported from bbe7f47f293c826be00ead46457377f475b810b7
  in master (ccoleman@redhat.com)

* Thu May 16 2013 Adam Miller <admiller@redhat.com> 1.6.2-1
- Remove old resources that should not be used, remove comment about secret
  key. (ccoleman@redhat.com)

* Thu Mar 07 2013 Adam Miller <admiller@redhat.com> 1.6.1-1
- bump_minor_versions for sprint 25 (admiller@redhat.com)

* Wed Mar 06 2013 Adam Miller 1.5.3-2
- Bump spec for mass drupal rebuild

* Mon Feb 25 2013 Adam Miller <admiller@redhat.com> 1.5.3-1
- Bug 909992 - Fix login errors outside of login (ccoleman@redhat.com)

* Mon Feb 18 2013 Adam Miller <admiller@redhat.com> 1.5.2-2
- Bump spec for mass drupal rebuild

* Fri Feb 08 2013 Adam Miller <admiller@redhat.com> 1.5.2-1
- bump Release: for all drupal packages for rebuild (admiller@redhat.com)
- US3291 US3292 US3293 - Move community to www.openshift.com
  (ccoleman@redhat.com)

* Fri Feb 08 2013 Adam Miller <admiller@redhat.com> - 1.5.1-2
- rebuilt

* Wed Jul 11 2012 Adam Miller <admiller@redhat.com> 1.5.1-1
- bump_minor_versions for sprint 15 (admiller@redhat.com)

* Mon Jul 02 2012 Adam Miller <admiller@redhat.com> 1.4.3-1
- Bug 834638 Allow normal caching mode to be enabled by fixing redhat_sso hooks
  to be earlier (ccoleman@redhat.com)

* Sat Jun 23 2012 Dan McPherson <dmcphers@redhat.com> 1.4.2-1
- new package built with tito

* Wed Jun 20 2012 Adam Miller <admiller@redhat.com> 1.4.1-1
- bump_minor_versions for sprint 14 (admiller@redhat.com)

* Thu Jun 14 2012 Adam Miller <admiller@redhat.com> 1.3.2-1
- Add caching to drupal views and blocks for better performance.  Remove
  unnecessary sections from UI (ccoleman@redhat.com)

* Thu May 10 2012 Adam Miller <admiller@redhat.com> 1.3.1-1
- bumping spec versions (admiller@redhat.com)

* Tue May 08 2012 Adam Miller <admiller@redhat.com> 1.2.2-1
- Begin tracking unique user ids on login of drupal. (ccoleman@redhat.com)

* Thu Apr 26 2012 Adam Miller <admiller@redhat.com> 1.2.1-1
- bumping spec versions (admiller@redhat.com)

* Wed Apr 18 2012 Dan McPherson <dmcphers@redhat.com> 1.1.7-1
- Touch all drupal modules to ensure a build. (ccoleman@redhat.com)

* Mon Apr 16 2012 Anderson Silva <ansilva@redhat.com> 1.1.6-1
- drupal6-openshift-redhat_sso: still fighting with tito and %%prep
  (ansilva@redhat.com)

* Mon Apr 16 2012 Anderson Silva <ansilva@redhat.com> 1.1.5-1
- drupal6-openshift-redhat_sso: fix %%prep step (ansilva@redhat.com)

* Mon Apr 16 2012 Anderson Silva <ansilva@redhat.com> 1.1.4-1
- drupal6-openshift-redhat_sso: one more fix for Source0 (ansilva@redhat.com)

* Mon Apr 16 2012 Anderson Silva <ansilva@redhat.com> 1.1.3-1
- drupal6-openshift-redhat_sso: change Source0 to comply with tito
  (ansilva@redhat.com)

* Mon Apr 16 2012 Anderson Silva <ansilva@redhat.com> 1.1.2-1
- drupal: changing layout of source code for proper tito rpm
  (ansilva@redhat.com)
- drupal6-openshift-redhat_sso update version (ansilva@redhat.com)

* Mon Apr 16 2012 Anderson Silva <ansilva@redhat.com> 1.1.1-1
- update version 

* Mon Apr 16 2012 Anderson Silva <ansilva@redhat.com> 1.1-1
- new package built with tito

* Mon Mar 5 2012 Anderson Silva <ansilva@redhat.com> - 1.0-1
- Initial rpm package
