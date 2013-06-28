#!/bin/bash
source "/etc/openshift/node.conf"

function openshift_origin_users() {
    grep ":${GEAR_GECOS}:" /etc/passwd | cut -d: -f1 | tr '\n' ' '
}

for u in `openshift_origin_users`; do
    echo $u
    home_file_path="/var/lib/openshift/$u/.env/HOME"
    if [ ! -f $home_file_path ]; then
        echo -n "/var/lib/openshift/$u/" > $home_file_path
        chown root.$u $home_file_path
        chcon "system_u:object_r:openshift_var_lib_t:s0" $home_file_path
    fi
done
