# misc
Misc utilities for Linux, Raspberry Pi, Python, etc...


## My VIM settings
![VIM screenshot](https://raw.githubusercontent.com/koss822/misc/master/imgs/vim-screenshot.png "VIM Screenshot")

### DESCRIPTION
This is my VIM settings. It makes just VIM look better, provide some basic support (e.g. intend, backspace, filename) and all things to be in VIM more comfortable.

### INSTALATION
RedHat/Ubuntu

1. sudo -s
2. git clone https://github.com/koss822/misc.git
3. cd misc
4. cp -R myvim/* /etc

Ubuntu additional steps

5. mv /usr/share/vim/vimrc /usr/share/vim/vimrc.old
6. ln -s /etc/vimrc /usr/share/vim/vimrc

## usb_backup
https://github.com/koss822/misc/tree/master/usb_backup
### DESCRIPTION

I wrote this tool because I needed simple utility which will backup
my hardrive to encrypted USB drive with compression and incremental
backups.

There are many backups tools, but many are too complex for just this
task. I mainly use Btrfs snapshot, compression ability with RSync
to make it really easy

### INFO
#### sudo
You do not need to run this script with sudo, it will ask automatically
If you run it with sudo, use sudo -s to preserve $USER variable

#### btrfs
Btrfs is experimental in terms of performance rather than stability
There are available recovery tools that prevents data loss
It is neccesary to use Btrfs for snapshot, and compression abilities

### USAGE
#### initial
1. generate keyfile
2. edit BKP_SOURCE and BKP_TARGET accordingly in usb_backup.sh
3. ./usb_backup.sh format /dev/sdX
4. edit /etc/fstab, see fstab.sample

#### continuous backups
1. ./usb_backup.sh mount /dev/sdX
2. ./usb_backup.sh backup
3. ./usb_backup.sh umount

## rpi_usb_stick
https://github.com/koss822/misc/tree/master/rpi_usb_stick
### DESCRIPTION

These are configuration files for using Raspberry Pi with 3G modem Huawei E173 from CZ O2 (might works with other E173 models)
You can find more information here:
https://www.enigma14.eu/wiki/RPi_3G_Mobile_connection_with_O2_Huawei_E173_%28CZ%29

## ad_pcf8591
https://github.com/koss822/misc/tree/master/ad_pcf8591
### DESCRIPTION

This is simple modified example to run correctly with pcf8591 AD converter

1. Find AD converter address - i2cdetect -y 1
2. Donwload and install quick2wire library - https://github.com/quick2wire/quick2wire-python-api
3. Run ./pcf8591read 48 1 (where 48 is device address detected by i2cdetect and 1 is input analog port)
