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
from datetime import datetime, timedelta
from threading import Thread
from random import randrange, uniform
# app_data
import base64
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, hmac
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

APP_NAME = "link"
server_identity = None
server_destination = None
server_connected_clients_count = None
tracked_destinations = []
tracked_links_on_server = []
tracked_links_on_client = []
destination_hashes_we_have_link = []

# A reference to the server link. Check is there race condition.
server_link = None
# A reference to the client identity
client_identity = None
g_link_statistic = False
g_initial_link_connect_delay = None
# database
db_file = "/opt/edgemap-persist/rns.db"

# Initialize the parser and read the file
config = configparser.ConfigParser()
config.read('rnslink.ini')
g_node_id = config['settings']['node_id']
g_node_callsign = config['settings']['callsign']
g_fifo_file_in = config['settings']['fifo_file_in']
g_fifo_file_out = config['settings']['fifo_file_out']
g_fifo_reticulum_control = config['settings']['fifo_file_reticulum_control']
# Announce rates & connect delay
g_initial_announce_delay = int(g_node_id) + (2 * int(g_node_id))
# Not in use in this version (where announces do not trigger connection)
g_initial_link_connect_delay = 4 * ( int(g_node_id) - 1 )
g_connection_in_progress=False

# Encrypt password placeholder
g_password = "strong_password"
g_encrypted = True

# Debug globals
g_enable_announcements = False
g_erase_db_at_server_start = False
g_startup_completed = False
g_user_message_is_being_sent = False

#
# Encrypt / decrypt functions
#
def generate_key(password: str, salt: bytes) -> bytes:
    """Derive a 32-byte key from the password using PBKDF2."""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    return kdf.derive(password.encode())

def encrypt_aes256(message: str, password: str) -> str:
    """Encrypts a message using AES-256 with HMAC for integrity, and returns a base64-encoded result."""
    
    # Generate random salt and IV
    salt = os.urandom(16)
    iv = os.urandom(16)
    
    # Derive AES key from password
    key = generate_key(password, salt)
    
    # Encrypt message
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(message.encode()) + encryptor.finalize()
    
    # Calculate HMAC for integrity check
    h = hmac.HMAC(key, hashes.SHA256(), backend=default_backend())
    h.update(ciphertext)
    hmac_value = h.finalize()
    
    # Combine salt, IV, HMAC, and ciphertext and encode as base64
    encrypted_data = salt + iv + hmac_value + ciphertext
    encoded_result = base64.b64encode(encrypted_data).decode('utf-8')
    return encoded_result

def decrypt_aes256(encoded_data: str, password: str) -> str:
    """Decrypts a base64-encoded, AES-256 encrypted message with HMAC integrity check."""
    
    # Decode the base64 data
    encrypted_data = base64.b64decode(encoded_data)
    
    # Extract salt, IV, HMAC, and ciphertext
    salt = encrypted_data[:16]
    iv = encrypted_data[16:32]
    hmac_value = encrypted_data[32:64]
    ciphertext = encrypted_data[64:]
    
    # Derive AES key from password
    key = generate_key(password, salt)
    
    # Verify HMAC for integrity
    h = hmac.HMAC(key, hashes.SHA256(), backend=default_backend())
    h.update(ciphertext)
    h.verify(hmac_value)  # Will raise an InvalidSignature exception if verification fails
    
    # Decrypt ciphertext
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    decrypted_message = decryptor.update(ciphertext) + decryptor.finalize()
    return decrypted_message.decode('utf-8')

# Read position from file to globals
# TODO: add Handle live GPS
def readManualPosition():
    
    if ( os.path.isfile("/opt/edgemap-persist/location.txt") ):
        
        # Callsign (TODO: which one to use?)            
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
                return t2_gps_array[0].rstrip(),t2_gps_array[1].rstrip()
    else:
        RNS.log("No location saved")
        return "-","-"
    

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
        cursor.execute("CREATE TABLE rnsnodes (id INTEGER PRIMARY KEY AUTOINCREMENT, callsign TEXT, destination TEXT, timestamp TEXT, identity TEXT,snr TEXT, rssi TEXT, quality TEXT )")
    else:
        RNS.log("[DB] found existing rnsnodes table")

