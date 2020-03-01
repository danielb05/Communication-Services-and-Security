import socket
import time
import threading


HOST = 'localhost'
PORT = 50007
PORTACK = 50008

sockt = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sockt2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sockt2.bind((HOST, PORTACK))

transmition_time = 1.
LastSent = -1
LastAck = -1
TimeOut = 10.
LimitTime = 200.
Buffer = []
RetransBuffer = []
errorrate = 0.3
alpha = 0.8
cwmax = 4
cwini = 1
cwnd = cwini
effectiveWindow = cwnd
# rtt = 5


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
    global Buffer, LastAck
    while 1:
        data, addr = sockt2.recvfrom(1024)
        data = data.decode('ascii')
        num = int(data.split('-')[1])-1

        if num == (LastAck+1):
            Trace("ACK received"+data)
            LastAck = num


def SendRetransBuffer():
    while len(RetransBuffer) > 0:
        num = RetransBuffer[0]
        datagram = '0-'+str(num)
        del RetransBuffer[0]
        time.sleep(transmition_time)
        sockt.sendto(datagram.encode(), (HOST, PORT))
        Trace('sent retrans: '+datagram)


def TimeOut(num):
    global RetransBuffer, LastAck
    time.sleep(TimeOut)
    if num >= LastAck:
        RetransBuffer.append(num)
        Trace("TimeOut "+str(num))
        SendRetransBuffer()


def SendBuffer():
    global Buffer, LastSent
    while len(Buffer) > 0:
        num = Buffer[0]
        del Buffer[0]
        error = '0'
        if isPrime(num):
            error = '1'
            print("Datagram", num, "lost")
        datagram = error+'-'+str(num)  # Segment:  errorindicator-seqnum
        time.sleep(transmition_time)
        LastSent = num
        sockt.sendto(datagram.encode(), (HOST, PORT))
        Trace('sent: '+datagram)
        t = threading.Thread(target=TimeOut, args=(num,))
        t.start()


def Trace(mess):
    t = time.time()-start_time
    print(t, '|', "'"+mess+"'")

x = threading.Thread(target=ProcessAck)
x.start()

for i in range(30):
    Buffer.append(i)

start_time = time.time()
while time.time()-start_time < LimitTime:
    SendBuffer()
