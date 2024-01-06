class Task:
    def __init__(self, function, args=None, name=""):
        self.function = function
        self.args = args if args is not None else []
        self.name = name

    def execute(self):
        self.function(*self.args)

