##########################################################
#                                                        #
# rnslink.py                                             #
#                                                        #
# Connect on message variant                             #
#                                                        #
##########################################################
#
# Simple example how reticulum link delivers messaging
# between Edgemap units. This script reads and writes
# fifo where edgemap UI delivers messages via gwsocket.
#
# This is tested with four RPi's connected via RNodes.
#
# FIFO's 
# 
# /tmp/rnsmsgoutput         FIFO out: messages which are received "from rns link"
# /tmp/rnsmsginput          FIFO in:  "messages in" to be sent "to link"
# /tmp/reticulumstatusin    FIFO out: Update UI status messages to UI
# /tmp/reticulumcontrol     FIFO in: control rnslink.py to send announces etc
#
# To develop, you need to read fifo's like:
#
# while [ 1 ]; do cat /tmp/rnslinkoutput; done;
# 
# BOLD: \033[1m \033[0m
# RED: \033[31m \033[0m
#
import os
import sys
import time
import argparse
import random
import asyncio
import threading
import RNS
import asyncio
import stat, os
import configparser
import sqlite3
from threading import Thread
from random import randrange, uniform

APP_NAME = "link"
fruits = ["Peach", "Quince", "Date", "Tangerine", "Pomelo", "Carambola", "Grape"]
server_identity = None
server_destination = None
server_connected_clients_count = None
tracked_announces = []
tracked_links_on_server = []
tracked_links_on_client = []
destinations_we_have_link = []
# A reference to the server link. Check is there race condition.
server_link = None
# A reference to the client identity
client_identity = None
g_link_statistic = False
g_initial_link_connect_delay = None
# database
db_file = "/tmp/rns.db"

# Initialize the parser and read the file
config = configparser.ConfigParser()
config.read('rnslink.ini')
g_node_id = config['settings']['node_id']
g_node_callsign = config['settings']['callsign']
g_fifo_file_in = config['settings']['fifo_file_in']
g_fifo_file_out = config['settings']['fifo_file_out']
g_fifo_reticulum_control = config['settings']['fifo_file_reticulum_control']
# Announce rates & connect delay
g_initial_announce_delay = int(g_node_id) + 2
# Not in use in this version (where announces do not trigger connection)
g_initial_link_connect_delay = 4 * ( int(g_node_id) - 1 )
g_connection_in_progress=False

##########################################################
# Database 
##########################################################

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

def reticulumDbErase():    
    connection = sqlite3.connect(db_file)
    cursor = connection.cursor()
    cursor.execute("DELETE FROM rnsnodes")
    connection.commit()
    connection.close()

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
        peer_callsign = row[1]
        peer_hash = row[2]
        peer_timestamp = row[3] # not used
        peer_age_in_minutes = row[4]
        peer_age_in_seconds = row[5]
        # Inform UI about nodes we have
        # do we have link to destination?
        
        if peer_hash in destinations_we_have_link:
            link_eshtablished = "Yes"
        else:
            link_eshtablished = "-";
        
        message_content = "reticulumnode," + peer_callsign + "," + str(peer_age_in_minutes) + "," + peer_hash + "," + link_eshtablished + "\n"
        write_reticulum_status_fifo(message_content)
        time.sleep(0.2)
    connection.commit()
    connection.close()

def write_reticulum_status_fifo(payload):
    fifo_write = open('/tmp/reticulumstatusin', 'w')
    fifo_write.write(payload)
    fifo_write.flush()

# Send nodes to UI every 15 s
async def update_ui_loop():
    while True:
        updateUserInterface()
        await asyncio.sleep(15)

def write_status_of_connected_client_count():
    tracked_client_connections=len(tracked_links_on_server)
    response_text="client_count," + str(tracked_client_connections)
    write_reticulum_status_fifo(response_text)

