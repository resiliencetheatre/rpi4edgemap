#!/usr/bin/env python3
#
# meshpipe - piping messages to/from FIFO over meshtastic radio
#
# Copyright (c) Resilience Theatre, 2024
# Copyright (c) 2021, datagod
# 
# https://github.com/meshtastic/python
# https://python.meshtastic.org/
#
# FIFO files:
#
# /tmp/msgincoming -> meshtastic radio
# /tmp/msgchannel <- meshtastic radio
#
# Run:
#
# python3 meshpipe.py --port=[usb_serial_device]
#
# This work is based on:
#
#  https://github.com/datagod/meshwatch/
#  See LICENSE.meshwatch
#
#  Out:
#  echo "3D,3,2024-06-24,01:24:17,50.7603593,23.6406054,0.1,55,0,0" > /tmp/gpssocket
#  edgey|trackMarker|23.6206054,50.7503593|GPS-snapshot
#
#  In:
#  edgex|trackMarker|23.6406054,50.7603593|GPS-snapshot
#
#  For development, read fifo's:
#
#  while [ 1 ]; do cat /tmp/msgchannel; sleep 1; done;
#  while [ 1 ]; do cat /tmp/statusin; sleep 1; done;
#
#  Export MESHTASTIC port:
#
#  export $(xargs < meshtastic.env )
#
#  Setting this option to 'true' means the device will ignore the hourly 
#  duty cycle limit in Europe. 
# 
#  meshtastic --port /dev/ttyACM0 --set lora.override_duty_cycle true
#

import meshtastic
import meshtastic.serial_interface
import meshtastic.tcp_interface
import time
import traceback
import argparse
import collections
import sys
import os
import stat, os
import math
import inspect
import subprocess
import select
import sqlite3
import threading
from random import randrange, uniform
# from meshtastic.mesh_pb2 import _HARDWAREMODEL
from meshtastic.node import Node
from pubsub import pub
from signal import signal, SIGINT
from sys import exit
from datetime import datetime


NAME = 'meshpipe'                   
DESCRIPTION = "FIFO pipe messages from Meshtastic devices"
DEBUG = False

parser = argparse.ArgumentParser(description=DESCRIPTION)
parser.add_argument('-p', '--port', type=str, help="meshtastic port (eg. /dev/ttyACM0)")
args = parser.parse_args()

global Interface
global DeviceStatus
global DeviceName
global DevicePort
global PacketsReceived
global PacketsSent
global LastPacketType
global BaseLat
global BaseLon
global MacAddress
global DeviceID
global DeviceBat
global DeviceAirUtilTx
global DeviceRxSnr
global DeviceHopLimit
global DeviceRxRssi
global myRadioHexId


def ErrorHandler(ErrorMessage,TraceMessage,AdditionalInfo):
  CallingFunction =  inspect.stack()[1][3]
  print("Error - Function (",CallingFunction, ") has encountered an error. ")
  print(ErrorMessage)
  print("Trace")
  print(TraceMessage)
  if (AdditionalInfo != ""):
    print("Additonal info:",AdditionalInfo)
  os._exit(0)  # Forcefully exits the entire Python process

#
# meshtastic
#
def DecodePacket(PacketParent,Packet):
  global DeviceStatus
  global DeviceName
  global DevicePort
  global PacketsReceived
  global PacketsSent
  global LastPacketType
  global HardwareModel
  global DeviceID 
  global DeviceBat  
  global DeviceAirUtilTx
  global DeviceRxSnr
  global DeviceHopLimit
  global DeviceRxRssi
  
  if isinstance(Packet, collections.abc.Mapping):

    for Key in Packet.keys():
      Value = Packet.get(Key) 
      if isinstance(Value, collections.abc.Mapping):
        LastPacketType = Key.upper()
        DecodePacket("{}/{}".format(PacketParent,Key).upper(),Value)  
      else:
        if(Key == 'raw'):
            pass
        else:
          if not isinstance(Value, bytes):
            # print("{: <20} {: <20}".format(Key,Value))
            if(Key=='batteryLevel'):
                DeviceBat = Value
            if(Key=='airUtilTx'):
                DeviceAirUtilTx = round(Value,2)
            if(Key=='rxSnr'):
                DeviceRxSnr = Value
            if(Key=='hopLimit'):
                DeviceHopLimit = Value
            if(Key=='rxRssi'):
                DeviceRxRssi = Value
           

  else:
      print('Warning: Not a packet!\n')
  

