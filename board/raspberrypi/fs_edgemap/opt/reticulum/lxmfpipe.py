#
# rnspipe - piping messages to/from FIFO over reticulum network with LXMF
#
# Copyright (c) Resilience Theatre, 2024
#
# fifo files:
#
# /tmp/rnsmsgoutput - messages from reticulum network
# /tmp/rnsmsginput - messages to reticulum network
#
# Remember you need to read /tmp/rnsmsgoutput continuously while developing:
#
#   while [ 1 ]; do cat /tmp/rnsmsgoutput; done; 
#
# These pipes are handled in Edgemap by gwsocket service
# 
# TODO: We need telemetry to UI
#
#

import RNS
import RNS.vendor.umsgpack as msgpack
import LXMF
import time
import random
import os
import sys
import sqlite3
import asyncio
import threading
import stat, os
from threading import Thread
from random import randrange, uniform
from urllib.parse import unquote

global lxmf_source
global announce_count
global lxmf_router

required_stamp_cost = 8
enforce_stamps = False

db_file = "/tmp/rns.db"
random_titles = ["m1", "m2", "m3"]

# Timeouts
message_send_delay_min=4 # 5 
message_send_delay_max=8 # 10
announce_min_time=120
announce_max_time=240
path_resolve_timeout_s=60
delivery_timeout_s=60

# Receive
# We will need to define an announce handler class that
# Reticulum can message when an announce arrives.
class AnnounceHandler:
    # The initialisation method takes the optional
    # aspect_filter argument. If aspect_filter is set to
    # None, all announces will be passed to the instance.
    # If only some announces are wanted, it can be set to
    # an aspect string.
    def __init__(self, aspect_filter=None):
        self.aspect_filter = aspect_filter
    # This method will be called by Reticulums Transport
    # system when an announce arrives that matches the
    # configured aspect filter. Filters must be specific,
    # and cannot use wildcards.
    def received_announce(self, destination_hash, announced_identity, app_data):
        
        # RNS.log("*** Announce: " + RNS.prettyhexrep(destination_hash))
        # We split app_data and check if announce has edgemap.[callsign] format
        # This is simple naming convention to separate edgemap announcements to our DB
        # Understanding lxmf better would be nicer, but it lacks documentation?
        if app_data is not None:
            # LXMF.display_name_from_app_data() was new thing
            callsign_split_string = LXMF.display_name_from_app_data( app_data )
            callsign_split_array = callsign_split_string.split('.')
            if len(callsign_split_array) == 2:
                insert_callsign = callsign_split_array[1]             
                if callsign_split_array[0] == 'edgemap':
                    RNS.log("Received edgemap announce: " + RNS.prettyhexrep(destination_hash) + " " + insert_callsign )
                    insert_destination = RNS.prettyhexrep(destination_hash)[1:-1]
                    insert_destination_hex = RNS.hexrep(destination_hash)
                    insert_destination_hex = insert_destination_hex.replace(":", "")
                    insert_destination_hex = str(insert_destination_hex)
                    reticulumDbUpdate( insert_callsign,insert_destination_hex )
                else:
                    RNS.log("Received non-edgemap announce: " + RNS.prettyhexrep(destination_hash) + " " + callsign_split_string )
            else:
                RNS.log("Received non-edgemap announce: " + RNS.prettyhexrep(destination_hash) + " " + callsign_split_string )

#
# UI update 
#
def updateUserInterface():

    row_count=0; 
    connection = sqlite3.connect(db_file)
    cursor = connection.cursor()
    sql_query = "SELECT *, (strftime('%s', 'now') - strftime('%s', timestamp)) / 60 AS elapsed_minutes,(strftime('%s', 'now') - strftime('%s', timestamp)) AS elapsed_seconds FROM rnsnodes"
    cursor.execute(sql_query)
    rows = cursor.fetchall()
    for row in rows:
        # print(row)
        peer_callsign = row[1]
        peer_hash = row[2]
        peer_timestamp = row[3] # not used
        peer_age_in_minutes = row[4]
        peer_age_in_seconds = row[5]
        # FIFO write to UI
        message_content = "reticulumnode," + peer_callsign + "," + str(peer_age_in_minutes) + "," + peer_hash + "\n"   
        # RNS.log("UI update: " + message_content )
        fifo_write = open('/tmp/reticulumstatusin', 'w')
        fifo_write.write(message_content)
        fifo_write.flush()
        time.sleep(0.2)
    connection.commit()
    connection.close()
    
