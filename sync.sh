#!/bin/sh
sudo apt-get update
sudo apt-get install rsync zsh -y
chsh -s /usr/bin/zsh
rsync -a --delete --info=progress2 td@desktop:/home/td/Documents/ /home/td/Documents/
sudo snapper create -d post-sync

