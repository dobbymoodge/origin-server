%if 0%{?fedora}%{?rhel} <= 6
    %global scl ruby193
    %global scl_prefix ruby193-
%endif
%{!?scl:%global pkg_name %{name}}
%{?scl:%scl_package rubygem-%{gem_name}}
%global gem_name openshift-origin-dns-dynect
%global rubyabi 1.9.1

Summary:        OpenShift plugin for Dynect DNS service

Name:           rubygem-%{gem_name}
Version: 1.5.4
Release:        1%{?dist}
Group:          Development/Languages
License:        ASL 2.0
URL:            http://openshift.redhat.com
Source0:        rubygem-%{gem_name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires:       %{?scl:%scl_prefix}ruby(abi) = %{rubyabi}
Requires:       %{?scl:%scl_prefix}ruby
Requires:       %{?scl:%scl_prefix}rubygems
Requires:       rubygem(openshift-origin-common)
Requires:       %{?scl:%scl_prefix}rubygem(json)

%if 0%{?fedora}%{?rhel} <= 6
BuildRequires:  ruby193-build
BuildRequires:  scl-utils-build
%endif
BuildRequires:  %{?scl:%scl_prefix}ruby(abi) = %{rubyabi}
BuildRequires:  %{?scl:%scl_prefix}ruby 
BuildRequires:  %{?scl:%scl_prefix}rubygems
BuildRequires:  %{?scl:%scl_prefix}rubygems-devel
BuildArch:      noarch
Provides:       rubygem(%{gem_name}) = %version
Obsoletes: rubygem-uplift-dynect-plugin

%description
Provides a DYN DNS service based plugin

%prep
%setup -q

%build
%{?scl:scl enable %scl - << \EOF}
mkdir -p ./%{gem_dir}
# Create the gem as gem install only works on a gem file
gem build %{gem_name}.gemspec
export CONFIGURE_ARGS="--with-cflags='%{optflags}'"
# gem install compiles any C extensions and installs into a directory
# We set that to be a local directory so that we can move it into the
# buildroot in %%install
gem install -V \
        --local \
        --install-dir ./%{gem_dir} \
        --bindir ./%{_bindir} \
        --force \
        --rdoc \
        %{gem_name}-%{version}.gem
%{?scl:EOF}

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a ./%{gem_dir}/* %{buildroot}%{gem_dir}/

mkdir -p %{buildroot}/etc/openshift/plugins.d
cp conf/openshift-origin-dns-dynect.conf %{buildroot}/etc/openshift/plugins.d/
cp conf/openshift-origin-dns-dynect-dev.conf %{buildroot}/etc/openshift/plugins.d/

%clean
rm -rf %{buildroot}                                

%files
%defattr(-,root,root,-)
%doc %{gem_docdir}
%{gem_instdir}
%{gem_spec}
%{gem_cache}
%config(noreplace) /etc/openshift/plugins.d/openshift-origin-dns-dynect.conf
/etc/openshift/plugins.d/openshift-origin-dns-dynect-dev.conf

%changelog
* Tue Jul 09 2013 Adam Miller <admiller@redhat.com> 1.5.4-1
- bump version to fix tito tags (admiller@redhat.com)
- Adjust to zone change (dmcphers@redhat.com)

* Tue Jul 09 2013 Adam Miller <admiller@redhat.com>
- Adjust to zone change (dmcphers@redhat.com)

* Wed May 08 2013 Adam Miller <admiller@redhat.com> 1.5.1-1
- bump_minor_versions for sprint 28 (admiller@redhat.com)

* Wed May 01 2013 Adam Miller <admiller@redhat.com> 1.4.2-1
- update dynect customer name (blentz@redhat.com)

* Thu Mar 07 2013 Adam Miller <admiller@redhat.com> 1.4.1-1
- bump_minor_versions for sprint 25 (admiller@redhat.com)

* Wed Feb 27 2013 Adam Miller <admiller@redhat.com> 1.3.2-1
- add debug timings of external operations (dmcphers@redhat.com)

* Thu Feb 07 2013 Adam Miller <admiller@redhat.com> 1.3.1-1
- bump_minor_versions for sprint 24 (admiller@redhat.com)

* Tue Jan 29 2013 Adam Miller <admiller@redhat.com> 1.2.2-1
- removing txt records (dmcphers@redhat.com)

* Sat Nov 17 2012 Adam Miller <admiller@redhat.com> 1.2.1-1
- bump_minor_versions for sprint 21 (admiller@redhat.com)

* Fri Nov 16 2012 Adam Miller <admiller@redhat.com> 1.1.3-1
- Bug 877479 (dmcphers@redhat.com)

* Wed Nov 14 2012 Adam Miller <admiller@redhat.com> 1.1.2-1
- Fixing gemspecs (kraman@gmail.com)
- Moving plugins to Rails 3.2.8 engines (kraman@gmail.com)
- sclizing gems (dmcphers@redhat.com)

* Thu Nov 08 2012 Adam Miller <admiller@redhat.com> 1.1.1-1
- Bumping specs to at least 1.1 (dmcphers@redhat.com)
- ruby 1.9 changes (dmcphers@redhat.com)

* Tue Oct 30 2012 Adam Miller <admiller@redhat.com> 1.0.1-1
- bumping specs to at least 1.0.0 (dmcphers@redhat.com)
