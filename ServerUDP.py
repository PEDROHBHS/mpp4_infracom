from socket import *
import time

class ServerUDP:
    def __init__(self, host, port, file):
        self.server = socket(AF_INET, SOCK_DGRAM)
        # self.addr = (host, port)
        self.addr = ("localhost", 53000)
        self.bufferSize = 2048
        self.fileName = file
        self.server.bind(self.addr)
        print('Servidor UDP está pronto!')
        

    def send(self):
        while 1:
            msg, addr = self.server.recvfrom(self.bufferSize)
            msg = msg.decode()
            if msg == 'comece':
                self.server.sendto(bytes(self.fileName, 'utf-8'), addr)
                with open(self.fileName, 'rb') as f:
                    while True:
                        bytes_read = f.read(self.bufferSize)
                        if not bytes_read:
                            break
                        self.server.sendto(bytes_read, addr)
                        time.sleep(0.1)
                msgFromServer = bytes('terminei', 'utf-8')
                self.server.sendto(msgFromServer, addr)
                print("Mensagem: ", msgFromServer.decode())
                print('Fechando servidor UDP...')
                self.server.close()
                break