# On update from announce we only need to update time
def reticulumDbUpdate(callsign,destination_hash,identity_hash):
    connection = sqlite3.connect(db_file)
    # print(connection.total_changes)
    cursor = connection.cursor()
    # Check if callsign exist
    cursor.execute("SELECT * FROM rnsnodes WHERE callsign = ?", (callsign,) )
    rows = len( cursor.fetchall() )
    if ( rows == 0 ):
        snr = "-"
        rssi = "-"
        quality = "-"
        cursor.execute("INSERT INTO rnsnodes (callsign,destination,timestamp,identity,snr,rssi,quality) VALUES (?,?,current_timestamp,?,?,?,?)", (callsign,destination_hash,identity_hash,snr,rssi,quality))
    else:
        cursor.execute("UPDATE rnsnodes SET callsign = ?, destination = ?, timestamp = current_timestamp, identity = ? WHERE callsign = ?", (callsign, destination_hash,identity_hash,callsign))
    
    affected_rows = cursor.rowcount
    connection.commit()
    cursor.close()
    connection.close()

def reticulumDbUpdateRadioLinkParams(destination_hash,snr,rssi,quality):    
    connection = sqlite3.connect(db_file)
    # print(connection.total_changes)
    cursor = connection.cursor()
    # Check if identity_hash exist
    cursor.execute("SELECT * FROM rnsnodes WHERE destination = ?", (destination_hash,) )
    rows = len( cursor.fetchall() )
    if ( rows == 0 ):
        cursor.execute("INSERT INTO rnsnodes (timestamp,destination,snr,rssi,quality) VALUES (current_timestamp,?,?,?,?)", (destination_hash,snr,rssi,quality))
    else:
        cursor.execute("UPDATE rnsnodes SET timestamp = current_timestamp, snr = ?, rssi = ?, quality = ? WHERE destination = ?", (snr,rssi,quality,destination_hash))
    connection.commit()
    cursor.close()
    connection.close()

def reticulumDbUpdateRadioLinkParamsWithIdentity(destination_identity,snr,rssi,quality):    
    connection = sqlite3.connect(db_file)
    # print(connection.total_changes)
    cursor = connection.cursor()
    # Check if identity_hash exist
    cursor.execute("SELECT * FROM rnsnodes WHERE identity = ?", (destination_identity,) )
    rows = len( cursor.fetchall() )
    if ( rows == 0 ):
        # should not happen
        RNS.log("reticulumDbUpdateRadioLinkParamsWithIdentity() - unknown identity")
    else:
        cursor.execute("UPDATE rnsnodes SET timestamp = current_timestamp, snr = ?, rssi = ?, quality = ? WHERE identity = ?", (snr,rssi,quality,destination_identity))
    connection.commit()
    cursor.close()
    connection.close()
    
def reticulumDbErase():    
    connection = sqlite3.connect(db_file)
    cursor = connection.cursor()
    cursor.execute("DELETE FROM rnsnodes")
    connection.commit()
    cursor.close()
    connection.close()


def reticulumDbNodes():
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    query = "SELECT destination FROM rnsnodes"
    
    try:
        cursor.execute(query)
        rows = cursor.fetchall()
        # Convert each row into a formatted plain text string
        plain_text_rows = []
        for row in rows:
            plain_text_row = " ".join(str(item) for item in row)
            plain_text_rows.append(plain_text_row)
    
    except sqlite3.Error as e:
        print("Error fetching data from table:", e)
        rows = []
    finally:
        conn.close()
    
    return plain_text_rows


