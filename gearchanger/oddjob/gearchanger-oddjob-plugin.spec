%global ruby_sitelib %(ruby -rrbconfig -e "puts Config::CONFIG['sitelibdir']")
%global gemdir %(ruby -rubygems -e 'puts Gem::dir' 2>/dev/null)
%global gemname gearchanger-oddjob-plugin
%global geminstdir %{gemdir}/gems/%{gemname}-%{version}

Summary:        GearChanger plugin for oddjob service
Name:           rubygem-%{gemname}
Version:        0.7.3
Release:        1%{?dist}
Group:          Development/Languages
License:        ASL 2.0
URL:            http://openshift.redhat.com
Source0:        rubygem-%{gemname}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires:       ruby(abi) = 1.8
Requires:       rubygems
Requires:       rubygem(stickshift-common)
Requires:       rubygem(json)

BuildRequires:  ruby
BuildRequires:  rubygems
BuildArch:      noarch
Provides:       rubygem(%{gemname}) = %version

%package -n ruby-%{gemname}
Summary:        GearChanger plugin for oddjob based node/gear manager
Requires:       rubygem(%{gemname}) = %version
Provides:       ruby(%{gemname}) = %version

%description
GearChanger plugin for oddjob based node/gear manager

%description -n ruby-%{gemname}
GearChanger plugin for oddjob based node/gear manager

%prep
%setup -q

%build

%post
/usr/sbin/semodule -i /var/lib/stickshift/stickshift.pp
/usr/sbin/semanage fcontext -a -e /home /var/lib/stickshift
/sbin/restorecon -R /var/lib/stickshift /usr/bin/ss-exec-command || :


%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{gemdir}
mkdir -p %{buildroot}%{ruby_sitelib}

# Build and install into the rubygem structure
gem build %{gemname}.gemspec
gem install --local --install-dir %{buildroot}%{gemdir} --force %{gemname}-%{version}.gem

# Symlink into the ruby site library directories
ln -s %{geminstdir}/lib/%{gemname} %{buildroot}%{ruby_sitelib}
ln -s %{geminstdir}/lib/%{gemname}.rb %{buildroot}%{ruby_sitelib}

# move the selinux policy files into proper location
mkdir -p /var/lib/stickshift
cp %{buildroot}%{geminstdir}/selinux/* /var/lib/stickshift/.
rm -rf %{buildroot}%{geminstdir}/selinux


%clean
rm -rf %{buildroot}                                


%postun
/usr/sbin/semodule -r stickshift
/usr/sbin/semanage fcontext -d /var/lib/stickshift
/sbin/restorecon -R /var/lib/stickshift /usr/bin/ss-exec-command || :



%files
%defattr(-,root,root,-)
%dir %{geminstdir}
%doc %{geminstdir}/Gemfile
%{gemdir}/doc/%{gemname}-%{version}
%{gemdir}/gems/%{gemname}-%{version}
%{gemdir}/cache/%{gemname}-%{version}.gem
%{gemdir}/specifications/%{gemname}-%{version}.gemspec

%files -n ruby-%{gemname}
%{ruby_sitelib}/%{gemname}
%{ruby_sitelib}/%{gemname}.rb

%changelog