# Read server control fifo from UI, manual announce and client count
async def read_server_control_fifo():
    
    while True:
        # Create FIFO in for reticulum control
        if not os.path.isfile(g_fifo_reticulum_control):
            # RNS.log("Creating fifo file: " + g_fifo_reticulum_control)
            create_fifo_pipe(g_fifo_reticulum_control)
        if not stat.S_ISFIFO(os.stat(g_fifo_reticulum_control).st_mode):
            # RNS.log("re-creating fifo file: " + g_fifo_reticulum_control)
            os.remove(g_fifo_reticulum_control)
            create_fifo_pipe(g_fifo_reticulum_control)
        # Open fifo
        fifo_read_control=open(g_fifo_reticulum_control,'r')
    
        while True:
            fifo_msg_in = fifo_read_control.readline()[:-1]            
            if not fifo_msg_in == "":
                # RNS.log("FIFO input for reticulum control: " + fifo_msg_in )                
                if fifo_msg_in == "announce":
                    announce_manual()
                if fifo_msg_in == "clients_connected":
                    write_status_of_connected_client_count()  
                await asyncio.sleep(1)
            else:
                # No fifo data
                await asyncio.sleep(1)
                pass

# Create database
reticulumDbCreate()

##########################################################
# Server Mode 
##########################################################

# Automatic announce loop (only server announces)
async def announce_loop(): 
    global server_destination
    global g_node_callsign
    global g_initial_announce_delay
    global g_announce_delay
    
    RNS.log("First periodic announce in " + str(g_initial_announce_delay) + " s." )
    await asyncio.sleep( g_initial_announce_delay )
    
    while True:
        callsign_app_data = "edgemap." + g_node_callsign
        callsign_app_data_encoded=callsign_app_data.encode('utf-8')
        server_destination.announce(app_data=callsign_app_data_encoded)
        g_announce_delay = randrange(120, 240)
        RNS.log("Periodic announce done. Next in " + str(g_announce_delay) + " s." )
        await asyncio.sleep(g_announce_delay)

# Manual announce, triggered from web ui
def announce_manual(): 
    global server_destination
    global g_node_callsign
    callsign_app_data = "edgemap." + g_node_callsign
    callsign_app_data_encoded=callsign_app_data.encode('utf-8')
    server_destination.announce(app_data=callsign_app_data_encoded)
    RNS.log("Sent manual announce")
    
# A reference to the latest client link that connected
latest_client_link = None

# edgemap-message request
def edgemap_message_request(path, data, request_id, link_id, remote_identity, requested_at):
    RNS.log("Message in from link: "+RNS.prettyhexrep(link_id))
    # RNS.log("Edgemap message: "+RNS.prettyhexrep(request_id)+" on link: "+RNS.prettyhexrep(link_id))
    # RNS.log(" Remote identity: "+str(remote_identity) ) 
    # RNS.log(" Data received: " + str(data) )
    # RNS.log(" Time stamp: " + str(requested_at) )
    
    # Write fifo and return ack field
    write_received_msg_to_fifo( str(data) )
    reply = "message-ack," + g_node_callsign
    return reply

# not in use: edgemap-link-connected request
def edgemap_link_connected_request(path, data, request_id, link_id, remote_identity, requested_at):
    RNS.log("Edgemap link-connected request: "+RNS.prettyhexrep(request_id)+" on link: "+RNS.prettyhexrep(link_id))
    RNS.log(" Remote identity: "+str(remote_identity) ) 
    RNS.log(" Data received: " + str(data) )
    RNS.log(" requested_at: " + str(requested_at) ) # timestamp
    # Write fifo and return ack field
    write_received_msg_to_fifo( str(data) )
    reply = "conn_ack," + g_node_callsign
    return reply

# FIFO functions
def create_fifo_pipe(pipe_path):
    try:
        os.mkfifo(pipe_path)
        RNS.log("FIFO created: " + pipe_path)
    except OSError as e:
        pass
        # print(f"Error: {e}")