#
# UI update 
#
#
# sqlite> SELECT *, (strftime('%s', 'now') - strftime('%s', timestamp)) / 60 AS elapsed_minutes,(strftime('%s', 'now') - strftime('%s', timestamp)) AS elapsed_seconds FROM rnsnodes;
# id  callsign  destination                       timestamp            identity                          snr  rssi  quality  elapsed_minutes  elapsed_seconds
# --  --------  --------------------------------  -------------------  --------------------------------  ---  ----  -------  ---------------  ---------------
# 28  edgemapz  5c09b917797306149cff844712eeb3fb  2024-11-03 05:54:47  a40f5a48c7e681cd0d8da86edd0dd4e3  -    -     -        6                412            
# 29  edgemapw  79fb0f022609584a9d68efa537b0c8b8  2024-11-03 05:55:57  0f6b1535fb933f79b36471725520c5e0  -    -     -        5                342            
# 30  edgemapy  fbd832b36033e50d2da2fae6d9f2fd34  2024-11-03 05:56:16  a11991c158d0f75fd6b22b04da49b37e  -    -     -        5                323            
# 31  edgemapx  4363b9b5a644688eb1e852125a383c89  2024-11-03 05:57:11  c62fb1e2ee44ad53a9a8dbb180d19b96  -    -     -        4                268            
# sqlite> 
#
def updateUserInterface():
    
    # FOR DEBUG DISABLED
    if True:
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
            peer_snr = row[5]
            peer_rssi = row[6]
            peer_q = row[7]
            peer_age_in_minutes = row[8]
            peer_age_in_seconds = row[9]
            # RNS.log(" ** peer_callsign " + str(peer_callsign ) )
            # RNS.log(" ** peer_hash " + str( peer_hash ) )
            # RNS.log(" ** peer_timestamp " + str(peer_timestamp) )
            # RNS.log(" ** peer_age_in_minutes: " + str(peer_age_in_minutes) )
            # RNS.log(" ** peer_age_in_seconds: " + str(peer_age_in_seconds) )
            # Inform UI about nodes we have
            # do we have link to destination?
            if peer_hash in destination_hashes_we_have_link:
                link_eshtablished = "Ⓛ"
            else:
                link_eshtablished = "-";
            
            if peer_snr is None:
                peer_snr = 0
            if peer_rssi is None:
                peer_rssi = 0
            if peer_q is None:
                peer_q = 0
            
            message_content = "reticulumnode," + peer_callsign + "," + str(peer_age_in_minutes) + "," + peer_hash + "," + link_eshtablished + "," + str(peer_snr) + "," + str(peer_rssi) + "," + str(peer_q) + "\n"
            write_reticulum_status_fifo(message_content)
            # Delay between entries to map UI
            time.sleep(0.5)
            
        connection.commit()
        connection.close()

def write_reticulum_status_fifo(payload):
    fifo_write = open('/tmp/reticulumstatusin', 'w')
    fifo_write.write(payload)
    fifo_write.flush()

# Send nodes to UI every 15 s 
async def update_ui_loop():
    while True:
        # RNS.log("** Updating UI...")
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
    global g_password
    global g_encrypted
    # Let's not announce immediately at start.
    while True:
        g_announce_delay = randrange(120, 240)
        RNS.log("Next periodic announcement in " + str(g_announce_delay) + " s." )
        await asyncio.sleep(g_announce_delay)
        
        # If encrypted, send also position in announcement
        if g_encrypted:
            lat,lon = readManualPosition()
            callsign_app_data_to_be_encrypted = "edgemap;" + g_node_callsign + ";" + str(lat) + "," + str(lon)
            callsign_app_data = encrypt_aes256(callsign_app_data_to_be_encrypted, g_password)
            pass
        else:
            callsign_app_data = "edgemap." + g_node_callsign
        
        callsign_app_data_encoded=callsign_app_data.encode('utf-8')
        server_destination.announce(app_data=callsign_app_data_encoded)


# Manual announce, triggered from web ui
def announce_manual(): 
    global server_destination
    global g_node_callsign
    if g_encrypted:
        lat,lon = readManualPosition()
        callsign_app_data_to_be_encrypted = "edgemap;" + g_node_callsign + ";" + str(lat) + "," + str(lon)
        callsign_app_data = encrypt_aes256(callsign_app_data_to_be_encrypted, g_password)
        pass
    else:
        callsign_app_data = "edgemap." + g_node_callsign
        
    # Send it
    callsign_app_data_encoded=callsign_app_data.encode('utf-8')
    server_destination.announce(app_data=callsign_app_data_encoded)
    RNS.log("Sent manual announce")

    
# edgemap-message request
def edgemap_message_request(path, data, request_id, link_id, remote_identity, requested_at):
    RNS.log("Message in from link: "+RNS.prettyhexrep(link_id))
    RNS.log("Edgemap message: "+RNS.prettyhexrep(request_id)+" on link: "+RNS.prettyhexrep(link_id))
    RNS.log(" Remote identity: "+str(remote_identity) ) 
    RNS.log(" Data received: " + str(data) )
    RNS.log(" Time stamp: " + str(requested_at) )
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
    if g_erase_db_at_server_start:
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
    
    # Start thread to announce periodically if -a is supplied
    if g_enable_announcements:        
        RNS.log("Starting periodic announcement thread.")
        thread = threading.Thread(target=asyncio.run, args=(announce_loop(),))
        thread.daemon = True
        thread.start()
    else:
        RNS.log("\033[0;36mPeriodic announcements disabled. Enable with -a option.\033[0m")
    
    # Everything's ready, run server_loop()
    server_loop(server_destination)

