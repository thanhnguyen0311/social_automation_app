import re
from datetime import datetime

from src.connection.mysqlConnection import connect_to_database


class FBAccount:
    def __init__(self,
                 first_name,
                 last_name,
                 email,
                 password,
                 facebook_account_id=None,
                 device=None,
                 last_login=None,
                 status="New",
                 is_deleted=False,
                 create_date=datetime.now(),
                 cookie="",
                 token="",
                 uid="",
                 auth_2fa="",
                 gender="",
                 secure=False,
                 clone_target_uid=""):
        self.facebook_account_id = facebook_account_id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.device = device
        self.last_login = last_login
        self.status = status
        self.cookie = cookie
        self.auth_2fa = auth_2fa
        self.gender= gender
        self.token = token
        self.uid = uid
        self.clone_target_uid = clone_target_uid
        self.is_deleted = is_deleted
        self.secure = secure
        self.create_date = create_date

    def __str__(self):
        return (f'FB_account{self.facebook_account_id} '
                f'{self.first_name} {self.last_name} '
                f'{str(self.email)} {self.password} '
                f'{self.status} {self.is_deleted} {self.last_login} {self.create_date}')

    @property
    def first_name(self):
        return self.__first_name

    @first_name.setter
    def first_name(self, value):
        if 2 <= len(value) <= 10 and not any(char.isdigit() for char in value):
            self.__first_name = value
        else:
            raise ValueError(f'Invalid first name: {value}')

    @property
    def last_name(self):
        return self.__last_name

    @last_name.setter
    def last_name(self, value):
        if 2 <= len(value) <= 10 and not any(char.isdigit() for char in value):
            self.__last_name = value
        else:
            raise ValueError(f'Invalid last name: {value}')

    @property
    def password(self):
        return self.__password

    @password.setter
    def password(self, value):
        if 6 <= len(value):
            self.__password = value
        else:
            raise ValueError(f'Invalid password: {value}')

    def save(self, email_address=None):
        try:
            connection = connect_to_database()
            cursor = connection.cursor()
            if email_address:
                select_query = "SELECT * FROM emails WHERE email_address = %s"
                cursor.execute(select_query, (email_address,))
                result = cursor.fetchone()

                if result:
                    email_id = result[0]
                    device_id = result[7]
                    insert_query = ("INSERT INTO fb_accounts (first_name, last_name, password, device_id, email_id, "
                                    "cookie, token, uid, auth_2fa, clone_target_uid, gender) VALUES (%s, %s, %s, %s, %s, %s, "
                                    "%s, %s, %s, %s, %s)")
                    cursor.execute(insert_query,
                                   (self.first_name, self.last_name, self.password, device_id, email_id, self.cookie,
                                    self.token, self.uid, self.auth_2fa, self.clone_target_uid, self.gender))

                alter_query = "UPDATE emails SET facebook = TRUE where email_address = %s"
                cursor.execute(alter_query, (email_address,))

            else:
                insert_query = ("INSERT INTO fb_accounts (first_name, last_name, password, cookie, token, uid, "
                                "auth_2fa, clone_target_uid, gender) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)")
                cursor.execute(insert_query,
                               (self.first_name, self.last_name, self.password, self.cookie, self.token, self.uid,
                                self.auth_2fa, self.clone_target_uid, self.gender))

            connection.commit()
            cursor.close()
            connection.close()
        except Exception as e:
            raise ConnectionError("Could not connect to database") from e