def write_received_msg_to_fifo(message):
    global g_fifo_file_out
    fifo_write = open(g_fifo_file_out, 'w')
    fifo_write.write(message)
    fifo_write.flush()

#
# Run as server
#
def server():
    global server_destination
    global g_fifo_file_out
    # Erase DB
    reticulumDbErase()
    # Create FIFO out (messages which are received, eg. "output from link")
    if not os.path.isfile(g_fifo_file_out):
        create_fifo_pipe(g_fifo_file_out)
    if not stat.S_ISFIFO(os.stat(g_fifo_file_out).st_mode):
        os.remove(g_fifo_file_out)
        create_fifo_pipe(g_fifo_file_out)

    # Thread to read UI commands
    thread = threading.Thread(target=asyncio.run, args=(read_server_control_fifo(),))
    thread.daemon = True
    thread.start()

    # Reticulum initialization
    reticulum = RNS.Reticulum("/opt/meshchat")
    
    # Load or persist SERVER identity
    server_identity_path="rnslink_server"
    identity_filename = server_identity_path + "/identity"
    if not os.path.exists(server_identity_path):
        RNS.log("Creating " + server_identity_path + " directory")
        os.mkdir(server_identity_path)

    if os.path.isfile(identity_filename):
        try:
            server_identity = RNS.Identity.from_file(identity_filename)
            if server_identity != None:
                RNS.log("Identity %s from %s" % (str(server_identity), identity_filename))
            else:
                RNS.log("Could not load the Primary Identity from "+identity_filename, RNS.LOG_ERROR)
                sys.exit()
        except Exception as e:
            RNS.log("Could not load the Primary Identity from "+identity_filename, RNS.LOG_ERROR)
            RNS.log("The contained exception was: %s" % (str(e)), RNS.LOG_ERROR)
            sys.exit()
    else:
        try:
            RNS.log("No Primary Identity file found, creating new...")
            server_identity = RNS.Identity()
            server_identity.to_file(identity_filename)
            RNS.log("Created new Primary Identity %s" % (str(server_identity)))
        except Exception as e:
            RNS.log("Could not create and save a new Primary Identity", RNS.LOG_ERROR)
            RNS.log("The contained exception was: %s" % (str(e)), RNS.LOG_ERROR)
            sys.exit()
        
    # Server destination
    server_destination = RNS.Destination(
        server_identity,
        RNS.Destination.IN,
        RNS.Destination.SINGLE,
        APP_NAME,
        "edgemap"
    )
        
    # Request registration for 'edgemap messages'
    server_destination.register_request_handler(
    "/edgemap-message",
    response_generator = edgemap_message_request,
    allow = RNS.Destination.ALLOW_ALL
    )
    
    # Not used: Request registration for 'edgemap link connection'
    server_destination.register_request_handler(
    "/edgemap-connection",
    response_generator = edgemap_link_connected_request,
    allow = RNS.Destination.ALLOW_ALL
    )
    
    # We configure the destination to automatically prove all
    # packets addressed to it. By doing this, RNS will automatically
    # generate a proof for each incoming packet and transmit it
    # back to the sender of that packet. This will let anyone that
    # tries to communicate with the destination know whether their
    # communication was received correctly.
    server_destination.set_proof_strategy(RNS.Destination.PROVE_ALL)
    
    # Callback for new client
    server_destination.set_link_established_callback(client_link_connected)
    
    # Start thread to announce periodically
    # NOTE: This version does not trigger link connection from client 
    # side when announce is received. Link connects when messages are sent
    # out.
    RNS.log("Starting periodic announcement thread.")
    thread = threading.Thread(target=asyncio.run, args=(announce_loop(),))
    thread.daemon = True
    thread.start()
    
    # Everything's ready, run server_loop()
    server_loop(server_destination)