def server_loop(destination):  
    # Let the user know that everything is ready
    RNS.log( "This server destination: \033[0;34m " + RNS.prettyhexrep(destination.hash) + "\033[0m" )
    
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
        RNS.log("Connected CLIENT identity:  " + str(identity), RNS.LOG_VERBOSE  )
        RNS.log("RSSI:   " + str( link.get_rssi() ), RNS.LOG_VERBOSE  )
        RNS.log("SNR:    " + str( link.get_snr() ), RNS.LOG_VERBOSE  )
        RNS.log("Quality:" + str( link.get_q() ), RNS.LOG_VERBOSE  )
    return

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
#

#
# announce handler class for client
#
class AnnounceHandler:
    def __init__(self, aspect_filter=None):
        self.aspect_filter = aspect_filter
    def received_announce(self, destination_hash, announced_identity, app_data):
        # RNS.log("[RAW] Announce: " + RNS.prettyhexrep(destination_hash))
        global g_connection_in_progress
        global tracked_destinations
        global server_link
        global g_encrypted
        global g_password
                                
        if app_data is not None:
            announce_app_data_encrypted = app_data.decode('utf-8')
            # RNS.log("[RAW] Announce app_data: " + str(announce_app_data_decoded) )
            
            if g_encrypted:
                try:
                    announce_app_data_decoded = decrypt_aes256(announce_app_data_encrypted, g_password)
                    # RNS.log("** announce_app_data_decoded: " + str( announce_app_data_decoded) )
                except Exception as e:
                    print("Decryption failed:", e)
            else:
                pass
                
            # Plaintext app_data
            callsign_split_array = announce_app_data_decoded.split(';')
            
            if len(callsign_split_array) == 3:
                # If we have connection to another announce in progress, skip any incoming announce handling (obsolete)
                if g_connection_in_progress == False:
                    insert_callsign = callsign_split_array[1]
                    insert_position_string = callsign_split_array[2]
                    if callsign_split_array[0] == 'edgemap':
                        # RNS.log("Received edgemap announce: " + RNS.prettyhexrep(destination_hash) + " " + insert_callsign + " " + insert_position_string)
                        # Generate trackMarker message and write it to FIFO
                        insert_position_string_fields = insert_position_string.split(",")
                        # Check if we have stored location and if so, send trackMarker
                        if ( (insert_position_string_fields[1] != "-") and (insert_position_string_fields[0] != "-" ) ):
                            announce_generated_message = insert_callsign + "|trackMarker|" + insert_position_string_fields[1] + "," + insert_position_string_fields[0] + "|Manual position"
                            write_received_msg_to_fifo(announce_generated_message)
                        else:
                            RNS.log("No position provided in announce")
                        
                        insert_destination = RNS.prettyhexrep(destination_hash)[1:-1]
                        insert_destination_hex = RNS.hexrep(destination_hash)
                        insert_destination_hex = insert_destination_hex.replace(":", "")
                        insert_destination_hex = str(insert_destination_hex)
                        announced_identity_hex = str(announced_identity)
                        announced_identity_hex = announced_identity_hex[1:-1]
                        # Update DB
                        reticulumDbUpdate( insert_callsign,insert_destination_hex,announced_identity_hex)
                        # Inform UI: announcereceived,[callsign],[hash]
                        message_content = "announcereceived," + insert_callsign + "," + insert_destination_hex + "\n"   
                        fifo_write = open('/tmp/reticulumstatusin', 'w')
                        fifo_write.write(message_content)
                        fifo_write.flush()
                        # Track announces as client
                        server_link = ""
                        if destination_hash.hex() not in tracked_destinations:                            
                            tracked_destinations.append(destination_hash.hex())
                            announce_entries=len(tracked_destinations)                            
                            RNS.log("\033[1m [" + str(announce_entries) + "]\033[0m [NEW] Announce: " + RNS.prettyhexrep(destination_hash) + " " + insert_callsign + " Identity:" +  str(announced_identity))
                        else:
                            # We've seen this announce already
                            pass
                else:
                    RNS.log("[SKIP] Connection in progress, skipping announce handling.")
            else:
                # Should not happen
                RNS.log("Received non-edgemap announce: " + RNS.prettyhexrep(destination_hash) + " " + callsign_split_string )
            
    
