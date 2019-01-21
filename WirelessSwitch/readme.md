# Wireless Connection Backup Switcher

## Network diagram
![Network diagram](https://www.enigma14.eu/wiki/images/thumb/8/8c/Rpi-backup1.png/799px-Rpi-backup1.png)

## Website
https://www.enigma14.eu/wiki/RPi_3G/4G_Wireless_Connection_Backup_Switcher

## Author
Author: Enigmaguy, martin [at] enigma14 [dot] eu

## License

see gpl.txt

## Installation in a nutshell

1. Sudo as root

```rpi ~$ sudo -i```
2. Install pip

```rpi ~# apt-get install pip```
3. Copy all files to /usr/local/ws
```
rpi ~# git clone https://github.com/koss822/misc.git
rpi ~# mkdir -p /usr/local/ws
rpi ~# cp ~/misc/WirelessSwitch /usr/local/ws
```
4. Install python packages
```
rpi ~# cd /usr/local/ws
rpi /usr/local/ws# pip install -r requirements.txt
```
5. Modify install/ifup.sh to your network requirements
    rpi ~# vi /usr/local/ws/install/ifup.sh
    change 192.168.0.1 -> your local lan network gateway
    change 192.168.0.0/24 -> your local lan network address/netmask
    rpi cp /usr/local/ws/install/ifup.sh /etc/network/if-up.d/
7. Create init scripts
    rpi ~# ln -s /usr/local/ws/rpi-init.py /etc/init.d/rpi-init
    rpi ~# chkconfig --add rpi-init
    rpi ~# chkconfig rpi-init on
8. Modify config file
    rpi ~# mv /usr/local/ws/rpi.ini.default /usr/local/ws/rpi.ini
    rpi ~# vi /usr/local/ws/rpi.ini
9. Activate services
    rpi ~# service networking restart
    rpi ~# service rpi-init start
