#!/bin/bash

source "/etc/stickshift/stickshift-node.conf"
source ${CARTRIDGE_BASE_PATH}/abstract/info/lib/util

# Control application's embedded Memcached server instance
1ERVICE_NAME=Memcached
CART_NAME=memcached
CART_VERSION=1.4
CART_DIRNAME=${CART_NAME}-$CART_VERSION
CART_INSTALL_DIR=${CARTRIDGE_BASE_PATH}
CART_INFO_DIR=$CART_INSTALL_DIR/embedded/$CART_DIRNAME/info
export STOPTIMEOUT=10

MEMCACHED_CACHESIZE=8
MEMCACHED_MAXCONN=10
MEMCACHED_OTHER_OPTIONS=""

function _is_service_running() {
   if [ -f $CART_INSTANCE_DIR/pid/memcached.pid ]; then
      memcached_pid=`$CART_INSTANCE_DIR/pid/memcached.pid 2> /dev/null`
      myid=`id -u`
      if `ps --pid $memcached_pid 2>&1 | grep memcached > /dev/null 2>&1`  ||  \
         `pgrep -x memcached -u $myid > /dev/null 2>&1`; then
         return 0
      fi
   fi

   return 1

}  #  End of function  _is_service_running.


function _service_status() {
   if _is_service_running; then
      echo "$SERVICE_NAME server instance is running" 1>&2
   else
      echo "$SERVICE_NAME server instance is stopped" 1>&2
   fi

}  #  End of function  _service_status.


function _service_start() {
   if _is_service_running; then
      echo "$SERVICE_NAME server instance already running" 1>&2
   else
      pidfile="$CART_INSTANCE_DIR/pid/memcached.pid"
      logfile="$CART_INSTANCE_DIR/log/memcached.log"
      /usr/bin/memcached -d -p $OPENSHIFT_CACHE_PORT -u $OPENSHIFT_APP_UUID  \
                         -m $MEMCACHED_CACHESIZE -c $MEMCACHED_MAXCONN       \
                         -P $pidfile $MEMCACHED_OTHER_OPTIONS > $logfile 2>&1
      wait_to_start_as_user
   fi

}  #  End of function  _service_start.


function _service_stop() {
   if [ -f $CART_INSTANCE_DIR/pid/memcached.pid ]; then
      pid=$( /bin/cat $CART_INSTANCE_DIR/pid/memcached.pid )
   fi

   if [ -n "$pid" ]; then
      /bin/kill $pid
      ret=$?
      if [ $ret -eq 0 ]; then
         TIMEOUT="$STOPTIMEOUT"
         while [ $TIMEOUT -gt 0 ]  &&   \
               [ -f "$CART_INSTANCE_DIR/pid/memcached.pid" ]; do
            /bin/kill -0 "$pid" >/dev/null 2>&1 || break
            sleep 1
            let TIMEOUT=${TIMEOUT}-1
         done
      fi
   else
      if `pgrep -x memcached -u $(id -u)  > /dev/null 2>&1`; then
         echo "Warning: $SERVICE_NAME server instance exists without a pid file.  Use force-stop to kill." 1>&2
      else
         echo "$SERVICE_NAME server instance already stopped" 1>&2
      fi
   fi

}  #  End of function  _service_stop.


function _service_restart() {
   _service_stop
   _service_start

}  #  End of function  _service_restart.


#
# main():
#
# Ensure arguments.
if ! [ $# -eq 1 ]; then
    echo "Usage: $0 [start|restart|stop]"
    exit 1
fi

# Import Environment Variables
for f in ~/.env/*; do
    . $f
done

# Cartridge instance dir and control script name.
CART_INSTANCE_DIR="$OPENSHIFT_HOMEDIR/$CART_DIRNAME"
CTL_SCRIPT="$CART_INSTANCE_DIR/${OPENSHIFT_APP_NAME}_${CART_NAME}_ctl.sh"
source ${CART_INFO_DIR}/lib/util

#  Ensure logged in as user.
if whoami | grep -q root
then
    echo 1>&2
    echo "Please don't run script as root, try:" 1>&2
    echo "runuser --shell /bin/sh $OPENSHIFT_APP_UUID $CTL_SCRIPT" 1>&2
    echo 2>&1
    exit 15
fi

case "$1" in
   start)    _service_start   ;;
   stop)     _service_stop    ;;
   restart)  _service_restart ;;
   status)   _service_status  ;;
esac