#
# Packet receive
#
def onReceive(packet, interface): 
    global PacketsReceived
    global PacketsSent
    global fifo_write
    global DeviceBat
    global DeviceAirUtilTx
    global DeviceRxSnr
    global DeviceHopLimit
    global DeviceRxRssi
    DeviceBat=None
    DeviceAirUtilTx=None
    DeviceRxSnr=None
    DeviceHopLimit=None
    DeviceRxRssi=None
    
    PacketsReceived = PacketsReceived + 1
    Decoded  = packet.get('decoded')
    To       = packet.get('to')
    From     = packet.get('from')
    
    # print('** onReceive() from: {}'.format(From))
    # print('** onReceive() Decoded: {}'.format(Decoded))
    # sys.stdout.flush()
        
    DecodePacket('MainPacket',packet)
    
    if packet is not None:
                
        fromIdentString = packet.get('fromId')
        if fromIdentString is not None:
            fromIdent = fromIdentString[1:]
    
            if(fromIdent):
                # print('** Packet from: {}'.format(fromIdent))
                # print('** battery: {}'.format(DeviceBat))
                # print('** air util: {}'.format( DeviceAirUtilTx ))
                # print('** RxSnr: {}'.format(DeviceRxSnr))
                # print('** HopLimit: {}'.format(DeviceHopLimit))
                # print('** rxRssi: {}'.format(DeviceRxRssi))
                
                # Update UI
                if DeviceBat is None: 
                    DeviceBat='-'
                if DeviceAirUtilTx is None: 
                    DeviceAirUtilTx='-'
                if DeviceRxSnr is None: 
                    DeviceRxSnr='-'
                if DeviceHopLimit is None: 
                    DeviceHopLimit='-'
                if DeviceRxRssi is None: 
                    DeviceRxRssi='-'
                
                meshtasticmessage = "peernode," + fromIdent + "," + str(DeviceBat) + "," + str(DeviceAirUtilTx) + "," + str(DeviceRxSnr) + "," + str(DeviceHopLimit) + "," + str(DeviceRxRssi)
                fifo_write = open('/tmp/statusin', 'w')
                fifo_write.write(meshtasticmessage)
                fifo_write.flush()
                fifo_write.close()

    if Decoded is not None:
        
        Message  = Decoded.get('text')
        
        if(Message):
            hexFromValue = "{0:0>8X}".format(From)
            print("Incoming: {: <20} {: <20}".format(hexFromValue,Message[:-1]))
            sys.stdout.flush()
            fifo_write = open('/tmp/msgchannel', 'w')
            fifo_write.write(Message)
            fifo_write.flush()
            fifo_write.close()
            if( fromIdent.upper() == hexFromValue ):
                # edgex|trackMarker|23.6406054,50.7603593|GPS-snapshot
                messageFields = Message.split('|')
                # print("messageFields count: ", len(messageFields) )
                if len(messageFields) > 1:
                    if ( messageFields[1] == "trackMarker" ):
                        messagePositionFields = messageFields[2].split(',')
                        lon = messagePositionFields[0]
                        lat = messagePositionFields[1] # done
                        callsign = messageFields[0]
                        messageType = messageFields[1]
                        # print("Meshtastic data to DB: {: <10} {: <10} {: <10} {: <10} {: <10} {: <10}".format(callsign,lat,lon,hexFromValue,DeviceRxSnr,DeviceRxRssi))
                        meshtasticDbUpdate(callsign,lat,lon,"trackMarker",hexFromValue,DeviceRxSnr,DeviceRxRssi)

