from datetime import datetime


class Device:
    def __init__(self, ID, name="", uuid='', imei="", manufacturer="", model="", imsi="", androidId="", simSerial="",
                 macAddress="", facebook="",  create_date=datetime.now()):
        self.ID = ID
        self.name = name
        self.uuid = uuid
        self.imei = imei
        self.manufacturer = manufacturer
        self.model = model
        self.imsi = imsi
        self.androidId = androidId
        self.simSerial = simSerial
        self.macAddress = macAddress
        self.facebook = facebook
        self.create_date = create_date