def server_loop(destination):  
    # Let the user know that everything is ready
    RNS.log( "This server destination: " + RNS.prettyhexrep(destination.hash)  )
    
    while True:
        time.sleep(1)
        # If needed: Method for server to send messages to all connected links:
        # entered = input()
        # if entered == "a":
        #     RNS.log("Sending announce...")
        #    announce_manual()
        #if entered == "m":
        #    for client_link in tracked_links_on_server:
        #        RNS.log("Sending message to link: " + str(client_link)  )
        #        reply_text = "[server outboud] from: " + g_node_callsign
        #        reply_data = reply_text.encode("utf-8")
        #        RNS.Packet(client_link, reply_data).send()
        #        time.sleep(0.5)
                

# Incoming client 'link establishment callback' for server
def client_link_connected(link):
    global tracked_links_on_server    
    RNS.log(" Client connected with link: " + str(link)  )
    # Track links on server
    tracked_links_on_server.append(link) 
    # enable phy status to experiment
    link.track_phy_stats(True)
    # Set callbacks 
    link.set_packet_callback(server_packet_received)
    link.set_link_closed_callback(client_disconnected)
    link.set_remote_identified_callback(server_remote_identified)
    # Inform UI
    write_status_of_connected_client_count()

def server_remote_identified(link, identity):
    # Enable for debug with 'True':
    if True:        
        RNS.log("Connected client identity:  " + str(identity)  )
        RNS.log("RSSI:   " + str( link.get_rssi() )  )
        RNS.log("SNR:    " + str( link.get_snr() )  )
        RNS.log("Quality:" + str( link.get_q() )  )

# Reply to incoming link packets. NOTE: We don't use this anymore,
# we have request method for message and ack delivery. 
# TODO: Remove this
def server_packet_received(message, packet):
    # Received on link
    received_on_link = packet.link
    # Get the originating identity for display
    remote_peer = "unidentified peer"
    if packet.link.get_remote_identity() != None:
        remote_peer = str(packet.link.get_remote_identity())

    # Display text, from and link
    text = message.decode("utf-8")
    RNS.log("Received from " + remote_peer + ": " + text )
    RNS.log(" Via link:" + str(received_on_link) )
    # Display link stats
    if g_link_statistic:
        RNS.log("  inactive_for(): " + str(received_on_link.inactive_for() ) )
        RNS.log("  no_data_for(): " + str(received_on_link.no_data_for() ) ) 
        RNS.log("  no_inbound_for(): " + str(received_on_link.no_inbound_for() ) ) 
        RNS.log("  no_outbound_for(): " + str(received_on_link.no_outbound_for() ) ) 
        RNS.log("  get_age(): " + str(received_on_link.get_age() ) ) 
        RNS.log("  Keep alive: " + str(received_on_link.KEEPALIVE ) )
        # TODO: get rssi, snr here
    RNS.log(" ------------------------------------------------------------" )
    # Send reply (commented out for testing)
    reply_text = text + " [ACK] [" + g_node_callsign +"]"
    reply_data = reply_text.encode("utf-8")
    RNS.Packet(received_on_link, reply_data).send()
    
def client_disconnected(link):
    global tracked_links_on_server
    RNS.log("Client disconnected with link: " + str(link) )
    tracked_links_on_server.remove(link)
    
def remote_identified(link, identity):
    RNS.log("Remote identified as: "+str(identity))




##########################################################
# Client Part
##########################################################

