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
    echo "Usage: \$0 [start|restart|graceful|graceful-stop|stop]"
    exit 1
fi

validate_run_as_user

. app_ctl_pre.sh

case "$1" in
    start)
    [ -f $OPENSHIFT_REPO_DIR/.openshift/action_hooks/start ] &&
         $OPENSHIFT_REPO_DIR/.openshift/action_hooks/start
    ;;
    graceful-stop|stop)
    [ -f $OPENSHIFT_REPO_DIR/.openshift/action_hooks/stop ] &&
         $OPENSHIFT_REPO_DIR/.openshift/action_hooks/stop
    ;;
    restart|graceful)
    [ -f $OPENSHIFT_REPO_DIR/.openshift/action_hooks/stop ] &&
         $OPENSHIFT_REPO_DIR/.openshift/action_hooks/stop
    [ -f $OPENSHIFT_REPO_DIR/.openshift/action_hooks/start ] &&
         $OPENSHIFT_REPO_DIR/.openshift/action_hooks/start
    ;;
    reload)
    [ -f $OPENSHIFT_REPO_DIR/.openshift/action_hooks/stop ] &&
         $OPENSHIFT_REPO_DIR/.openshift/action_hooks/stop
    [ -f $OPENSHIFT_REPO_DIR/.openshift/action_hooks/start ] &&
         $OPENSHIFT_REPO_DIR/.openshift/action_hooks/start
    ;;
    status)
        print_running_processes
    ;;
esac
