#!/bin/bash
cd /tmp
git clone https://github.com/koss822/misc.git
cd misc
cp -R myvim/* /etc
mv /usr/share/vim/vimrc /usr/share/vim/vimrc.old
ln -s /etc/vimrc /usr/share/vim/vimrc
