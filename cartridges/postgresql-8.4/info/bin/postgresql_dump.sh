#!/bin/bash

# Import Environment Variables
for f in ~/.env/*
do
    . $f
done

CART_DIR=${CART_DIR:=/usr/libexec/li/cartridges}
CART_INFO_DIR=$CART_DIR/embedded/postgresql-8.4/info
source ${CART_INFO_DIR}/lib/util

start_postgresql_as_user

# Dump all databases but remove any sql statements that drop, create and alter
# the admin and user roles.
rexp="^\s*\(DROP\|CREATE\|ALTER\)\s*ROLE\s*\(\"$OPENSHIFT_APP_UUID\"\|admin\).*"
/usr/bin/pg_dumpall -c | sed "/$rexp/d;" |   \
            /bin/gzip -v > $OPENSHIFT_DATA_DIR/postgresql_dump_snapshot.gz

if [ ! ${PIPESTATUS[0]} -eq 0 ]
then
    echo 1>&2
    echo "WARNING!  Could not dump PostgreSQL databases!  Continuing anyway" 1>&2
    echo 1>&2
    /bin/rm -rf $OPENSHIFT_DATA_DIR/postgresql_dump_snapshot.gz
fi
