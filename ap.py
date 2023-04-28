import re
import json

class AP:
    def __init__(self):
        pass

    def __str__(self):
        return f"{self.ssid} - {self.mac} - {self.channel} - {self.power}"

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
                          sort_keys=True)

    def clean(self):
        if re.search(r"\\x[0-9a-fA-F]{2}", self.ssid) or self.ssid == "":
            self.ssid = "Unknown SSID"