class Task:
    def __init__(self, function, args=None, list_account=None, name=""):
        self.function = function
        self.name = name
        self.is_running = False
        self.list_account = list_account if list_account is not None else []
        self.args = args if args is not None else []

    def execute(self):
        self.is_running = True
        self.function(*self.args)

    def __stop__(self):
        for account in self.list_account:
            if account.task is not None:
                account.task.__stop__()
        self.is_running = False