def meshtasticDbCreate():
    connection = sqlite3.connect("/tmp/radio.db")
    print(connection.total_changes)
    cursor = connection.cursor()
    # Check if table exist
    listOfTables = cursor.execute("""SELECT tbl_name FROM sqlite_master WHERE type='table' AND tbl_name="meshradio";""").fetchall();
    if listOfTables == []:
        print('Creating table')
        cursor.execute("CREATE TABLE meshradio (id INTEGER PRIMARY KEY AUTOINCREMENT, callsign TEXT, lat TEXT, lon TEXT, time TEXT, event TEXT, radio_id TEXT, snr TEXT, rssi TEXT)")
    else:
        print('Radio DB found')

# Not used
def meshtasticDbInsert(callsign,lat,lon,event,radio_id,snr,rssi):
    connection = sqlite3.connect("/tmp/radio.db")
    print(connection.total_changes)
    cursor = connection.cursor()
    cursor.execute("INSERT INTO meshradio (callsign, lat, lon,event,radio_id,snr,rssi) VALUES (?,?,?,?,?,?,?)", (callsign, lat, lon,event,radio_id,snr,rssi))
    print("Inserted", callsign, lat, lon,event,radio_id,snr,rssi)
    connection.commit()
    connection.close()

def meshtasticDbUpdate(callsign,lat,lon,event,radio_id,snr,rssi):
    connection = sqlite3.connect("/tmp/radio.db")
    # print(connection.total_changes)
    cursor = connection.cursor()
    # Check if callsign exist
    cursor.execute("SELECT * FROM meshradio WHERE callsign = ?", (callsign,) )
    rows = len( cursor.fetchall() )
    if ( rows == 0 ):
        # print("Inserting new callsign: ", callsign)
        cursor.execute("INSERT INTO meshradio (callsign, lat, lon,event,radio_id,snr,rssi) VALUES (?,?,?,?,?,?,?)", (callsign, lat, lon,event,radio_id,snr,rssi))
    else:
        # print("Updating existing callsign: ",callsign)
        cursor.execute("UPDATE meshradio SET lat=?, lon=?,event=?,radio_id=?,snr=?,rssi=? WHERE callsign = ?", (lat, lon,event,radio_id,snr,rssi,callsign))
    connection.commit()
    connection.close()


def onConnectionEstablished(interface, topic=pub.AUTO_TOPIC): 
    
    # To   = "All"
    # current_time = datetime.now().strftime("%H:%M:%S")
    # Message = "{}|meshpipe|-|{}".format(current_time,DeviceName[1:])

    try:
      print("Connected to meshtastic radio: {}".format(myRadioHexId) )
      sys.stdout.flush()
      # interface.sendText(Message, wantAck=False)
      # print("== Connection up packet sent ==")
      # print("To:      {}".format(To))
      # print("Message: {}".format(Message))

    except Exception as ErrorMessage:
      TraceMessage = traceback.format_exc()
      AdditionalInfo = "Sending text message ({})".format(Message)
      ErrorHandler(ErrorMessage,TraceMessage,AdditionalInfo)


def onConnectionLost(interface, topic=pub.AUTO_TOPIC): 
    print('onConnectionLost, exiting. \n')
    sys.stdout.flush()
    os._exit(0)  # Forcefully exits the entire Python process

def onNodeUpdated(interface, topic=pub.AUTO_TOPIC): 
    print('onNodeUpdated \n')
    sys.stdout.flush()
   

def SIGINT_handler(signal_received, frame):
    print('SIGINT detected. \n')
    sys.stdout.flush()
    os._exit(0)  # Forcefully exits the entire Python process


#
# Send message functions
#
def send_msg(interface, Message):
    interface.sendText(Message, wantAck=True)
    print("== Packet SENT ==")
    # print("To:      All:")
    # print("From:    BaseStation")
    # print('Message: {}'.format(Message))
    # print('')

