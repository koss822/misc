#!/bin/bash
# EXEC - curl http://bit.ly/rpiwhitenoise | sudo bash
apt install mpg123
systemctl enable autologin@tty1.service
wget https://s3-eu-west-1.amazonaws.com/koss-public-misc/github/fan.mp3
wget https://raw.githubusercontent.com/koss822/misc/master/rpiwhitenoise/fan.sh
chmod +x fan.sh
echo "./fan.sh" >> ~/.bashrc
reboot
