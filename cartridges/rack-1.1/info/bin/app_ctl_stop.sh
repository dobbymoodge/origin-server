#!/bin/bash

# Import Environment Variables
for f in ~/.env/*
do
    . $f
done

source "/etc/stickshift/stickshift-node.conf"
CART_CONF_DIR=${CARTRIDGE_BASE_PATH}/${OPENSHIFT_GEAR_TYPE}/info/configuration/etc/conf

# Stop the app
httpd_pid=`cat ${OPENSHIFT_RUN_DIR}httpd.pid 2> /dev/null`
/usr/sbin/httpd -C "Include ${OPENSHIFT_GEAR_DIR}conf.d/*.conf" -f $CART_CONF_DIR/httpd_nolog.conf -k $1
for i in {1..20}
do
    if `ps --pid $httpd_pid > /dev/null 2>&1` || `pgrep Passenger.* > /dev/null 2>&1`
    then
        echo "Waiting for stop to finish"
        sleep 3
    else
        break
    fi
done