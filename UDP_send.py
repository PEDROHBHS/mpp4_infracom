import socket
import time
import os

UDP_IP = "127.0.0.1"
UDP_PORT = 5005
buf = 10*2**10


def send(file_name):
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