def log_connection_statistics():
    global tracked_links_on_client
    global tracked_destinations
    edegmap_destinations = reticulumDbNodes()
    tracked_destinations_count=len(tracked_destinations)
    tracked_links_count=len(tracked_links_on_client)
    RNS.log("Stored: \033[1m[" + str(len(edegmap_destinations)) + "]\033[0m Announced: \033[1m[" +  str(tracked_destinations_count) + "]\033[0m Links: \033[1m["+ str(tracked_links_count) +"]\033[0m" )


def get_activation_times(time_window, node_count):
    # Get the current time
    current_time = datetime.now()
    # Calculate the interval between each node's activation time
    interval = time_window / node_count
    # Generate a list of activation times
    activation_times = []
    for i in range(node_count):
        # Calculate the activation time for each node
        activation_time = current_time + timedelta(seconds=i * interval)
        # Format the time as hh:mm:ss and add it to the list
        activation_times.append(activation_time.strftime('%H:%M:%S'))
    return activation_times

def wait_until_single_activation(activation_time_str):
    # Get the current date and convert activation time string to datetime object for today
    now = datetime.now()
    activation_time = datetime.strptime(activation_time_str, '%H:%M:%S').replace(
        year=now.year, month=now.month, day=now.day
    )
    
    # Check if the activation time has already passed today
    if activation_time < now:
        activation_message = f"{activation_time_str} has already passed."
        RNS.log(str(activation_message))
        return
        
    time_remaining = (activation_time - datetime.now()).total_seconds()
    activation_message = f"Waiting {int(time_remaining)} seconds until {activation_time_str}..."
    RNS.log(str(activation_message))
    
    # Wait until the activation time is reached
    while datetime.now() < activation_time:
        time_remaining = (activation_time - datetime.now()).total_seconds()
        time.sleep(min(time_remaining, 1))  # Sleep in small increments to check the time frequently
    
    # Activation time reached
    activation_message = f"Activated at {datetime.now().strftime('%H:%M:%S')} for scheduled time {activation_time_str}"
    RNS.log(str(activation_message))



#
# Run as 'client'
#
def client():
    global client_identity
    global server_link
    global g_initial_link_connect_delay
    global tracked_links_on_client
    global tracked_destinations
    global g_startup_completed
    
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

    
    # Setup announce handler
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
    
    # client_send_periodic_trackMarker thread
    thread_trackmarker = threading.Thread(target=asyncio.run, args=(client_send_periodic_trackMarker(),))
    thread_trackmarker.daemon = True
    thread_trackmarker.start()

    #
    # Time window for initial start
    #
    if True:
        # Parameter how many nodes and what is activation lenght
        node_count = 4
        activation_length = 20
        time_window = node_count * activation_length
        RNS.log("We have " + str(node_count) + " nodes. Time window is " + str(time_window) + " seconds" )
        activation_times = get_activation_times(time_window, node_count)
        # Wait based on node_id 
        wait_until_single_activation( activation_times[int(g_node_id)-1] )
        g_startup_completed = True

    #
    # New era. This will setup links to stored edgemap announces at the start.
    #
    while True:
        # Read stored edgemap destinations from DB
        edegmap_destinations = reticulumDbNodes()
        # Show stats
        log_connection_statistics()
        # Try to setup links
        for dest_item in edegmap_destinations:
            
            if dest_item not in destination_hashes_we_have_link: 
                destination_hash = bytes.fromhex(dest_item)   
                g_connection_in_progress = True;           
                path_found = False
                # Check if we know a path to the destination
                if not RNS.Transport.has_path(destination_hash):
                    RNS.Transport.request_path(destination_hash)
                    # Timeout for path resolve, how long can this take?
                    timeout = 0
                    while timeout < 5:
                        if RNS.Transport.has_path(destination_hash):
                            path_found = True
                            break
                        time.sleep(1)
                        timeout += 1
                else:
                    path_found = True

                if path_found:
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
                    g_connection_in_progress = True
                    link = RNS.Link(server_destination)
                    link.track_phy_stats(True)
                    link.set_packet_callback(client_packet_received)
                    link.set_link_established_callback(link_to_server_established)
                    link.set_link_closed_callback( link_closed )
                    # Is delay really the only way ?
                    time.sleep(2)
                else:
                    RNS.log("\033[31mNo path\033[0m - skipping link establish to: " + RNS.prettyhexrep(destination_hash) )
                    
            else:
                pass
                # RNS.log("\033[32mExisting link\033[0m to: " + str(dest_item) )
        
        time.sleep(randrange(30, 60))

    RNS.log("*** END **** ")


