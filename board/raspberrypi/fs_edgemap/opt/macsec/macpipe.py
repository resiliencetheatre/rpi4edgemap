# ----------------------------------------------------------------------
# macpipe
# 
# Copyright (C) 2024  Resilience Theatre
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
# ----------------------------------------------------------------------
# 
# Small python exercise: macsec keying via ethernet frames
#
# Adjust macpipe.ini and then run:
#
# sudo python3 macpipe.py -s
# sudo python3 macpipe.py -r 
# 
# Uses some strange US based algorithm, check can you trust this math.
# 
# Requirements:
#
#  sudo apt install python3-scapy python3-cryptography
#
# Unused features:
# 
# * Reads fifo to encrypt/decrypt payload and writes result to fifo
#
# Remember you need to read fifo output (unused feature):
#
#  cat /tmp/encrypted_message
#  cat /tmp/decrypted_message
#
#  BOLD: \033[1m \033[0m
#  RED: \033[31m \033[0m
#
import os
import sys
import time
import argparse
import random
import stat, os
import configparser
import logging
from datetime import datetime, timedelta
from random import randrange, uniform
import base64
import uuid
import subprocess
import re
from scapy.all import Ether, sendp, sniff

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, hmac
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

# Read ini file
config = configparser.ConfigParser()
config.read('macpipe.ini')
g_fifo_decrypt_in = config['settings']['decrypt_fifo_in']
g_fifo_decrypt_out = config['settings']['decrypt_fifo_out']
g_fifo_encrypt_in = config['settings']['encrypt_fifo_in']
g_fifo_encrypt_out = config['settings']['encrypt_fifo_out']
g_my_macsec_address = config['settings']['my_address']
g_my_macsec_interface = config['settings']['my_interface']
g_password = config['settings']['shared_secret']
g_my_mac_address = ""
g_my_macsec_key = ""

# Ethernet Broadcast MAC address
g_destination_mac = "ff:ff:ff:ff:ff:ff"

# List to store mac address and encryption key pairs
mac_key_store = []

# System functions
def check_root_privileges():
    if os.geteuid() != 0:
        print("This script must be run as root!")
        sys.exit(1)
    else:
        pass
    
