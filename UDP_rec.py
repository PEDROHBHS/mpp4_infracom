import socket
import select
from GUI import MainWindow
from UDP_func import *


timeout = 3
buf = 4096

def start(window : MainWindow, ip, port):
    UDP_IP = ip
    IN_PORT = port

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((UDP_IP, IN_PORT))

    while True:
        exp_seq = 0
        
        data, addr = sock.recvfrom(buf)
        
        if data is None:
            print('breaking')
            break

        portaorigem_r = int(data[0:16].decode())
        portadestino_r = int(data[16:32].decode())
        comprimento_r = int(data[32:48].decode())
        soma_r = int(data[48:64].decode())
        seq_r = int(data[64:65].decode())
        dado_r = data[65:].decode()

        soma = checksum(portaorigem_r, portadestino_r, comprimento_r)

        if soma_r != soma or seq_r != exp_seq or (portaorigem_r, portadestino_r) != (addr[1], IN_PORT):
            print('falhou', soma_r, soma, seq_r, exp_seq)
            continue

        exp_seq = 1

        pkt = cria_pacote_servidor(IN_PORT, addr[1], 65, seq_r, exp_seq)
        sock.sendto(pkt, addr)

        print ("File name:", dado_r)
        file_name = dado_r.strip()

        f = open(file_name, 'wb')

        while True:
            ready = select.select([sock], [], [], timeout)
            if ready[0]:
                data, addr = sock.recvfrom(65 + buf)

                portaorigem_r = int(data[0:16].decode())
                portadestino_r = int(data[16:32].decode())
                comprimento_r = int(data[32:48].decode())
                soma_r = int(data[48:64].decode())
                seq_r = int(data[64:65].decode())
                dado_r = data[65:]

                soma = checksum(portaorigem_r, portadestino_r, comprimento_r)

                if soma_r != soma or seq_r != exp_seq or (portaorigem_r, portadestino_r) != (addr[1], IN_PORT):
                    continue

                if exp_seq:
                    exp_seq = 0
                else:
                    exp_seq = 1

                pkt = cria_pacote_servidor(IN_PORT, addr[1], 65, seq_r, exp_seq)
                sock.sendto(pkt, addr)

                f.write(dado_r)
            else:
                print ("%s Finish!" % file_name)
                f.close()
                window.create_file(file_name)
                break