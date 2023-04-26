import subprocess
import os
import re

class Interface:
    def __init__(self):
        self.monitor = False
        self.get_interfaces()

    def get_interfaces(self):
        print("[*] Finding interfaces...")
        interfaces = self.read_iw_dev()
        mon_interfaces = list(filter(lambda x: 'mon' in x, interfaces))
        if len(mon_interfaces) == 1:
            print(f"[*] {mon_interfaces[0]} is already in monitor mode, using that")
            self.name = mon_interfaces[0]
            self.monitor = True
        elif len(mon_interfaces) == 0:
            if len(interfaces) == 0:
                return "[!] No interfaces detected"
            for index, interface in enumerate(interfaces):
                print(f"[{index}] - {interface}")
            choice = input("[?] Choose an interface to use: ")
            if int(choice) in range(len(interfaces)):
                self.name = interfaces[int(choice)]
        # Handle more than 1 monitor device - give choice

    def monitor_on(self):
        # can't hard code 6
        os.system(f"sudo airmon-ng start {self.name} 6 > /dev/null 2>&1")
        self.name = f"{self.name}mon"
        self.monitor = True

    def monitor_off(self):
        os.system(f"sudo airmon-ng stop {self.name} > /dev/null 2>&1")
        self.name = self.name[:-3]
        os.system(f"sudo ifconfig {self.name} up > /dev/null 2>&1")
        self.monitor = False

    def read_iw_dev(self):
        "Read contents of 'iw dev' command to get interfaces"
        output = subprocess.check_output("iw dev", stderr=subprocess.STDOUT, 
                                         shell=True)
        # Replace \n\t with END so we can use regex to extract IF name
        output = str(output).replace(r"\n\t", "END")
        interfaces = re.findall(r"Interface(.+?(?=END))", output)
        return interfaces