def run_sudo_command(command: str) -> str:
    """
    Runs a shell command with sudo privileges.

    Parameters:
        command (str): The shell command to be executed.

    Returns:
        str: The output of the command.

    Raises:
        subprocess.CalledProcessError: If the command execution fails.
    """
    try:
        # Use 'sudo' to run the command with elevated privileges
        result = subprocess.run(
            f"sudo {command}",
            shell=True,
            text=True,
            capture_output=True,
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        # Handle command errors
        raise RuntimeError(f"Command failed with exit code {e.returncode}: {e.stderr.strip()}") from e

def shell_command(command: str) -> str:
    try:
        output = run_sudo_command(command)
        # print("Command succeeded. Output:")
        # print(output)
    except RuntimeError as e:
        # print("Command failed. Error:")
        # print(e)
        pass
    
    
#
# Ethernet packets
#
def send_ethernet_frame(destination_mac, source_mac, payload, iface):
    """
    Sends an Ethernet frame.
    
    Args:
        destination_mac: Destination MAC address (e.g., 'ff:ff:ff:ff:ff:ff' for broadcast)
        source_mac: Source MAC address
        payload: The payload data as bytes
        iface: Network interface to send on (e.g., 'eth0')
    """
    frame = Ether(dst=destination_mac, src=source_mac) / payload    
    # print(f"Sending frame: {frame.summary()}")
    sendp(frame, iface=iface,verbose=False)
    


def receive_ethernet_frames(iface, filter_function=None, timeout=10):
    """
    Receives Ethernet frames.
    
    Args:
        iface: Network interface to listen on (e.g., 'eth0')
        filter_function: Optional filter function that takes a packet and returns True/False
        timeout: Time in seconds to listen for frames
    
    Returns:
        List of received packets.
    """
    global g_my_macsec_interface
    global mac_key_store
    
    def process_packet(packet):
        # Print the summary of the packet
        # print(f"Packet Summary: {packet.summary()}")

        # Print the raw payload content
        if packet.payload:
            # print(f"Payload (raw bytes): {bytes(packet.payload)}")
            try:
                decoded_payload = bytes(packet.payload).decode('utf-8', errors='ignore')
                decrypted_payload = decrypt_aes256(decoded_payload, g_password)
                if decrypted_payload is not None:
                    split_payload = decrypted_payload.split(",")
                    g_my_mac_address = get_mac_address(g_my_macsec_interface)
                    received_mac = split_payload[1]
                    received_key = split_payload[2]
                    
                    # Check that received mac address is not my own
                    if received_mac != g_my_mac_address:
                        if update_encryption_key( received_mac, received_key ) :
                            execute_remote_macsec()
                    else:
                        pass
                        
            except Exception as e:
                print(f"Error decoding payload: {e}")

    # ether proto 0x0800 for IPv4 packets
    # ether proto 0x0806 for ARP packets
    # ether broadcast for broadcast packets
    # packets = sniff(iface=iface, filter="ether broadcast", prn=filter_function, timeout=timeout)
    packets = sniff(iface=iface, filter="ether broadcast", prn=process_packet, timeout=timeout)
    return packets


def update_encryption_key(mac_address, encryption_key):
    """
    Updates the encryption key for the given MAC address.
    If mac is new, adds mac and key => returns 1
    If the MAC address exists and key differes => updates its key and returns 1
    If the MAC address exists and key is same => returns 0

    Args:
        mac_address (str): The MAC address.
        encryption_key (str): The encryption key.
    
    Returns:
        0 if changes were not made
        1 if there is changes
    """
    global mac_key_store
    for item in mac_key_store:
        if item[0] == mac_address and item[1] != encryption_key:
            # mac address is found, but encryption key has changed
            print(f"New key for: {mac_address}")
            item[1] = encryption_key  
            return 1
        if item[0] == mac_address:
            return 0
    
    # If MAC address not found, add a new entry
    print(f"New mac and key: {mac_address}")
    mac_key_store.append([mac_address, encryption_key])
    return 1
    
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
    
    try:
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
    except:
        pass
        # print("Decrypt error.")

# FIFO functions
def create_fifo_pipe(pipe_path):
    try:
        os.mkfifo(pipe_path)
        print(f"FIFO created {pipe_path}" )
        
    except OSError as e:
        pass
        # print(f"Error: {e}")

def write_encrypted_message_to_fifo(message):
    global g_fifo_encrypt_out
    fifo_write = open(g_fifo_encrypt_out, 'w')
    fifo_write.write(message + "\n") # NOTE: \n
    fifo_write.flush()
    fifo_write.close()

def write_decrypted_message_to_fifo(message):
    global g_fifo_decrypt_out
    fifo_write = open(g_fifo_decrypt_out, 'w')
    fifo_write.write(message + "\n") # NOTE: \n
    fifo_write.flush()
    fifo_write.close()

def read_fifo_for_encryption():
    global g_fifo_encrypt_in
    
    if not os.path.isfile(g_fifo_encrypt_in):
        create_fifo_pipe(g_fifo_encrypt_in)
    if not stat.S_ISFIFO(os.stat(g_fifo_encrypt_in).st_mode):
        os.remove(g_fifo_encrypt_in)
        create_fifo_pipe(g_fifo_encrypt_in)
    
    if not os.path.isfile(g_fifo_encrypt_out):
        create_fifo_pipe(g_fifo_encrypt_out)
    if not stat.S_ISFIFO(os.stat(g_fifo_encrypt_out).st_mode):
        os.remove(g_fifo_encrypt_out)
        create_fifo_pipe(g_fifo_encrypt_out)
    
    fifo_read=open(g_fifo_encrypt_in,'r')
    
    while True:
        fifo_msg_in = fifo_read.readline()[:-1]

        if not fifo_msg_in == "":
            encrypted_payload = encrypt_aes256(fifo_msg_in, g_password)
            write_encrypted_message_to_fifo(encrypted_payload)
        else:
            time.sleep(1)


def read_fifo_for_decryption():
    global g_fifo_decrypt_in
    if not os.path.isfile(g_fifo_decrypt_in):
        create_fifo_pipe(g_fifo_decrypt_in)
    if not stat.S_ISFIFO(os.stat(g_fifo_decrypt_in).st_mode):
        os.remove(g_fifo_decrypt_in)
        create_fifo_pipe(g_fifo_decrypt_in)
        
    if not os.path.isfile(g_fifo_decrypt_out):
        create_fifo_pipe(g_fifo_decrypt_out)
    if not stat.S_ISFIFO(os.stat(g_fifo_decrypt_out).st_mode):
        os.remove(g_fifo_decrypt_out)
        create_fifo_pipe(g_fifo_decrypt_out)
        
    fifo_read=open(g_fifo_decrypt_in,'r')

    while True:
        fifo_msg_in = fifo_read.readline()[:-1]
        if not fifo_msg_in == "":
            # print(f'Input: {fifo_msg_in}')
            decrypted_payload = decrypt_aes256(fifo_msg_in, g_password)
            write_decrypted_message_to_fifo(decrypted_payload)
        else:
            time.sleep(1)

def get_mac_address(interface_name):
    """
    Gets the MAC address of a given network interface.
    
    Args:
        interface_name (str): The name of the network interface (e.g., 'eth0', 'wlan0').
    
    Returns:
        str: MAC address if found, otherwise None.
    """
    try:
        # Check if the system supports 'ip' or 'ifconfig' commands
        if os.name != 'nt':
            # Use the `ip` or `ifconfig` command to fetch details
            result = os.popen(f'ip link show {interface_name}').read()
            if not result:
                # Fallback to ifconfig if ip is unavailable
                result = os.popen(f'ifconfig {interface_name}').read()
            
            # Extract MAC address from the result using a regex
            mac_match = re.search(r"([0-9a-fA-F]{2}(:|-)){5}[0-9a-fA-F]{2}", result)
            if mac_match:
                return mac_match.group(0)
        else:
            print("This script is designed for Linux or MacOS systems.")
    except Exception as e:
        print(f"An error occurred: {e}")
    return None
 
def generate_encryption_key(bit_length=128):
    """
    Generates a random encryption key in hexadecimal format.

    Args:
        bit_length (int): The desired length of the key in bits (e.g., 128, 256).

    Returns:
        str: A random hexadecimal key of the specified bit length.
    """
    if bit_length % 8 != 0:
        raise ValueError("Bit length must be a multiple of 8.")
    
    # Calculate the number of bytes needed
    byte_length = bit_length // 8
    
    # Generate random bytes and convert to hexadecimal
    random_bytes = os.urandom(byte_length)
    hex_key = random_bytes.hex()
    
    return hex_key

#
# Run as encrypt
#
def encrypt():
    read_fifo_for_encryption()
    sys.exit()
        
#
# Run as decrypt
#
def decrypt():
    read_fifo_for_decryption()
    sys.exit()

#
# Ethernet frame functions
#
def frame_receiver():
    def display_packet(packet):
        pass
        # print(f"Received frame: {packet.summary()}")
            
    received_frames = receive_ethernet_frames(g_my_macsec_interface, display_packet)
    # print(f"Received {len(received_frames)} frames.")

#
# Send my mac and key every 10 s
#
def frame_sender():
    global g_my_macsec_key
    
    while True:
        g_my_mac_address = get_mac_address(g_my_macsec_interface)
        node_payload = g_my_macsec_address+","+g_my_mac_address+","+g_my_macsec_key
        encrypted_payload = encrypt_aes256(node_payload, g_password)
        send_ethernet_frame(g_destination_mac, g_my_mac_address, encrypted_payload, g_my_macsec_interface)
        time.sleep(10)

# Unused
def write_shell_script(file_name):
    """
    Write shell script for macsec activation.

    Args:
        file_name (str): The name of the file to write to..
    """    
    global g_my_macsec_key
    
    try:
        with open(file_name, 'w') as file:
            file.write(f"ip link set {g_my_macsec_interface} up \n")
            file.write("ip link delete macsec0 \n")
            file.write(f"ip link add link {g_my_macsec_interface} macsec0 type macsec encrypt on \n")
            file.write(f"ip macsec add macsec0 tx sa 0 pn 1 on key 01 {g_my_macsec_key} \n")
            # Create peers
            for mac, key in get_all_items():
                file.write(f"ip macsec add macsec0 rx port 1 address {mac} \n")
                file.write(f"ip macsec add macsec0 rx port 1 address {mac} sa 0 pn 1 on key 00 {key} \n")
            # Interface up and set address
            file.write(f"ip link set macsec0 up \n")
            file.write(f"ip addr add {g_my_macsec_address} dev macsec0 \n")

        print(f"File '{file_name}' written successfully!")
    except Exception as e:
        print(f"An error occurred: {e}")


def init_my_macsec():
    global g_my_macsec_key
    g_my_macsec_key = generate_encryption_key(128)    
    print("Initializing macsec interface. Remember to restart receiver as well (-r).")
    shell_command(f"ip link set {g_my_macsec_interface} up ")
    shell_command("ip link delete macsec0 ")
    shell_command(f"ip link add link {g_my_macsec_interface} macsec0 type macsec encrypt on ")
    shell_command(f"ip macsec add macsec0 tx sa 0 pn 1 on key 01 {g_my_macsec_key} ")
    shell_command(f"ip link set macsec0 up ")
    shell_command(f"ip addr add {g_my_macsec_address} dev macsec0 ")
    

def execute_remote_macsec():
    global g_my_macsec_key
    for mac, key in get_all_items():
        shell_command(f"ip macsec del macsec0 rx port 1 address {mac} ")
        shell_command(f"ip macsec add macsec0 rx port 1 address {mac} ")
        shell_command(f"ip macsec add macsec0 rx port 1 address {mac} sa 0 pn 1 on key 00 {key} ")

def get_all_items():
    """
    Returns all stored MAC address and encryption key pairs.

    Returns:
        list: List of [MAC address, encryption key] pairs.
    """
    return mac_key_store



#
# Start up
#
if __name__ == "__main__":
    
    check_root_privileges()
    
    try:
        parser = argparse.ArgumentParser(description="macpipe example")
        parser.add_argument(
            "-e",
            "--encrypt",
            action="store_true",
            help="read fifo data for encryption (not in use)"
        )
        
        parser.add_argument(
            "-d",
            "--decrypt",
            action="store_true",
            help="read fifo data for decryption (not in use)"
        )
        
        parser.add_argument(
            "-r",
            "--receive",
            action="store_true",
            help="Receives key broadcasts from other hosts. Requires you to run -s option first."
        )
        
        parser.add_argument(
            "-s",
            "--send",
            action="store_true",
            help="Init macsec and keeps broadcasting the key. "
        )
        
        args = parser.parse_args()
        if args.encrypt:
            encrypt()
        if args.decrypt: 
            decrypt()
        if args.receive:
            while True:
                frame_receiver()
                time.sleep(1)
            
        if args.send:
            init_my_macsec()
            frame_sender()
        
        
    except KeyboardInterrupt:
        print("")
        exit()
