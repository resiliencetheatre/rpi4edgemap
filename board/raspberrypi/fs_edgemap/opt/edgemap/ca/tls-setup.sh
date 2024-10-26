#!/bin/sh
#
# This script will create CA and sign a certificate with it.
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
# ./tls-setup.sh myEdgeCA edgemap8
#

#
# Create CA and sign certificate
#

CA_NAME=$1
DNS_NAME=$2

if [ -z "$CA_NAME" ]
then
echo "Usage: tls-setup.sh [CA-NAME] [DNS-NAME]"
exit
else
echo "CA name: $CA_NAME"
fi

if [ -z "$DNS_NAME" ]
then
echo "Usage: tls-setup.sh [CA-NAME] [DNS-NAME]"
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
echo "Remember to edit /opt/rnslink/rnslink.ini and change node_id manually!"
echo " "

echo " "
echo "Done. Reboot unit."
echo " "
