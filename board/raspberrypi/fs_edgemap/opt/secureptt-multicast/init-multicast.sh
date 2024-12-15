#!/bin/sh
ip link set wlan0 multicast off
ip link set wg0 multicast off
ip link set end0 multicast off
ip route add 239.0.0.0/8 dev macsec0
exit 0
