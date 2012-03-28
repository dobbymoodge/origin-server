#!/bin/bash -e

source /etc/stickshift/stickshift-node.conf
source ${CARTRIDGE_BASE_PATH}/abstract/info/lib/util

export STOPTIMEOUT=20

# Import Environment Variables
for f in ~/.env/*
do
    . $f
done

export HAPROXY_PID="${OPENSHIFT_HOMEDIR}/haproxy-1.4/run/haproxy.pid"

if ! [ $# -eq 1 ]
then
    echo "Usage: \$0 [start|restart|graceful|graceful-stop|stop]"
    exit 1
fi

validate_run_as_user

. app_ctl_pre.sh

isrunning() {
    if [ -f "${HAPROXY_PID}" ]; then
        haproxy_pid=`$HAPROXY_PID 2> /dev/null`
        if `ps --pid $haproxy_pid > /dev/null 2>&1` || `pgrep -x haproxy > /dev/null 2>&1`
        then
            return 0
        fi
    fi
    return 1
}

function wait_to_start() {
   ep=$(grep "listen express" $OPENSHIFT_HOMEDIR/haproxy-1.4/conf/haproxy.cfg | sed 's#listen\s*express\s*\(.*\)#\1#')
   i=0
   while ( ! curl "http://$ep/haproxy-status/;csv" &> /dev/null )  && [ $i -lt 10 ]; do
       sleep 1
       i=$(($i + 1))
   done
}

start() {
    set_app_state started
    if ! isrunning
    then
        /usr/sbin/haproxy -f $OPENSHIFT_HOMEDIR/haproxy-1.4/conf/haproxy.cfg > /dev/null 2>&1
        #haproxy_ctld_daemon start > /dev/null 2>&1
    else
        echo "Haproxy already running" 1>&2
    fi

    wait_to_start
}


stop() {
    set_app_state stopped
    #haproxy_ctld_daemon stop > /dev/null 2>&1
    if [ -f $HAPROXY_PID ]; then
        pid=$( /bin/cat "${HAPROXY_PID}" )
        /bin/kill $pid
        ret=$?
        if [ $ret -eq 0 ]; then
            TIMEOUT="$STOPTIMEOUT"
            while [ $TIMEOUT -gt 0 ] && [ -f "$HAPROXY_PID" ]; do
                /bin/kill -0 "$pid" >/dev/null 2>&1 || break
                sleep .5
                let TIMEOUT=${TIMEOUT}-1
            done
        fi
    else
        if `pgrep -x haproxy > /dev/null 2>&1`
        then
            echo "Warning: Haproxy process exists without a pid file.  Use force-stop to kill." 1>&2
        else
            echo "Haproxy already stopped" 1>&2
        fi
    fi
}


function restart() {
   stop || pkill haproxy || :
   start
}


function _reload_haproxy_service() {
    [ -n "$1" ]  &&  zopts="-sf $1"
    /usr/sbin/haproxy -f $OPENSHIFT_HOMEDIR/haproxy-1.4/conf/haproxy.cfg ${zopts} > /dev/null 2>&1

}

function backgrounded_reload() {
    set -x
    [ -f $HAPROXY_PID ]  &&  zpid=$( /bin/cat "${HAPROXY_PID}" )
    i=0
    while (! _reload_haproxy_service "$zpid" )  && [ $i -lt 60 ]; do
        sleep 1
        i=$(($i + 1))
    done

    wait_to_start
}

reload() {
    if ! isrunning; then
       start
    else
       echo "Reloading haproxy gracefully without service interruption" 1>&2
       echo "    - reload is being done in the background ..." 1>&2
       nohup "$0" backgrounded-reload > /tmp/haproxy-reload.log 2>&1 &
       # wait_to_start
    fi
    #haproxy_ctld_daemon restart > /dev/null 2>&1
}


case "$1" in
    start)               start               ;;
    graceful-stop|stop)  stop                ;;
    restart)             restart             ;;
    graceful|reload)     reload              ;;
    backgrounded-reload) backgrounded_reload ;;
    force-stop)          pkill haproxy       ;;
    status)              print_running_processes ;;
    # FIXME:  status should just report on haproxy not all the user's processes.
esac
