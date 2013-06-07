%global drupal_release 6
%global drupal_base %{_datadir}/drupal%{drupal_release}
%global drupal_sites_all %{drupal_base}/sites/all
%global drupal_modules %{drupal_sites_all}/modules/custom
%global modname partner_program

Name: drupal%{drupal_release}-openshift-%{modname}
Version: 0.0.3
Release: 4%{?dist}
Summary: OpenShift Partner Program Drupal Content
Group: Applications/Publishing
License: GPLv2+
Source0: %{name}-%{version}.tar.gz
BuildArch: noarch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires: drupal6

%description
Openshift Online Partner Program Module


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
* Fri Jun 07 2013 Adam Miller 0.0.3-4
- Bump spec for mass drupal rebuild

* Thu Jun 06 2013 Adam Miller 0.0.3-3
- Bump spec for mass drupal rebuild

* Wed Jun 05 2013 Adam Miller 0.0.3-2
- Bump spec for mass drupal rebuild

* Tue Jun 04 2013 Adam Miller <admiller@redhat.com> 0.0.3-1
- new package built with tito

* Tue Jun 04 2013 Adam Miller - 0.0.1-1
- First package for Drupal Partner Program Content
