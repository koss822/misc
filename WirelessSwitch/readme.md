You can find full documentation on https://www.enigma14.eu/wiki/RPi_3G/4G_Wireless_Connection_Backup_Switcher
Author: Enigmaguy

=========================================================================
WirelessSwitcher is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

WirelessSwitcher is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.
If not, see http://www.gnu.org/licenses/
=========================================================================


1. Sudo as root
rpi# sudo -s
2. Install pip
rpi# apt-get install pip
3. Copy all files to /usr/local/ws
rpi# mkdir -p /usr/local/ws
local# cd /yourpath/WirelessSwitch/
local# scp * rpi:/usr/local/ws
4. Install python packages
rpi# cd /usr/local/ws
rpi# pip install -r requirements.txt
5. Modify install/ifup.sh to your network requirements
local# vi install/ifup.sh
change 192.168.0.1 -> your local lan network gateway
change 192.168.0.0/24 -> your local lan network address/netmask
6. Upload ifup.sh
local# scp install/ifup.sh rpi:/tmp
rpi# mv /tmp/ifup.sh /etc/network/if-up.d
7. Create init scripts
rpi# ln -s /usr/local/ws/rpi-init.py /etc/init.d/rpi-init
rpi# chkconfig --add rpi-init
rpi# chkconfig rpi-init on
8. Modify config file
rpi# mv /usr/local/ws/rpi.ini.default /usr/local/ws/rpi.ini
rpi# vi /usr/local/ws/rpi.ini
9. Activate services
rpi# service networking restart
rpi# service rpi-init start
