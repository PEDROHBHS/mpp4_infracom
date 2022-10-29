from socket import socket, AF_INET, SOCK_DGRAM


def ip_checksum(the_bytes):
    return b'%02X' % (sum(the_bytes) & 0xFF)


class ReceiverUDP:
    def __init__(self, dest_addr, dest_port, listen_addr, listen_port):
        self.dest_addr = dest_addr
        self.dest_port = int(dest_port)
        self.dest = (dest_addr, dest_port)
        self.listen_addr = listen_addr
        self.listen_port = int(listen_port)
        self.listen = (listen_addr, listen_port)

        self.send_sock = socket(AF_INET, SOCK_DGRAM)
        self.recv_sock = socket(AF_INET, SOCK_DGRAM)

        self.recv_sock.bind(self.listen)

        self.expecting_seq = 0

    def send(self, content, to):
        checksum = ip_checksum(content)
        self.send_sock.sendto(checksum + content, to)

    def receive(self):
        with open('imagem.png', 'wb') as new_file:
            while True:
                message, address = self.recv_sock.recvfrom(4096)

                checksum = message[:2].decode()
                seq = message[2].decode()
                content = message[3:]

                if ip_checksum(content, checksum) == checksum:
                    self.send("ACK" + seq, self.dest)
                    if seq == str(expecting_seq):
                        new_file.write(content)
                        expecting_seq = 1 - expecting_seq
                else:
                    negative_seq = str(1 - expecting_seq)
                    self.send("ACK" + negative_seq, self.dest)