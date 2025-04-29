#!/bin/sh
# Create third partition
echo "Creating third partition without encryption"
TARGET_DEV=/dev/mmcblk0
parted --script $TARGET_DEV 'mkpart primary ext4 3500 -1'
# Creating filesystems
echo "Creating filesystem to $TARGET_DEVp3"
mkfs.ext4 -F -L maps ${TARGET_DEV}p3
exit 0

