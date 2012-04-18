%global drupal_release      6
%global drupal_base         %{_datadir}/drupal%{drupal_release}
%global drupal_sites_all    %{drupal_base}/sites/all        
%global drupal_modules      %{drupal_sites_all}/modules/features
%global modname             user_profile

Name:    drupal%{drupal_release}-openshift-features-%{modname}
Version: 1.0.2
Release: 1%{?dist}
Summary: Openshift Red Hat Custom User Profile Feature for Drupal6
Group:   Applications/Publishing
License: GPLv2+
Source0: %{modname}-%{drupal_release}.x-%{version}.tar.gz
BuildArch: noarch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires:  drupal6, drupal6-votingapi, drupal6-rules, drupal6-flag, drupal6-og, drupal6-token, drupal6-userpoints, drupal6-views, drupal6-faq, drupal6-fivestar, drupal6-admin_menu, drupal6-advanced-help, drupal6-better_formats, drupal6-context, drupal6-devel, drupal6-homebox, drupal6-stringoverrides, drupal6-userpoints, drupal6-eazylaunch, drupal6-custom_breadcrumbs

%description
Openshift Red Hat Custom User Profile Feature for Drupal6


%prep
%setup -qn %{modname}
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
* Wed Apr 18 2012 Dan McPherson <dmcphers@redhat.com> 1.0.2-1
- new package built with tito

* Mon Apr 16 2012 Anderson Silva <ansilva@redhat.com> - 1.0.1-1
- update version 

* Mon Mar 5 2012 Anderson Silva <ansilva@redhat.com> - 1.0-1
- Initial rpm package
