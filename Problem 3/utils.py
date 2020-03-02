logFile = 'log.md'

def createLogFile():
    header = "|Time (s)|Event|Eff.Win. (MSS)|cwnd (MSS)|RTT (s)|sRTT (s)|TOut (s)\n"
    secondLine = "|---|---|---|---|---|---|---|\n"
    with open(logFile, mode='w', newline='\n') as file:
        file.write(header)
        file.write(secondLine)
        file.close()


def logData(t, log, effectiveWindow, cwnd, rtt, srtt, TOut):
    with open(logFile, mode='a', newline='\n') as file:
        row = ("%.2f" % t)
        row += "|" + log
        row += "|" + str(effectiveWindow)
        row += "|" + str(cwnd)
        row += "|" + str(rtt)
        row += "|" + ("%.2f" % srtt) 
        row += "|" + str(TOut)
        row += "\n"
        file.write(row)
        file.close()

def isPrime(number):
    if number > 1:
        for i in range(2, number):
            if (number % i) == 0:
                return False
                break
        else:
            return True
    return False

def updatesRTT(alpha, srtt, rtt):
    return alpha * srtt + (1 - alpha) * rtt