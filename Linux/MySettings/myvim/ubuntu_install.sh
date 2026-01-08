#!/bin/bash
cd /tmp
git clone https://github.com/koss822/misc.git
cd misc
cp -R Linux/MySettings/myvim/* /etc
mv /etc/vim/vimrc /etc/vim/vimrc.old
ln -s /etc/vimrc /etc/vim/vimrc
mkdir -p /usr/share/vim/
mv /usr/share/vim/vimrc /usr/share/vim/vimrc.old 2>/dev/null
ln -s /etc/vimrc /usr/share/vim/vimrc
rm -rf /tmp/misc
update-alternatives --set editor /usr/bin/vim.basic
