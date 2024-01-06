import requests

from src.connection.mysqlConnection import connect_to_database
from src.models.Email import EmailAccount
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
            email = None
            if row['email_id']:
                email = find_email_by_id(row['email_id'])
            else:
                if row['uid']:
                    email = EmailAccount(first_name=row['first_name'],
                                         email_address=row['uid'],
                                         last_name=row['last_name'],
                                         password=row['password'])

            device = find_device_by_id(row['device_id'], email.email_address)
            fb_accounts[row['fb_id']] = FBAccount(facebook_account_id=row['fb_id'],
                                                  first_name=row['first_name'],
                                                  last_name=row['last_name'],
                                                  device=device,
                                                  email=email,
                                                  password=row['password'],
                                                  last_login=row['last_login'],
                                                  create_date=row['date'],
                                                  status=row['status'],
                                                  is_deleted=bool(row['is_deleted']),
                                                  cookie=row['cookie'],
                                                  token=row['token'],
                                                  auth_2fa=row['auth_2fa'],
                                                  uid=row['uid'],
                                                  secure=bool(row['secure']),
                                                  clone_target_uid=row['clone_target_uid'],
                                                  gender=row['gender']
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


def get_2fa_code(string):
    response = requests.get(f"https://2fa.live/tok/{string}")
    if response.status_code == 200:
        code = response.json()
        return code['token']
