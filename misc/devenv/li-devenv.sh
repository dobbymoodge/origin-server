echo "nameserver 4.2.2.2" >> /etc/resolv.conf

#rpm -Uhv http://download.fedora.redhat.com/pub/epel/6/x86_64/epel-release-6-5.noarch.rpm
rpm -Uhv http://download.fedoraproject.org/pub/epel/6/x86_64/epel-release-6-5.noarch.rpm

#sed -i s/sslverify=1/sslverify=0/g /etc/yum.repos.d/rh-cloud.repo

cat > /etc/yum.repos.d/li.repo <<EOF
[li]
name=Li repo for Enterprise Linux 6 - \$basearch
baseurl=http://209.132.178.9/gpxe/trees/libra-rhel-6.2-${1-candidate}/\$basearch/
failovermethod=priority
enabled=1
gpgcheck=0
gpgkey=http://209.132.178.9/gpxe/trees/RPM-GPG-KEY-redhat-beta
ggpkey=http://209.132.178.9/gpxe/trees/RPM-GPG-KEY-redhat-release

[li-source]
name=Li repo for Enterprise Linux 6 - Source
baseurl=http://209.132.178.9/gpxe/trees/libra-rhel-6.2-${1-candidate}/source/SRPMS/
failovermethod=priority
enabled=0
gpgkey=http://209.132.178.9/gpxe/trees/RPM-GPG-KEY-redhat-beta
ggpkey=http://209.132.178.9/gpxe/trees/RPM-GPG-KEY-redhat-release
gpgcheck=0

[qpid]
name=Qpid repo
baseurl=http://209.132.178.9/gpxe/trees/qpid/\$basearch/Packages/
failovermethod=priority
enabled=1
gpgcheck=1
gpgkey=http://209.132.178.9/gpxe/trees/li/li-signing.asc

[passenger]
name=Passenger repo for Enterprise Linux 6
baseurl=http://209.132.178.9/gpxe/trees/passenger
failovermethod=priority
enabled=1
gpgcheck=0

[rhui-us-east-1-rhel-server-releases-i386]
name=Red Hat Enterprise Linux Server 6 -i386 (RPMs)
mirrorlist=https://rhui2-cds01.us-east-1.aws.ce.redhat.com/pulp/mirror/content/dist/rhel/rhui/server/6/\$releasever/i386/os
enabled=1
gpgcheck=1
gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-redhat-release file:///etc/pki/rpm-gpg/RPM-GPG-KEY-redhat-auxiliary
sslverify=1
sslclientkey=/etc/pki/entitlement/content-rhel6-key.pem
sslclientcert=/etc/pki/entitlement/product/content-rhel6.crt
sslcacert=/etc/pki/entitlement/cdn.redhat.com-chain.crt
includepkgs=java-1.6.0-openjdk*

EOF

ls /etc/yum.repos.d/
cat /etc/yum.repos.d/*.repo

# Install the 32 bit java before anything else
yum update -y --exclude='rhc*'; yum -y install java-1.6.0-openjdk.i686 java-1.6.0-openjdk-devel.i686

function install_build_requires {
  spec_file=$1
  for s in `grep -e "^BuildRequires:" $spec_file`
  do
    if [[ $s =~ ^[a-z]+ ]]
    then
      yum install -y $s
    fi
  done
}

if [ "$2" == "--install_from_source" ]
then
  rm -rf /root/li-working
  git clone git://git1.ops.rhcloud.com/li.git/ /root/li-working
  rm -rf /root/os-client-tools
  git clone https://github.com/openshift/os-client-tools.git /root/os-client-tools
  pushd /root/li-working > /dev/null
  for x in `find -name *.spec`
  do
    dir=`dirname $x`
    if [ "$dir" != "./build/seigiku" ]
    then
      install_build_requires "$x"
      pushd $dir > /dev/null
	  tito build --test --rpm
	  popd > /dev/null
    fi
  done
  cp /tmp/tito/x86_64/*.rpm /tmp/tito/noarch/
  pushd /root/os-client-tools/express > /dev/null
    install_build_requires "client.spec"
    tito build --test --rpm
  popd > /dev/null
  yum localinstall -y /tmp/tito/noarch/*.rpm
  build/devenv write_sync_history
  popd > /dev/null
  rm -rf /root/os-client-tools
  rm -rf /root/li-working
  rm -rf /tmp/tito
  git init --bare /root/os-client-tools
elif [ "$2" == "--install_build_prereqs" ]
then
  yum -y install git tito
else
  yum -y install rhc-devenv
fi
