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
        self.token = token
        self.uid = uid
        self.clone_target_uid = clone_target_uid
        self.is_deleted = is_deleted
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
        if 8 <= len(value):
            self.__password = value
        else:
            raise ValueError(f'Invalid password: {value}')

    def save(self):
        try:
            connection = connect_to_database()
            cursor = connection.cursor()

            email_id = self.email.save()
            select_query = "SELECT * FROM fb_accounts WHERE email_id = %s"
            cursor.execute(select_query, (email_id,))
            result = cursor.fetchone()

            if result:
                raise ValueError("Email already registered")

            else:
                insert_query = "INSERT INTO fb_accounts (first_name, last_name, password, email_id) VALUES (%s, %s, %s, %s)"
                cursor.execute(insert_query,
                               (self.first_name, self.last_name, self.password,
                                email_id))

            connection.commit()
            cursor.close()
            connection.close()
        except Exception as e:
            raise ConnectionError("Could not connect to database") from e
