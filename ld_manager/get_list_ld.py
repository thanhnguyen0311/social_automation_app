import subprocess
from constants.constants import LDPLAYER_PATH
import sys
import os

from ld_manager.create_ld import open_file
from models.device import Device

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))


def get_list_ld():
    ld_players = []
    vms_path = os.path.join(LDPLAYER_PATH, "vms")
    config_path = os.path.join(LDPLAYER_PATH, "vms", "config")
    try:
        id_list = []
        file_list = os.listdir(vms_path)
        for file in file_list:
            if file[:7] == "leidian":
                id_list.append(file[7:])
            else:
                continue

        for i in id_list:
            name_ld = f"LDPlayer-{i}"
            if int(i) == 0:
                name_ld = "LDPlayer"

            try:
                data = open_file(f'leidian{i}.config', config_path)
            except FileNotFoundError:
                device = Device(ID=i, name=name_ld, uuid=f"emulator-{5554 + (int(i) * 2)}")
                ld_players.append(device)
                continue

            data_fb = data.get('facebook')
            data_email = data.get('email')

            if data_fb is None or data_email is None:
                data_fb = False
                data_email = False

            device = Device(ID=i,
                            name=name_ld,
                            imei=data["propertySettings.phoneIMEI"],
                            uuid=f"emulator-{5554 + (int(i) * 2)}",
                            manufacturer=data["propertySettings.phoneManufacturer"],
                            model=data["propertySettings.phoneModel"],
                            imsi=data["propertySettings.phoneIMSI"],
                            androidId=data["propertySettings.phoneAndroidId"],
                            simSerial=data["propertySettings.phoneSimSerial"],
                            macAddress=data["propertySettings.macAddress"],
                            facebook=data_fb)

            ld_players.append(device)

    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        return None

    return ld_players
