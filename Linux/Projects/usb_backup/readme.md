# USB drive backup tool

## Description

This tool allow you to backup volumes attached to Linux machine to USB drive with encryption and snapshots.

## Used technologies
* btrfs (snapshots)
* luks (encryption)
* rsync

# Benefits
* Uses standard technologies - basically it is just a bash script which you can modify to your requests
* If you have encrypted hard drive you can store encrypted key on it and for backup there is no need to enter password
* Easy restore - just mount drive and copy file from current or dated directory

# How it works?
* Drive is formatted and encrypted as LUKS device with your generated key and passphrase (e.g. if you backup your drive you can use stored key on your hard drive but if you lose your hard drive and encryption key you can use passphrase to decrypt)
* It uses BTRFS for snapshots - on every backup it create a new snapshot and store old snapshot in directory named after a date when it was taken. If there is not enough hard-drive space oldest snapshot is deleted
* It uses rsync to sync drive with newest snapshots

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

3. Restore
Just copy files from mounted folder /mnt/backups/current (or directory named after a date when it was taken)

4. Umount USB drive
~~~~
./usb_backup.sh umount
~~~~
