from datetime import datetime


class Device:
    def __init__(self, ID, name="", email_address='', uuid='', imei="", manufacturer="", model="", imsi="", androidId="", simSerial="",
                 macAddress="",  create_date=""):
        self.ID = ID
        self.name = name
        self.email_address = email_address
        self.uuid = uuid
        self.imei = imei
        self.manufacturer = manufacturer
        self.model = model
        self.imsi = imsi
        self.androidId = androidId
        self.simSerial = simSerial
        self.macAddress = macAddress
        self.create_date = create_date
