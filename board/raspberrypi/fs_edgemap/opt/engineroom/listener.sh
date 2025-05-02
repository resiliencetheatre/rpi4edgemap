#!/bin/sh
#
# fifo pipe reader, implements system functions
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
        
        # Writing settings values back to system from UI (work in progress)
        first_item=$(echo "$line" | cut -d',' -f1)

        if [ "$first_item" = "settings_save" ]; then
            # Assign following items to variables using cut
            CALLSIGN=$(echo "$line" | cut -d',' -f2)
            GPS_PORT=$(echo "$line" | cut -d',' -f3)
            IRC_SERVER_STRING=$(echo "$line" | cut -d',' -f4)
            MESHTASTIC_PORT=$(echo "$line" | cut -d',' -f5)
            MESSAGING_MEDIUM=$(echo "$line" | cut -d',' -f6)
            
            # echo "Message:         $first_item"
            # echo "callsign:        $CALLSIGN"
            # echo "GPS port:        $GPS_PORT"
            # echo "IRC server:      $IRC_SERVER_STRING"
            # echo "Meshtastic port: $MESHTASTIC_PORT"
            # echo "Messaging medium: $MESSAGING_MEDIUM"


            # Update only non empty and less than 5 char callsign
            if [ -n "$CALLSIGN" ] && [ "${#CALLSIGN}" -le 5 ]; then
                echo $CALLSIGN > /opt/edgemap-persist/callsign.txt
            else
                echo "Ignoring callsign setting"
            fi

            # gpsd 
            if [ "$GPS_PORT" = "-- Select GPS device --" ]; then
                echo "Skipping gpsd port setting"
            else
                if [ "$GPS_PORT" = "No GPS attached" ]; then
                    echo "No GPS, stopping and disabling (gpsd.service gpsd.socket gpsreader.service)"
                    systemctl stop gpsd.service gpsd.socket gpsreader.service
                    systemctl disable gpsd.service gpsd.socket gpsreader.service
                else
                    echo "DEVICES=\"$GPS_PORT\"" >  /etc/default/gpsd
                    echo "GPSD_OPTIONS=\"\"" >>  /etc/default/gpsd
                    echo "Starting & enabling (gpsd.service gps.socket and gpsreader.service)"
                    systemctl start gpsd.service gpsd.socket gpsreader.service
                    systemctl enable gpsd.service gpsd.socket gpsreader.service
                fi                
            fi

            # irc server
            if [ -n "$CALLSIGN" ] && [ -n "$IRC_SERVER_STRING" ]; then
                IRC_SERVER="${IRC_SERVER_STRING%%:*}"
                IRC_SERVER_PORT="${IRC_SERVER_STRING##*:}"
                echo "[irc]" > /opt/ircpipe/ircpipe.ini
                echo "server = $IRC_SERVER" >> /opt/ircpipe/ircpipe.ini
                echo "port = $IRC_SERVER_PORT" >> /opt/ircpipe/ircpipe.ini
                echo "nick = $CALLSIGN" >> /opt/ircpipe/ircpipe.ini
                echo "user = $CALLSIGN" >> /opt/ircpipe/ircpipe.ini
                echo "channel = #edgemap" >> /opt/ircpipe/ircpipe.ini
                echo " " >> /opt/ircpipe/ircpipe.ini
                echo "[fifo]" >> /opt/ircpipe/ircpipe.ini
                echo "in = /tmp/outmessages" >> /opt/ircpipe/ircpipe.ini
                echo "out = /tmp/channelmessages" >> /opt/ircpipe/ircpipe.ini
            fi
            
            # Empty IRC server
            if [ -z "$IRC_SERVER_STRING" ]; then
                IRC_SERVER=""
                IRC_SERVER_PORT=""
                echo "[irc]" > /opt/ircpipe/ircpipe.ini
                echo "server = $IRC_SERVER" >> /opt/ircpipe/ircpipe.ini
                echo "port = $IRC_SERVER_PORT" >> /opt/ircpipe/ircpipe.ini
                echo "nick = $CALLSIGN" >> /opt/ircpipe/ircpipe.ini
                echo "user = $CALLSIGN" >> /opt/ircpipe/ircpipe.ini
                echo "channel = #edgemap" >> /opt/ircpipe/ircpipe.ini
                echo " " >> /opt/ircpipe/ircpipe.ini
                echo "[fifo]" >> /opt/ircpipe/ircpipe.ini
                echo "in = /tmp/outmessages" >> /opt/ircpipe/ircpipe.ini
                echo "out = /tmp/channelmessages" >> /opt/ircpipe/ircpipe.ini
            fi
            

            # Meshtastic
            if [ "$MESHTASTIC_PORT" = "-- Select Meshtastic device --" ]; then
                echo "Skipping meshtastic port setting"
            else
            
                if [ "$MESHTASTIC_PORT" = "No meshtastic radio" ]; then
                    echo "No meshtastic, stopping and disabling (meshpipe.service wss-messaging.service) "
                    systemctl stop meshpipe.service wss-messaging.service 
                    systemctl disable meshpipe.service wss-messaging.service
                else
                    echo "MESHTASTIC_PORT=\"$MESHTASTIC_PORT\""> /opt/edgemap/meshpipe/meshtastic.env
                    echo "Starting & enabling (meshpipe.service and wss-messaging.service)"
                    
                fi
            fi

            # Set messaging medium
            if [ "$MESSAGING_MEDIUM" = "irc" ]; then
                # Switch messaging to IRC:
                systemctl stop meshpipe.service wss-messaging.service
                systemctl disable meshpipe.service wss-messaging.service
                systemctl enable ircpipe.service wss-messaging-irc.service
                systemctl restart ircpipe.service wss-messaging-irc.service
            fi
            if [ "$MESSAGING_MEDIUM" = "meshtastic" ]; then
                # Switch messaging to Meshtastic:
                systemctl stop ircpipe.service wss-messaging-irc.service
                systemctl disable ircpipe.service wss-messaging-irc.service
                systemctl start meshpipe.service wss-messaging.service 
                systemctl enable meshpipe.service wss-messaging.service
            fi
        
        fi

        # Fetch setting values from system to UI
        if [ "$line" == "read_settings" ]; then
            
            # Get serial ports on system
            list=""
            for dev in /dev/ttyUSB* /dev/ttyACM* /dev/ttyAMA*; do
                if [ -e "$dev" ]; then
                    [ -n "$list" ] && list="$list,"
                    list="$list\"$dev\""
                fi
            done
            
            # read callsign, meshtastic port and GPS port
            CALLSIGN=$(cat /opt/edgemap-persist/callsign.txt)
            MESHTASTIC_PORT=$(grep '^MESHTASTIC_PORT=' /opt/edgemap/meshpipe/meshtastic.env | cut -d= -f2 | tr -d '"')
            GPS_PORT=$(grep '^DEVICES=' /etc/default/gpsd | cut -d= -f2- | tr -d '"')
            
            # read meshpipe and ircpipe pid's
            IRCPIPE_PID=$(ps | grep '[i]rcpipe' | awk '{print $1}')
            [ -z "$IRCPIPE_PID" ] && IRCPIPE_PID=0

            MESHPIPE_PID=$(ps | grep '[m]eshpipe.py' | awk '{print $1}')
            [ -z "$MESHPIPE_PID" ] && MESHPIPE_PID=0

            
            # read ircpipe ini start
            INI_FILE="/opt/ircpipe/ircpipe.ini"
            SECTION="irc"
            server=""
            port=""
            in_section=0

            while IFS= read -r line; do
                # Remove leading/trailing spaces
                line=$(echo "$line" | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')

                # Skip empty lines or comments
                [ -z "$line" ] && continue
                echo "$line" | grep -qE '^\s*#' && continue

                # Check for section headers
                case "$line" in
                    \[*\])
                        current_section=$(echo "$line" | sed 's/^\[\(.*\)\]$/\1/')
                        if [ "$current_section" = "$SECTION" ]; then
                            in_section=1
                        else
                            in_section=0
                        fi
                        ;;
                    *)
                        if [ "$in_section" -eq 1 ]; then
                            key=$(echo "$line" | cut -d '=' -f 1 | sed 's/[[:space:]]//g')
                            value=$(echo "$line" | cut -d '=' -f 2- | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')
                            case "$key" in
                                server) IRC_SERVER="$value" ;;
                                port) IRC_PORT="$value" ;;
                            esac
                        fi
                        ;;
                esac
            done < "$INI_FILE"
            # read ircpipe.ini end
            
            IRCSERVER="$IRC_SERVER:$IRC_PORT"
            
            # form json
            message="{ \"callsign\": [\"$CALLSIGN\"], \"serials\":[$list], \"meshtastic_port\": [\"$MESHTASTIC_PORT\"], \"gps_port\": [\"$GPS_PORT\"], \"irc_server\": [\"$IRCSERVER\"], \"ircpipe_pid\": [\"$IRCPIPE_PID\"], \"meshpipe_pid\": [\"$MESHPIPE_PID\"] }"
            # deliver json via FIFO pipe
            echo $message > /tmp/fromengine
        fi
        
        #
        # encrypt and decrypt symbols for transport
        # This is just an example, handle keys and saving with better security in real life
        # eg. create gpg user and store plain text outside microsd partitions
        #
        if [ "$line" == "encrypt_symbols" ]; then
            chown daemon:daemon /opt/edgemap-persist/symbols.txt*
            /bin/gpg --yes --quiet -ea -r edgemap --output /opt/edgemap-persist/symbols.txt.asc /opt/edgemap-persist/symbols.txt
            chown daemon:daemon /opt/edgemap-persist/symbols.txt*
        fi
        
        if [ "$line" == "decrypt_symbols" ]; then
            chown daemon:daemon /opt/edgemap-persist/symbols.txt*
            /bin/gpg --yes --quiet  -d --output /opt/edgemap-persist/symbols.txt /opt/edgemap-persist/symbols.txt.asc 
            chown daemon:daemon /opt/edgemap-persist/symbols.txt*
        fi
    fi
done


