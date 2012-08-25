#!/bin/bash

cartridge_type="zend-5.6"
source "/etc/stickshift/stickshift-node.conf"
source "/etc/stickshift/resource_limits.conf"
source ${CARTRIDGE_BASE_PATH}/abstract/info/lib/util

application="$1"
uuid="$2"
IP="$3"

APP_HOME="$GEAR_BASE_DIR/$uuid"
ZEND_INSTANCE_DIR=$(get_cartridge_instance_dir "$cartridge_type")
source "$APP_HOME/.env/OPENSHIFT_REPO_DIR"

cat <<EOF > "$ZEND_INSTANCE_DIR/conf.d/stickshift.conf"
ServerRoot "$ZEND_INSTANCE_DIR"
DocumentRoot "$OPENSHIFT_REPO_DIR/php"
Listen $IP:8080
User $uuid
Group $uuid
ErrorLog "|/usr/sbin/rotatelogs $ZEND_INSTANCE_DIR/logs/error_log$rotatelogs_format $rotatelogs_interval"
CustomLog "|/usr/sbin/rotatelogs $ZEND_INSTANCE_DIR/logs/access_log$rotatelogs_format $rotatelogs_interval" combined
php_value include_path ".:$OPENSHIFT_REPO_DIR/libs/:$ZEND_INSTANCE_DIR/phplib/pear/pear/php/:/usr/share/pear/:$OPENSHIFT_GEAR_DIR/share/ZendFramework/library:$OPENSHIFT_GEAR_DIR/share/pear"
# TODO: Adjust from ALL to more conservative values
<Directory "$OPENSHIFT_REPO_DIR/php">
  AllowOverride All
</Directory>
Include "${ZEND_INSTANCE_DIR}/etc/sites.d/zend-default-vhost-80.conf"
# TODO: Adjust from ALL to more conservative values
<IfModule !mod_bw.c>
    LoadModule bw_module    modules/mod_bw.so
</IfModule>

<ifModule mod_bw.c>
  BandWidthModule On
  ForceBandWidthModule On
  BandWidth $apache_bandwidth
  MaxConnection $apache_maxconnection
  BandWidthError $apache_bandwidtherror
</IfModule>

EOF