#
# announce handler class for client
#
class AnnounceHandler:
    def __init__(self, aspect_filter=None):
        self.aspect_filter = aspect_filter
    def received_announce(self, destination_hash, announced_identity, app_data):
        # RNS.log("[RAW] Announce: " + RNS.prettyhexrep(destination_hash))
        global g_connection_in_progress
        global tracked_announces
        global server_link
                                
        if app_data is not None:
            announce_app_data_decoded = app_data.decode('utf-8')
            # RNS.log("[RAW] Announce app_data: " + str(announce_app_data_decoded) )
            callsign_split_array = announce_app_data_decoded.split('.')
            
            if len(callsign_split_array) == 2:
                # If we have connection to another announce in progress, skip any incoming announce handling
                if g_connection_in_progress == False:
                    insert_callsign = callsign_split_array[1]
                    if callsign_split_array[0] == 'edgemap':
                        # RNS.log("Received edgemap announce: " + RNS.prettyhexrep(destination_hash) + " " + insert_callsign )
                        insert_destination = RNS.prettyhexrep(destination_hash)[1:-1]
                        insert_destination_hex = RNS.hexrep(destination_hash)
                        insert_destination_hex = insert_destination_hex.replace(":", "")
                        insert_destination_hex = str(insert_destination_hex)
                        reticulumDbUpdate( insert_callsign,insert_destination_hex )
                        # Inform UI: announcereceived,[callsign],[hash]
                        message_content = "announcereceived," + insert_callsign + "," + insert_destination_hex + "\n"   
                        fifo_write = open('/tmp/reticulumstatusin', 'w')
                        fifo_write.write(message_content)
                        fifo_write.flush()
                        # Track announces as client
                        server_link = ""
                        if destination_hash.hex() not in tracked_announces:                            
                            # Append destination_hash to tracked_announces
                            tracked_announces.append(destination_hash.hex())
                            announce_entries=len(tracked_announces)                            
                            RNS.log("\033[1m [" + str(announce_entries) + "]\033[0m [NEW] Announce: " + RNS.prettyhexrep(destination_hash) + " " + insert_callsign)
                        else:
                            # We've seen this announce already
                            pass
                else:
                    RNS.log("[SKIP] Connection in progress, skipping announce handling.")
            else:
                # Should not happen
                RNS.log("Received non-edgemap announce: " + RNS.prettyhexrep(destination_hash) + " " + callsign_split_string )
                

# Run as 'client'
def client():
    global client_identity
    global server_link
    global g_initial_link_connect_delay
    
    # Reticulum instance
    reticulum = RNS.Reticulum("/opt/meshchat")
    
    # Load or persist CLIENT identity
    client_identity_path="rnslink_client"
    identity_filename = client_identity_path + "/identity"
    if not os.path.exists(client_identity_path):
        RNS.log("Creating " + client_identity_path + " directory")
        os.mkdir(client_identity_path)

    if os.path.isfile(identity_filename):
        try:
            client_identity = RNS.Identity.from_file(identity_filename)
            if client_identity != None:
                RNS.log("Identity %s from %s" % (str(client_identity), identity_filename))
            else:
                RNS.log("Could not load the Primary Identity from "+identity_filename, RNS.LOG_ERROR)
                sys.exit()
        except Exception as e:
            RNS.log("Could not load the Primary Identity from "+identity_filename, RNS.LOG_ERROR)
            RNS.log("The contained exception was: %s" % (str(e)), RNS.LOG_ERROR)
            sys.exit()
    else:
        try:
            RNS.log("No Primary Identity file found, creating new...")
            client_identity = RNS.Identity()
            client_identity.to_file(identity_filename)
            RNS.log("Created new Primary Identity %s" % (str(client_identity)))
        except Exception as e:
            RNS.log("Could not create and save a new Primary Identity", RNS.LOG_ERROR)
            RNS.log("The contained exception was: %s" % (str(e)), RNS.LOG_ERROR)
            sys.exit()

    
    # Setup announce handler, everything is threaded from announce handler
    announce_handler = AnnounceHandler(
        aspect_filter="link.edgemap"
    )
    RNS.Transport.register_announce_handler(announce_handler)
    
    # Thread to update UI 
    thread = threading.Thread(target=asyncio.run, args=(update_ui_loop(),))
    thread.daemon = True
    thread.start()
    
    # Thread to read fifo input for sending
    thread_fifo_read = threading.Thread(target=asyncio.run, args=(client_fifo_read(),))
    thread_fifo_read.daemon = True
    thread_fifo_read.start()
    
    # We run on announce handler -> threads now on
    while True:
        time.sleep(1)

