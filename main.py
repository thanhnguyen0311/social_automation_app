import tkinter as tk
import asyncio

from src.services.socketService import SocketClient
from src.views.layouts.SideBar import SideBar
from src.constants.constants import SERVER_SOCKET


class Login(tk.Tk):
    def __init__(self):
        super().__init__()


class HomePage(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Social Automation")
        self.geometry("1400x600")
        # self.websocket_client = SocketClient(SERVER_SOCKET, self.display_message)
        self.websocket_client = None
        SideBar(self, self.websocket_client)
        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def display_message(self, message):
        print(message)

    def on_close(self):
        # asyncio.get_event_loop().run_until_complete(self.websocket_client.close())
        # self.websocket_client.websocket_thread.join()
        self.destroy()


if __name__ == '__main__':
    app = HomePage()
    app.mainloop()
