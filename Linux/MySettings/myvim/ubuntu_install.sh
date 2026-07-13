#!/bin/bash
cd /tmp
git clone https://github.com/koss822/misc.git
cd misc/Linux/MySettings/myvim
mv /etc/vim/vimrc /etc/vim/vimrc.old
cp -R vim /etc
mkdir -p /usr/share/vim/
mv /usr/share/vim/vimrc /usr/share/vim/vimrc.old 2>/dev/null
ln -s /etc/vim/vimrc /usr/share/vim/vimrc
rm -rf /tmp/misc
update-alternatives --set editor /usr/bin/vim.basic

# Czech spellcheck dictionary (vimrc má spelllang=cs,en), do domova skutečného uživatele
TARGET_HOME=$(getent passwd "${SUDO_USER:-$USER}" | cut -d: -f6)
sudo -u "${SUDO_USER:-$USER}" mkdir -p "$TARGET_HOME/.vim/spell"
sudo -u "${SUDO_USER:-$USER}" curl -fsSL -o "$TARGET_HOME/.vim/spell/cs.utf-8.spl" http://ftp.vim.org/pub/vim/runtime/spell/cs.utf-8.spl
sudo -u "${SUDO_USER:-$USER}" curl -fsSL -o "$TARGET_HOME/.vim/spell/cs.utf-8.sug" http://ftp.vim.org/pub/vim/runtime/spell/cs.utf-8.sug
