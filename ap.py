"""Access Point Object"""
import re
import json


class AP:
    """Access point object"""
    def __init__(self):
        self.ssid = None
        self.mac = None
        self.channel = None
        self.power = None
        self.id = None

    def __str__(self):
        return f"{self.ssid} - {self.mac} - {self.channel} - {self.power}"

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True)

    def clean(self):
        if re.search(r"\\x[0-9a-fA-F]{2}", self.ssid) or self.ssid == "":
            self.ssid = "Unknown SSID"
