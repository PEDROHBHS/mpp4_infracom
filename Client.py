import socket
import sys

class Client:
    def __init__(self, host, port, id):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.id = host, port
        try:
            self.client.bind(self.id)
            self.client.connect(id)
        except:
            self.client.close()
            sys.exit(2)

    def receive(self):
        try:
            message = self.client.recv(1024).decode('utf-8')
            return message
        except:
            print("error of receive")
            self.client.close()

    def send(self, message):
        try:
            self.client.send(message.encode())
            print(f"enviado : {message}")
        except:
            print("error to send")
            self.client.close()
