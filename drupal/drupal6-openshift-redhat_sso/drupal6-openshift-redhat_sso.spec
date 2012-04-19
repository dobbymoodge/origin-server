%global drupal_release      6
%global drupal_base         %{_datadir}/drupal%{drupal_release}
%global drupal_sites_all    %{drupal_base}/sites/all        
%global drupal_modules      %{drupal_sites_all}/modules/custom
%global modname             redhat_sso

Name:    drupal%{drupal_release}-openshift-%{modname}
Version: 1.1.7
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
