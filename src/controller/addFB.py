class AddFacebook:
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def add(self, fb_acc):
        try:
            self.model.fb_acc = fb_acc
            self.model.save()
            self.view.show_success(f'The facebook {fb_acc.email} added!')

        except ValueError as error:
            self.view.show_error(error)
