#!/usr/bin/env bash

apt-get update

apt-get -y install rsync
apt-get -y install bash

curl -sL https://deb.nodesource.com/setup_lts.x | bash -
apt install -y nodejs
apt install -y npm
npm install npm@latest -g



