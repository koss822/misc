# USB drive backup tool

## Description

This tool allow you to backup volumes attached to Linux machine to USB drive with encryption and snapshots.

## Installation
1. Create your keyfile for encryption
~~~~
dd if=/dev/random of=/root/keyfile bs=2048 count=1
~~~~

2. Add this line to your /etc/fstab
~~~~
/dev/mapper/backups /mnt/backups btrfs noauto
~~~~

3. Format your usb drive
~~~~
lsblk (find your usb drive)
./usb_backup.sh format /dev/sdX
~~~~

4. Modify PATH settings in usb_backup.sh
~~~~
BKP_SOURCE=/data
~~~~

## Usage

1. Mount drive
~~~~
lsblk (find your USB drive)
./usb_backup.sh mount /dev/sdX
~~~~

2. Backup
~~~~
./usb_backup.sh backup
~~~~

3. Umount USB drive
~~~~
./usb_backup.sh umount
~~~~
