import socket
import time
import threading
from collections import deque


HOST = 'localhost'                 # Symbolic name meaning all available interfaces
PORT = 50007              # Arbitrary non-privileged port
PORTACK = 50008

sockt = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sockt.bind((HOST, PORT))

time_to_ack = 2

packagesBuffer = []
timesBuffer = []
nextExpected = 0


def ReceivePackages():
    while 1:
        data, addr = sockt.recvfrom(1024)
        t3 = threading.Thread(target=manageIncomming(data))
        t3.start()


def manageIncomming(data):
    global packagesBuffer, timesBuffer
    data = data.decode('ascii')
    error = int(data.split("-")[0])
    num = int(data.split("-")[1])
    if error == 0:
            packagesBuffer.append(num)
            timesBuffer.append(time.time())


def ManageBuffer():
    global packagesBuffer, timesBuffer
    while 1:
        if (len(packagesBuffer) >= 3):
            package = packagesBuffer[2]
            packagesBuffer = packagesBuffer[3:]
            timesBuffer = timesBuffer[3:]
            SendAck(package)
        elif (len(timesBuffer) > 0 and timesBuffer[0] - time.time() > 2):
            package = packagesBuffer[0]
            packagesBuffer = packagesBuffer[1:]
            timesBuffer = timesBuffer[1:]
            SendAck(package)


def SendAck(ne):
    time.sleep(time_to_ack)
    datagram = 'ACK-'+str(ne)
    sockt.sendto(datagram.encode(), (HOST, PORTACK))
    print("SENT ACK ", ne)


t1 = threading.Thread(target=ReceivePackages)
t1.start()

t2 = threading.Thread(target=ManageBuffer())
t2.start()