# 
# Sending trackMarker peridiocally to all peers as message
# 
async def client_send_periodic_trackMarker():
    global g_startup_completed
    global g_user_message_is_being_sent
    
    while not g_startup_completed:
        delay_time = randrange(60, 120)
        RNS.log("Waiting " + str(delay_time) + " s before releasing periodic trackMarkers")
        await asyncio.sleep(delay_time)
        
    while True:
        # Send only periodic message if user is not sending message
        if not g_user_message_is_being_sent:            
            lat,lon = readManualPosition()
            message = g_node_callsign + "|trackMarker|" + lon + "," + lat + "|Manual position"
            client_send_message(message)
            RNS.log("trackMarker message sent")
        else:
            RNS.log("Skipped trackMarker message because user message.")
        
        await asyncio.sleep(randrange(120, 240))

#
# Client Send message
# If we don't have links yet, establish them before send
#
def client_send_message(message):
    global tracked_destinations
    global tracked_links_on_client
    global destination_hashes_we_have_link
    
    if not message == "":
        for tracked_destination_hash in tracked_destinations:
            if tracked_destination_hash not in destination_hashes_we_have_link: 
                # Inline link setup to destinations
                destination_hash = bytes.fromhex(tracked_destination_hash)    
                g_connection_in_progress = True;                     
                # Check if we know a path to the destination
                path_found = False
                if not RNS.Transport.has_path(destination_hash):
                    RNS.log(" Destination is not yet known. Requesting path and waiting for announce to arrive...")
                    RNS.Transport.request_path(destination_hash)

                    # Timeout for path resolve
                    timeout = 0
                    while timeout < 5:
                        if RNS.Transport.has_path(destination_hash):
                            path_found = True
                            break
                        time.sleep(1)
                        timeout += 1
                        
                if path_found:
                    server_identity = RNS.Identity.recall(destination_hash)
                    server_destination = RNS.Destination(
                        server_identity,
                        RNS.Destination.OUT,
                        RNS.Destination.SINGLE,
                        APP_NAME,
                        "edgemap"
                    )
                    # When a link instance is created, Reticulum will attempt to establish
                    # verified and encrypted connectivity with the specified destination.
                    g_connection_in_progress = True
                    link = RNS.Link(server_destination)
                    link.track_phy_stats(True)
                    link.set_packet_callback(client_packet_received)
                    link.set_link_established_callback(link_to_server_established)
                    link.set_link_closed_callback( link_closed )
                    # Is delay really the only way ?
                    time.sleep(2)
                else:
                    RNS.log("\033[31mNo path\033[0m - skipping link establish")
                    
            else:
                RNS.log(" Found existing link to: " + str(tracked_destination_hash) )
        
        
        RNS.log("Sending message to all peers in 1 s")
        time.sleep(1)

        # Send messages
        # Q: Do we just send to all ?
        loop_entry=1
        loop_entries=len(tracked_links_on_client)
        for server_link_entry in tracked_links_on_client:                
            RNS.log("\033[1m[" + str(loop_entry) + "/" + str(loop_entries)+"]\033[0m Making edgemap-message request to: " + str(server_link_entry))
            # Make request and set callbacks
            request_recipe = server_link_entry.request(
                "/edgemap-message",
                data = message, 
                response_callback = client_request_response_received,
                failed_callback = client_request_failed,
                progress_callback = client_request_progress_callback
            )
            RNS.log(" Message "+RNS.prettyhexrep(request_recipe.request_id) + " requested", RNS.LOG_VERBOSE )
            
            # Update physical link values on every msg send
            rssi = server_link_entry.get_rssi()
            snr = server_link_entry.get_snr()
            quality = server_link_entry.get_q()
            remote_identity = str(server_link_entry.get_remote_identity())
            remote_identity = remote_identity[1:-1]
            reticulumDbUpdateRadioLinkParamsWithIdentity(remote_identity,snr,rssi,quality)
            
            # Is delay really the only way?
            # Adjust this delay based on your transport testing
            time.sleep(4) 
            loop_entry+=1

