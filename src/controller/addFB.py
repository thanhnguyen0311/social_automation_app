from src.models.Email import EmailAccount


class AddFacebookController:
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def save(self, data):
        try:
            email = EmailAccount(email_address=data['email'],
                                 password=data['password'],
                                 first_name=data['first_name'],
                                 last_name=data['last_name'])
            if data['email_password']:
                email.password = data['email_password']

            self.model.email = email
            self.model.password = data['password']
            self.model.first_name = data['first_name']
            self.model.last_name = data['last_name']
            self.model.save()
            self.view.show_success(f'The facebook {data["email"]} added!')

        except Exception as error:
            self.view.show_error(error)
