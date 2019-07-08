#!/bin/bash -x
# usb_backup.sh - see README.md
# https://github.com/koss822/misc/Linux/Projects/usb_backup
# ========================================================================
# GNU GENERAL PUBLIC LICENSE - http://www.gnu.org/licenses/gpl-3.0.en.html
# Author martin@enigma14.eu
# Tested and developed on Xubuntu 14.04
# ========================================================================

BKP_SOURCE=/data
BKP_TARGET=/mnt/backups

# Add this line to /etc/fstab
# ========================================================================
# /dev/mapper/backups /mnt/backups btrfs noauto
# ========================================================================

# Keyfile will make it easier to you mount backups second time
# Always keep keyfile on encrypted drive
# You can generate keyfile with this command:
# dd if=/dev/random of=/root/keyfile bs=2048 count=1

KEYFILE=/root/keyfile

# If you want to exclude some directories from backup
# please update exclude.txt, see exclude.samples for examples

EXCLUDE=exclude.txt

# Clean free space and backup
function backup_and_clean() {
    while true; do
        rsync --exclude-from=$EXCLUDE -av --del --ignore-errors $BKP_SOURCE/* \
            $BKP_TARGET/current/ 2>&1 | tee /tmp/rsync.log
        if ! grep -qi "No space left" /tmp/rsync.log; then
            break
        fi
        # remove old backup
        oldest=$(sudo btrfs subvolume list -a $BKP_TARGET/ | grep snaps \
            | head -n1 | awk '{ print $9 }' | cut -d/ -f2)
        # check we are not removing last backup
        if [ "$backups" = "$taken" ]; then
            read -n1 -r -p  \
                "Do you want to delete last backup, there is no space on device... [y/n]" key
            if [ ! "$key" = "y" ]; then
                echo "No space left, exiting..."
                exit 1
            fi
        fi
        echo "Removing $oldest"
        if ! sudo btrfs subvolume delete $BKP_TARGET/snaps/$oldest; then
            echo "Cannot remove $BKP_TARGET/snaps/$oldest, exiting..."
            exit 1
        fi
    done
}

case "$1" in
    backup)
        taken=`cat $BKP_TARGET/taken`
        if [ -f $BKP_TARGET/taken ]; then
            mkdir -p $BKP_TARGET/snaps
            sudo btrfs subvolume snapshot $BKP_TARGET/current $BKP_TARGET/snaps/$taken
        fi
        date +%Y-%m-%d_%H:%M > $BKP_TARGET/taken
        backup_and_clean
        ;;
    mount)
        sudo cryptsetup luksOpen $2 backups --key-file $KEYFILE
        sudo mount $BKP_TARGET
        sudo chmod 777 $BKP_TARGET/
        ;;
    umount)
        sudo umount $BKP_TARGET
        sudo cryptsetup close backups
        ;;
    format)
        sudo cryptsetup -y -v luksFormat $2
        sudo cryptsetup luksAddKey $2 $KEYFILE
        sudo cryptsetup luksOpen $2 backups --key-file $KEYFILE
        sudo mkfs.btrfs /dev/mapper/backups
        mount $BKP_TARGET
        sudo btrfs subvolume create $BKP_TARGET/current
        sudo chown -R $USER:$USER $BKP_TARGET
        umount $BKP_TARGET
        sudo cryptsetup close backups
        ;;
    *)
        echo $"Usage: $0 {mount /dev/sdX|backup|umount|format /dev/sdX}"
        echo $"For find usb drive use lsblk command"
esac
