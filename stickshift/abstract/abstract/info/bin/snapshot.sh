#!/bin/bash

# Import Environment Variables
for f in ~/.env/*
do
    . $f
done

# Run pre-dump dumps
for cmd in `awk 'BEGIN { for (a in ENVIRON) if (a ~ /_DUMP$/) print ENVIRON[a] }'`
do
    echo "Running extra dump: $(/bin/basename $cmd)" 1>&2
    $cmd
done

# stop
stop_app.sh 1>&2

# Run tar, saving to stdout
cd ~
cd ..
echo "Creating and sending tar.gz" 1>&2
/bin/tar --ignore-failed-read -czf - \
        --exclude=./$OPENSHIFT_APP_UUID/.tmp \
        --exclude=./$OPENSHIFT_APP_UUID/.ssh \
        --exclude=./$OPENSHIFT_APP_UUID/$OPENSHIFT_APP_NAME/${OPENSHIFT_APP_NAME}_ctl.sh \
        --exclude=./$OPENSHIFT_APP_UUID/$OPENSHIFT_APP_NAME/conf.d/stickshift.conf \
        --exclude=./$OPENSHIFT_APP_UUID/$OPENSHIFT_APP_NAME/run/httpd.pid \
        ./$OPENSHIFT_APP_UUID

# Cleanup
for cmd in `awk 'BEGIN { for (a in ENVIRON) if (a ~ /_DUMP_CLEANUP$/) print ENVIRON[a] }'`
do
    echo "Running extra cleanup: $(/bin/basename $cmd)" 1>&2
    $cmd
done


# start_app
start_app.sh 1>&2
