#!/bin/bash

# Import Environment Variables
for f in ~/.env/*
do
    . $f
done

standalone_tmp=${OPENSHIFT_APP_DIR}${OPENSHIFT_APP_TYPE}/standalone/tmp
if [ -d $standalone_tmp ]
then
    for d in $standalone_tmp/*
    do
        if [ -d $d ]
        then
            echo "Emptying tmp dir: $d"
            rm -rf $d/* $d/.[^.]*
        fi
    done
fi

user_deploy.sh