from socket import *
class ClientUDP:
    def __init__(self, id):
        self.id = ("localhost", 53000)
        # self.id = id
        self.bufferSize = 2048
        self.client = socket(AF_INET, SOCK_DGRAM)

    
    def receive(self):
        msgFromClient = bytes('comece', 'utf-8')
        self.client.sendto(msgFromClient, self.id)
        msgFromServer = self.client.recvfrom(self.bufferSize)
        fileName = msgFromServer[0].decode()
        print('Recebendo: ',fileName)

        with open(f'{fileName}', "wb") as f:
            loop = 0
            while True:
                loop += 1
                print(f'Recebendo... ', loop)
                bytes_read = self.client.recvfrom(self.bufferSize)[0]
                try:
                    if bytes_read.decode() == 'terminei':
                        print(f'"{fileName}" recebido com sucesso!')
                        print(f'Mensagem do Servidor: {bytes_read.decode()}')
                        break
                except UnicodeDecodeError:
                    f.write(bytes_read)
        return fileName