#!/bin/bash

CART_DIR=$(dirname $(dirname $(dirname $0)))
source ${CART_DIR}/info/bin/load_config.sh
source ${CARTRIDGE_BASE_PATH}/abstract/info/lib/util

application="$1"
uuid="$2"
IP="$3"

APP_HOME="$GEAR_BASE_DIR/$uuid"
APP_DIR=`echo $APP_HOME/$application | tr -s /`

cat <<EOF > "$APP_DIR/conf.d/stickshift.conf"
ServerRoot "$APP_DIR"
DocumentRoot "$APP_DIR/repo/php"
Listen $IP:8080
User $uuid
Group $uuid
ErrorLog "|/usr/sbin/rotatelogs $APP_DIR/logs/error_log$rotatelogs_format $rotatelogs_interval"
CustomLog "|/usr/sbin/rotatelogs $APP_DIR/logs/access_log$rotatelogs_format $rotatelogs_interval" combined
php_value include_path ".:$APP_DIR/repo/libs/:$APP_DIR/phplib/pear/pear/php/:/usr/share/pear/"
# TODO: Adjust from ALL to more conservative values
<Directory "$APP_DIR/repo/php">
  AllowOverride All
</Directory>
EOF