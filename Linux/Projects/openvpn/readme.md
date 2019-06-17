# OpenVPN configuration generator and restart script

## Intro

Ok, here is the quick intro. I was solving problem how to create my own VPN network where all clients on VPN can communicate internally between them even if there is not set-up default gateway. OpenVPN supports something like network topology where all clients are on the same subnet.

So I created my own script which is quite unique in one-way. It uses only one YAML configuration file. After you edit thus YAML you just run the python script and it will generetaes all neccessary config files which you can distribute between machines.

I also had an issue that VPNs sometimes crashed and stopped working so I created an automatic restart scripts for Windows and Linux which just ping VPN gateway and if it is unreachable it will restarts VPNs.

You can see documentation on MediaWiki site below.

# Sketch

![Sketch](https://raw.githubusercontent.com/koss822/misc/master/imgs/openvpn.png "OpenVPN diagram")

## Links
- https://www.enigma14.eu/wiki/OpenVPN_config_generator
- https://www.enigma14.eu/wiki/OpenVPN_Windows_auto-restart
- https://www.enigma14.eu/wiki/OpenVPN_Linux_auto-restart

## Directory structure
    .
    ├── conf_generator
    │   ├── genkey.py
    │   ├── readme.md
    │   └── vpn.yml
    └── restart
        ├── linux
        │   ├── openvpn-restart.service
        │   └── restart_openvpn.py
        └── win
            ├── OpenVPNAutoRestart.ps1
    
