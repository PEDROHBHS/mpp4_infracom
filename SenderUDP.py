from socket import socket, AF_INET, SOCK_DGRAM, timeout

def ip_checksum(the_bytes):
    return b'%02X' % (sum(the_bytes) & 0xFF)


SEGMENT_SIZE = 100


class SenderUDP:
    def __init__(self, dest_addr, dest_port, listen_addr, listen_port, filename):
        self.dest_addr = dest_addr
        self.dest_port = int(dest_port)
        self.dest = (dest_addr, dest_port)
        self.listen_addr = listen_addr
        self.listen_port = int(listen_port)
        self.listen = (listen_addr, listen_port)
        self.filename = filename
        self.file = open(filename, 'rb')

        with open(filename, 'rb') as f:
            self.content = f.read()

        self.send_sock = socket(AF_INET, SOCK_DGRAM)
        self.recv_sock = socket(AF_INET, SOCK_DGRAM)

        self.recv_sock.bind(self.listen)
        self.recv_sock.settimeout(1)

        self.offset = 0
        self.seq = 0

    def send(self):
        while self.offset < len(self.content):
            if self.offset + SEGMENT_SIZE > len(self.content):
                segment = self.content[self.offset:]
            else:
                segment = self.content[self.offset:self.offset + SEGMENT_SIZE]
            self.offset += SEGMENT_SIZE

            ack_received = False
            while not ack_received:
                self.send_sock.sendto((ip_checksum(segment) + str(self.seq) + segment).encode(), self.dest)

                try:
                    message, address = self.recv_sock.recvfrom(4096)
                except timeout:
                    print("Timeout")
                else:
                    print(message)
                    checksum = message[:2]
                    ack_seq = message[5]
                    if ip_checksum(message[2:]) == checksum and ack_seq == str(self.seq):
                        ack_received = True

            self.seq = 1 - self.seq