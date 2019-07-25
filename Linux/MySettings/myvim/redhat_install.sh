#!/bin/bash
cd /tmp
git clone https://github.com/koss822/misc.git
cd misc
mv /etc/vimrc /etc/vimrc.old
cp -R Linux/MySettings/myvim/* /etc
rm -rf /tmp/misc
