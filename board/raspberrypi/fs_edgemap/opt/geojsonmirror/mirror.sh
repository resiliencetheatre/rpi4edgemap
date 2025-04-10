#!/bin/sh

# Ensure the pipes exist
#[ -p /tmp/inpipe ] || mkfifo /tmp/inpipe
#[ -p /tmp/outpipe ] || mkfifo /tmp/outpipe

# Loop and echo back everything received
while true; do
  if read line < /tmp/outpipe; then
    # echo "Mirroring: $line"
    echo "$line" > /tmp/inpipe
  fi
done

