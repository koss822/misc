# Martin Konicek's repository

## About
Reliable and trustworthy B2B DevOps services
see https://www.martinkonicek.eu/

## Docker & Kubernetes
![Logo](https://raw.githubusercontent.com/koss822/misc/master/imgs/frontlogos/moby-logo.png "Docker logo")
- [**docker-selenium-firefox**](https://github.com/koss822/misc/blob/master/Docker/selenium-firefox) - (created June/19/2022) Docker image for headless scrapping with Python, Selenium and Firefox

## Python
![Logo](https://raw.githubusercontent.com/koss822/misc/master/imgs/frontlogos/python.png "Python logo")
- [**yahoo-scraper**](https://github.com/koss822/misc/blob/master/Python/yahoo-scraper/) - (created March/23/2021) Simple yahoo finance scraper to download financial data and convert them to currency you need (using Google Chrome and Docker)
- [**tapo-watchdog**](https://github.com/koss822/misc/blob/master/Python/tapo-watchdog/) - (created May/7/2021) Sometimes modem stop responding and you need to restart it. For this purpose I have created an automation which uses TP-Link Tapo P100 power socket to reboot modem 

## [Aws](https://github.com/koss822/misc/tree/master/Aws)
![Logo](https://raw.githubusercontent.com/koss822/misc/master/imgs/frontlogos/aws.png "AWS logo")
- [**route53-healthcheck-instance-reboot**](https://github.com/koss822/misc/blob/master/Aws/route53-healthcheck-instance-reboot/) - (created May/25/2020) This is a SAM application which watches Route53 HealthCheck and when it goes to ALARM state it reboots specified ec2 instance.
- [**dht11**](https://github.com/koss822/misc/tree/master/Aws/dht11) - (updated Feb/2020) - DHT11 utilities for Raspberry Pi which reports temperature and humidity into AWS Cloudwatch
- [**s3logs**](https://github.com/koss822/misc/tree/master/Aws/s3logs) - Few tools to upload S3 access logs to MySQL database using AWS Lambda and SQS
- [**HTTP HealthCheck Reboot Tool**](https://github.com/koss822/misc/blob/master/Aws/website_check/) - Simple lambda script to check availability of HTTP webserver and in case of unreachability reboot it. **OBSOLETE** (replaced with route53-healthcheck-instance-reboot)
- [**APC_UPS**](https://github.com/koss822/misc/blob/master/Aws/apcupsarn/) - Script for sending alerts when there is a power outage through AWS SNS to your Email or Mobile

## [Linux](https://github.com/koss822/misc/tree/master/Linux)
![Logo](https://raw.githubusercontent.com/koss822/misc/master/imgs/frontlogos/tux.png "Linux logo")
### [MySettings](https://github.com/koss822/misc/tree/master/Linux/MySettings)
- [**mygit**](https://github.com/koss822/misc/tree/master/Linux/MySettings/mygit) - allow caching password in memory, basic gitignore file for VIM editor, shell prompt settings for Bash
- [**myvim**](https://github.com/koss822/misc/tree/master/Linux/MySettings/myvim) - my VIM configuration, optimized for Python development
- [**myvnc**](https://github.com/koss822/misc/tree/master/Linux/MySettings/myvnc) - my TightVNC configuration for Lubuntu or other Ubuntu versions, tested on 18.04 with LXDE
### [Ansible](https://github.com/koss822/misc/tree/master/Linux/Ansible)
![Logo](https://raw.githubusercontent.com/koss822/misc/master/imgs/frontlogos/ansible.png "Ansible logo")
- [**smtp**](https://github.com/koss822/misc/tree/master/Linux/Ansible/smtp) - tutorial how to set-up SMTP relay with Ansible on Ubuntu 18.04

### [Projects](https://github.com/koss822/misc/tree/master/Linux/Projects)
![Logo](https://raw.githubusercontent.com/koss822/misc/master/imgs/frontlogos/openvpn.png "OpenVPN logo")
- [**openvpn**](https://github.com/koss822/misc/tree/master/Linux/Projects/openvpn) - OpenVPN generator of configuration and keys based on single YAML file. There are also attached tools for automatic restart of OpenVPN client on Windows and Linux systems
- [**sshtunnel-daemon**](https://github.com/koss822/misc/tree/master/Linux/Projects/sshtunnel-daemon) - Simple docker image to allow creation of stable SSH tunnels with single YAML file configuration
- [**usb_backup**](https://github.com/koss822/misc/tree/master/Linux/Projects/usb_backup) - Simple script for backup hard drive to USB drive using Btrfs file system, snapshots and LUKS encryption
- [**dante_socks**](https://github.com/koss822/misc/tree/master/Linux/Projects/dante_socks) - Dante Socks RPM package for Dante Socks proxy installation

## [RaspberryPi](https://github.com/koss822/misc/tree/master/RaspberryPi)
![Logo](https://raw.githubusercontent.com/koss822/misc/master/imgs/frontlogos/raspberry.png "Rpi logo")
- [**WirelessSwitch**](https://github.com/koss822/misc/tree/master/RaspberryPi/WirelessSwitch) - Utility to switch between WiFi and 3G/4G/LTE connection on RaspberryPi in case of network failure
- [**ad_pcf8591**](https://github.com/koss822/misc/tree/master/RaspberryPi/ad_pcf8591) - Chip for measuring voltage (mainly of 12V battery)
- [**rpi_usb_stick**](https://github.com/koss822/misc/tree/master/RaspberryPi/rpi_usb_stick) - Raspbian settings for 3G modem Huawei E173
- [**rpiwhitenoise**](https://github.com/koss822/misc/tree/master/RaspberryPi/rpiwhitenoise) - Tools for generating whitenoise (FAN) on RaspberryPi

## [imgs](https://github.com/koss822/misc/tree/master/imgs)
Various images and screenshots

## License
see [gpl.txt](https://github.com/koss822/misc/blob/master/gpl.txt)


