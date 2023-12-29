import queue
import tkinter as tk

from src.services.socketService import SocketServer
from src.views.layouts.SideBar import SideBar


class Login(tk.Tk):
    def __init__(self):
        super().__init__()


class HomePage(tk.Tk):
    def __init__(self, server):
        super().__init__()
        self.title("Social Automation")
        self.server = server
        self.geometry("1000x600")
        SideBar(self, self.server)


if __name__ == '__main__':
    socket_server = SocketServer('0.0.0.0', 7070, queue.Queue())
    app = HomePage(socket_server)
    try:
        app.mainloop()
    finally:
        # Stop the server when done
        socket_server.stop()
        print("Socket Closed")
