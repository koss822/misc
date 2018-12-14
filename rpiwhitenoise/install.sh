#!/bin/bash
# EXEC - curl -L http://bit.ly/rpiwhitenoise | bash
sudo apt install mpg123
sudo systemctl enable autologin@tty1.service
sudo systemctl start ssh
sudo systemctl enable ssh
wget https://s3-eu-west-1.amazonaws.com/koss-public-misc/github/fan.mp3
wget https://raw.githubusercontent.com/koss822/misc/master/rpiwhitenoise/fan.sh
chmod +x fan.sh
echo "./fan.sh" >> ~/.bashrc
sudo reboot
