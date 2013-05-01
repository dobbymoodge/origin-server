<?php
/**
 * If the domain name of the community is different than the
 * OpenShift server, uncomment this line and set it to the
 * base URL of the OpenShift server.
 */
//$conf['redhat_sso_host_url'] = 'https://openshift.redhat.com';

//$conf['redhat_sso_register_uri'] = '/app/account/new';
//$conf['redhat_sso_change_password_uri'] = '/app/account/password/new';

/**
 * If the domain name of the community is different than the
 * OpenShift server, uncomment this line and set it to the
 * assets URL of the OpenShift server.  If left commented it will
 * default to the value of <redhat_sso_host_url>/app/assets.
 */
//$conf['openshift_assets_url'] = 'https://openshift.redhat.com/app/assets';

$conf['redhat_sso_enabled'] = true;

/**
 * If true, will not check the password for a login.  Only use
 * in development mode.
 */
$conf['redhat_sso_skip_password'] = true;

/**
 * The Streamline API server base URL
 */
$streamline_host = 'https://streamline-proxy1.ops.rhcloud.com';

$conf['redhat_sso_login_url'] = $streamline_host . '/wapps/streamline/login.html';
$conf['redhat_user_info_url'] = $streamline_host . '/wapps/streamline/userInfo.html';
$conf['redhat_user_info_secret_key'] = 'sw33tl1Qu0r';

# Enable memcached for devenv
$conf['memcache_servers'] = array(
  '127.0.0.1:11211' => 'default',
  '127.0.0.1:11212' => 'default'
);
$conf['cache_inc'] ='sites/all/modules/memcache/memcache.inc';
?>
