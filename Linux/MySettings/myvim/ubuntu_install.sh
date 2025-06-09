#!/bin/bash
cd /tmp
git clone https://github.com/koss822/misc.git
cd misc
cp -R Linux/MySettings/myvim/* /etc
ln -s /etc/vimrc /etc/vim/vimrc
mv /usr/share/vim/vimrc /usr/share/vim/vimrc.old
ln -s /etc/vimrc /usr/share/vim/vimrc
rm -rf /tmp/misc
