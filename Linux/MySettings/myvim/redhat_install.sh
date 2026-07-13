#!/bin/bash
cd /tmp
git clone https://github.com/koss822/misc.git
cd misc/Linux/MySettings/myvim
mv /etc/vimrc /etc/vimrc.old 2>/dev/null
cp -R vim /etc
ln -s /etc/vim/vimrc /etc/vimrc
rm -rf /tmp/misc

# Czech spellcheck dictionary (vimrc má spelllang=cs,en), do domova skutečného uživatele
TARGET_HOME=$(getent passwd "${SUDO_USER:-$USER}" | cut -d: -f6)
sudo -u "${SUDO_USER:-$USER}" mkdir -p "$TARGET_HOME/.vim/spell"
sudo -u "${SUDO_USER:-$USER}" curl -fsSL -o "$TARGET_HOME/.vim/spell/cs.utf-8.spl" https://ftp.nluug.nl/vim/runtime/spell/cs.utf-8.spl
sudo -u "${SUDO_USER:-$USER}" curl -fsSL -o "$TARGET_HOME/.vim/spell/cs.utf-8.sug" https://ftp.nluug.nl/vim/runtime/spell/cs.utf-8.sug
