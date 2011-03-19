#!/bin/sh
#
#
# Initialize quotas for Libra
#
#
# Get libra_dir configured value
# TODO: MAL 20110317 restore when libra_dir is in it's own filesystem
if [ -f /etc/libra/node.conf ]
then
    . /etc/libra/node.conf
fi

# override if the user requests it explicitly
if [ -n "$1" ]
then
    libra_dir=$1
fi

# default if no one gives you a good answer
# this applies until we get a separate partition for Libra
# because you can't apply quotas to bind mounts
libra_dir=${libra_dir:=/var/lib/libra}

# remove trailing / as they mess up the searches
libra_dir=`echo $libra_dir | tr -s / | perl -p -e 's:(.)/$:$1 :'`

#function get_filesystem() {
#    # $1=libra_dir
#    df $1 | tail -1 | tr -s ' ' | cut -d' ' -f 1
#}

# find the mount point above a given file or directory
function get_mountpoint() {
    df $1 | tail -1 | tr -s ' ' | cut -d' ' -f 6 | sort -u
}

# get the fstab options for a given mount point
function get_fstab_mount_options() {
    cat /etc/fstab | tr -s ' ' | grep " $1 "| awk '{print $4;}'
}

# get the current mount options for a given mount point
function get_current_mount_options() {
    # options are the comma delimited string between parens
    mount | grep " $1 " | sed -e 's/^.*(// ; s/).*$// ' | sort -u
}

#LIBRA_FILESYSTEM=`get_filesystem $libra_dir`
LIBRA_MOUNTPOINT=`get_mountpoint $libra_dir`
QUOTA_FILE=$( echo ${LIBRA_MOUNTPOINT}/aquota.user | tr -s /)


#
# Add quota options to libra filesystem mount
#
function update_fstab() {
    # LIBRA_MOUNTPOINT=$1
    FSTAB_OPTIONS=`get_fstab_mount_options $1`
    QUOTA_OPTIONS=usrjquota=aquota.user,jqfmt=vfsv0
    NEW_OPTIONS=${FSTAB_OPTIONS},${QUOTA_OPTIONS}
    # check before you replace.
    # NOTE: double quotes - Variables are shell-substituted before perl runs
    perl -p -i -e "m: $1 : && s/${FSTAB_OPTIONS}/${NEW_OPTIONS}/" /etc/fstab
}

#
# Initialize the quota database on the filesystem
#
function init_quota_db() {
    # LIBRA_MOUNTPOINT=$1
    # create the quota DB file on the filesystem
    QUOTA_FILE=$(echo $1/aquota.user | tr -s /)
    touch $QUOTA_FILE
    chmod 600 $QUOTA_FILE
    # initialize quota db on the filesystem
    quotacheck -cmuf $1
}


#
# MAIN
#
update_fstab $LIBRA_MOUNTPOINT

# remount to enable
CURRENT_OPTIONS=`get_current_mount_options $LIBRA_MOUNTPOINT`
QUOTA_OPTIONS=usrjquota=aquota.user,jqfmt=vfsv0
# check to avoid doing it again
NEW_OPTIONS=${CURRENT_OPTIONS},${QUOTA_OPTIONS}

mount -o remount,${NEW_OPTIONS} $LIBRA_MOUNTPOINT

init_quota_db $LIBRA_MOUNTPOINT

# enable quotas
quotaon -a