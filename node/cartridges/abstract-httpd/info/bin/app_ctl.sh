#!/bin/bash -e

# Import Environment Variables
for f in ~/.env/*
do
    . $f
done

if ! [ $# -eq 1 ]
then
    echo "Usage: \$0 [start|restart|graceful|graceful-stop|stop]"
    exit 1
fi

validate_user_context.sh

. app_ctl_pre.sh

CART_CONF_DIR=/usr/libexec/li/cartridges/${OPENSHIFT_APP_TYPE}/info/configuration/etc/conf

case "$1" in
    start)
        if [ -f ${OPENSHIFT_APP_DIR}run/stop_lock ]
        then
            echo "Application is explicitly stopped!  Use 'rhc-ctl-app -a ${OPENSHIFT_APP_NAME} -c start' to start back up." 1>&2
            exit 0
        else
            /usr/sbin/httpd -C 'Include ${OPENSHIFT_APP_DIR}conf.d/*.conf' -f $CART_CONF_DIR/httpd_nolog.conf -k $1
        fi
    ;;
    graceful-stop|stop)
        app_ctl_stop.sh $1
    ;;
    restart|graceful)
        /usr/sbin/httpd -C 'Include ${OPENSHIFT_APP_DIR}conf.d/*.conf' -f $CART_CONF_DIR/httpd_nolog.conf -k $1
    ;;
esac