import socket
import time
import os


buf = 2**12


def send(file_name, ip, port):
    UDP_IP = ip
    UDP_PORT = port
    file_name_ = os.path.basename(file_name)


    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(file_name_.encode(), (UDP_IP, UDP_PORT))
    print ("Sending %s ..." % file_name)

    f = open(file_name, "rb")
    data = f.read(buf)
    while(data):
        if(sock.sendto(data, (UDP_IP, UDP_PORT))):
            data = f.read(buf)
            time.sleep(0.02) # Give receiver a bit time to save

    sock.close()
    f.close()