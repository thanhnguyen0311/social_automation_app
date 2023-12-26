from src.connection.mysqlConnection import connect_to_database
from src.ld_manager.create_ld import clone_ld, create_ld
from src.ld_manager.get_list_ld import get_list_ld
from src.models.Device import Device


def find_device_by_id(device_id):
    try:
        device = None
        connect = connect_to_database()
        cursor = connect.cursor(dictionary=True)
        query = "SELECT * FROM devices where device_id = %s"
        cursor.execute(query, (device_id,))
        result = cursor.fetchone()
        cursor.close()
        connect.close()
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


def check_device_exists(device):
    try:
        if device:
            list_device = get_list_ld()
            for dvc in list_device:
                if dvc.imei == device.imei:
                    get_device = device
                    get_device.name = dvc.name
                    get_device.uuid = dvc.uuid
                    return get_device
            get_device = clone_ld(device)
        else:
            get_device = create_ld()

        return get_device

    except Exception as e:
        print("Failed to clone device")
        raise ConnectionError("Couldn't clone device") from e
