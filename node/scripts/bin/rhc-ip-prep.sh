#!/bin/bash

# This script will lock down the host so only specific users are allowed to bind to specific IP addresses
# It can be called with:
#
# [ $(semanage node -l | grep -c 255.255.255.128) -lt 1000 ] && ./rhc-ip-prep.sh

# lock down the localhost ip addresses

for uid in `seq 500 1550`
do
    a=$(($uid*128+2130706432))
    net=$(($a>>24 )).$(($(($a%16777216))<<8>>24)).$(($(($a%65536))<<16>>24)).$(($(($a%256))<<24>>24))
    source /usr/libexec/li/cartridges/abstract/info/lib/selinux
    mcs_level=`openshift_mcs_level $uid`
    echo "node -a -t node_t -r $mcs_level -M  255.255.255.128 -p ipv4 $net"
done > /tmp/selinux
echo "node -a -t node_t -r s0:c1023 -M  255.0.0.0 -p ipv4 127.0.0.0" >> /tmp/selinux
echo "node -a -t node_t -r s0 -p ipv4 -M 255.255.255.255 127.0.0.1" >> /tmp/selinux

semanage -S targeted -i - < /tmp/selinux
rm -f /tmp/selinux
