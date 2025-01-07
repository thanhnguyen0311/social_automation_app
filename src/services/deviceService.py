import os
import sys
import time
import warnings

from src.connection.mysqlConnection import connect_to_database
from src.constants.constants import vms_path, config_path
from src.ld_manager.adb_shells import restart_adb_server
from src.ld_manager.create_ld import create_ld
from src.ld_manager.quit_ld import quit_all
from src.ld_manager.run_ld import run_ld
from src.ld_manager.sort_ld import sort_ld
from src.models.Device import Device
from src.models.Email import EmailAccount
from src.models.Facebook import FBAccount
from src.models.ListDevices import ListDevices
from src.utils.fileUtils import rename_folder, save_json_file

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
warnings.filterwarnings("ignore", message=r"\[Deprecated\] Please use 'find_element' with 'AppiumBy.ANDROID_UIAUTOMATOR' instead\.")


def find_device_by_id(device_id, email_address=""):
    try:
        device = None
        connection = connect_to_database()
        cursor = connection.cursor(dictionary=True)
        query = "SELECT * FROM devices where device_id = %s"
        cursor.execute(query, (device_id,))
        result = cursor.fetchone()
        cursor.close()
        connection.close()
        if result:
            device = Device(ID=result['device_id'],
                            imei=result['imei'],
                            email_address=email_address,
                            manufacturer=result['manufacturer'],
                            model=result['model'],
                            imsi=result['imsi'],
                            androidId=result['android_id'],
                            simSerial=result['sim_serial'],
                            macAddress=result['mac_address'],
                            create_date=result['create_date'])
            if (ListDevices.ld_list.get(device_id) is not None
                    and ListDevices.ld_list.get(device_id).name == email_address):
                device = ListDevices.ld_list[device_id]

        return device

    except Exception as e:
        raise ConnectionError("Could not connect to database") from e


def add_device_to_facebook(fb_account_id, device_id):
    if fb_account_id is not None:
        try:
            connection = connect_to_database()
            cursor = connection.cursor(dictionary=True)
            alter_query = "UPDATE fb_accounts SET device_id = %s WHERE fb_id = %s"
            cursor.execute(alter_query, (device_id, fb_account_id,))
            connection.commit()
            cursor.close()
            connection.close()

        except Exception as e:
            raise ConnectionError("Could not connect to database") from e
    else:
        raise ValueError("FB account ID required")


def add_device_to_email(email_id, device_id):
    if email_id is not None:
        try:
            connection = connect_to_database()
            cursor = connection.cursor(dictionary=True)
            alter_query = "UPDATE emails SET device_id = %s WHERE email_id = %s"
            cursor.execute(alter_query, (device_id, email_id,))
            connection.commit()
            cursor.close()
            connection.close()

        except Exception as e:
            raise ConnectionError("Could not create device for email") from e


def create_device(data=None):
    try:
        get_device = create_ld(data)
        if data is not None:
            if data.device is not None:
                device = ListDevices.ld_list.get(data.device.ID)
                if device is not None:
                    return ListDevices.ld_list[data.device.ID]
                else:
                    for key, value in ListDevices.ld_list.items():
                        if value.ID is None and data.device.email_address == value.email_address:
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
                                "statusSettings.playerName": data.device.email_address,
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
                            contents = {**contents, **config}
                            save_json_file(contents, f'leidian{str(key)}.config', config_path)
                            old_vms_path = os.path.join(vms_path, f"leidian{str(key)}")
                            new_vms_path = os.path.join(vms_path, f"leidian{str(data.device.ID)}")
                            rename_folder(old_vms_path, new_vms_path)
                            old_config_path = os.path.join(config_path, f"leidian{str(key)}.config")
                            new_config_path = os.path.join(config_path, f"leidian{str(data.device.ID)}.config")
                            rename_folder(old_config_path, new_config_path)
                            value.uuid = f"emulator-{5554 + (int(data.device.ID) * 2)}"
                            ListDevices.ld_list[data.device.ID] = ListDevices.ld_list.pop(key)
                            return ListDevices.ld_list[data.device.ID]

            else:
                connection = connect_to_database()
                cursor = connection.cursor(dictionary=True)
                insert_query = (
                    "INSERT INTO devices (imei, manufacturer, model, imsi, android_id, sim_serial, mac_address)"
                    "VALUES (%s, %s, %s, %s, %s, %s, %s)")
                cursor.execute(insert_query, (
                    get_device.imei, get_device.manufacturer,
                    get_device.model, get_device.imsi,
                    get_device.androidId, get_device.simSerial,
                    get_device.macAddress))
                device_id = cursor.lastrowid
                connection.commit()
                cursor.close()
                connection.close()

                if isinstance(data, FBAccount):
                    add_device_to_facebook(data.facebook_account_id, device_id)
                if isinstance(data, EmailAccount):
                    add_device_to_email(data.email_id, device_id)

                for key, value in ListDevices.ld_list.items():
                    if value.ID is None:
                        old_vms_path = os.path.join(vms_path, f"leidian{str(key)}")
                        new_vms_path = os.path.join(vms_path, f"leidian{str(device_id)}")
                        rename_folder(old_vms_path, new_vms_path)
                        old_config_path = os.path.join(config_path, f"leidian{str(key)}.config")
                        new_config_path = os.path.join(config_path, f"leidian{str(device_id)}.config")
                        rename_folder(old_config_path, new_config_path)
                        value.ID = device_id
                        value.uuid = f"emulator-{5554 + (int(device_id) * 2)}"
                        ListDevices.ld_list[device_id] = ListDevices.ld_list.pop(key)
                        data.device = ListDevices.ld_list[device_id]
                        return ListDevices.ld_list[device_id]
        return get_device

    except Exception as e:
        raise ConnectionError("Could not create device for email") from e


def run_account_devices(list_account):
    print("Kill all devices...")
    quit_all()
    restart_adb_server(count=len(list_account))
    while True:
        for account in list_account:
            if account.device is None:
                create_device(account)
                run_ld(account.device)
            else:
                if not account.device.is_ready:
                    create_device(account)
                else:
                    print(f"Start LD for {account.device.name}")
                    time.sleep(1)
                run_ld(account.device)

        break
    time.sleep(20)
    sort_ld()
    print("Restart adb server....")
