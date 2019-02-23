# Raspberry Pi White Noise machine
*fan.mp3 included with automatic install*

![My RPI White noise machine](https://s3-eu-west-1.amazonaws.com/koss-public-misc/images/rpiwhitenoise.jpg)

## Basic Description
If you are living in a flat you probably know it. There is always some noise from neighbours and it is difficult to focus on reading books, sleeping or any other activity which requires focus. So it is usefull to have a white noise machine which for example do sound like a fan which eliminates distractions.

This project is very easy to install and realize. You can buy all components in a computer store and aliexpress and installation is a matter of one command (I made it really easy).

## What you need?
- Raspberry Pi (v1,v2,v3 or any version) connected to internet
- Noobs (v3.0 and higher with SystemD support)
- Raspberry Pi box (search for "Raspberry Pi 3 ABS Case w/ Camera Frame" on [AliExpress](http://www.aliexpress.com/) )
- USB Charger (search for "Travel USB Charger, ORICO DCV-4U 4 Ports" on Ali)
- Speakers (I use Genius SP-HF160 which you can buy on [Alza](http://www.alza.com/) )

## How to install?
1. Follow this [Tutorial](https://www.raspberrypi.org/documentation/installation/installing-images/) and install Raspbian Lite
2. Login to machine with username "pi" and password "raspberry"
3. Run "curl -L http://bit.ly/rpinoise | bash"

## Note
This installation will enable SSH server with default username and password. Either change your password with "passwd" utility or disconnect machine after installation from network.

## FAQ
1. **What will happen after installation?**
Machine will be automatically installed and rebooted. After each boot the noise will be automatically started
2. **Can I change volume?**
Yes, you can, if you edit fan.sh file. But I recommend you to buy speakers with volume control. My recommended speakers costs around 10 USD which is very affordable price and they provide good quality of sound.
3. **Is it safe to install something from internet?**
There are basically no risks. I suppose this machine will be disconnected from network so it won't have access anywhere and only generate sounds.
4. **Can I contact you?**
Yes, I will be very happy if you share with me your experience or questions. You can contact me on martin [at] enigma14 [dot] eu