#
# Open link to announced destination
#
async def create_link_to_destination(destination_hash_string):
    
    global server_link
    global g_initial_link_connect_delay
    global g_connection_in_progress    
    global destinations_we_have_link
    
    destination_hash = bytes.fromhex(destination_hash_string)    
    g_connection_in_progress = True;
        
    # Check if we know a path to the destination
    if not RNS.Transport.has_path(destination_hash):
        RNS.log(" Destination is not yet known. Requesting path and waiting for announce to arrive...")
        RNS.Transport.request_path(destination_hash)
        while not RNS.Transport.has_path(destination_hash):
            time.sleep(0.1)
            
    # Recall server identity
    server_identity = RNS.Identity.recall(destination_hash)
    
    # When the server identity is known, we set up a destination to server 
    server_destination = RNS.Destination(
        server_identity,
        RNS.Destination.OUT,
        RNS.Destination.SINGLE,
        APP_NAME,
        "edgemap"
    )
    
    # When a link instance is created, Reticulum will attempt to establish
    # verified and encrypted connectivity with the specified destination.
    link = RNS.Link(server_destination)
    link.set_packet_callback(client_packet_received)
    link.set_link_established_callback(link_to_server_established)
    link.set_link_closed_callback( link_closed )
    
    # We use global 'server_link' which is set on call back link_to_server_established()
    while not server_link:
        time.sleep(0.1)

    # 'Post connection message' - after thread is done
    pcm = "Thread terminated for a link: " + str(link)    
    # Run loop until exit
    client_loop( server_link )
    # Log terminated link
    RNS.log(pcm)
    tracked_announces.remove( destination_hash.hex() ) 
    # TODO CHECK THIS 
    destinations_we_have_link.remove( destination_hash.hex() )
    RNS.log("Removed tracked announce: " + str( destination_hash.hex() )) 


# Client loop
def client_loop(server_link):
    thread_id=str(threading.get_ident())
    should_quit = False
    global tracked_announces
    global tracked_links_on_client
    global g_fifo_file_in    
    # We moved fifo read to own thread: client_fifo_read()
    # I think we need this to keep thread alive
    while True:
        time.sleep(1)
    

# Client reads fifo and sends to all: tracked_links_on_client[]
def client_fifo_read():
    global g_fifo_file_in
    global tracked_announces
    global tracked_links_on_client
    global destinations_we_have_link
    # Create FIFO In ( "messages in" to be sent out on link )
    if not os.path.isfile(g_fifo_file_in):
        create_fifo_pipe(g_fifo_file_in)
    if not stat.S_ISFIFO(os.stat(g_fifo_file_in).st_mode):
        os.remove(g_fifo_file_in)
        create_fifo_pipe(g_fifo_file_in)
    
    fifo_read=open(g_fifo_file_in,'r')
    
    # Connect destination links when fifo hits 

    # Read fifo and send requests to link(s)
    while True:
        fifo_msg_in = fifo_read.readline()[:-1]
        
        if not fifo_msg_in == "":
            announce_entries=len(tracked_announces)
            for tracked_destination_hash in tracked_announces:
                # Test do we have a link already before doing threads               
                if tracked_destination_hash not in destinations_we_have_link:
                    thread = threading.Thread(target=asyncio.run, args=(create_link_to_destination(tracked_destination_hash),))
                    thread.daemon = True
                    thread.start()
                    # Delay between thread starting
                    time.sleep(5)
                else:
                    RNS.log(" Found existing link to: " + str(tracked_destination_hash) )

            # Send message to link entries
            loop_entry=1
            loop_entries=len(tracked_links_on_client)
            for server_link_entry in tracked_links_on_client:                
                RNS.log("[" + str(loop_entry) + "/" + str(loop_entries)+"] Making edgemap-message request to: " + str(server_link_entry))
                request_recipe = server_link_entry.request(
                    "/edgemap-message",
                    data = fifo_msg_in, 
                    response_callback = request_response_received,
                    failed_callback = request_failed,
                    progress_callback = request_progress_callback
                )
                # Sleep between requests
                time.sleep( 4 ) 
                loop_entry+=1
        
            time.sleep(0.1)    
        
        else:
            # No fifo data
            time.sleep(1)
            pass

