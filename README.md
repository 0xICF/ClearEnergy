ClearEnergy | UMASploit v1.1
============

![Alt text](https://0xicf.files.wordpress.com/2017/04/clearenergy-banner.jpg?w=676 "ClearEnergy - UMASploit")




Introduction
============

UMASploit framework developed to test if a remote PLC hardware device is vulnerable to CVE-2017-6032 and CVE-2017-6034 vulnerabilities (ClearEnergy) as documented in ICSA-17-101-01 (ICS-CERT Advisory) and SEVD-2017-065-01 (Schneider Electric Advisory). UMASploit combines the advantages of both vulnerabilities in order to a send remote administrative commands to a target PLCs.

The current version of UMASploit includes the following classes and will be updated soon:
UMAS Login Key Generator (ULKG)
Modbus Remote Command Tool (MRCT)

NOTE: The full source of ClearEnergy is currently under restrictions and cannot be released.




Background
============
In April 4, 2017 researchers at CRITIFENCE® Critical Infrastructure and SCADA/ICS Cyber Threats Research Group have demonstrated a new proof of concept ransomware attack aiming to erase (clear) the ladder logic diagram in Programmable Logic Controllers (PLCs). UMASploit is the library behind ClearEnergy proof of concept ransomware attack that CRITIFENCE researchers used in their proof of concept ransomware research.

The vulnerabilities behind the ransomware a.k.a ClearEnergy affects a massive range of PLC models of world’s largest manufacturers of SCADA and Industrial Control Systems. This includes Schneider Electric Unity series PLCs and Unity OS from version 2.6 and later, other PLC models of leading vendors include GE and Allen-Bradley (MicroLogix family) which are also found to be vulnerable to the ransomware attack.

ClearEnergy, which was based on vulnerabilities CVE-2017-6032 (SVE-82003203) and CVE-2017-6034 (SVE-82003204) that have been discovered by CRITIFENCE security researchers, disclosed profound security flaws in the UMAS protocol of the vendor Schneider Electric. 



UMAS protocol vulnerabilities
============
UMAS protocol seems to suffer from critical vulnerabilities in the form of bad design of the protocol session key, which results in authentication bypass. UMAS is a Kernel level protocol and an administrative control layer used in Unity series PLC and Unity OS from 2.6. It relies on the Modicon Modbus protocol, a common protocol in Critical Infrastructure, SCADA and industrial control systems and used to access both unallocated and allocated Memory from PLC to SCADA system.




NOTICE
============
UMASploit can send remote administrative command to wide range of vulnerable PLC from diferent vendors, it is strongly recommended not to use this framework or the relevant library in production environments. 
UMASploit developed for research purposes only, it is strongly recommended that you do not use this tool for illegal purposes. 





UMAS Login Key Generator (ULKG)
============

Overview
-
UMAS Login Key Generator (ULKG) is part of ClearEnergy - UMASploit package. ULKG allows to send a login request to target PLC that vulnerable to ClearEnergy vulnerabilities in order to get a UMAS Session Key (Identifier). You can use this session key later with Modbus Remote Command Tool (MRCT) in order to send remote adminitrative commands to the vulnerable PLC.


How to Use
-
Call to UKLG using the 'start_uklg()' function.
The funcion returns a valid session key.


Example use in code
-
from _UMASploit import ULKG
key = ULKG.start_ulkg()

Example output:
\x6b




Modbus Remote Command Tool (MRCT)
============

Overview
-
Modbus Remote Command Tool (MRCT) is part of ClearEnergy - UMASploit library. 
MRCT allows to send a remote administrative commands to a target PLC that vulnerable to ClearEnery vulnerabilities.


How to Use
-
Call to MRCT using the 'start_mrct()' function, specify the 'key' (the one you fetched with ULKG) 
and the 'command' (1=RUN/2=STOP/3=RESTART/4=UPLOAD/5=DOWNLOAD/0=Cancel) parameters.
The funcion returns a boolean flag (True or False).


Example use in code
-
from _UMASploit import MRCT
output = MRCT.start_mrct(key, "STOP")

Example output:
True




WARNING
============
ClearEnergy - UMASploit is a a set of tools allows to test if a target PLC on a SCADA networks is vulnerable to ClearEnergy vulnerabilities, irespponsible use of ClearEnergy - UMASploit can cause damage to Critical Infrastructure, SCADA, Industrial Control Systems and other field hardware. CRITIFENCE will not be responsible for any damage that caused by using this source code.



Change log
============
April 4, 2017 - UMASploit v1.0.1 Beta


Screenshots
============

![Alt text](https://0xicf.files.wordpress.com/2017/04/umasploit.jpg "ClearEnergy | UMASploit v1.1")

ClearEnergy | UMASploit v1.1




Authors
============

CrabonFiber51, BlackPian0


License
============
GNU GPL v3



References
============



Vulnerabilities
-

CVE-2017-6032
http://www.cve.mitre.org/cgi-bin/cvename.cgi?name=2017-6032

CVE-2017-6034
http://www.cve.mitre.org/cgi-bin/cvename.cgi?name=2017-6034

SVE-82003203
http://www.critifence.com/sve/sve.php?id=82003203

SVE-82003204
http://www.critifence.com/sve/sve.php?id=82003204



Advisories
-

Schneider Electric - SEVD-2017-065-01
http://www.schneider-electric.com/en/download/document/SEVD-2017-065-01/

ICS-CERT, Department of Homeland Security (DHS) - ICSA-17-101-01
https://ics-cert.us-cert.gov/advisories/ICSA-17-101-01



News
-

SecurityAffairs - http://securityaffairs.co/wordpress/57731/malware/clearenergy-ransomware-scada.html

0xICF - https://0xicf.wordpress.com/2017/04/09/clearenergy-ransomware-can-destroy-process-automation-logics-in-critical-infrastructure-scada-and-industrial-control-systems/

VirusGuides - http://virusguides.com/clearenergy-ransomware-targets-critical-infrastructure-scada-industrial-control-systems/

CRITIFENCE - http://critifence.com/blog/clear_energy/

