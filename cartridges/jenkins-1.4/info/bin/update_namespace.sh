#!/bin/bash

# Exit on any errors
set -e
#set -x

CART_DIR=/usr/libexec/li/cartridges
CART_INFO_DIR=$CART_DIR/jenkins-1.4/info

source ${CART_DIR}/li-controller/info/lib/selinux
source ${CART_DIR}/li-controller/info/lib/util

load_node_conf

function print_help {
    echo "Usage: $0 app-name new_namespace old_namespace uuid"

    echo "$0 $@" | logger -p local0.notice -t libra_update_namespace
    exit 1
}

[ $# -eq 4 ] || print_help

application="$1"
new_namespace="$2"
old_namespace="$3"
uuid=$4

setup_basic_vars

echo "export JENKINS_URL='http://${application}-${new_namespace}.${libra_domain}/'" > $APP_HOME/.env/JENKINS_URL
. $APP_HOME/.env/OPENSHIFT_INTERNAL_IP
. $APP_HOME/.env/OPENSHIFT_INTERNAL_PORT
export JENKINS_URL="http://$OPENSHIFT_INTERNAL_IP:$OPENSHIFT_INTERNAL_PORT"
. $APP_HOME/.env/JENKINS_USERNAME
. $APP_HOME/.env/JENKINS_PASSWORD
. $APP_HOME/.env/OPENSHIFT_DATA_DIR

#TODO only have this here because some apps in stg might not have this file
echo $JENKINS_PASSWORD > $APP_HOME/.jenkins_password

if ls $APP_DIR/data/jobs/*/config.xml > /dev/null 2>&1
then
    sed -i "s/-${old_namespace}.${libra_domain}/-${new_namespace}.${libra_domain}/g" $APP_DIR/data/jobs/*/config.xml
fi

if ! out=$(runuser --shell /bin/sh "$uuid" -c "runcon -t libra_t -l $mcs_level $CART_INFO_DIR/bin/jenkins-cli reload-configuration --username '$JENKINS_USERNAME' --password-file '${APP_HOME}/.jenkins_password'" 2>&1)
then
    # An error occurred reloading jenkins configuration
    client_message ""
    client_message "Could not reload Jenkins server '${application}' configuration:"
    client_message "   $out"
    client_message "This might be expected if '${application}' isn't running."
    client_message "Otherwise you might need to reload it with 'rhc-ctl-app -a ${application} -c reload'"
    client_message "or by using the Jenkins interface:"
    client_message "http://${application}-${new_namespace}.${libra_domain}/manage"
    client_message ""
fi

add_env_var "JENKINS_URL=http://${application}-${new_namespace}.${libra_domain}/"

