#!/bin/bash
sudo mv /etc/vim/vimrc /etc/vim/vimrc.old
sudo cp -R vim /etc
sudo mkdir -p /usr/share/vim/
sudo mv /usr/share/vim/vimrc /usr/share/vim/vimrc.old 2>/dev/null
sudo ln -s /etc/vim/vimrc /usr/share/vim/vimrc
sudo update-alternatives --set editor /usr/bin/vim.basic

# Czech spellcheck dictionary (vimrc má spelllang=cs,en)
mkdir -p ~/.vim/spell
curl -fsSL -o ~/.vim/spell/cs.utf-8.spl https://ftp.nluug.nl/vim/runtime/spell/cs.utf-8.spl
curl -fsSL -o ~/.vim/spell/cs.utf-8.sug https://ftp.nluug.nl/vim/runtime/spell/cs.utf-8.sug
