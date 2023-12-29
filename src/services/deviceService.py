from src.connection.mysqlConnection import connect_to_database
from src.ld_manager.create_ld import clone_ld, create_ld
from src.ld_manager.get_list_ld import get_list_ld
from src.models.Device import Device


def check_device_exists(data):
    try:
        if data.device:
            list_device = get_list_ld()
            for dvc in list_device:
                if dvc.imei == data.device.imei:
                    get_device = data.device
                    get_device.name = dvc.name
                    get_device.uuid = dvc.uuid
                    get_device.created = False
                    return get_device
            get_device = clone_ld(data.device)
            get_device.created = True
        else:
            get_device = create_ld()
            get_device.created = True
            add_device_to_facebook(data.facebook_account_id, get_device)

        return get_device

    except Exception as e:
        print("Failed to clone device")
        raise ConnectionError("Couldn't clone device") from e


def find_device_by_id(device_id):
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
                            manufacturer=result['manufacturer'],
                            model=result['model'],
                            imsi=result['imsi'],
                            androidId=result['android_id'],
                            simSerial=result['sim_serial'],
                            macAddress=result['mac_address'],
                            create_date=result['create_date'])

        return device

    except Exception as e:
        raise ConnectionError("Could not connect to database") from e


def add_device_to_facebook(fb_account_id, device):
    try:
        connection = connect_to_database()
        cursor = connection.cursor(dictionary=True)
        insert_query = "INSERT INTO devices (imei, manufacturer, model, imsi, android_id, sim_serial, mac_address) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(insert_query, (
            device.imei, device.manufacturer, device.model, device.imsi, device.androidId, device.simSerial,
            device.macAddress))
        device_id = cursor.lastrowid

        alter_query = "UPDATE fb_accounts SET device_id = %s WHERE fb_id = %s"
        cursor.execute(alter_query, (device_id, fb_account_id,))
        connection.commit()
        cursor.close()
        connection.close()
        return device_id

    except Exception as e:
        raise ConnectionError("Could not connect to database") from e