def send_msg_from_fifo(interface, Message):
    outMsg = Message + '\n'
    interface.sendText(outMsg, wantAck=True)
    print('  Sending broadcast message (wantAck=True) : {}'.format(Message))
    sys.stdout.flush()

def send_msg_from_fifo_to_one_node(interface, Message, nodeId):
    outMsg = Message + '\n'
    interface.sendText(outMsg, wantAck=True,destinationId=nodeId)
    print("Sending p2p message to: {}".format(nodeId) )
    sys.stdout.flush()
    # print("To:      {}".format(nodeId))
    # print("From:    BaseStation")
    # print('Message: {}'.format(Message))
    # print('')

def GetMyNodeInfo(interface):

    global DeviceName
    global DeviceBat
    global myRadioHexId
    Distance   = 0
    DeviceName = ''
    BaseLat    = 0
    BaseLon    = 0
    TheNode = interface.getMyNodeInfo()
    DecodePacket('MYNODE',TheNode)

    print("\n--GetMyNodeInfo--")

    if 'latitude' in TheNode['position'] and 'longitude' in TheNode['position']:
      BaseLat = TheNode['position']['latitude']
      BaseLon = TheNode['position']['longitude']
      print('** GPS Location: ', BaseLat,BaseLon)

    if 'longName' in TheNode['user']:
      print('Long name: ', TheNode['user']['longName'])
      # Inform my node ID
      # meshtasticmessage = 'mynode,' + TheNode['user']['longName']
      # fifo_write = open('/tmp/statusin', 'w')
      # fifo_write.write(meshtasticmessage)
      # fifo_write.flush()

    if 'hwModel' in TheNode['user']:
      print('HW model:  ',TheNode['user']['hwModel'])
    
    if 'macaddr' in TheNode['user']:
      print('Mac addr.  ', TheNode['user']['macaddr'])

    if 'id' in TheNode['user']:
      print('User ID:   ',TheNode['user']['id'])
      DeviceName = TheNode['user']['id']
      myRadioHexId = DeviceName[1:].upper()
      print('myRadioHexId   ',myRadioHexId)

    if 'batteryLevel' in TheNode['position']:
      print('Battery:   ',TheNode['position']['batteryLevel'])

    print('---\n')
    sys.stdout.flush()


def deg2num(lat_deg, lon_deg, zoom):
  lat_rad = math.radians(lat_deg)
  n = 2.0 ** zoom
  xtile = int((lon_deg + 180.0) / 360.0 * n)
  ytile = int((1.0 - math.asinh(math.tan(lat_rad)) / math.pi) / 2.0 * n)
  return (xtile, ytile)
      

# TODO: Deliver nodes to fifo or create mesh status fifo for UI?
def DisplayNodes(interface):
    
    print('\n-- DisplayNodes --')

    try:
      for node in (interface.nodes.values()):
        print("NAME:      {}".format(node['user']['longName']))  
        print("NODE:      {}".format(node['num']))  
        print("ID:        {}".format(node['user']['id']))  
        sys.stdout.flush()
        #print("MAC:       {}".format(node['user']['macaddr']))
        if 'position' in node.keys():
          #used to calculate XY for tile servers
          if 'latitude' in node['position'] and 'longitude' in node['position']:
            Lat = node['position']['latitude']
            Lon = node['position']['longitude']
            xtile,ytile = deg2num(Lat,Lon,10)
            print("Tile:      {}/{}".format(xtile,ytile)) 
            print("LAT:       {}".format(node['position']['latitude']))  
            print("LONG:      {}".format(node['position']['longitude']))
            sys.stdout.flush()

          if 'batteryLevel' in node['position']:
            Battery = node['position']['batteryLevel']
            print("Battery:   {}".format(Battery))  
            sys.stdout.flush()
        
        if 'lastHeard' in node.keys():
          LastHeardDatetime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(node['lastHeard']))
          print("LastHeard: {}".format(LastHeardDatetime))  
          sys.stdout.flush()
        print('-----')
        
        # Update UI
        nodeidstring = node['user']['id']
        nodeidstring = nodeidstring[1:]
        meshtasticmessage = "peernode," + nodeidstring + "\n"
        fifo_status_write = open('/tmp/statusin', 'w')
        fifo_status_write.write(meshtasticmessage)
        fifo_status_write.flush()
        fifo_status_write.close()

    except Exception as ErrorMessage:
      TraceMessage = traceback.format_exc()
      AdditionalInfo = "Processing node info"
      ErrorHandler(ErrorMessage,TraceMessage,AdditionalInfo)


