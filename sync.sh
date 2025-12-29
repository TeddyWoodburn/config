#!/bin/sh
sudo apt-get update
sudo apt-get install rsync -y
rsync -ar --delete --info=progress2 td@desktop:/home/td/Documents /home/td/Documents
