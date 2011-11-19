#!/bin/bash -e

CART_DIR=/usr/libexec/li/cartridges
source ${CART_DIR}/abstract/info/lib/util

# Import Environment Variables
for f in ~/.env/*
do
    . $f
done

if ! [ $# -eq 1 ]
then
    echo "Usage: $0 [start|restart|graceful|graceful-stop|stop]"
    exit 1
fi


validate_user_context.sh

export PHPRC="${OPENSHIFT_PHPMOADMIN_APP_DIR}conf/php.ini"

CART_CONF_DIR=/usr/libexec/li/cartridges/embedded/phpmoadmin-1.0/info/configuration/etc/conf

case "$1" in
    start)
        if [ -f ${OPENSHIFT_PHPMOADMIN_APP_DIR}run/stop_lock ]
        then
            echo "Application is explicitly stopped!  Use 'rhc-ctl-app -a ${OPENSHIFT_APP_NAME} -e start-phpmoadmin-1.0' to start back up." 1>&2
            exit 0
        else
            /usr/sbin/httpd -C 'Include ${OPENSHIFT_PHPMOADMIN_APP_DIR}/conf.d/*.conf' -f $CART_CONF_DIR/httpd_nolog.conf -k $1
        fi
    ;;

    graceful-stop|stop)
        httpd_pid=`cat ${OPENSHIFT_PHPMOADMIN_APP_DIR}run/httpd.pid 2> /dev/null`
        /usr/sbin/httpd -C 'Include ${OPENSHIFT_PHPMOADMIN_APP_DIR}/conf.d/*.conf' -f $CART_CONF_DIR/httpd_nolog.conf -k $1
        wait_for_stop $httpd_pid
    ;;

    restart|graceful)
        /usr/sbin/httpd -C 'Include ${OPENSHIFT_PHPMOADMIN_APP_DIR}/conf.d/*.conf' -f $CART_CONF_DIR/httpd_nolog.conf -k $1
    ;;
esac
