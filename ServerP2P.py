import socket
from datetime import datetime

class ServerP2P:
    def __init__(self, host, port):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.id = host, port
        self.server.bind(self.id)
        self.server.listen(1)
        print("server ready...")

        self.client, self.address = self.server.accept()
        print(f"connected server: {self.address[0]} {self.address[1]}")

    def receive(self):
        try:
            message = self.client.recv(1024).decode("utf-8")
            return message
        except:
            print("error to receive")
            self.client.close()
            return None

    def send(self, message):
        try:
            self.client.send(message.encode())
            print(f"enviado : {message}")
        except:
            print("error to send")
            self.client.close()
