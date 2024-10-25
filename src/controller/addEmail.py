from src.models.Email import EmailAccount


class AddEmailController:
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def save(self, data):
        try:
            self.model.email_address = data["email"]
            self.model.password = data['password']
            self.model.first_name = data['first_name']
            self.model.last_name = data['last_name']
            self.model.save()
            self.view.show_success(f'The email {data["email"]} added!')

        except Exception as error:
            self.view.show_error(error)