#
# Client:   read fifo and send to all: tracked_links_on_client[]
#           If there is no link to destination, create link before
#           sending. 
#
async def client_fifo_read():
    global g_fifo_file_in
    global tracked_destinations
    global tracked_links_on_client
    global destination_hashes_we_have_link
    global g_user_message_is_being_sent
    
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
            
            g_user_message_is_being_sent = True
            
            for tracked_destination_hash in tracked_destinations:
                
                # Test do we have a link already
                if tracked_destination_hash not in destination_hashes_we_have_link: 
                    
                    # Inline link setup to destinations
                    destination_hash = bytes.fromhex(tracked_destination_hash)    
                    g_connection_in_progress = True;                     
                    # Check if we know a path to the destination
                    if not RNS.Transport.has_path(destination_hash):
                        RNS.log(" Destination is not yet known. Requesting path and waiting for announce to arrive...")
                        RNS.Transport.request_path(destination_hash)
                        # TODO: Do timeout here
                        while not RNS.Transport.has_path(destination_hash):
                            time.sleep(0.1)
                    
                    # Recall identity
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
                    g_connection_in_progress = True
                    link = RNS.Link(server_destination)
                    link.track_phy_stats(True) # aku
                    link.set_packet_callback(client_packet_received)
                    link.set_link_established_callback(link_to_server_established)
                    link.set_link_closed_callback( link_closed )

                    # Is delay really the only way ?
                    await asyncio.sleep(2)
                
                else:
                    RNS.log(" Found existing link to: " + str(tracked_destination_hash), RNS.LOG_VERBOSE )

            RNS.log("Sending message to all peers in 1 s")
            await asyncio.sleep(1)

            if True:
                # Send message to link entries. 
                # What if request takes ..long.. time ?
                loop_entry=1
                loop_entries=len(tracked_links_on_client)
                for server_link_entry in tracked_links_on_client:                
                    RNS.log("\033[1m[" + str(loop_entry) + "/" + str(loop_entries)+"]\033[0m Making edgemap-message request to: " + str(server_link_entry))
                    # Make request and set callbacks
                    request_recipe = server_link_entry.request(
                        "/edgemap-message",
                        data = fifo_msg_in, 
                        response_callback = client_request_response_received,
                        failed_callback = client_request_failed,
                        progress_callback = client_request_progress_callback
                    )
                    RNS.log(" Message "+RNS.prettyhexrep(request_recipe.request_id) + " requested", RNS.LOG_VERBOSE )
                    
                    # Update physical link values on every msg send
                    rssi = server_link_entry.get_rssi()
                    snr = server_link_entry.get_snr()
                    quality = server_link_entry.get_q()
                    remote_identity = str(server_link_entry.get_remote_identity())
                    remote_identity = remote_identity[1:-1]
                    reticulumDbUpdateRadioLinkParamsWithIdentity(remote_identity,snr,rssi,quality)
                    
                    # Is delay really the only way?
                    # Adjust this delay based on your transport testing
                    await asyncio.sleep(4) 
                    loop_entry+=1
                #
                g_user_message_is_being_sent = False
        else:
            # No fifo data
            await asyncio.sleep(1)
            pass
        


#
# This function is called when a link (from Client to Server) has been established
# 
def link_to_server_established(link):
    global tracked_links_on_client
    global g_connection_in_progress
    global destination_hashes_we_have_link
        
    # Identifies the initiator of the link to the remote peer
    link.identify(client_identity)
    # Append link to track links (TODO: this info to Web UI ?)
    tracked_links_on_client.append(link)
    # get destination hash and log it
    destination_hash_of_link = link.destination.hash.hex()
    destination_hashes_we_have_link.append(destination_hash_of_link) 
    RNS.log("\033[1m[" + str( len(tracked_links_on_client) ) + "]\033[0m [NEW] Link " + str(link) + " to " + str( destination_hash_of_link ) )
    # Store physical link values
    rssi = link.get_rssi()
    snr = link.get_snr()
    quality = link.get_q()
    reticulumDbUpdateRadioLinkParams(destination_hash_of_link,snr,rssi,quality)
    # Connection has been completed
    g_connection_in_progress = False    
    