#
# This function is called when a link (from Client to Server) has been established
#
def link_to_server_established(link):
    global tracked_links_on_client
    global g_connection_in_progress
    global destinations_we_have_link
    
    # We store a reference to the link instance for later use
    # create_link_to_destination() requires this global server_link to start
    # Q: Can we do this without global variable?
    global server_link 
    server_link = link
    
    # Identifies the initiator of the link to the remote peer
    link.identify(client_identity)
    
    # Append link to track links (TODO: this info to Web UI ?)
    tracked_links_on_client.append(link)
    # get destination hash
    destination_hash_of_link = link.destination.hash.hex()
    destinations_we_have_link.append(destination_hash_of_link)
 
    RNS.log("\033[1m[" + str( len(tracked_links_on_client) ) + "]\033[0m Link " + str(link) + " to " + str( destination_hash_of_link ) )
    #RNS.log("\033[1mTracking now " + str( len(tracked_links_on_client) ) + " link connections \033[0m")
    
    # Connection has been completed
    g_connection_in_progress = False    
    

# When a link is closed
def link_closed(link):
    global tracked_links_on_client
    global g_connection_in_progress
    global tracked_announces
    
    if link.teardown_reason == RNS.Link.TIMEOUT:
        RNS.log("\033[31m\033[1mThe link timed out:  \033[0m" + str(link) )
    elif link.teardown_reason == RNS.Link.DESTINATION_CLOSED:
        RNS.log("The link was closed by the server: " + str(link)  )
    else:
        RNS.log("Link closed: " + str(link)  )

    # List announces
    announce_entries=len(tracked_announces)
    RNS.log("We have now: " + str(announce_entries) + " announces for destinations")
    for announce_entry in tracked_announces:
        RNS.log(" => " + str( announce_entry ) )
    
    # Maybe we don't have that link on array
    try:
        destination_hash = link.destination.hash.hex()
        tracked_links_on_client.remove(link)
        
        if destination_hash in destinations_we_have_link:
            RNS.log("\033[31m[UNTRACK LINK]: \033[0m " + str(destination_hash) )
            destinations_we_have_link.remove(destination_hash)
        if destination_hash in tracked_announces:
            RNS.log("\033[31m[UNTRACK ANNOUNCE]: \033[0m " + str(destination_hash) )
            tracked_announces.remove(destination_hash)
        
    except Exception as e:
                
        RNS.log(" Failed to remove entry from tracked links: %s" % (str(e)), RNS.LOG_ERROR)
        
        # Remove announced destination from tracked_announces
        destination_hash = link.destination.hash.hex()
        RNS.log(" link_closed() destination hex: " + str( destination_hash ))
        
        # TODO does this work?
        if destination_hash in destinations_we_have_link:
            destinations_we_have_link.remove(destination_hash)
        
        if destination_hash in tracked_announces:
            RNS.log("\033[31m[UNTRACK] announce: \033[0m " + str(destination_hash) )
            tracked_announces.remove(destination_hash)
                            
            announce_entries = len(tracked_announces)
            RNS.log("We have now: " + str(announce_entries) + " announces for destinations")
            for announce_entry in tracked_announces:
                RNS.log(" => " + str(announce_entry) )

        if link.get_remote_identity() != None:
            RNS.log(" XXXXX Server identity: " + str( link.get_remote_identity() ) )
        
    RNS.log("\033[1mTracking now " + str( len(tracked_links_on_client) ) + " link connections \033[0m")
    g_connection_in_progress=False
    time.sleep(1.5)
    