def create_fifo_pipe(pipe_path):
    try:
        os.mkfifo(pipe_path)
        print(f"Named pipe created at {pipe_path}")
        sys.stdout.flush()
        
    except OSError as e:
        print(f"Error: {e}")
        sys.stdout.flush()
  
  
# Thread T2
def read_manual_gps():
    global myRadioHexId
    global interface # Nov 16th
    
    # Randomize time
    min_interval_time=120
    max_interval_time=240
    
    # Position broadcast on
    send_positions = True

    print("Starting read_manual_gps()")
    sys.stdout.flush()
    t2_start_time = time.time()
    t2_interval_rand = randrange(min_interval_time, max_interval_time)
    t2_callsign_from_file = "no-callsign"
    t2_lkg_lat = "-"
    t2_lkg_lon = "-"
    
    try:
        while True:
            
            # Manual loop should only run when location.txt is present!
            if ( os.path.isfile("/opt/edgemap-persist/location.txt") ):

                # Read send interval from /opt/edgemap-persist/pos_interval.txt (if present)
                if ( os.path.isfile("/opt/edgemap-persist/pos_interval.txt") ):
                    t2_interval_file = open("/opt/edgemap-persist/pos_interval.txt","r")
                    t2_interval_from_file = t2_interval_file.readline().rstrip()
                    t2_interval_file.close()
                    
                    # Based on Web UI instructed values, implement 2,4 and 10 minutes
                    # position sending over meshtastic. Random minutes +/- 30 seconds. 
                    # TODO: Implement off and manual send
                    if t2_interval_from_file == '2':
                        t2_interval_rand = randrange(90, 150)
                        send_positions = True
                    if t2_interval_from_file == '4':
                        t2_interval_rand = randrange(210, 270)
                        send_positions = True
                    if t2_interval_from_file == '10':
                        t2_interval_rand = randrange(570, 630)
                        send_positions = True
                    if t2_interval_from_file == 'off':
                        send_positions = False
                
                # Slow loop down a bit
                time.sleep(1)
                
                # Send if allowed
                if ( send_positions ):          
                    # Randomize sending interval
                    t2_end_time = time.time()
                    t2_elapsed_time = t2_end_time - t2_start_time
                
                    if ( t2_elapsed_time > t2_interval_rand ):
                        # print("Manual loop",t2_elapsed_time,t2_interval_rand)
                        if ( os.path.isfile("/opt/edgemap-persist/callsign.txt") ):
                            t2_callsign_file = open("/opt/edgemap-persist/callsign.txt", "r")
                            t2_callsign_from_file = t2_callsign_file.readline()
                            t2_callsign_file.close()
                            # Read location from file
                            if ( os.path.isfile("/opt/edgemap-persist/location.txt") ):
                                t2_location_file = open("/opt/edgemap-persist/location.txt","r")
                                t2_location_from_file = t2_location_file.readline()
                                t2_location_file.close()
                                t2_gps_array = t2_location_from_file.split(",")
                                t2_lkg_lat = t2_gps_array[0].rstrip()
                                t2_lkg_lon = t2_gps_array[1].rstrip()
                                # print("Manual GPS: ",t2_callsign_from_file,t2_location_from_file)                
                                # Send
                                t2_track_marker_string= t2_callsign_from_file.rstrip() + "|trackMarker|" + t2_lkg_lon + "," + t2_lkg_lat + "|Manual position"
                                send_msg_from_fifo(interface, t2_track_marker_string)
                                # Update own location to radio.db when fix is manual
                                meshtasticDbUpdate(t2_callsign_from_file,t2_lkg_lat,t2_lkg_lon,"trackMarker",myRadioHexId,"0","0");
                                t2_start_time = time.time()
                                t2_interval_rand = randrange(min_interval_time, max_interval_time)
                                    
                        else:
                            t2_callsign_from_file = "no-callsign"
                        
                        t2_start_time = time.time()
                        t2_interval_rand = randrange(min_interval_time, max_interval_time)
                else:
                    time.sleep(60)
                    print("Position send is OFF")
                    
    
    except Exception as e:
        print(f"Exception caught in thread: {e}")
        sys.stdout.flush()
        os._exit(0)  # Forcefully exits the entire Python process


