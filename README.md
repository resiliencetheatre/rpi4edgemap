# Edgemap for RPi4

Edgemap is small project built on embedded ARM targets like RaspberryPi4 and Raspberry Pi Zero 2W. It can be cross compiled to various other platforms and integrated to work with AMD64 based PC architectures. 

System delivers small browser usable user interface where full world map can be accessed with any End User Device (EUD). Implementation is based on various open source projects like [Protomaps](https://protomaps.com/), [Meshtastic](https://meshtastic.org/) and [maplibre-gl-js](https://github.com/maplibre/maplibre-gl-js).

Please note that Edgemap is not complete product as such but offers great integration point to your own developments. 

![meshtastic](https://github.com/resiliencetheatre/rpi4edgemap/blob/main/doc/edgemap-with-batterypack.png?raw=true)

## Features

System contains features which might work out of the box for you or require more detailed configuration. Especially networking, SecurePTT and CoT receiving requires quite deep knowledge and planning to be really useful. 

### CoT Server

Image contains [taky](https://github.com/tkuester/taky) a simple [COT](https://www.mitre.org/sites/default/files/pdf/09_4937.pdf) server for [ATAK](https://tak.gov/products). CoT server is mainly targeted to read CoT targets in network and illustrate them on Web user interface. 
This functionality was tested with [AN/PRC-169](https://silvustechnologies.com/) radios.

CoT implementation to battle space with TLS certificates is painful and dangerous. But as it's running on consumer platforms, there is really no options available, I believe.

### Video conference

![videoconference](https://github.com/resiliencetheatre/rpi4edgemap/blob/main/doc/videoconference.png?raw=true)

Image contains TLS encryption for Web UI connection and offers experimental video conference for 6 team members directly from map user interface. Video conference is based on WebRTC and is implemented with [Janus](https://github.com/meetecho/janus-gateway) by Meetecho. Please note that TLS is really bad for your OPSEC and I generally would like to use other means to secure connectivity. But with consumer grade EUD's and browsers we are forced to use TLS to make WebRTC working. 

### Local display support & QT

![localdisplay](https://github.com/resiliencetheatre/rpi4edgemap/blob/meshtastic/doc/waveshare-display.png?raw=true)

QT 5.11.5 is enabled for build and it allows us to do small and simple local 
[user interface](https://github.com/resiliencetheatre/qrencode-ui) to
[Hyperpixel 4](https://shop.pimoroni.com/products/hyperpixel-4?variant=12569485443155) touch screen. 

This feature is currently proof of concept placeholder and contains no usable functionality. 
You could take this further with ease by using QT Creator and configuring it to use toolchain 
from buildroot environment. 

If you wish to use [Waveshare 4.3" DSI LCD case](https://www.waveshare.com/wiki/4.3inch_DSI_LCD), include following
configuration to `/opt/boot/config.txt` 

```
# Waveshare 4.3" DSI LCD case
dtoverlay=vc4-kms-v3d
dtoverlay=vc4-kms-dsi-7inch
dtparam=i2c_arm=on

```

### Meshtastic 

By default this image contains message delivery over [Meshtastic](https://meshtastic.org/) LoRA radios. (This can be changed to IP bearer if you need more bandwidth to image transfers for example).

Setup is tested with [LILYGO LoRa32 V2.1_1.6 radios](https://www.lilygo.cc/products/lora3) and [Heltec V3](https://heltec.org/project/wifi-lora-32-v3/) radios and others should work after configuring correct serial port to "/opt/edgemap/meshpipe/meshtastic.env"

Meshtastic implementation is still highly experimental and contains only message delivery over meshtastic radios. Following picture gives overview how FIFO pipes are used to deliver payload to/from radios.

![meshtastic](https://github.com/resiliencetheatre/rpi4edgemap/blob/main/doc/meshtastic.png?raw=true)

You can deliver MIL symbols as sensor markers between Edgemap nodes with 'sensorMarker' message. 

![meshtastic](https://github.com/resiliencetheatre/rpi4edgemap/blob/main/doc/map.png?raw=true)

Copy paste following messages to message dialog on Edgemap UI and expect them to appear to other nodes map after delivery is done via Meshtastic radios.

```
sensorMarker|[58.9074826,23.5766601]|path13,GSM Network,30046000001302000000
sensorMarker|[58.3830883,27.3655486]|path14,Water pump control override,30066000001504000000
sensorMarker|[58.3102102,27.3957824]|path15,Cloud outages,30066000001608000000
sensorMarker|[58.2887415,27.6258087]|path17,GNSS L2,30065200001102000001
sensorMarker|[58.2887415,27.6258087]|path18,GNSS L2+L1,30065200001102000001
sensorMarker|[58.0967511,27.5097656]|path19,Hand over delays,30055200000000000000
sensorMarker|[58.1616254,27.1953678]|path20,Core router #12,30046000001402000000
sensorMarker|[58.2340188,27.4486541]|path21,Power outage,30046000001606000000
sensorMarker|[58.3786785,26.7249298]|path22,OT + Sensory team,30031000001505010000
sensorMarker|[58.2320306,27.3464727]|path23,Cellular Jamming,30011000001505040000Z
sensorMarker|[58.0549952,27.0552062]|path24,Starlink uplink detected 04:19,30015000001101000000
```

To save bandwidth on Meshtastic communication, some of messaging channel functions have been commented out on UI code. We don't deliver 'drag marker' or 'geolocation' over Meshtastic and we have increased presence indication sending interval to 2 minute.


### Meshtastic detection sensor

![meshtastic](https://github.com/resiliencetheatre/rpi4edgemap/blob/main/doc/sensor-alarm.png?raw=true)

Edgemap contains simple example which shows you how to use Meshtastic node as detection sensor. Example is done with RAK wireless 
[Wisblock Meshtastic Starter Kit](https://store.rakwireless.com/products/wisblock-meshtastic-starter-kit?variant=43683420438726)
and you can use closing switch between J12: PIN1 (VDD) and J11: PIN2 (IO2). 

First you need to configure your Sensor unit. Note that 'detection_sensor.name' must contain given 
format and only ID ('12') can be changed by user, based on your sensor numbering.

```
meshtastic --port /dev/ttyACM0 --set detection_sensor.name "12|sensor|||"
meshtastic --port /dev/ttyACM0 --set detection_sensor.monitor_pin 34
meshtastic --port /dev/ttyACM0 --set detection_sensor.state_broadcast_secs 300
meshtastic --port /dev/ttyACM0 --set detection_sensor.minimum_broadcast_secs 5
meshtastic --port /dev/ttyACM0 --set detection_sensor.detection_triggered_high true
meshtastic --port /dev/ttyACM0 --set detection_sensor.enabled true
```

![meshtastic](https://github.com/resiliencetheatre/rpi4edgemap/blob/main/doc/sensor-alarm-create.png?raw=true)

Configuring sensor to Edgemap is simple. You send one alarm event and Edgemap will show 'unknown sensor' indication, 
where you can pick location on map and give description. All further alarms are then shown on map.

Note that this implementation is still work in progress.

### Local symbols

You can edit locally stored symbols with built in "symbols editor" and save them to be displayed on your map.

![symbols-editor](https://github.com/resiliencetheatre/rpi4edgemap/blob/main/doc/symbols-editor.png?raw=true)

Symbols are stored at `/opt/edgemap-persist/symbols.txt` and symbols editor loads and saves this file. Feel free
to build some more clever logic around this demonstration. You can use [unit symbols generator](https://spatialillusions.com/unitgenerator/) to define your symbols. 

For example, with updated milsymbols 3.0 we get some nice cyber security symbols:

```
sensorMarker|[58.9074826,23.5766601]|path13,KOLD,130460000012000000000000000000
sensorMarker|[52.5578409,-0.6288282]|path14,TWIST,130460000017060000000000000000
sensorMarker|[48.0131228,16.3930026]|path15,BINARY,130460000011020000000000000000
sensorMarker|[45.3958035,9.11607187]|path16,OBSOLETE,130460000011080000000000000000
sensorMarker|[53.3570698,29.2069794]|path17,INSBRUCK,130560000017030100000000000000
```

### Highrate

![highrate](https://github.com/resiliencetheatre/rpi4edgemap/blob/main/doc/highrate.png?raw=true)

You can also update highrate target information to map via websocket connection. See readme in highrate/ directory.

### Reticulum

Experimental support for reticulum network is included on build. Currently we have to disable meshtastic when reticulum is  activated into use, but this might change in future. For reticulum there is "Reticulum MeshChat" included, which is
independent browser usable chat and nomad network access tool. 

For reticulum message delivery image contains [LXMF](https://github.com/markqvist/LXMF) based messaging and reticulum links based option. Both of these are currently under development and field testing. 

![edgemap-phone](https://github.com/resiliencetheatre/rpi4edgemap/blob/main/doc/edgmap-with-phone.png?raw=true)

### SecurePTT

SecurePTT branch contains possbility to use small scale demo of full duplex Push-To-Talk (PTT) with exclusive level of security, where PTT streams are encrypted with One-Time-Pad (OTP). This functionality can be configured to following modes, depending on use case:

* Global unicast SecurePTT coverage via routing gateway servers 
* Global multicast SecurePTT coverage via routing gateway servers 
* Local MESH/MANET network segments 

SecurePTT offers flexibility to cipher your PTT streams and by default we use three layers to transport UDP packets between nodes. 

![tunnel](https://github.com/resiliencetheatre/rpi4edgemap/blob/main/doc/secureptt-tunnel.png?raw=true)

Outermost level (A) can be selected to hide meta-data of layer (B) which encapsulates (C), One-Time-Pad encrypted stream between nodes. 

![streams](https://github.com/resiliencetheatre/rpi4edgemap/blob/main/doc/SecurePTT-Keyed-Streams-3-peers.png?raw=true)

### PTT button wiring

Depending what audio hardware you choose to use, wiring of PTT button varies. You could use USB attached headset and utilize GPIO pin to act like a PTT button:

![gpioptt](https://github.com/resiliencetheatre/rpi4edgemap/blob/main/doc/secureptt-GPIO-PTT-button.png?raw=true)

For [Codec Zero](https://www.raspberrypi.com/products/codec-zero/) with [Kenwood SMC-34](https://www.kenwood.eu/comm/accessories/audio/SMC-34/) wiring looks like this:

![codecptt](https://github.com/resiliencetheatre/rpi4edgemap/blob/main/doc/rpi4ptt-codec-zero-wiring.png?raw=true)

### SecurePTT options

You can modify SecurePTT code to support Symmetric algorithms (if you find a math you can trust). Implementation supports also securing plain text UDP streams of your existing MESH/MANET gears like [AN/PRC-169](https://silvustechnologies.com/) making your PTT comms resistant to UDP jamming and interception. 

### SecurePTT keying

Note that this repository does not contain [keying environment](https://github.com/resiliencetheatre/rpi4ptt-init) and you need separately configure your network setup and nodes to support SecurePTT.

### Secure imagery storage

For [operations security](https://en.wikipedia.org/wiki/Operations_security) we can use optional Linux Unified Key Setup (LUKS) to encrypt data partition on same MicroSD card (or external USB drive).
Since we aim to use RPi4 in headless configuration we use [systemd-cryptsetup](https://www.freedesktop.org/software/systemd/man/latest/systemd-cryptsetup@.service.html)
with [FIDO2](https://shop.nitrokey.com/shop/product/nkfi2-nitrokey-fido2-55) key. With this approach we can start unit to fully operational state with FIDO2 key plugged in to USB port and after unit is booted (and LUKS partitions are opened) - we can remove FIDO2 key. 

Note that this branch is configured to use third partition for maps, elevation model and imagery without encryption. 

### Additional notes

This version does NOT have high rate target, simulations, CoT reading and [AN/PRC-169](https://silvustechnologies.com/) support. 

If you choose to use browser based geolocation, configure installation to use TLS connection. 


## Building

To build edgemap firmware, you need to install Buildroot environment and clone this repository 
as 'external tree' to buildroot. Make sure you check buildroot manual for required packages for your host, before building.

Clone repositories and checkout either tested buildroot commit or be brave and try with master. 

```
mkdir ~/build-directory
cd ~/build-directory/
git clone https://github.com/resiliencetheatre/rpi4edgemap.git
git clone https://git.buildroot.net/buildroot
cd buildroot/
# We checkout verified version on master branch
git checkout aa2d7ca53f704af901f6c33c13e4bb1591886700
```

You can use latest buildroot master or checkout version `aa2d7ca53f704af901f6c33c13e4bb1591886700` as above,
which I've tested at Mar 27th, 2025. Please note that buildroot version, kernel and other system
components needs to be in 'sync' and this is an art in embedded design.

Optionally you can modify buildroot standard `rpi-firmware` package file and change  firmware version tag to match kernel version we're using. Note that you need to track firmware version from RPi repositories yourself if you face any issues with HW compatibility (or stick with this version).

```
# package/rpi-firmware/rpi-firmware.mk
RPI_FIRMWARE_VERSION = 8a8adaf2f1d6836facdc1c66f4e838b2025ec851
```

Disable hash check by deleting `rpi-firmware.hash` file:

```
cd ~/build-directory/buildroot
rm package/rpi-firmware/rpi-firmware.hash
```

## Start build

Export BR2_EXTERNAL variable, make defconfig and start build with make:

```
export BR2_EXTERNAL=~/build-directory/rpi4edgemap
cd ~/build-directory/buildroot
make rpi4_edgemap_6.12_voip_defconfig
make
```

After build is completed, you find image file for MicroSD card at:

```
~/build-directory/buildroot/output/images/sdcard.img
```

Use 'dd' to copy this image to your MicroSD card.

## First boot

First boot requires you to create maps partition, set hostname and create CA certificate. You can login with 'root' and 
'edgemap' as password to your Edgemap instance. 

First create partition for maps:

```
create-partition-noenc.sh
```

Create CA and set hostname:

```
# /opt/edgemap/ca/tls-setup.sh
Usage: tls-setup.sh [CA-NAME] [DNS-NAME]

# Example:
/opt/edgemap/ca/tls-setup.sh edgeCA edgemapx
# Reboot after this completes:
reboot
```

This will set your unit hostname and create wifi access point with same name. Wifi AP psk is 'abc12345', feel free to change it.

### Copying pmtiles to map partition

You can copy `planet.pmtiles` to your map partition with computer or try to download it directly from Edgemap:

```
cd /opt/data
wget --no-check-certificate https://build.protomaps.com/20240520.pmtiles -O planet.pmtiles
```

Check latest pmtiles [here](https://maps.protomaps.com/builds/) or [generate it yourself](https://resilience-theatre.com/wiki/doku.php?id=edgemap:planet_with_tilemaker). 

Link downloaded `planet.pmtiles` under `/opt/edgemap/edgeui`

```
cd /opt/edgemap/edgeui/
ln -s /opt/data/planet.pmtiles .
```

## Patching iqaudio driver

You can optionally patch iqaudio-codec.c driver to remove really anoying 
delay on audio opening. Download [this patch](https://gist.github.com/resiliencetheatre/9b9323e37b81a49a5724f68c04ac7dff) and place it under buildroot/linux/ before build.

## codec2 binaries

If you wish to have codec2 binaries on your edgemap device, use provided `buildroot-extras/libcodec2.mk` file
and copy it over to buildroot provided one:

```
# libcodec2  (optional)
rm ~/build-directory/buildroot/package/libcodec2/libcodec2.hash
cd ~/build-directory/rpi4edgemap/buildroot-extras/
cp libcodec2.mk ~/build-directory/buildroot/package/libcodec2/libcodec2.hash
```

## Map data

You need to have full [planet OSM](https://maps.protomaps.com/builds/) pmtiles and A global terrain RGB dataset from [Mapzen Joerd](https://github.com/tilezen/joerd) project.

As full planet pmtiles file is HUGE (>100 GB) you can either copy it manually to card or use inbuilt wget to download it.

Preparing card 'maps' partition after first boot, you could enter following command:

```
# create-partition-noenc.sh
```

This will create third partition with EXT4 filesystem and label 'maps'. After create completes, reboot your RPi4 to automount partition on next boot.

After boot completes with and created 'maps' partition is usable, you can download pmtiles to card with:

```
# cd /opt/data
# wget --no-check-certificate https://build.protomaps.com/20240520.pmtiles -O planet.pmtiles
# sync
```

Note that downloading over 100 GB file might take several hours to complete, depending your connection speed.

## Meshtastic 

Configure USB serial port of your meshtastic radios:

```
# /opt/edgemap/meshpipe/meshtastic.env 
MESHTASTIC_PORT="/dev/ttyACM0"
```

* LilyGo: /dev/ttyUSB0
* Heltec: /dev/ttyACM0

## Reticulum configuration

You can find reticulum (rnsd) configuration file at:

```
/opt/meshchat/config
```

## Local GPS

This branch has [gpsd ](https://gpsd.io/) package which can read your locally attached GPS receiver(s) and expose location information to localhost socket. There is also [gpsreader](https://github.com/resiliencetheatre/gpsreader) as buildroot package and it's used to read gpsd socket and output location string to fifo file. This fifo is delivered to map UI via websocket. 

Locally connected GPS is good companion for Edgemap with Meshtastic radios. Typically browser based geolocation (also present in edgemap UI) requires TLS connection between EUD (client) and edgemap (server). Since TLS connection requires complex and meta data enriched certificates to be present and real time (difficult to obtain in battle space) we offer edgemap UI without TLS to local network connected EUD's. Browser geolocation requires also Cell, Wifi and BT to be active (stupidity in battle space) for optimum results.

You can configure GPS serial port:

```
# /etc/default/gpsd
DEVICES="/dev/ttyUSB1"
```

Daemon (gpsd) and 'gpsreader' is started automatically after you plug GPS in USB port.

## Cryptpad

If you built `rpi4_edgemap_6.13_nodejs_defconfig` configuration, there is experimental [cryptpad](https://github.com/cryptpad/cryptpad) 
built into edgemap image. It needs following configuration step before it can be used.

Complete cryptpad installation by visiting installation URL. It's shown on first (manual) run of Cryptpad.

```
# Let's make sure we don't run cryptpad service (as root):
systemctl stop cryptpad
# Change user to 'cryptpad'
su cryptpad
# Manually execute server.js (as cryptpad):
cd
node server.js
```

Visit given URL and setup cryptpad admin user and password on web interface. After this step
is completed, you may enable cryptpad service:

```
systemctl enable cryptpad
```

Starting this service or rebooting edgemap instance, should make cryptpad working on your instance.

### Reset cryptpad

If you screw up, like I've done, you can 'reset' cryptpad from installation directory.

Remove /opt/cryptmap on edgemap:

```
rm -rf /opt/cryptmap
```

Copy build directory from buildroot directory to edgemap:

```
cd [your buildroot directory]
scp -r output/target/opt/cryptpad/ [EDGEMAP_IP]:/opt
```

Then re-configure like described in “first run” section above. 


## Links

* https://jvns.ca/blog/2024/11/29/why-pipes-get-stuck-buffering/
