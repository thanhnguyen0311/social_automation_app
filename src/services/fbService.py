import requests

from src.connection.mysqlConnection import connect_to_database
from src.models.Email import EmailAccount
from src.models.Facebook import FBAccount
from src.services.deviceService import find_device_by_id
from src.services.emailService import find_email_by_id
from datetime import datetime


def find_fb_account_by_ID(fb_account_id):
    try:
        connection = connect_to_database()
        cursor = connection.cursor(dictionary=True)
        query = "SELECT * FROM fb_accounts where fb_id = %s and is_deleted = False"
        cursor.execute(query, (fb_account_id,))
        result = cursor.fetchall()
        cursor.close()
        connection.close()
        for row in result:
            if row['email_id']:
                email = find_email_by_id(row['email_id'])
                email_address = email.email_address
            else:
                email = None
                email_address = row['uid']
            if row['device_id']:
                device = find_device_by_id(row['device_id'], email_address)
            else:
                device = None
            account = FBAccount(facebook_account_id=fb_account_id,
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
            return account



    except Exception as e:
        raise ConnectionError("Could not connect to database") from e


def get_all_fb_accounts(user_id):
    try:
        connection = connect_to_database()
        cursor = connection.cursor(dictionary=True)
        query = "SELECT * FROM fb_accounts where user_id = %s and is_deleted = False"
        cursor.execute(query, (user_id,))
        result = cursor.fetchall()
        cursor.close()
        connection.close()
        FBAccount.list_accounts = {}
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
            FBAccount.list_accounts[row['fb_id']] = FBAccount(facebook_account_id=row['fb_id'],
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

        return FBAccount.list_accounts

    except Exception as e:
        raise ConnectionError("Could not connect to database") from e


def get_ready_fb_accounts(user_id):
    try:
        connection = connect_to_database()
        cursor = connection.cursor(dictionary=True)
        query = "SELECT * FROM fb_accounts where user_id = %s and status = %s and is_deleted = False "
        cursor.execute(query, (user_id, "ALIVE",))
        result = cursor.fetchall()
        cursor.close()
        connection.close()
        ready_accounts = []
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
            if not device.is_ready:
                continue

            account = FBAccount(facebook_account_id=row['fb_id'],
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
            ready_accounts.append(account)

        return ready_accounts

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
        alter_query = 'UPDATE fb_accounts SET last_login = %s, status = %s WHERE fb_id = %s'
        cursor.execute(alter_query, (datetime.now(), 'ALIVE', fb_account_id,))
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
