from src.connection.mysqlConnection import connect_to_database
from src.models.Facebook import FBAccount
from src.services.deviceService import find_device_by_id
from src.services.emailService import find_email_by_id
from datetime import datetime


def get_all_fb_accounts(user_id):
    try:
        connection = connect_to_database()
        cursor = connection.cursor(dictionary=True)
        query = "SELECT * FROM fb_accounts where user_id = %s and is_deleted = False"
        cursor.execute(query, (user_id,))
        result = cursor.fetchall()
        cursor.close()
        connection.close()
        fb_accounts = {}
        for row in result:
            fb_accounts[row['fb_id']] = FBAccount(facebook_account_id=row['fb_id'],
                                                  first_name=row['first_name'],
                                                  last_name=row['last_name'],
                                                  device=find_device_by_id(row['device_id']),
                                                  email=find_email_by_id(row['email_id']),
                                                  password=row['password'],
                                                  last_login=row['last_login'],
                                                  create_date=row['date'],
                                                  status=row['status'],
                                                  is_deleted=bool(row['is_deleted'])
                                                  )

        return fb_accounts

    except Exception as e:
        raise ConnectionError("Could not connect to database") from e


def remove_fb_accounts(fb_account_id):
    try:
        connection = connect_to_database()
        cursor = connection.cursor(dictionary=True)
        alter_query = "UPDATE fb_accounts SET is_deleted = 1 WHERE fb_id = %s"
        cursor.execute(alter_query, (fb_account_id,))
        connection.commit()
        cursor.close()
        connection.close()
        return True

    except Exception as e:
        raise ConnectionError("Could not connect to database") from e


def update_last_login(fb_account_id):
    try:
        connection = connect_to_database()
        cursor = connection.cursor(dictionary=True)
        alter_query = "UPDATE fb_accounts SET last_login = %s WHERE fb_id = %s"
        cursor.execute(alter_query, (datetime.now(), fb_account_id,))
        connection.commit()
        cursor.close()
        connection.close()
        return True

    except Exception as e:
        raise ConnectionError("Could not connect to database") from e


def update_account_status(fb_account_id, status):
    try:
        connection = connect_to_database()
        cursor = connection.cursor(dictionary=True)
        alter_query = "UPDATE fb_accounts SET status = %s WHERE fb_id = %s"
        cursor.execute(alter_query, (status, fb_account_id,))
        connection.commit()
        cursor.close()
        connection.close()

    except Exception as e:
        raise ConnectionError("Could not connect to database") from e
