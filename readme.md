# Martin Konicek's repository

## About
- Personal website - [www.martinkonicek.eu](https://www.martinkonicek.eu/)

## [Home Set-Up](https://github.com/koss822/misc/tree/master/Home)
<img src="https://raw.githubusercontent.com/koss822/misc/master/imgs/diagrams/homesetup.drawio.png" alt="diagram" /><br />

## Docker & Kubernetes
<img src="https://raw.githubusercontent.com/koss822/misc/master/imgs/logos-svg/docker.svg" alt="Docker logo" width="100" height="100"/><br />
- [**docker-selenium-firefox**](https://github.com/koss822/misc/blob/master/Docker/selenium-firefox) - Docker image for headless scrapping with Python, Selenium and Firefox
- [**mikrotik-exporter**](https://github.com/koss822/mktxp) - Kubernetes version of Mikrotik mktxp exporter with builded image through CI/CD pipeline GitHub actions saved on Docker.IO
- [**blackbox-exporter**](https://github.com/koss822/misc/blob/master/Kubernetes/website-monitoring/blackbox.yml) - Blackbox exporter for Kubernetes (monitor websites in Grafana)
- [**cnb-prometheus-exporter**](https://github.com/koss822/misc/blob/master/Kubernetes/cnb-prometheus-exporter) - CNB exporter for Prometheus (monitor exchange rates in Grafana)
- [**sp500-prometheus-exporter**](https://github.com/koss822/misc/blob/master/Kubernetes/sp500exporter) - SP500 exporter for Prometheus
- [**slack-alarm**](https://github.com/koss822/misc/blob/master/Kubernetes/slack-alarm) - Notification of IKEA Parasoll door/window sensor to slack
- [**sops**](https://github.com/koss822/misc/blob/master/Kubernetes/sops) - SOPS Git Hooks for Kubernetes Secrets Management
- [**pod-by-pid**](https://github.com/koss822/misc/blob/master/Kubernetes/pod-by-pid) - A Script to Find the Kubernetes Pod Associated with a Process (PID) on MicroK8s
- [**plantuml**](https://github.com/koss822/misc/blob/master/Kubernetes/plantuml) - (created June/2025) Docker image for PlantUML Server optimized for Kubernetes deployments. Includes built-in health checks and security hardening.

## Python
<img src="https://raw.githubusercontent.com/koss822/misc/master/imgs/logos-svg/python.svg" alt="logo" width="100" height="100"/><br />
- [**yahoo-scraper**](https://github.com/koss822/misc/blob/master/Python/yahoo-scraper/) - (created March/23/2021) Simple yahoo finance scraper to download financial data and convert them to currency you need (using Google Chrome and Docker)
- [**tapo-watchdog**](https://github.com/koss822/misc/blob/master/Python/tapo-watchdog/) - (created May/7/2021) Sometimes modem stop responding and you need to restart it. For this purpose I have created an automation which uses TP-Link Tapo P100 power socket to reboot modem 

## [Aws](https://github.com/koss822/misc/tree/master/Aws)
<img src="https://raw.githubusercontent.com/koss822/misc/master/imgs/logos-svg/aws.svg" alt="logo" width="100" height="100"/><br />
- [**route53-healthcheck-instance-reboot**](https://github.com/koss822/misc/blob/master/Aws/route53-healthcheck-instance-reboot/) - (created May/25/2020) This is a SAM application which watches Route53 HealthCheck and when it goes to ALARM state it reboots specified ec2 instance.
- [**dht11**](https://github.com/koss822/misc/tree/master/Aws/dht11) - (updated Feb/2020) - DHT11 utilities for Raspberry Pi which reports temperature and humidity into AWS Cloudwatch
- [**s3logs**](https://github.com/koss822/misc/tree/master/Aws/s3logs) - Few tools to upload S3 access logs to MySQL database using AWS Lambda and SQS
- [**HTTP HealthCheck Reboot Tool**](https://github.com/koss822/misc/blob/master/Aws/website_check/) - Simple lambda script to check availability of HTTP webserver and in case of unreachability reboot it. **OBSOLETE** (replaced with route53-healthcheck-instance-reboot)
- [**APC_UPS**](https://github.com/koss822/misc/blob/master/Aws/apcupsarn/) - Script for sending alerts when there is a power outage through AWS SNS to your Email or Mobile

## [Linux](https://github.com/koss822/misc/tree/master/Linux)
<img src="https://raw.githubusercontent.com/koss822/misc/master/imgs/logos-svg/linux.svg" alt="logo" width="100" height="100"/><br />
### [MySettings](https://github.com/koss822/misc/tree/master/Linux/MySettings)
- [**mygit**](https://github.com/koss822/misc/tree/master/Linux/MySettings/mygit) - allow caching password in memory, basic gitignore file for VIM editor, shell prompt settings for Bash
- [**myvim**](https://github.com/koss822/misc/tree/master/Linux/MySettings/myvim) - my VIM configuration, optimized for Python development
- [**myvnc**](https://github.com/koss822/misc/tree/master/Linux/MySettings/myvnc) - my TightVNC configuration for Lubuntu or other Ubuntu versions, tested on 18.04 with LXDE
### [Ansible](https://github.com/koss822/misc/tree/master/Linux/Ansible/)
<img src="https://raw.githubusercontent.com/koss822/misc/master/imgs/logos-svg/ansible.svg" alt="logo" width="100" height="100"/><br />
- [**smtp**](https://github.com/koss822/misc/tree/master/Linux/Ansible/smtp) - tutorial how to set-up SMTP relay with Ansible on Ubuntu 18.04
- [**smtp-test**](https://github.com/koss822/misc/tree/master/Linux/Ansible/smtp-test) - send test email using python and smtp
### Tools
- [**bacula**](https://github.com/koss822/misc/tree/master/Linux/Bacula) - Monitor daily backup sizes from Bacula using InfluxDB and Grafana and Nagios plugin to check bacula director running
- [**nagios**](https://github.com/koss822/misc/tree/master/Linux/Nagios) - Nagios NRPE plugins, e.g. for checking running PODs on Kubernetes

### [Projects](https://github.com/koss822/misc/tree/master/Linux/Projects)
<img src="https://raw.githubusercontent.com/koss822/misc/master/imgs/logos-svg/projects.svg" alt="logo" width="100" height="100"/><br />
- [**openvpn**](https://github.com/koss822/misc/tree/master/Linux/Projects/openvpn) - OpenVPN generator of configuration and keys based on single YAML file. There are also attached tools for automatic restart of OpenVPN client on Windows and Linux systems
- [**sshtunnel-daemon**](https://github.com/koss822/misc/tree/master/Linux/Projects/sshtunnel-daemon) - Simple docker image to allow creation of stable SSH tunnels with single YAML file configuration
- [**usb_backup**](https://github.com/koss822/misc/tree/master/Linux/Projects/usb_backup) - Simple script for backup hard drive to USB drive using Btrfs file system, snapshots and LUKS encryption
- [**dante_socks**](https://github.com/koss822/misc/tree/master/Linux/Projects/dante_socks) - Dante Socks RPM package for Dante Socks proxy installation

## [RaspberryPi](https://github.com/koss822/misc/tree/master/RaspberryPi)
<img src="https://raw.githubusercontent.com/koss822/misc/master/imgs/logos-svg/raspberry-pi.svg" alt="logo" width="100" height="100"/><br />
- [**WirelessSwitch**](https://github.com/koss822/misc/tree/master/RaspberryPi/WirelessSwitch) - Utility to switch between WiFi and 3G/4G/LTE connection on RaspberryPi in case of network failure
- [**ad_pcf8591**](https://github.com/koss822/misc/tree/master/RaspberryPi/ad_pcf8591) - Chip for measuring voltage (mainly of 12V battery)
- [**rpi_usb_stick**](https://github.com/koss822/misc/tree/master/RaspberryPi/rpi_usb_stick) - Raspbian settings for 3G modem Huawei E173
- [**rpiwhitenoise**](https://github.com/koss822/misc/tree/master/RaspberryPi/rpiwhitenoise) - Tools for generating whitenoise (FAN) on RaspberryPi

## [Windows](https://github.com/koss822/misc/tree/master/windows)
<img src="https://raw.githubusercontent.com/koss822/misc/master/imgs/logos-svg/windows.svg" alt="logo" width="100" height="100"/><br />
- [**ClearRecentItems**](https://github.com/koss822/misc/tree/master/Windows/clear-recent) - automates the process of clearing recent files from Windows File Explorer and Windows Media Player.

## [3D Print](3Dprinting/)
<img src="https://raw.githubusercontent.com/koss822/misc/master/imgs/logos-svg/print.svg" alt="logo" width="100" height="100"/><br />
- [**3D printing Tips and Tricks**](3Dprinting/) - Tips and Tricks for Creality Ender S1 Pro and Octoprint


## [imgs](https://github.com/koss822/misc/tree/master/imgs)
Various images and screenshots

## Ostatní (Czech)
<img src="https://raw.githubusercontent.com/koss822/misc/master/imgs/logos-svg/projects.svg" alt="logo" width="100" height="100"/><br />
- [**prevodnik-cnb-excel**](https://github.com/koss822/misc/blob/master/Other/cnb-convert-currency/excel) - (vytvořeno Květen/30/2024) Převodník měn pro Excel pomocí VBA skriptu, který načítá aktuální kurzy z webových stránek ČNB a umožňuje převod měn na základě zadaného data a částky.
- [**prevodnik-cnb-google-sheets**](https://github.com/koss822/misc/blob/master/Other/cnb-convert-currency/google-sheets) - (vytvořeno Květen/30/2024) Převodník měn pro Google Sheets pomocí Apps Script, který načítá aktuální kurzy z webových stránek ČNB a umožňuje převod měn na základě zadaného data a částky.

## License
see [gpl.txt](https://github.com/koss822/misc/blob/master/gpl.txt)


