import re

class AP:
    def __init__(self):
        pass

    def clean(self):
        if re.search(r"\\x[0-9a-fA-F]{2}", self.ssid) or self.ssid == "":
            self.ssid = "Unknown SSID"