#!/bin/bash
set +x

# Import Environment Variables
for f in ~/.env/*
do
    . $f
done

CART_DIR=$(dirname $(dirname $(dirname $0)))
source ${CART_DIR}/info/bin/load_config.sh
source ${CARTRIDGE_BASE_PATH}/abstract/info/lib/util

if [ -n "$JENKINS_URL" ]
then
	REPO_LINK=${OPENSHIFT_APP_DIR}/runtime/repo
    rm -rf $REPO_LINK
    ln -s ~/$WORKSPACE $REPO_LINK
fi

set_app_state building

user_pre_build.sh

. build.sh

set -x
