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

case "$1" in
    start)
        exec 1>&- # close stdout
        app_ctl_impl.sh start >/dev/null 2>&1
        exec 1>&2 # redirect stdout to stderr
    ;;
    *)
        app_ctl_impl.sh $1
    ;;
esac