#
# When a link is closed
#
def link_closed(link):
    global tracked_links_on_client
    global g_connection_in_progress
    global tracked_destinations
    
    if link.teardown_reason == RNS.Link.TIMEOUT:
        RNS.log("\033[31m\033[1mThe link timed out:  \033[0m" + str(link), RNS.LOG_ERROR )
    elif link.teardown_reason == RNS.Link.DESTINATION_CLOSED:
        RNS.log("The link was closed by the server: " + str(link)  )
    else:
        RNS.log("Link closed: " + str(link)  )

    # List destinations
    # announce_entries=len(tracked_destinations)
    # RNS.log("link_closed() We have now: " + str(announce_entries) + " destinations")
    
    #for announce_entry in tracked_destinations:
    #    RNS.log(" Destination: " + str( announce_entry ) )
    
    # List link
    # link_entries=len(tracked_links_on_client)
    # RNS.log("link_closed() We have now: " + str(link_entries) + " links")
    #for link_entry in tracked_links_on_client:
    #    RNS.log(" Link: " + str( link_entry ) )
    
    # Maybe we don't have that link on array
    try:
        destination_hash = link.destination.hash.hex()
        
        # link is gone at this point, it won't be found in tracked_links_on_client
        # I think we need to get link as hex ? 
        if link in tracked_links_on_client:
            RNS.log("\033[31m[UNTRACK LINK]: \033[0m " + str(link) )
            tracked_links_on_client.remove(link) #???
        
        if destination_hash in destination_hashes_we_have_link: 
            RNS.log("\033[31m[UNTRACK DESTINATION (STR)]: \033[0m " + str(destination_hash) )
            destination_hashes_we_have_link.remove(destination_hash)
        
        if destination_hash in tracked_destinations:
            RNS.log("\033[31m[UNTRACK DESTINATION (LINK)]: \033[0m " + str(destination_hash) )
            tracked_destinations.remove(destination_hash)
        
    except Exception as e:
        
        # NOTE: This segment is totally untested part - should be reviewed!
        
        RNS.log(" Failed to remove entry from tracked links: %s" % (str(e)), RNS.LOG_ERROR)
        
        # Remove announced destination from tracked_destinations
        destination_hash = link.destination.hash.hex()
        RNS.log(" link_closed() destination hex: " + str( destination_hash ))
        
        # TODO does this work?
        if destination_hash in destination_hashes_we_have_link:
            destination_hashes_we_have_link.remove(destination_hash)
        
        if destination_hash in tracked_destinations:
            RNS.log("\033[31m[UNTRACK] announce: \033[0m " + str(destination_hash) )
            tracked_destinations.remove(destination_hash)
                            
            announce_entries = len(tracked_destinations)
            RNS.log("link_closed() We have now: " + str(announce_entries) + " announces for destinations")
            for announce_entry in tracked_destinations:
                RNS.log(" => " + str(announce_entry) )

        if link.get_remote_identity() != None:
            RNS.log(" XXXXX Server identity: " + str( link.get_remote_identity() ), RNS.LOG_ERROR )
        
    # RNS.log("\033[1mTracking now " + str( len(tracked_links_on_client) ) + " link connections \033[0m")
    g_connection_in_progress=False
    log_connection_statistics()
    time.sleep(randrange(5, 15))
    

# When a packet is received over the link (from server), we
# simply print out the data. This is unused at the moment.
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
def client_request_response_received(request_receipt):
    request_id = request_receipt.request_id
    response = request_receipt.response
    RNS.log(" Message " + RNS.prettyhexrep(request_receipt.request_id) + " succeed (" + str( round(request_receipt.get_response_time(),2) ) + " s)" )
    RNS.log(" Response: " + str(response))
    response_string = str(response)
    write_reticulum_status_fifo( response_string )

# TODO: What to do when msg fails, inform UI ?
def client_request_failed(request_receipt):
    RNS.log(" \033[31mMessage " + RNS.prettyhexrep(request_receipt.request_id) + " failed\033[0m", RNS.LOG_ERROR)    
    # I think we don't need to disconnect link, we may try again

# what is this?
def client_request_received(request_receipt):
    RNS.log("The request "+RNS.prettyhexrep(request_receipt.request_id)+" was received by the remote peer.")

def client_request_progress_callback(request_receipt):
    pass
    #RNS.log("The request "+RNS.prettyhexrep(request_receipt.request_id)+" progress: " +  str(request_receipt.progress) )

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
        parser.add_argument(
            "-e",
            "--erasedb",
            action="store_true",
            help="Erase stored edgemap announcement at server start from rns.db"
        )
        parser.add_argument(
            "-a",
            "--announce",
            action="store_true",
            help="Enable automatic announcements"
        )

        args = parser.parse_args()
        if args.linkstat:
           RNS.log("Enabled link statistic") 
           g_link_statistic = True
        if args.erasedb:
            RNS.log("Erasing rns.db")
            g_erase_db_at_server_start = True
        if args.announce:
            RNS.log("Enabling automatic announcements")
            g_enable_announcements = True
        if args.server:
            server()
        if args.client: 
            client()
        
    except KeyboardInterrupt:
        print("")
        exit()
