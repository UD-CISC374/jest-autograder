#!/usr/bin/env bash

add-apt-repository -y ppa:openjdk-r/ppa
apt-get update
apt install -y openjdk-11-jdk

apt-get -y install rsync
apt-get -y install maven
apt-get -y install bash

curl -sL https://deb.nodesource.com/setup_lts.x | bash -
apt install -y nodejs
apt install -y npm
npm install npm@latest -g



