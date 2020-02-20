import socket
from time import sleep



def SendAck(ne):
    sleep(t_toack)
    s.sendto('ACK-'+str(ne),(HOST,PORTACK))
    print "SENT ACK ",ne 




HOST = 'localhost'                 # Symbolic name meaning all available interfaces
PORT = 50007              # Arbitrary non-privileged port
PORTACK=50008
t_toack=0.1



s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((HOST,PORT))
NextExpected=0

while 1:
    data,addr = s.recvfrom(1024)
    error=int(data.split("-")[0])
    num=int(data.split("-")[1])
    if error==0:
        if  num==NextExpected:
            SendAck(NextExpected+1)
            NextExpected+=1

