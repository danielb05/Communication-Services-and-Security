import socket
from time import sleep


def SendAck(ne):
    sleep(t_toack)
    datagram = 'ACK-'+str(ne)
    s.sendto(datagram.encode(), (HOST, PORTACK))
    print("SENT ACK ", ne)


HOST = 'localhost'                 # Symbolic name meaning all available interfaces
PORT = 50007              # Arbitrary non-privileged port
PORTACK = 50006
t_toack = 2


s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((HOST, PORT))
NextExpected = 0

while 1:
    data, addr = s.recvfrom(1024)
    data = data.decode('ascii')
    error = int(data.split("-")[0])
    num = int(data.split("-")[1])
    if error == 0:
        if num == NextExpected:
            NextExpected += 1
            SendAck(NextExpected)

    # else:
    #     print("Datagram " + str(num) + " lost")