# Live GPS thread T1
def read_live_gps():
    global myRadioHexId
    global interface # Nov 16th
    min_interval_time=60
    max_interval_time=90
    print('Starting read_live_gps()')
    sys.stdout.flush()
    FIFO = '/tmp/livegps'
    fifo_read=open(FIFO,'r')
    # Get initial state
    start_time = time.time()
    interval_rand = randrange(min_interval_time, max_interval_time)
    callsign_from_file = "no-callsign"
    lkg_lat = "-"
    lkg_lon = "-"

    try:

        while True:
          fifo_msg_in = fifo_read.readline()[:-1]
          if not fifo_msg_in == "":
            # print('FIFO Message in read_live_gps(): ', fifo_msg_in)
            # [mode],[mode_id],[timestamp],[lat],[lon],[speed],[track],[sat_used],[sat_visible]
            # TODO: Evaluate 'mode' => 3D, 2D or none
            gps_array=fifo_msg_in.split(",")
            
            # Manually provided location always override GPS
            # So if we have location.txt file, don't send GPS position.
            if ( not os.path.isfile("/opt/edgemap-persist/location.txt") ):
                # Send only when we have a fix (2D, 3D)
                if ( gps_array[0] == "2D" or gps_array[0] == "3D" ):
                    # Randomize sending interval (min_interval_time <-> max_interval_time)
                    end_time = time.time()
                    elapsed_time = end_time - start_time
                    if ( elapsed_time > interval_rand ):
                        # Read callsign from /opt/edgemap-persist/callsign.txt
                        if ( os.path.isfile("/opt/edgemap-persist/callsign.txt") ):
                            callsign_file = open("/opt/edgemap-persist/callsign.txt", "r")
                            callsign_from_file = callsign_file.readline()
                            callsign_file.close()
                        else:
                            callsign_from_file = "no-callsign"

                        track_marker_string= callsign_from_file + "|trackMarker|"+gps_array[5]+","+gps_array[4]+"|GPS: " + gps_array[0] +" SV: " + gps_array[8]            
                        send_msg_from_fifo(interface, track_marker_string)
                        
                        # Update own location to radio.db when fix is 2D or 3D
                        # meshtasticDbUpdate(callsign_from_file,gps_array[4],gps_array[5],"trackMarker",myRadioHexId,"0","0");
                        
                        start_time = time.time()
                        interval_rand = randrange(min_interval_time, max_interval_time)
                        print("track_marker_string: ", track_marker_string)
                        lkg_lat = gps_array[5]
                        lkg_lon = gps_array[4]
                    
                    
                    # If location.txt is NOT present
                    if ( not os.path.isfile("/opt/edgemap-persist/location.txt") ):
                        # Update own location to radio.db when fix is 2D or 3D
                        # Read callsign from /opt/edgemap-persist/callsign.txt
                        if ( os.path.isfile("/opt/edgemap-persist/callsign.txt") ):
                            callsign_file = open("/opt/edgemap-persist/callsign.txt", "r")
                            callsign_from_file = callsign_file.readline()
                            callsign_file.close()
                        else:
                            callsign_from_file = "no-callsign"
                        
                        # print("DEBUG: ", callsign_from_file,gps_array[4],gps_array[5],"trackMarker",myRadioHexId,"0","0")
                        meshtasticDbUpdate(callsign_from_file,gps_array[4],gps_array[5],"trackMarker",myRadioHexId,"0","0")
                        time.sleep(1)
                    
                    pass
                    
                else:
                    # Send last known good location when there is no fix from GPS
                    # and we have stored last known good (lkg) position.
                    end_time = time.time()
                    elapsed_time = end_time - start_time
                    if ( elapsed_time > interval_rand ):
                        if ( os.path.isfile("/opt/edgemap-persist/callsign.txt") ):
                            callsign_file = open("/opt/edgemap-persist/callsign.txt", "r")
                            callsign_from_file = callsign_file.readline()
                            callsign_file.close()
                        else:
                            callsign_from_file = "no-callsign"
                        
                        if ( lkg_lat != "-" ):
                            track_marker_string= callsign_from_file + "|trackMarker|" + lkg_lat + "," + lkg_lon + "|No FIX: Last known good"
                            send_msg_from_fifo(interface, track_marker_string)
                            
                            # Update own location to radio.db when fix is LKG
                            meshtasticDbUpdate(callsign_from_file,lkg_lat,lkg_lon,"trackMarker",myRadioHexId,"0","0");
                            
                            start_time = time.time()
                            interval_rand = randrange(min_interval_time, max_interval_time)
                            print("LKG: track_marker_string: ", track_marker_string)
                        else:
                            print("We don't have last known good position. Not sending anything. ")
                            start_time = time.time()
                            interval_rand = randrange(min_interval_time, max_interval_time)
                                
                    pass
            else:
                # print("GPS location send is overridden by manually provided location!")
                # let thread sleep a bit
                time.sleep(2) 
                pass
          
          else:
            # No fifo data
            # let thread sleep a bit
            time.sleep(2)
            pass
    
    except Exception as e:
        print(f"Exception caught in thread: {e}")
        os._exit(0)  # Forcefully exits the entire Python process