#
# Automatic announce loop
#
async def announce_loop():
    
    global announce_count
    global lxmf_source
    global lxmf_router
    
    while True:
        # Announce
        lxmf_router.announce(destination_hash=lxmf_source.hash)
        RNS.log("Announced "  + RNS.prettyhexrep(lxmf_source.hash))
        if announce_count < 1:
            sleep_time = randrange(10, 30)
            announce_count = announce_count +1
        else:
            sleep_time = randrange(announce_min_time, announce_max_time)
        
        RNS.log("Periodic announce, next in " + str(sleep_time) + " seconds")
        await asyncio.sleep(sleep_time)


async def update_ui_loop():
    while True:
        # RNS.log("Updating UI")
        updateUserInterface()
        await asyncio.sleep(30)


# Receive
def reticulumDbCreate():
    connection = sqlite3.connect(db_file)
    # print(connection.total_changes)
    cursor = connection.cursor()
    # Check if table exist
    listOfTables = cursor.execute("""SELECT tbl_name FROM sqlite_master WHERE type='table' AND tbl_name="rnsnodes";""").fetchall();
    if listOfTables == []:
        RNS.log("[DB] creating rnsnodes table")
        cursor.execute("CREATE TABLE rnsnodes (id INTEGER PRIMARY KEY AUTOINCREMENT, callsign TEXT, destination TEXT, timestamp TEXT )")
    else:
        RNS.log("[DB] found existing rnsnodes table")

# Receive
def reticulumDbUpdate(callsign,destination_hash):    
    connection = sqlite3.connect(db_file)
    # print(connection.total_changes)
    cursor = connection.cursor()
    # Check if callsign exist
    cursor.execute("SELECT * FROM rnsnodes WHERE callsign = ?", (callsign,) )
    rows = len( cursor.fetchall() )
    if ( rows == 0 ):
        cursor.execute("INSERT INTO rnsnodes (callsign,destination,timestamp) VALUES (?,?,current_timestamp)", (callsign,destination_hash))
    else:
        cursor.execute("UPDATE rnsnodes SET callsign = ?, destination = ?, timestamp = current_timestamp  WHERE callsign = ?", (callsign, destination_hash, callsign))
    connection.commit()
    connection.close()

# Read DB for all destination hashes
def reticulumDbReadAll():
    row_count=0; 
    connection = sqlite3.connect(db_file)
    cursor = connection.cursor()
    # Select all
    cursor.execute("SELECT * FROM rnsnodes" )
    rows = cursor.fetchall()
    for row in rows:
        # print(row)
        peer_hash_array.append(row[2])
        peer_callsign_array.append(row[1])
        row_count+=1
    connection.commit()
    connection.close()
    return row_count


#
# Read DB for nodes within time limit (NOTE: Not in use, we use inline!)
#
# id  callsign  destination                       timestamp            elapsed_minutes  elapsed_seconds
# --  --------  --------------------------------  -------------------  ---------------  ---------------
# 1   edgez     4b4c4977d30b13ee2235e446ea23231f  2024-09-10 02:10:25  1                91             
# 2   edgey     33bdac14112980fad6367651e7729620  2024-09-10 02:11:04  0                52             
# 3   edgex     ebcf01a0e80d2d5c397d6ac98c050cbd  2024-09-10 02:11:47  0                9     
#
def reticulumDbReadTimeLimitNodes(age_limit_in_minutes):
    row_count=0; 
    connection = sqlite3.connect(db_file)
    cursor = connection.cursor()
    cursor.execute("SELECT *, (strftime('%s', 'now') - strftime('%s', timestamp)) / 60 AS elapsed_minutes,(strftime('%s', 'now') - strftime('%s', timestamp)) AS elapsed_seconds FROM rnsnodes" )
    rows = cursor.fetchall()
    for row in rows:
        print(row)
        if row[4] < age_limit_in_minutes:
            peer_callsign_array.append(row[1])
            peer_hash_array.append(row[2])
            peer_age_in_minutes_array.append(row[4])
            peer_age_in_seconds_array.append(row[5])
            row_count+=1
    connection.commit()
    connection.close()
    return row_count

