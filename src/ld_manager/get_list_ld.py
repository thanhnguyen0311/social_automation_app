from src.constants.constants import LDPLAYER_PATH
import sys
import os

from src.models.Device import Device
from src.models.ListDevices import ListDevices
from src.utils.fileUtils import open_file

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))


def get_list_ld():
    vms_path = os.path.join(LDPLAYER_PATH, "vms")
    config_path = os.path.join(LDPLAYER_PATH, "vms", "config")
    file_list = os.listdir(vms_path)
    ListDevices.ld_list = {}
    list_index = []
    for file in file_list:
        if file[:7] == "leidian":
            if int(file[7:]) == 0:
                continue
            list_index.append(int(file[7:]))
            continue

    for index in sorted(list_index):
        try:
            data = open_file(f'leidian{index}.config', config_path)
            data_email = data.get('statusSettings.playerName')
            if data_email:
                name = data_email
                email_address = data_email
            else:
                name = f"LDPlayer-{index}"
                email_address = None

            device = Device(ID=index,
                            name=name,
                            email_address=email_address,
                            imei=data["propertySettings.phoneIMEI"],
                            manufacturer=data["propertySettings.phoneManufacturer"],
                            model=data["propertySettings.phoneModel"],
                            imsi=data["propertySettings.phoneIMSI"],
                            androidId=data["propertySettings.phoneAndroidId"],
                            simSerial=data["propertySettings.phoneSimSerial"],
                            macAddress=data["propertySettings.macAddress"],
                            is_ready=True)
            ListDevices.ld_list[index] = device

        except FileNotFoundError:
            ListDevices.ld_list[index] = None
            continue
    return ListDevices.ld_list
