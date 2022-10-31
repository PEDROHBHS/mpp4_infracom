import socket
import time
import os
from UDP_func import *


buf = 4096


def send(file_name, ip, port, self_ip, self_port):
    seq = 0
    UDP_IP = ip
    UDP_PORT = port
    file_name_ = os.path.basename(file_name)


    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((self_ip, self_port))
    sock.settimeout(1.0)

    pkt = cria_pacote_cliente(self_port, UDP_PORT, 65 + len(file_name_), seq, file_name_)
    print(pkt)

    while True:
        sock.sendto(pkt, (UDP_IP, UDP_PORT))

        try:
            msg_recv, addr = sock.recvfrom(buf)

            if msg_recv is None:
                print('breaking1')
                break

            portaorigem_r = int(msg_recv[0:16].decode())
            portadestino_r = int(msg_recv[16:32].decode())
            comprimento_r = int(msg_recv[32:48].decode())
            ack_r = int(msg_recv[48:49].decode())
            seq_r = int(msg_recv[49:50].decode())
            soma_r = int(msg_recv[50:66].decode())

            soma = checksum(portaorigem_r, portadestino_r, comprimento_r)

            if soma_r != soma or (portaorigem_r, portadestino_r) != (UDP_PORT, self_port) or ack_r != seq:
                print('falhou1')
                continue

        except socket.timeout:
            print('timeout1')
            continue

        print ("Sending %s ..." % file_name)

        seq = 1
        break

    f = open(file_name, "rb")
    data = f.read(buf)
    while(data):
        pkt = cria_pacote_cliente(self_port, UDP_PORT, 65 + len(data), seq, data)

        if(sock.sendto(pkt, (UDP_IP, UDP_PORT))):
            try:
                msg_recv, addr = sock.recvfrom(buf)

                portaorigem_r = int(msg_recv[0:16].decode())
                portadestino_r = int(msg_recv[16:32].decode())
                comprimento_r = int(msg_recv[32:48].decode())
                ack_r = int(msg_recv[48:49].decode())
                seq_r = int(msg_recv[49:50].decode())
                soma_r = int(msg_recv[50:66].decode())

                soma = checksum(portaorigem_r, portadestino_r, comprimento_r)

                if soma_r != soma or (portaorigem_r, portadestino_r) != (UDP_PORT, self_port) or ack_r != seq:
                    print('falhou2')
                    continue

            except socket.timeout:
                print('timeout2')
                continue

            if seq:
                seq = 0
            else:
                seq = 1
                
            data = f.read(buf)
            time.sleep(0.02)

    sock.close()
    f.close()