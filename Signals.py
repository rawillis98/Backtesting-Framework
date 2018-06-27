from Datafile import *

timestamp_ = 0
open_ = 1
high_ = 2
low_ = 3
close_ = 4
volumebtc_ = 5
volumeusd_ = 6
weightedprice_ = 7
tr_ = 8
n_ = 9

def buySignal(equity, data): #returns true if we should buy stock
    maxUnits = equity.unitsHolding > 3

    #System 1
    system1 = max([x[5] for x in data[len(data)-10:len(data)]]) == data[-1][close_]
    
    #don't buy if last breakout would have worked
    if system1:
        if equity.lastBreakoutIndex == 'a':
            equity.lastBreakoutIndex = len(data)-1
        else:
            N = data[equity.lastBreakoutIndex][8]
            theoreticalBuyPrice = data[equity.lastBreakoutIndex][close_]
            theoreticalStop = getStop(equity, equity.lastBreakoutIndex, theoreticalBuyPrice, False)
            
            for i in range(equity.lastBreakoutIndex, len(data)):
                if data[i][close_] < theoreticalStop:
                    #last time would have been a losing trade so this one is good
                    system1 = True
                    break
                if min([x[close_] for x in data[i-9:i+1]]) == data[i][close_]:
                    #last time would have been a winning trade so this one won't work
                    system1 = False
                
        
    
    #System 2
    system2 = max([x[close_] for x in data[len(data)-20:len(data)]]) == data[-1][close_]
    
    equity.system1 = system1
    equity.system2 = system2
    return (system1 or system2) and (not maxUnits)

def sellSignal(equity, data):
    close = data[-1][close_]

    system1 = min([x[close_] for x in data[len(data)-10:len(data)]]) == data[-1][close_]
    
    system2 = min([x[close_] for x in data[len(data)-20:len(data)]]) == data[-1][close_]

    stopLoss = close < equity.stop
    return (equity.system1 and system1) or (equity.system2 and system2) or stopLoss

def increaseSignal(equity, data):
    N = data[-1][n_]
    price = data[-1][close_]
    buyPrices = [x[1] for x in equity.purchases]
    try: asdf = price > (0.5*N + buyPrices[-1])
    except: print(equity.purchases)
    if asdf:
        return True
    else:
        return False
    
def getStop(equity, todaysIndex, pricePerShare, increase):
    N = equity.array[todaysIndex][n_]
    if increase:
        return equity.stop + 0.5*N
    else:
        return pricePerShare - 2*N