# For UI ( REMOVE THIS ??) 
def reticulumDbReadNodeAge(callsign):
    row_count=0; 
    connection = sqlite3.connect(db_file)
    cursor = connection.cursor()
    sql_query = "SELECT *, (strftime('%s', 'now') - strftime('%s', timestamp)) / 60 AS elapsed_minutes,(strftime('%s', 'now') - strftime('%s', timestamp)) AS elapsed_seconds FROM rnsnodes WHERE callsign IS '" + callsign + "'"
    cursor.execute(sql_query)
    rows = cursor.fetchall()
    for row in rows:
        print(row)
        peer_age_in_minutes = row[4]
        peer_age_in_seconds = row[5]

    connection.commit()
    connection.close()
    
    return peer_age_in_minutes

# For incoming message
def delivery_callback(message):
    time_string      = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(message.timestamp))
    signature_string = "Signature is invalid, reason undetermined"
    if message.signature_validated:
        signature_string = "Validated"
    else:
        if message.unverified_reason == LXMF.LXMessage.SIGNATURE_INVALID:
            signature_string = "Invalid signature"
        if message.unverified_reason == LXMF.LXMessage.SOURCE_UNKNOWN:
            signature_string = "Cannot verify, source is unknown"
    
    if message.stamp_valid:
        stamp_string = "Validated"
    else:
        stamp_string = "Invalid"
    
    RNS.log("\t+--- LXMF Delivery ---------------------------------------------")
    RNS.log("\t| Source hash            : "+RNS.prettyhexrep(message.source_hash))
    RNS.log("\t| Source instance        : "+str(message.get_source()))
    RNS.log("\t| Destination hash       : "+RNS.prettyhexrep(message.destination_hash))
    RNS.log("\t| Destination instance   : "+str(message.get_destination()))
    RNS.log("\t| Transport Encryption   : "+str(message.transport_encryption))
    RNS.log("\t| Timestamp              : "+time_string)
    RNS.log("\t| Title                  : "+message.title_as_string())
    RNS.log("\t| Content                : "+message.content_as_string())
    RNS.log("\t| Fields                 : "+str(message.fields))
    RNS.log("\t| Message signature      : "+signature_string)
    RNS.log("\t+---------------------------------------------------------------")

    # Write fifo 
    message_content = message.content_as_string()
    write_msg_fifo(message_content)
    
    #fifo_write = open('/tmp/rnsmsgoutput', 'w')
    #fifo_write.write(message_content)
    #fifo_write.flush()


def write_msg_fifo(message):
    fifo_write = open('/tmp/rnsmsgoutput', 'w')
    fifo_write.write(message)
    fifo_write.flush()

async def handle_message_delivery(peer_hash,lxmf_message,peer_callsign):

    # Set timeout in seconds
    timeout_after_seconds = time.time() + delivery_timeout_s
    
    while lxmf_message.state != LXMF.LXMessage.DELIVERED and lxmf_message.state != LXMF.LXMessage.FAILED:
        # RNS.log("Waiting:  " + str(time.time()) + " vs " + str(timeout_after_seconds) )
        if time.time() > timeout_after_seconds:
            RNS.log("Delivery timeout:  <" + peer_hash + "> " + peer_callsign)
            return_value = "Timeout: " + peer_hash + " " + peer_callsign
            delivery_message="|msg_delivery_timeout||" + peer_callsign 
            write_msg_fifo(delivery_message)
            return return_value
        await asyncio.sleep(1)
    
    if lxmf_message.state == LXMF.LXMessage.FAILED:
        RNS.log("Delivery: LXMF.LXMessage.FAILED")
        delivery_message="|msg_delivery_timeout||" + peer_callsign 
        write_msg_fifo(delivery_message)
        return_value = "Failed: " + peer_hash + " " + peer_callsign
        return return_value
    
    return_value = "Delivered: " + peer_hash + " " + peer_callsign
    RNS.log("Delivered: <" + peer_hash + "> " + peer_callsign )
    delivery_message="|msg_delivery_ok||" + peer_callsign 
    write_msg_fifo(delivery_message)
    return return_value



