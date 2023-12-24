import re

from src.connection.mysqlConnection import connect_to_database


class FBAccountRequestDto:
    def __init__(self,
                 first_name,
                 last_name,
                 email,
                 password,
                 email_password):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.email_password = email_password

    @property
    def email(self):
        return self.email

    @email.setter
    def email(self, value):
        """
        Validate the email
        :param value:
        :return:
        """
        pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if re.fullmatch(pattern, value):
            self.email = value
        else:
            raise ValueError(f'Invalid email address: {value}')

    def add(self):
        try:
            connection = connect_to_database()
        except Exception as e:
            raise ValueError("Failed! Can't connect to database")


