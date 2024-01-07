import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))


class Device:
    def __init__(self, ID=None, email_address='', imei="", manufacturer="",
                 model="", imsi="", androidId="", simSerial="", name=None,
                 macAddress="", create_date="", is_ready=False, is_running=False):
        self.ID = ID
        self.name = name if name is not None else email_address
        self.email_address = email_address
        self.uuid = f"emulator-{5554 + (int(self.ID) * 2)}" if ID is not None else None
        self.imei = imei
        self.manufacturer = manufacturer
        self.model = model
        self.imsi = imsi
        self.androidId = androidId
        self.simSerial = simSerial
        self.macAddress = macAddress
        self.create_date = create_date
        self.thread = None
        self.is_ready = is_ready
        self.is_running = is_running
