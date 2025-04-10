#!/bin/sh
# busybox-compatible shell script
line="settings_save,edgew,/dev/ttyUSB0,irc.server:6667,/dev/ttyUSB1"

# Get the first item
first_item=$(echo "$line" | cut -d',' -f1)

if [ "$first_item" = "settings_save" ]; then
    # Assign following items to variables using cut
    var1=$(echo "$line" | cut -d',' -f2)
    var2=$(echo "$line" | cut -d',' -f3)
    var3=$(echo "$line" | cut -d',' -f4)
    var4=$(echo "$line" | cut -d',' -f5)

    echo "First item matched: $first_item"
    echo "var1: $var1"
    echo "var2: $var2"
    echo "var3: $var3"
    echo "var4: $var4"
else
    echo "First item is not 'settings_save'"
fi
