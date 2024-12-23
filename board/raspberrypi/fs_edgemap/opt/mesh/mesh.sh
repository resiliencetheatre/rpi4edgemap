#!/bin/sh
INTERFACE=wlan0
MESH_IP=192.168.10.2
ip link set $INTERFACE down
ip addr del $MESH_IP/32 dev $INTERFACE
iwconfig $INTERFACE mode ad-hoc channel 11 essid "mesh"
ip addr add $MESH_IP dev $INTERFACE
ip link set $INTERFACE up
# sleep 5
# babeld $INTERFACE
exit 0
