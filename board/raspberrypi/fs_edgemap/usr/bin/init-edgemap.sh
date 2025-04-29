#!/bin/sh
#
# This script will initialize freshly flashed edgemap microsd for you.
#
# It's evolved from tls-setup.sh
#
# Functions
#
# * CA and certificate creation
# * Sets callsign to various places (hostapd, dnsmasq, cryptpad)
# * Sets services to initial state
# * Creates cryptpad and thelounge users
# * Creates third partition to microsd for maps
#
#
# * CA certificate (myCA.crt) is copied to web server document root
#   so user can download and install it to web browser.
# * DNS name is equipped as wifi AP name to /etc/hostapd.conf
# * DNS name is equipped to /etc/dnsmasq.conf and /etc/dnsmasq.hosts
# * DNS name is used as /etc/hostname
# * DNS name is used at /opt/rnslink/rnslink.ini
#   NOTE: ID Number must be modified by hand!
#
# Example run:
#
# ./init-edgemap.sh myedgeCA edgemapx
#
#
# NOTE: This whole CA and certificate world is screwed and it does 
#       create security only against lowest level of adversary.
# 
#       Will most probably drop TLS on wire at some point. Currently
#       it's needed because browser geolocate and webRTC. If you don't
#       use those (and you should not) - go to http alone. You should
#       be in your local segment anyhow in real use. And if you require
#       security to your local segment, use macsec or something better
#       than TLS.
#
#
#
#


#
# Create CA and sign certificate
#

CA_NAME=$1
DNS_NAME=$2

if [ -z "$CA_NAME" ]
then
echo "Usage: init-edgemap.sh [CA-NAME] [DNS-NAME]"
exit
else
echo "CA name: $CA_NAME"
fi

if [ -z "$DNS_NAME" ]
then
echo "Usage: init-edgemap.sh [CA-NAME] [DNS-NAME]"
exit
else
echo "DNS: $DNS_NAME"
fi


#
# Create CA
#
openssl req -x509 -new -nodes -newkey rsa:2048 -keyout myCA.key \
  -sha256 -days 365 -out myCA.crt -subj /CN=$CA_NAME

#
# Create CSR
#
openssl req -newkey rsa:2048 -nodes -keyout edgemap.key -out edgemap.csr \
  -subj /CN=edgemap -addext subjectAltName=DNS:$DNS_NAME
#
# Sign
#
openssl x509 -req -in edgemap.csr -copy_extensions copy \
  -CA myCA.crt -CAkey myCA.key -CAcreateserial -out edgemap.crt -days 365 -sha256

#
# Copy files in place for web server and gwsocket daemons
#
cp myCA.crt edgemap.crt edgemap.key /etc/apache2

#
# Copy CA for client download via http://edgemap/myCA.crt
#
cp myCA.crt /usr/htdocs/

#
# Set wifi AP name
#
sed -i "s/^ssid=.*/ssid=${DNS_NAME}/" /etc/hostapd.conf

#
# Set /etc/dnsmasq.hosts and /etc/hostname
#
echo "10.1.1.1 $DNS_NAME" > /etc/dnsmasq.hosts
echo $DNS_NAME > /etc/hostname

#
# Set /etc/dnsmasq.conf
#
sed -i "s/^local=.*/local=\/${DNS_NAME}\//" /etc/dnsmasq.conf

#
# Set /opt/rnslink/rnslink.ini
#
sed -i "s/^callsign=.*/callsign=${DNS_NAME}/" /opt/rnslink/rnslink.ini

echo " "
echo "Remember to edit /opt/rnslink/rnslink.ini and change node_id manually"
echo "if you configure reticulum in use. Reticulum is disabled by default"
echo "and it is work in progress status..."
echo " "

#
# /opt/ircpipe/ircpipe.ini 
#

sed -i -E "s/^[[:space:]]*user[[:space:]]*=[[:space:]]*.*/user = ${DNS_NAME}/" /opt/ircpipe/ircpipe.ini
sed -i -E "s/^[[:space:]]*nick[[:space:]]*=[[:space:]]*.*/nick = ${DNS_NAME}/" /opt/ircpipe/ircpipe.ini
sed -i -E "s/^[[:space:]]*channel[[:space:]]*=[[:space:]]*.*/channel = #edgemap/" /opt/ircpipe/ircpipe.ini

echo "Configured: /opt/ircpipe/ircpipe.ini"

#
# cryptpad
#
cp /opt/cryptpad/config/config.example.js /opt/cryptpad/config/config.js
sed -i -E "s|^[[:space:]]*httpUnsafeOrigin:[[:space:]]*.*|httpUnsafeOrigin: 'http://${DNS_NAME}:3000',|" /opt/cryptpad/config/config.js
sed -i -E "s|^[[:space:]]*//[[:space:]]*httpAddress:[[:space:]]*'[^']*',?|httpAddress: '0.0.0.0',|" /opt/cryptpad/config/config.js

echo "Configured: /opt/cryptpad/config/config.js"
echo "NOTE: Cryptpad is work in progress"

#
# Configure services as you like
#
rm /etc/systemd/system/multi-user.target.wants/i2pd.service
rm /etc/systemd/system/multi-user.target.wants/babeld.service
rm /etc/systemd/system/multi-user.target.wants/mysqld.service
rm /etc/systemd/system/multi-user.target.wants/pttcomm-multicast*
rm /etc/systemd/system/multi-user.target.wants/janus.service
ln -s /etc/systemd/system/mirror.service /etc/systemd/system/multi-user.target.wants/mirror.service
ln -s /etc/systemd/system/wss-mirror.service /etc/systemd/system/multi-user.target.wants/wss-mirror.service

echo "Services configured!"

echo "Adding cryptpad and thelounge users"

#
# Cryptpad user
#
adduser -H -h /opt/cryptpad/ -D cryptpad cryptpad
chown -R cryptpad:cryptpad /opt/cryptpad

#
# The lounge user
#
adduser -H -h /opt/thelounge/ -D thelounge thelounge
chown -R thelounge:thelounge /opt/thelounge

#
# Create third partition (taken from create-partition-noenc.sh)
# 

if [ -b /dev/mmcblk0p3 ]; then
    echo "It seems that your card has already third partition (/dev/mmcblk0p3)!"
    echo "-> Skipping partition create."
else
    echo "Creating third partition (without encryption) to MicroSD"
    TARGET_DEV=/dev/mmcblk0
    parted --script $TARGET_DEV 'mkpart primary ext4 3500 -1'
    # Creating filesystems
    echo "Creating filesystem to $TARGET_DEVp3"
    mkfs.ext4 -F -L maps ${TARGET_DEV}p3
fi





#
# Instruct cryptpad first run to finalize setup
#
echo " "
echo "== CRYPTPAD =="
echo " "
echo "To finalize cryptpad setup, you need manually do following:"
echo "(or you can ignore this, if you plan not to use cryptpad)"
echo " "
echo "systemctl stop cryptpad "
echo "su cryptpad"
echo "cd"
echo "node server.js"
echo " "
echo " -> Visit indicated setup URL and create admin user & password"
echo " -> After you are good, you can enable service:"
echo " "
echo "systemctl enable cryptpad.service"
echo " "
echo "You can do this now or after reboot"
echo " "
echo "== The Lounge (browser based IRC client) =="
echo " "
echo "Before using Thelounge, configure it via  /opt/thelounge/config.js"
echo "Remember you need to be 'thelounge' user to use 'thelounge' command:"
echo " "
echo "su thelounge"
echo "cd"
echo "thelounge help"
echo " "
echo " "
echo " "
echo "All set, reboot unit."
echo " "