# When a packet is received over the link, we
# simply print out the data.
def client_packet_received(message, packet):
    text = message.decode("utf-8")
    thread_id=str(threading.get_ident())
    # Remote identity
    if packet.link.get_remote_identity() != None:
        remote_peer = str(packet.link.get_remote_identity())
    
    RNS.log(" Client RX: " + text )
    RNS.log(" From: " + remote_peer )    
    RNS.log("---------------------------------------------------------------")
    sys.stdout.flush()

# request callbacks for messages
def request_response_received(request_receipt):
    request_id = request_receipt.request_id
    response = request_receipt.response
    RNS.log(" Response: " + str(response) + " in " + str( round(request_receipt.get_response_time(),2) ) + " s")
    response_string = str(response)
    write_reticulum_status_fifo( response_string )

# TODO: What to do when msg fails  ???
def request_failed(request_receipt):
    # RED: \033[31m \033[0m
    RNS.log("\033[31mMessage request "+RNS.prettyhexrep(request_receipt.request_id)+" failed.\033[0m")
    RNS.log(" Response time: " + str(request_receipt.get_response_time() ) )
    # TODO: How do we tear link down?

def request_received(request_receipt):
    RNS.log("The request "+RNS.prettyhexrep(request_receipt.request_id)+" was received by the remote peer.")

def request_progress_callback(request_receipt):
    pass
    # RNS.log("The request "+RNS.prettyhexrep(request_receipt.request_id)+" progress: " +  str(request_receipt.progress) )

#
# Connection request (unused at the moment)
#
def send_edgemap_connection_request(server_link_entry):
    RNS.log("Making connection-request to: " + str(server_link_entry))
    request_recipe = server_link_entry.request(
        "/edgemap-connection",
        data = g_node_callsign,
        response_callback = connection_response_received,
        failed_callback = connection_request_failed,
        progress_callback = connection_request_progress_callback
    )
# request callbacks for edgemap-connection 
def connection_response_received(request_receipt):
    request_id = request_receipt.request_id
    response = request_receipt.response
    RNS.log("Got response for connection-request "+RNS.prettyhexrep(request_id)+": "+str(response) )
    RNS.log(" Response time: " + str(request_receipt.get_response_time() ) )
    # response_string = str(response)
    # write_reticulum_status_fifo( response_string )

def connection_request_failed(request_receipt):
    RNS.log("The connection-request "+RNS.prettyhexrep(request_receipt.request_id)+" failed.")
    RNS.log(" Response time: " + str(request_receipt.get_response_time() ) )

def connection_request_received(request_receipt):
    RNS.log("The connection-request "+RNS.prettyhexrep(request_receipt.request_id)+" was received by the remote peer.")

def connection_request_progress_callback(request_receipt):
    pass
    # RNS.log("The request "+RNS.prettyhexrep(request_receipt.request_id)+" progress: " +  str(request_receipt.progress) )




##########################################################
#### Program Startup #####################################
##########################################################

if __name__ == "__main__":
    
    try:
        server_connected_clients_count = 0
        parser = argparse.ArgumentParser(description="Link example")
        parser.add_argument(
            "-s",
            "--server",
            action="store_true",
            help="wait for incoming link requests from clients"
        )
        
        parser.add_argument(
            "-c",
            "--client",
            action="store_true",
            help="wait from server announce and act as client"
        )

        parser.add_argument(
            "-l",
            "--linkstat",
            action="store_true",
            help="Show link statistic"
        )

        args = parser.parse_args()
        if args.linkstat:
           RNS.log("Enabled link statistic") 
           g_link_statistic = True
        if args.server:
            server()
        if args.client: 
            client()
        
    except KeyboardInterrupt:
        print("")
        exit()
