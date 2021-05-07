# Modem watchdog with automatic restart

## Intro
Sometimes modem stop responding and you need to restart it. For this purpose I have created an automation which uses TP-Link Tapo P100 power socket to reboot modem when the ping to specified address (I use Google DNS) is unavailable.

## How it works?
When run it power on Tapo P100 socket (if it was not powered initially, e.g. after power outage) and tries to ping specified IP address. If pings become unavailable it power down and power on the socket. It does it only once before internet become available again to prevent loops.