# Main task
async def send_msg_out(message_payload):
    
    global lxmf_source # ??
    
    # Arrays
    recipient_hash_array = []
    recipient_array = []
    dest_array = []
    lxm_array = []
    pindex=0;
    
    # Message delivery tasks
    deliverytasks = []
    peer_hash_array = []
    peer_callsign_array = []
    peer_age_in_minutes_array = []
    peer_age_in_seconds_array = []
    
    # Read nodes within timelimit from DB
    within_timelimit = 6
        
    # Inline DB read
    row_count=0; 
    connection = sqlite3.connect(db_file)
    cursor = connection.cursor()
    cursor.execute("SELECT *, (strftime('%s', 'now') - strftime('%s', timestamp)) / 60 AS elapsed_minutes,(strftime('%s', 'now') - strftime('%s', timestamp)) AS elapsed_seconds FROM rnsnodes" )
    rows = cursor.fetchall()
    for row in rows:
        # print(row)
        if row[4] < within_timelimit:
            peer_callsign_array.append(row[1])
            peer_hash_array.append(row[2])
            peer_age_in_minutes_array.append(row[4])
            peer_age_in_seconds_array.append(row[5])
            row_count+=1
    connection.commit()
    connection.close()
    
    node_count=row_count
    RNS.log("Node Count: " + str(node_count) + " (last heard within " + str(within_timelimit) + " minutes) ")
    
    about_to_send_message="|msg_send_start||" + str(node_count)
    write_msg_fifo(about_to_send_message)
    
    for x in peer_hash_array:
        
        # print("----- ", pindex, " -----")
        recipient_hash_array.append( bytes.fromhex(x) )
        timeout_after_seconds = time.time() + path_resolve_timeout_s
        
        if not RNS.Transport.has_path(recipient_hash_array[pindex]):
            # RNS.log("Requesting destination path: " + x + " " + peer_callsign_array[pindex])
            RNS.Transport.request_path( recipient_hash_array[pindex] )
            
            while not RNS.Transport.has_path( recipient_hash_array[pindex] ) and time.time() < timeout_after_seconds:
                await asyncio.sleep(0.1)
            
            if time.time() >= timeout_after_seconds:
                RNS.log("Timeout for destination path: " + x + " " + peer_callsign_array[pindex] )
                pindex -= 1 # check this
            else:
                RNS.log( "[" + str(pindex) + "] Sending to new destination path: <" + x + "> " + peer_callsign_array[pindex] + " Age: " + str(peer_age_in_minutes_array[pindex]) + " min / " + str(peer_age_in_seconds_array[pindex]) + " s" )
                recipient_array.append( RNS.Identity.recall(recipient_hash_array[pindex]) )
                dest_array.append( RNS.Destination(recipient_array[pindex], RNS.Destination.OUT, RNS.Destination.SINGLE, "lxmf", "delivery") )
                lxm_array.append( LXMF.LXMessage(dest_array[pindex], lxmf_source, message_payload, random_titles[random.randint(0,len(random_titles)-1)], desired_method=LXMF.LXMessage.DIRECT) )
                # RNS.log("Sending message to: " + peer_callsign_array[pindex])
                lxmf_router.handle_outbound(lxm_array[pindex])
                deliverytasks.append( asyncio.create_task(handle_message_delivery(x,lxm_array[pindex],peer_callsign_array[pindex])) )            
            pindex += 1 # check this
        else:
            RNS.log( "[" + str(pindex) + "] Sending to known path: <" + x + "> " + peer_callsign_array[pindex] + " Age: " + str(peer_age_in_minutes_array[pindex]) + " min / " + str(peer_age_in_seconds_array[pindex]) + " s" )
            recipient_array.append( RNS.Identity.recall(recipient_hash_array[pindex]) )
            dest_array.append( RNS.Destination(recipient_array[pindex], RNS.Destination.OUT, RNS.Destination.SINGLE, "lxmf", "delivery") )
            lxm_array.append( LXMF.LXMessage(dest_array[pindex], lxmf_source, message_payload, random_titles[random.randint(0,len(random_titles)-1)], desired_method=LXMF.LXMessage.DIRECT) )
            # RNS.log("Sending message to: "  + peer_callsign_array[pindex] )
            lxmf_router.handle_outbound(lxm_array[pindex])
            deliverytasks.append( asyncio.create_task(handle_message_delivery(x,lxm_array[pindex],peer_callsign_array[pindex])) )
            pindex += 1 # check this
        
        # Don't push all messages out at once, randomly wait between msg
        sleep_time = randrange(message_send_delay_min, message_send_delay_max)
        await asyncio.sleep(sleep_time)
    
    RNS.log("=========")
    RNS.log("Waiting for delivery ack's")
    results = await asyncio.gather(*deliverytasks)
    sresults = ' '.join(results)
    # TODO: Check using this results array in future
    # RNS.log("Results: " + sresults)
    # WORK IN PROGRESS
    # Write fifo 
    # message_content = message.content_as_string()
    # fifo_write = open('/tmp/rnsmsgoutput', 'w')
    # fifo_write.write(message_content)
    # fifo_write.flush()
    
    

