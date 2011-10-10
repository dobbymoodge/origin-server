#!/bin/bash

libra_server=$1

# Import Environment Variables
for f in ~/.env/*
do
    . $f
done

USED_BUNDLER=false 

JENKINS_ENABLED=false
if [ -f ~/.env/OPENSHIFT_CI_TYPE ]
then
    JENKINS_ENABLED=true
else

    # If the previous and current commits didn't upload .bundle and you have .bundle and vendor/bundle already deployed then store away for redeploy
    # Also adding .openshift/markers/force_clean_build at the root of the repo will trigger a clean rebundle
    if ! git show master:.openshift/markers/force_clean_build > /dev/null 2>&1 && ! git show master:.bundle > /dev/null 2>&1 && ! git show master~1:.bundle > /dev/null 2>&1 && [ -d ${OPENSHIFT_REPO_DIR}.bundle ] && [ -d ${OPENSHIFT_REPO_DIR}vendor/bundle ]
    then
      USED_BUNDLER=true
      echo 'Saving away previously bundled RubyGems'
      rm -rf ${OPENSHIFT_APP_DIR}tmp/.bundle ${OPENSHIFT_APP_DIR}tmp/vendor
      mv ${OPENSHIFT_REPO_DIR}.bundle ${OPENSHIFT_APP_DIR}tmp/
      mv ${OPENSHIFT_REPO_DIR}vendor ${OPENSHIFT_APP_DIR}tmp/
    fi
  
    redeploy_repo_dir.sh
fi

if [ -z "$JENKINS_ENABLED" ]
then
    if $USED_BUNDLER
    then
      echo 'Restoring previously bundled RubyGems (note: you can commit .openshift/markers/force_clean_build at the root of your repo to force a clean bundle)'
      mv ${OPENSHIFT_APP_DIR}tmp/.bundle ${OPENSHIFT_REPO_DIR}
      if [ -d ${OPENSHIFT_REPO_DIR}vendor ]
      then
        mv ${OPENSHIFT_APP_DIR}/tmp/vendor/bundle ${OPENSHIFT_REPO_DIR}vendor/
      else
        mv ${OPENSHIFT_APP_DIR}tmp/vendor ${OPENSHIFT_REPO_DIR}
      fi
      rm -rf ${OPENSHIFT_APP_DIR}tmp/.bundle ${OPENSHIFT_APP_DIR}tmp/vendor
    fi
  
    # If .bundle isn't currently committed and a Gemfile is then bundle install
    if ! git show master:.bundle > /dev/null 2>&1 && [ -f ${OPENSHIFT_REPO_DIR}Gemfile ] 
    then
      echo 'Bundling RubyGems based on Gemfile/Gemfile.lock to deploy/vendor/bundle'
      pushd ${OPENSHIFT_REPO_DIR} > /dev/null
      bundle install --deployment
      popd > /dev/null
    fi
else
    set -e
    echo "Executing Jenkins build."
    echo
    echo "NOTE: If build fails, deployment will halt.  Last previous 'good' build will continue to run."
    echo
    echo "You can track your build at http://${JENKINS_URL}/job/${OPENSHIFT_APP_NAME}-build"
    echo
    jenkins-cli build -s ${OPENSHIFT_APP_NAME}-build 
    set +e
fi

if [ -z "$BUILD_NUMBER" ]
then
    user_build.sh
fi

if [ -z "$JENKINS_ENABLED" ] && [ -z "$BUILD_NUMBER" ]
then
    # Start the app
    start_app.sh
fi

if [ -z "$BUILD_NUMBER" ]
then
    # Not running inside a build
    nurture_app_push.sh $libra_server
fi