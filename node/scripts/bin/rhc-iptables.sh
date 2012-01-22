#!/bin/bash

#
# Create iptables rules for application compartmentalization.
#

UID_BEGIN=500
# UID_END=12700   # Too large for port numbers
UID_END=6500
UTABLE="rhc-app-table"
PTABLE="rhc-port-table"
PIFACE="eth0"
PORT_BEGIN=35531
PORTS_PER_USER=5

DEBUG=""
SYSCONFIG=""

function help {
  cat <<EOF >&2
Usage: $0 [ -h ] [ -i | -n | -s ] [ -b UID ] [ -e UID ] [ -t name ] [ -p name ] [ -i iface ]

    Basic options:
    -h       Print this message and exit.

    Output/execution type
    -i       Run iptables (default mode)
    -n       Print what would be done instead of calling iptables.
    -s       Print output suitable for /etc/sysconfig/iptables.

    Less common options that must remain consistent across invocation
    -b UID   Beginning UID.  (default: $UID_BEGIN)
    -e UID   Ending UID.  (default: $UID_END)
    -t name  Table Name (default: $UTABLE)
    -p name  Port Table Name (default: $PTABLE)
    -i name  Proxy Interface (default: $PIFACE)
EOF
}

while getopts ':hinsb:e:t:p:' opt; do
  case $opt in
    'h')
      help
      exit 0
      ;;
    'i')
      DEBUG=""
      SYSCONFIG=""
      ;;
    'n')
      DEBUG=1
      ;;
    's')
      SYSCONFIG=1
      ;;
    'b')
      UID_BEGIN="${OPTARG}"
      ;;
    'e')
      UID_END="${OPTARG}"
      ;;
    't')
      UTABLE="${OPTARG}"
      ;;
    'p')
      PTABLE="${OPTARG}"
      ;;
    '?')
      echo "Invalid option: -$OPTARG" >&2
      exit 1
      ;;
    ':')
      echo "Option requires argument: -$OPTARG" >&2
      exit 1
      ;;
  esac
done

# Test combinations of arguments for compatibility
if [ "${DEBUG}" = "1" -a "${SYSCONFIG}" = "1" ]; then
  echo "Debug (-n) and Sysconfig (-s) are mutually exclusive." >&2
  exit 1
fi

function iptables {
  if [ "${SYSCONFIG}" ]; then
    echo "$@"
  elif [ "${DEBUG}" ]; then
    echo /sbin/iptables "$@"
  else
    /sbin/iptables "$@"
  fi
}

function new_table {
  if [ "${SYSCONFIG}" ]; then
    echo ':'"$1"' - [0:0]'
  else
    iptables -N "$1" || :
    iptables -F "$1"
  fi
}

function uid_to_ip {
  # Logic copied from rhc-ip-prep
  a=$(($1*128+2130706432))
  h1=$(($a/16777216))
  h2=$(($(($a%16777216))/65536))
  h3=$(($(($a%65536))/256))
  h4=$(($a%256))

  echo "${h1}.${h2}.${h3}.${h4}"
}

function uid_to_portbegin {
  echo $(($(($(($1-$UID_BEGIN))*$PORTS_PER_USER))+$PORT_BEGIN))
}

function uid_to_portend {
  pbegin=`uid_to_portbegin $1`
  echo $(( $pbegin + $PORTS_PER_USER - 1 ))
}

# Create the table and clear it
new_table ${UTABLE}
new_table ${PTABLE}

# Established connections quickly bypass
iptables -A OUTPUT \
  -m owner --uid-owner ${UID_BEGIN}-${UID_END} \
  -m state --state ESTABLISHED,RELATED \
  -j ACCEPT

# Bottom block is system services
iptables -A OUTPUT -o lo -d 127.0.0.0/25 \
  -m owner --uid-owner ${UID_BEGIN}-${UID_END} \
  -m state --state NEW \
  -j ACCEPT

# New connections with specific uids get checked on the app table.
iptables -A OUTPUT -o lo -d 127.0.0.0/8 \
  -m owner --uid-owner ${UID_BEGIN}-${UID_END} \
  -m state --state NEW \
  -j ${UTABLE}

# New port proxy connections
iptables -A OUTPUT -p tcp -o ${PIFACE} \
  -m multiport \
  --dports `uid_to_portbegin $UID_BEGIN`:`uid_to_portend $UID_END` \
  -m owner --uid-owner ${UID_BEGIN}-${UID_END} \
  -m state --state NEW \
  -j ${PTABLE}

# Per UID rules
seq ${UID_BEGIN} ${UID_END} | while read uid; do
  iptables -A ${UTABLE} -d `uid_to_ip $uid`/25 \
    -m owner --uid-owner $uid \
    -j ACCEPT
done
iptables -A ${UTABLE} -j REJECT --reject-with icmp-host-prohibited

seq ${UID_BEGIN} ${UID_END} | while read uid; do
  iptables -A ${PTABLE} -p tcp \
    -m multiport --dports `uid_to_portbegin $uid`:`uid_to_portend $uid` \
    -m owner --uid-owner $uid \
    -j ACCEPT
done
iptables -A ${PTABLE} -j REJECT --reject-with icmp-host-prohibited
