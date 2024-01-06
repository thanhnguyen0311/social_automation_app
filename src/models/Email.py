import re
from datetime import datetime

from src.connection.mysqlConnection import connect_to_database


class EmailAccount:
    def __init__(self,
                 first_name,
                 last_name,
                 email_address,
                 password,
                 email_id=None,
                 create_date=datetime.now(),
                 device=None,
                 facebook=False,
                 tiktok=False,
                 telegram=False,
                 status=None,
                 secure=False,
                 is_deleted=False,
                 task=None):
        self.email_id = email_id
        self.first_name = first_name
        self.last_name = last_name
        self.email_address = email_address
        self.password = password
        self.create_date = create_date
        self.task = task
        self.device = device
        self.facebook = facebook
        self.status = status
        self.tiktok = tiktok
        self.telegram = telegram
        self.secure = secure
        self.is_deleted = is_deleted

    def __str__(self):
        return f'Email_account{self.first_name} {self.last_name} {self.email_address} {self.password} {self.create_date}'

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
    def email_address(self):
        return self.__email_address

    @email_address.setter
    def email_address(self, value):
        if value.isdigit():
            self.__email_address = value
            return

        pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if re.fullmatch(pattern, value):
            self.__email_address = value
        else:
            raise ValueError(f'Invalid email address: {value}')

    def save(self):
        try:
            connection = connect_to_database()
            cursor = connection.cursor()
            select_query = "SELECT * FROM emails WHERE email_address = %s"
            cursor.execute(select_query, (self.email_address,))
            result = cursor.fetchone()

            if result:
                email_id = result[0]
                raise ValueError("This email already exists")

            else:
                insert_query = "INSERT INTO emails (first_name, last_name, email_address, password) VALUES (%s, %s, %s, %s)"
                cursor.execute(insert_query, (self.first_name, self.last_name, self.email_address, self.password))
                email_id = cursor.lastrowid

            connection.commit()
            cursor.close()
            connection.close()
            return email_id
        except Exception as e:
            raise ConnectionError("Could not connect to database") from e
