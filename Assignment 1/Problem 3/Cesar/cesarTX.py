import socket
import time 
import random
import threading


HOST = 'localhost'    
PORT = 50007 
PORTACK = 50008

LastSent=-1
LastAck=-1
TO=5.
LimitTime=200.
Buffer=[]
RetransBuffer=[]
errorrate=0.3


s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
t_time=1.0
s2.bind((HOST,PORTACK))

def isPrime(number):
    if number > 1:
        for i in range(2, number):
            if (number % i) == 0:
                return False
                break
        else:
            return True
    return False

def ProcessAck():
    global Buffer,LastAck
    while 1:
        data,addr = s2.recvfrom(1024)
        data = data.decode('ascii')
        num=int(data.split('-')[1])-1

        if num==(LastAck+1):
            Trace("ACK rec"+data)
            LastAck=num

def SendRetransBuffer():
    while len(RetransBuffer)>0:
        num=RetransBuffer[0]
        datagram='0-'+str(num)
        del RetransBuffer[0]
        time.sleep(t_time)
        s.sendto(datagram.encode(),(HOST,PORT))
        Trace('sent retrans: '+datagram)

def TimeOut(num):
    global RetransBuffer,LastAck
    time.sleep(TO)
    if num>=LastAck:
        RetransBuffer.append(num)
        Trace("TOU "+str(num))
        SendRetransBuffer()

def SendBuffer():
    global Buffer,LastSent
    while  len(Buffer)>0:
        num=Buffer[0]
        del Buffer[0]       
        error='0'
        if isPrime(num):
            error='1'
            print("Datagram", num, "lost")
        datagram=error+'-'+str(num)   #   Segment:  errorindicator-seqnum
        time.sleep(t_time)
        LastSent=num
        s.sendto(datagram.encode(),(HOST,PORT))
        Trace('sent: '+datagram)
        t = threading.Thread(target=TimeOut, args=(num,))   
        t.start()

def Trace(mess):
    t=time.time()-start_time
    print(t,'|',"'"+mess+"'")


random.seed(0)

x = threading.Thread(target=ProcessAck)   
x.start()

for i in range(30):
    Buffer.append(i)

start_time = time.time()
while time.time()-start_time<LimitTime:
    SendBuffer()