from datetime import datetime


class User:
    def __init__(self,
                 name,
                 email,
                 password,
                 ID,
                 phone=None,
                 last_seen=None,
                 is_active=False,
                 is_deleted=False,
                 create_date=datetime.now()):
        self.ID = ID
        self.name = name
        self.email = email
        self.password = password
        self.phone = phone
        self.last_seen = last_seen
        self.is_active = is_active
        self.is_deleted = is_deleted
        self.create_date = create_date

