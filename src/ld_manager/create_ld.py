import subprocess
import shutil
import sys
import os
import json
from src.constants.constants import LDPLAYER_PATH, LDCONSOLE_PATH, CLONE_LD_DATA
from src.models.Device import Device
from src.models.Email import EmailAccount
from src.models.Facebook import FBAccount

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

config_path = os.path.join(LDPLAYER_PATH, "vms", "config")
vms_path = os.path.join(LDPLAYER_PATH, "vms")


def open_file(filename, folder):
    # Get the full path to the file
    path = os.path.join(os.path.expanduser('~'), folder, filename)
    # Open the file and read its contents
    with open(path, 'r') as f:
        contents = json.load(f)
    # Return the contents of the file
    return contents


def save_json_file(data, filename, folder):
    path = os.path.join(os.path.expanduser('~'), folder, filename)
    with open(path, 'w') as file:
        json.dump(data, file, indent=2)


def create_ld(data=None):
    email_address = None
    if isinstance(data, FBAccount):
        email_address = data.email.email_address
    if isinstance(data, EmailAccount):
        email_address = data.email_address
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

        subprocess.call([LDCONSOLE_PATH] + ["add"], shell=True)

        contents = open_file(f'leidian{str(i)}.config', config_path)

        source_data = os.path.join(LDPLAYER_PATH, "vms", "data.vmdk")
        destination_data = os.path.join(LDPLAYER_PATH, "vms", f'leidian{str(i)}')
        if CLONE_LD_DATA:
            shutil.copy(source_data, destination_data)

        name_ld = f"LDPlayer-{str(i)}"
        if int(i) == 0:
            name_ld = "LDPlayer"

        new_ldplayer = Device(ID=i,
                              name=name_ld,
                              imei=contents["propertySettings.phoneIMEI"],
                              uuid=f"emulator-{str(5554 + (int(i) * 2))}",
                              manufacturer=contents["propertySettings.phoneManufacturer"],
                              model=contents["propertySettings.phoneModel"],
                              imsi=contents["propertySettings.phoneIMSI"],
                              androidId=contents["propertySettings.phoneAndroidId"],
                              simSerial=contents["propertySettings.phoneSimSerial"],
                              macAddress=contents["propertySettings.macAddress"]
                              )

        config = {
            "name": name_ld,
            "uuid": f"emulator-{str(5554 + (int(i) * 2))}",
            "email": email_address,
            "basicSettings.rootMode": True,
            "basicSettings.adbDebug": 2,
            "advancedSettings.resolution": {
                "width": 720,
                "height": 1280
            },
            "advancedSettings.resolutionDpi": 320,
            "basicSettings.HDRQuality": 0,
            "advancedSettings.cpuCount": 1,
            "advancedSettings.memorySize": 1024
        }

        # Merge 2 json data
        contents = {**contents, **config}
        save_json_file(contents, f'leidian{str(i)}.config', config_path)

    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        return None

    return new_ldplayer


def clone_ld(data):
    email_address = None
    if isinstance(data, FBAccount):
        email_address = data.email.email_address
    if isinstance(data, EmailAccount):
        email_address = data.email_address
    try:
        id_list = []
        file_list = os.listdir(vms_path)

        for file in file_list:
            if file[:7] == "leidian":
                id_list.append(file[7:])
            else:
                continue

        id_list = sorted(id_list, key=lambda x: int(x))
        i = 0

        while str(i) in id_list:
            i = i + 1

        subprocess.call([LDCONSOLE_PATH] + ["add"], shell=True)

        source_data = os.path.join(LDPLAYER_PATH, "vms", "data.vmdk")
        destination_data = os.path.join(LDPLAYER_PATH, "vms", f'leidian{str(i)}')
        if CLONE_LD_DATA:
            shutil.copy(source_data, destination_data)

        name_ld = f"LDPlayer-{str(i)}"
        if int(i) == 0:
            name_ld = "LDPlayer"

        contents = {
            "propertySettings.phoneIMEI": data.device.imei,
            "propertySettings.phoneIMSI": data.device.imsi,
            "propertySettings.phoneSimSerial": data.device.simSerial,
            "propertySettings.phoneAndroidId": data.device.androidId,
            "propertySettings.phoneModel": data.device.model,
            "propertySettings.phoneManufacturer": data.device.manufacturer,
            "propertySettings.macAddress": data.device.macAddress
        }

        config = {
            "name": name_ld,
            "uuid": f"emulator-{str(5554 + (int(i) * 2))}",
            "email": email_address,
            "basicSettings.rootMode": True,
            "basicSettings.adbDebug": 2,
            "advancedSettings.resolution": {
                "width": 720,
                "height": 1280
            },
            "advancedSettings.resolutionDpi": 320,
            "basicSettings.HDRQuality": 0,
            "advancedSettings.cpuCount": 1,
            "advancedSettings.memorySize": 1024
        }

        new_ld = Device(ID=str(i),
                        name=name_ld,
                        imei=data.device.imei,
                        uuid=f"emulator-{str(5554 + (int(i) * 2))}",
                        manufacturer=data.device.manufacturer,
                        model=data.device.model,
                        imsi=data.device.imsi,
                        androidId=data.device.androidId,
                        simSerial=data.device.simSerial,
                        macAddress=data.device.macAddress)

        # Merge 2 json data
        contents = {**contents, **config}
        save_json_file(contents, f'leidian{str(i)}.config', config_path)

    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        return None

    return new_ld