# Read incoming FIFO thread T3
def read_incoming_fifo():
    global interface # Nov 16th
    print("Started read_incoming_fifo()")
    sys.stdout.flush()
    # Open FIFO for reading
    FIFO = '/tmp/msgincoming'
    fifo_read=open(FIFO,'r')
    
    try:
        while True:
          time.sleep(2)
          # print('While loop')
          fifo_msg_in = fifo_read.readline()[:-1]
          if not fifo_msg_in == "":
            print('FIFO Message in: ', fifo_msg_in)
            sys.stdout.flush()
            # Send to single NODE:  [CALLSIGN]|[MESSAGE]|[TO_NODE_ID]
            # Send to broadcast:    [CALLSIGN]|[MESSAGE]
            answer_array=fifo_msg_in.split("|")
            # Evaluate array len
            array_len = len(answer_array)
            # Send as broadcast by default on Edgemap UI
            if array_len == 2 or array_len == 4:
                print("Sending to broadcast")
                sys.stdout.flush()
                send_msg_from_fifo(interface, fifo_msg_in)
            # Send as individual recipient
            if array_len == 3:
                print("Sending to single recipient")
                sys.stdout.flush()
                answer_recipient = '!'+answer_array[2]
                answer_payload = answer_array[0]+"|"+answer_array[1]
                send_msg_from_fifo_to_one_node(interface, answer_payload, answer_recipient)
          else:
            # No fifo data
            # print('While loop: no fifo data')
            pass
            
    except Exception as e:
        print(f"Exception caught in thread: {e}")
        os._exit(0)  # Forcefully exits the entire Python process
