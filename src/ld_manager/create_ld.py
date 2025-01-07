import subprocess
import sys
import os
from src.constants.constants import LDCONSOLE_PATH, vms_path, config_path
from src.models.Device import Device
from src.models.Email import EmailAccount
from src.models.Facebook import FBAccount
from src.models.ListDevices import ListDevices
from src.utils.fileUtils import open_file, save_json_file

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))


def create_ld(data=None):
    try:
        id_list = []
        file_list = os.listdir(vms_path)

        for file in file_list:
            if file[:7] == "leidian":
                id_list.append(file[7:])
            else:
                continue

        i = 0
        if len(id_list) > 0:
            id_list = sorted(id_list, key=lambda x: int(x))

            while str(i) in id_list:
                i = i + 1

        email_address = f'new{i}'
        if isinstance(data, FBAccount):
            email_address = data.email.email_address
        if isinstance(data, EmailAccount):
            email_address = data.email_address

        subprocess.call([LDCONSOLE_PATH] + ["copy", "--name", email_address, "--from", "fake"], shell=True)
        if data is not None:
            if data.device is None:
                contents = open_file(f'leidian{str(i)}.config', config_path)

                new_ldplayer = Device(ID=None,
                                      name=email_address,
                                      email_address=email_address,
                                      imei=contents["propertySettings.phoneIMEI"],
                                      manufacturer=contents["propertySettings.phoneManufacturer"],
                                      model=contents["propertySettings.phoneModel"],
                                      imsi=contents["propertySettings.phoneIMSI"],
                                      androidId=contents["propertySettings.phoneAndroidId"],
                                      simSerial=contents["propertySettings.phoneSimSerial"],
                                      macAddress=contents["propertySettings.macAddress"],
                                      is_ready=True)

            else:
                new_ldplayer = Device(ID=None,
                                      name=email_address,
                                      email_address=email_address,
                                      imei=data.device.imei,
                                      manufacturer=data.device.manufacturer,
                                      model=data.device.model,
                                      imsi=data.device.imsi,
                                      androidId=data.device.androidId,
                                      simSerial=data.device.simSerial,
                                      macAddress=data.device.macAddress,
                                      is_ready=True)


        else:
            contents = open_file(f'leidian{str(i)}.config', config_path)
            new_ldplayer = Device(ID=None,
                                  name=email_address,
                                  email_address=email_address,
                                  imei=contents["propertySettings.phoneIMEI"],
                                  manufacturer=contents["propertySettings.phoneManufacturer"],
                                  model=contents["propertySettings.phoneModel"],
                                  imsi=contents["propertySettings.phoneIMSI"],
                                  androidId=contents["propertySettings.phoneAndroidId"],
                                  simSerial=contents["propertySettings.phoneSimSerial"],
                                  macAddress=contents["propertySettings.macAddress"],
                                  is_ready=True)

        ListDevices.ld_list[i] = new_ldplayer
        return ListDevices.ld_list[i]

    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        return None
