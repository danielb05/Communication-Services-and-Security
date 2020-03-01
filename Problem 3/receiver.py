import socket
from time import sleep


def SendAck(ne):
    sleep(time_to_ack)
    datagram = 'ACK-'+str(ne)
    sockt.sendto(datagram.encode(), (HOST, PORTACK))
    print("SENT ACK ", ne)


HOST = 'localhost'                 # Symbolic name meaning all available interfaces
PORT = 50007              # Arbitrary non-privileged port
PORTACK = 50008

sockt = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sockt.bind((HOST, PORT))

time_to_ack = 2

buffer = []
nextExpected = 0

while 1:
    data, addr = sockt.recvfrom(1024)
    data = data.decode('ascii')
    error = int(data.split("-")[0])
    num = int(data.split("-")[1])
    if error == 0:
        buffer.append(num)
        if num == nextExpected:
            SendAck(nextExpected+1)
            nextExpected += 1
