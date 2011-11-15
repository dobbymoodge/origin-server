#!/bin/bash

# Import Environment Variables
for f in ~/.env/*
do
    . $f
done

CART_DIR=/usr/libexec/li/cartridges
source ${CART_DIR}/li-controller/info/lib/util

client_message "Running 'git gc --prune --aggressive'"
pushd ${OPENSHIFT_HOME_DIR}git/${OPENSHIFT_APP_NAME}.git > /dev/null
git gc --prune --aggressive 
popd > /dev/null

client_message "Emptying log dir: ${OPENSHIFT_LOG_DIR}"
rm -rf ${OPENSHIFT_LOG_DIR}* ${OPENSHIFT_LOG_DIR}.[^.]*

client_message "Emptying tmp dir: ${OPENSHIFT_TMP_DIR}"
rm -rf ${OPENSHIFT_TMP_DIR}* ${OPENSHIFT_TMP_DIR}.[^.]*

if [ -d ${OPENSHIFT_APP_DIR}tmp/ ]
then
    client_message "Emptying tmp dir: ${OPENSHIFT_APP_DIR}tmp/"
    rm -rf ${OPENSHIFT_APP_DIR}tmp/* ${OPENSHIFT_APP_DIR}tmp/.[^.]*
fi