# Fifo create
def create_fifo_pipe(pipe_path):
    try:
        os.mkfifo(pipe_path)
        RNS.log("Fifo created: " + pipe_path)
    except OSError as e:
        pass
        # print(f"Error: {e}")



#
# == Start here ==
#
RNS.log("Message send delays (s) " + str(message_send_delay_min) +" - " + str(message_send_delay_max) ) 
RNS.log("Announce interval (s) " + str(announce_min_time) +" - " + str(announce_max_time) ) 
RNS.log("Path resolve timeout (s): " + str(path_resolve_timeout_s) +" Delivery timeout (s): " + str(delivery_timeout_s) ) 

# Load callsign
if ( os.path.isfile("/opt/edgemap-persist/callsign.txt") ):
    callsign_file = open("/opt/edgemap-persist/callsign.txt", "r")
    callsign = callsign_file.readline()
    callsign_file.close()
    callsign=callsign[:-1]
    # callsign=callsign.encode("utf-8")
else:
    callsign = "no-callsign"

RNS.log("Callsign: " + str(callsign) )

# Load identity
path="rns-edgemap"
identitypath = "rns-edgemap/identity"
if not os.path.exists(path):
    RNS.log("Creating rns-edgemap directory")
    os.mkdir(path)

if os.path.isfile(identitypath):
    try:
        ident = RNS.Identity.from_file(identitypath)
        if ident != None:
            RNS.log("Identity %s from %s" % (str(ident), identitypath))
        else:
            RNS.log("Could not load the Primary Identity from "+identitypath, RNS.LOG_ERROR)
            sys.exit()
    except Exception as e:
        RNS.log("Could not load the Primary Identity from "+identitypath, RNS.LOG_ERROR)
        RNS.log("The contained exception was: %s" % (str(e)), RNS.LOG_ERROR)
        sys.exit()
else:
    try:
        RNS.log("No Primary Identity file found, creating new...")
        ident = RNS.Identity()
        ident.to_file(identitypath)
        RNS.log("Created new Primary Identity %s" % (str(ident)))
    except Exception as e:
        RNS.log("Could not create and save a new Primary Identity", RNS.LOG_ERROR)
        RNS.log("The contained exception was: %s" % (str(e)), RNS.LOG_ERROR)
        sys.exit()


