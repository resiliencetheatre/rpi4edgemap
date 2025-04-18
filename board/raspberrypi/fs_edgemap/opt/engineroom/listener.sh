#!/bin/sh
#
# fifo pipe reader, implements functions towards system
# 
# ui menu (main.js: engine() ) -> engine.php -> fifo -> listener.sh
#
FIFO_PATH="/tmp/engine"
mkfifo $FIFO_PATH
chmod 777 $FIFO_PATH

FIFO_PATH_FROM="/tmp/fromengine"
mkfifo $FIFO_PATH_FROM
chmod 777 $FIFO_PATH_FROM

echo "Listening for messages ( $FIFO_PATH )"
while true; do
    if IFS= read -r line < "$FIFO_PATH"; then
       
        echo "Received: $line"
        
        # Placeholders
        if [ "$line" == "poweroff" ]; then
            echo "poweroff"
            #sync
            #poweroff
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
        
        # Writing settings values back to system from UI (work in progress)
        first_item=$(echo "$line" | cut -d',' -f1)

        if [ "$first_item" = "settings_save" ]; then
            # Assign following items to variables using cut
            CALLSIGN=$(echo "$line" | cut -d',' -f2)
            GPS_PORT=$(echo "$line" | cut -d',' -f3)
            var3=$(echo "$line" | cut -d',' -f4)
            MESHTASTIC_PORT=$(echo "$line" | cut -d',' -f5)

            # echo "Message:         $first_item"
            # echo "callsign:        $CALLSIGN"
            # echo "GPS port:        $GPS_PORT"
            # echo "IRC server:      $var3"
            # echo "Meshtastic port: $MESHTASTIC_PORT"

            # TODO: Do some sanity checking to provided data
            
            # callsign
            echo $CALLSIGN > /opt/edgemap-persist/callsign.txt
            
            # gpsd port
            echo "DEVICES=\"$GPS_PORT\"" >  /etc/default/gpsd
            echo "GPSD_OPTIONS=\"\"" >>  /etc/default/gpsd

            # meshtastic port
            echo "MESHTASTIC_PORT=\"$MESHTASTIC_PORT\""> /opt/edgemap/meshpipe/meshtastic.env
        
            # TODO: Service restart
        
        fi
        
        
        
        # Fetch setting values from system to UI
        if [ "$line" == "read_settings" ]; then
            # serial ports on system
            list=""
            for dev in /dev/ttyUSB* /dev/ttyACM*; do
                if [ -e "$dev" ]; then
                    [ -n "$list" ] && list="$list,"
                    list="$list\"$dev\""
                fi
            done
            
            # read callsign, meshtastic port and GPS port
            CALLSIGN=$(cat /opt/edgemap-persist/callsign.txt)
            MESHTASTIC_PORT=$(grep '^MESHTASTIC_PORT=' /opt/edgemap/meshpipe/meshtastic.env | cut -d= -f2 | tr -d '"')
            GPS_PORT=$(grep '^DEVICES=' /etc/default/gpsd | cut -d= -f2- | tr -d '"')
            
            # read GPS service state
            # read meshtastic service state
            # read ircpipe ini and service state (not done yet)
            # restart services
            
            # form json
            message="{ \"callsign\": [\"$CALLSIGN\"], \"serials\":[$list], \"meshtastic_port\": [\"$MESHTASTIC_PORT\"], \"gps_port\": [\"$GPS_PORT\"] }"
            # deliver json via FIFO pipe
            echo $message > /tmp/fromengine
        fi
        
    fi
done


