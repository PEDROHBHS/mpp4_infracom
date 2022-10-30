import socket
import select
from GUI import MainWindow


timeout = 3
buf = 2**12

def start(window : MainWindow, ip, port):
    UDP_IP = ip
    IN_PORT = port

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((UDP_IP, IN_PORT))

    while True:
        data, addr = sock.recvfrom(buf)
        if data:
            print ("File name:", data)
            file_name = data.strip()

        f = open(file_name, 'wb')

        while True:
            ready = select.select([sock], [], [], timeout)
            if ready[0]:
                data, addr = sock.recvfrom(buf)
                f.write(data)
            else:
                print ("%s Finish!" % file_name)
                f.close()
                window.create_file(file_name.decode())
                break