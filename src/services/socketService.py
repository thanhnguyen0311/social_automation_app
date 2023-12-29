import socket
import threading
import queue


class SocketServer(threading.Thread):
    def __init__(self, host, port, task_queue):
        super().__init__()
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((host, port))
        self.server_socket.listen(5)
        self.clients = []
        self.running = True
        self.task_queue = task_queue
        print("Socket started in " + str(self.port) + "/" + str(self.host))

    def run(self):
        while self.running:
            try:
                client_socket, client_address = self.server_socket.accept()
                print(f"Accepted connection from {client_address}")
                self.clients.append((client_socket, client_address))
                self.handle_client(client_socket, client_address)
            except socket.error:
                pass

    def handle_client(self, client_socket, client_address):
        while self.running:
            try:
                data = client_socket.recv(1024)
                if not data:
                    break
                message = data.decode()
                print(f"Received from {client_address}: {message}")

                self.task_queue.put((client_address, message))
            except socket.error:
                break

    def stop(self):
        self.running = False
        for client_socket, _ in self.clients:
            client_socket.close()
        self.server_socket.close()

