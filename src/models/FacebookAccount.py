class FBAccount:
    def __init__(self,
                 ID,
                 first_name,
                 last_name,
                 email,
                 password,
                 device,
                 last_login,
                 status,
                 is_deleted,
                 create_date):
        self.ID = ID
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.device = device
        self.last_login = last_login
        self.status = status
        self.is_deleted = is_deleted
        self.create_date = create_date
