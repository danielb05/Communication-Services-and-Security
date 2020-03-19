from time import sleep

MaxP = 0.4
MinTh = 4
MaxTh = 10
AvgLen = 8
queue = []
dropped = []
seg = 0
P = 0


def computeProbability():
    global P 
    P = MaxP * (AvgLen - MinTh) / (MaxTh - MinTh)


def dropSegment(seg):
    dropped.append(seg)


for seg in range(5):
    if(AvgLen <= MinTh):
        queue.append(seg)
    if(MinTh < AvgLen < MaxTh):
        computeProbability()
        dropSegment(seg)        
    if(AvgLen >= MaxTh):
        dropSegment(seg)

print("Probability: ", P)
print("Dropped segments: ", dropped)
print("Queued segments: ", queue)
