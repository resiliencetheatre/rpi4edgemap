#!/bin/sh
#
# fifo pipe reader, implements functions towards system
#
# ui menu (main.js: engine() ) -> engine.php -> fifo -> listener.sh
#
FIFO_PATH="/tmp/engine"
mkfifo $FIFO_PATH
chmod 777 $FIFO_PATH
echo "Listening for messages ( $FIFO_PATH )"
while true; do
    if IFS= read -r line < "$FIFO_PATH"; then
        echo "Received: $line"

        # Placeholders
        if [ "$line" == "poweroff" ]; then
            echo "poweroff"
            sync
            poweroff
        fi
        # off,2,4,10,manual,random
        if [ "$line" == "pos_off" ]; then
            echo off > /opt/edgemap-persist/pos_interval.txt
        fi
        if [ "$line" == "pos_2" ]; then
            echo 2 > /opt/edgemap-persist/pos_interval.txt
        fi
        if [ "$line" == "pos_4" ]; then
            echo 4 > /opt/edgemap-persist/pos_interval.txt
        fi
        if [ "$line" == "pos_10" ]; then
            echo 10 > /opt/edgemap-persist/pos_interval.txt
        fi
        if [ "$line" == "pos_manual" ]; then
            echo manual > /opt/edgemap-persist/pos_interval.txt
        fi
        if [ "$line" == "pos_random" ]; then
            echo random > /opt/edgemap-persist/pos_interval.txt
        fi
    fi
done


