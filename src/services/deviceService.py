from src.connection.mysqlConnection import connect_to_database
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