# Create database
reticulumDbCreate()

# Use configuration under /opt/meshchat
if os.path.exists("/opt/meshchat"):
    RNS.log("Using configuration from /opt/meshchat")
    r = RNS.Reticulum("/opt/meshchat")
else:
    RNS.log("Using default configuration file")
    r = RNS.Reticulum()


announce_count=0
announce_handler = AnnounceHandler(
    aspect_filter="lxmf.delivery"
)
RNS.Transport.register_announce_handler(announce_handler)

# LXMF Router
lxmf_router = LXMF.LXMRouter(storagepath="rns-send-storage", enforce_stamps=enforce_stamps)
lxmf_router.register_delivery_callback(delivery_callback) # incoming messages 

RNS.log("LXMF router created")

# Form appdata as edgemap.[callsign] * BUG Fixing * ??  lxmf_source_callsign,
lxmf_source_callsign = str("edgemap." + str(callsign))
RNS.log("LXMF source callsign: " + lxmf_source_callsign)

lxmf_source = lxmf_router.register_delivery_identity(identity=ident,display_name=lxmf_source_callsign,stamp_cost=required_stamp_cost)
lxmf_source.PROCESSING_INTERVAL = 1

# Thread to announce periodically
RNS.log("Starting periodic announcements with random intervals")
thread = threading.Thread(target=asyncio.run, args=(announce_loop(),))
thread.daemon = True
thread.start()

# Thread to update UI periodically
RNS.log("Starting periodic UI update")
thread = threading.Thread(target=asyncio.run, args=(update_ui_loop(),))
thread.daemon = True
thread.start()

# Create FIFO out to websocket
fifo_file_out='/tmp/reticulumstatusin'
if not os.path.isfile(fifo_file_out):
    RNS.log("Creating fifo file: " + fifo_file_out)
    create_fifo_pipe(fifo_file_out)
if not stat.S_ISFIFO(os.stat(fifo_file_out).st_mode):
    RNS.log("re-creating fifo file: " + fifo_file_out)
    os.remove(fifo_file_out)
    create_fifo_pipe(fifo_file_out)

# Create FIFO out
fifo_file_out='/tmp/rnsmsgoutput'
if not os.path.isfile(fifo_file_out):
    RNS.log("Creating fifo file: " + fifo_file_out)
    create_fifo_pipe(fifo_file_out)
if not stat.S_ISFIFO(os.stat(fifo_file_out).st_mode):
    RNS.log("re-creating fifo file: " + fifo_file_out)
    os.remove(fifo_file_out)
    create_fifo_pipe(fifo_file_out)

# Create FIFO In
fifo_file='/tmp/rnsmsginput'
if not os.path.isfile(fifo_file):
    RNS.log("Creating fifo file: " + fifo_file)
    create_fifo_pipe(fifo_file)
if not stat.S_ISFIFO(os.stat(fifo_file).st_mode):
    RNS.log("re-creating fifo file: " + fifo_file)
    os.remove(fifo_file)
    create_fifo_pipe(fifo_file)


# Read incoming fifo for outgoing messages
while True:
    
    fifo_file='/tmp/rnsmsginput'
    
    fifo_read=open(fifo_file,'r')
    fifo_msg_in = fifo_read.readline()[:-1]
    
    if not fifo_msg_in == "":
        RNS.log("FIFO input: " + fifo_msg_in )
        start_time = time.time()
        asyncio.run( send_msg_out(fifo_msg_in) )
        end_time = time.time()
        RNS.log("Send time: " + str( round(end_time - start_time,2) ) + " seconds (for all destinations)")
        RNS.log("Waiting for FIFO input...")
        send_compeleted_message="|msg_delivery_complete||" + str( round(end_time - start_time,2) ) 
        write_msg_fifo(send_compeleted_message)
    
    time.sleep(0.1)
    
else:
    # No fifo data
    time.sleep(1)
    pass
        
#except Exception as e:
        #print(f"Exception caught: {e}")


sys.exit()
