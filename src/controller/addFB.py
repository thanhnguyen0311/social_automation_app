from src.models.Email import EmailAccount


class AddFacebookController:
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def save(self, data):
        try:
            self.model.password = data['password']
            self.model.first_name = data['first_name']
            self.model.last_name = data['last_name']
            self.model.auth_2fa = data['auth_2fa']
            self.model.cookie = data['cookie']
            self.model.uid = data['uid']
            self.model.token = data['token']
            self.model.save(data['email'])
            self.view.show_success(f'The facebook {data["email"]} added!')

        except Exception as error:
            self.view.show_error(error)