#
# main 
#
def main():
  global interface
  global DeviceStatus
  global DeviceName
  global DevicePort
  global PacketsSent
  global PacketsReceived
  global LastPacketType
  global HardwareModel
  global MacAddress
  global DeviceID
  global HardwareModel
  global BaseLat
  global BaseLon

  try:

    DeviceName      = '??'
    DeviceStatus    = '??'
    DevicePort      = '??'
    PacketsReceived = 0
    PacketsSent     = 0
    LastPacketType  = ''
    HardwareModel   = ''
    MacAddress      = ''
    DeviceName      = ''
    DeviceID        = ''
    HardwareModel   = '??'
    BaseLat         = 0
    BaseLon         = 0


    # Check fifo files
    fifo_file='/tmp/msgchannel'
    if not os.path.isfile(fifo_file):
        print('Creating fifo file: ',fifo_file)
        create_fifo_pipe(fifo_file)
    if not stat.S_ISFIFO(os.stat(fifo_file).st_mode):
        print('re-creating fifo file: ',fifo_file)
        os.remove(fifo_file)
        create_fifo_pipe(fifo_file)
    
    fifo_file='/tmp/msgincoming'
    if not os.path.isfile(fifo_file):
        print('Creating fifo file: ',fifo_file)
        create_fifo_pipe(fifo_file)
    if not stat.S_ISFIFO(os.stat(fifo_file).st_mode):
        print('Missing fifo file: ',fifo_file)
        os.remove(fifo_file)
        create_fifo_pipe(fifo_file)

    fifo_file='/tmp/statusin'
    if not os.path.isfile(fifo_file):
        print('Creating fifo file: ',fifo_file)
        create_fifo_pipe(fifo_file)
    if not stat.S_ISFIFO(os.stat(fifo_file).st_mode):
        print('Missing fifo file: ',fifo_file)
        os.remove(fifo_file)
        create_fifo_pipe(fifo_file)

    fifo_file='/tmp/livegps'
    if not os.path.isfile(fifo_file):
        print('Creating fifo file: ',fifo_file)
        create_fifo_pipe(fifo_file)
    if not stat.S_ISFIFO(os.stat(fifo_file).st_mode):
        print('Missing fifo file: ',fifo_file)
        os.remove(fifo_file)
        create_fifo_pipe(fifo_file)

    # 
    # Create DB 
    #
    meshtasticDbCreate()


    print("Connecting to device at port {}".format(args.port))
    sys.stdout.flush()
    interface = meshtastic.serial_interface.SerialInterface(args.port)

    # Get node info for connected device
    GetMyNodeInfo(interface)
    # time.sleep(2)
    # print('*** MY NAME *** ',DeviceName)

    # subscribe to connection and receive channels
    pub.subscribe(onConnectionEstablished, "meshtastic.connection.established")
    pub.subscribe(onConnectionLost,        "meshtastic.connection.lost")
    pub.subscribe(onReceive, "meshtastic.receive")

    # Display nodes
    # DisplayNodes(interface)

    # Launch threads
    # BUG: Live blocks execution => 
    #      looks that loop in read_live_gps() was without time.sleep() 
    #      and it blocked. Disabling t1 was temporal cure, now there is 
    #      time.sleep() in thread to prevent blocking.
    t1 = threading.Thread(target=read_live_gps, args=())
    t2 = threading.Thread(target=read_manual_gps, args=()) 
    t3 = threading.Thread(target=read_incoming_fifo, args=()) 
    t1.start()
    t2.start()
    t3.start()
    t1.join()
    t2.join()
    t3.join()
    
    print("XXXXXXXXXXXXXXXXXXXXX")

    interface.close()  

  except Exception as ErrorMessage:
    time.sleep(2)
    TraceMessage = traceback.format_exc()
    AdditionalInfo = "Main function "
    ErrorHandler(ErrorMessage,TraceMessage,AdditionalInfo)

  signal(SIGINT, SIGINT_handler)


if __name__=='__main__':
  try:
      main()

  except Exception as ErrorMessage:
      TraceMessage = traceback.format_exc()
      AdditionalInfo = "Main pre-amble"
      ErrorHandler(ErrorMessage,TraceMessage,AdditionalInfo)

# %%

