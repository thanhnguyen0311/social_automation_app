import tkinter as tk

from src.views.layouts.SideBar import SideBar


class Login(tk.Tk):
    def __init__(self):
        super().__init__()
        HomePage()


class HomePage(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Social Automation")
        self.geometry("1000x600")
        SideBar(self)


if __name__ == '__main__':
    app = HomePage()
    app.mainloop()
