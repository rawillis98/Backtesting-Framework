from Signals import *
from Datafile import *
import matplotlib.pyplot as plt

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

class Portfolio:
    def __init__(self, startingEquity, maxUnits, verbose):
        self.startingEquity = startingEquity
        self.cash = startingEquity
        self.cashHistory = {}
        self.holdings = {}
        self.equityHistory = {}
        self.numUnitsHoldingHistory = {}
        self.numUnitsHolding = 0
        self.totalEquity = startingEquity
        self.maxUnits = maxUnits
        self.verbose = verbose
        self.bhhistory = {}
        
    def long(self, equity, todayIndex):
        if self.numUnitsHolding < 0:
            raise Exception("negative units holding")
        if self.numUnitsHolding < self.maxUnits - 5:
            #holding size by equal percent of equity
            pricePerShare = equity.array[todayIndex][close_]
            cashPerUnit = int(self.totalEquity/self.maxUnits)
            equalEquity = cashPerUnit*0.95/pricePerShare
            
            #holding size in units with ATR (N)
            unitSize = 0.01*self.totalEquity/(equity.array[todayIndex][n_]*5)

            #all in
            allIn = self.cash/pricePerShare

            #number of shares to buy should be minimum of the above to prevent negative cash
            numShares = allIn
            if equity in self.holdings:
                self.holdings[equity] += numShares
                equity.stop = getStop(equity, todayIndex, pricePerShare, True)
            else:
                self.holdings[equity] = numShares
                equity.stop = getStop(equity, todayIndex, pricePerShare, False)
                
            success = True

            #Update portfolio stats 
            self.numUnitsHolding += 1
            self.cash -= int(numShares*pricePerShare)
            equity.purchases.append((todayIndex, pricePerShare))
            equity.unitsHolding += 1
            
            #Set stop loss
            

            #Check for negative cash
            if self.cash < -100:
                raise Exception("Negative cash")
            
            if not self.verbose:
                print(ymdtodt(equity.array[todayIndex][0]))
            print("Bought " + str(numShares) + " of " + equity.name + " for " + str(pricePerShare) + "  Total: " + str(int(pricePerShare*numShares)))
        else:
            success = False
        return success

    def update(self, todayymd, bhprice):
        refresh = True
        #get old things out of self.holdings
        toDelete = []
        for equity, shares in self.holdings.items():
            today = getToday(todayymd, equity)
            if today == 'a':
                refresh = False
            if self.holdings[equity] == 0:
                toDelete.append(equity)
        for equity in toDelete:
            del self.holdings[equity]
        
        #If we can/need to update equity stuff:
        if refresh:
            self.totalEquity = self.cash
            for equity, shares in self.holdings.items():
               self.totalEquity += int(equity.array[getToday(todayymd, equity)][close_]*shares)
               if self.verbose:
                 print(equity.name + ": " + str(shares) + "@" + str(equity.array[getToday(todayymd, equity)][close_]))
            if self.verbose:
                 print("Cash: " + str(self.cash))
                 print("Units Holding: " + str(self.numUnitsHolding))

            #update historical stats
            self.equityHistory[ymdtodt(todayymd)] = self.totalEquity
            self.cashHistory[ymdtodt(todayymd)] = self.cash
            self.numUnitsHoldingHistory[ymdtodt(todayymd)] = self.numUnitsHolding
            self.bhhistory[ymdtodt(todayymd)] = bhprice
        if self.verbose:
            print("Equity: $" + str(self.totalEquity))

    def sell(self, equity, todaysIndex):
        pricePerShare = equity.array[todaysIndex][close_]
        numShares = self.holdings[equity]
        print("Sold " + str(numShares) + " of " + equity.name + " for " + str(pricePerShare))
        
        self.cash += numShares*pricePerShare
        self.holdings[equity] = 0
        self.numUnitsHolding -= equity.unitsHolding
        equity.unitsHolding = 0
        return True
    def checkForSell(self, todayymd):
        for equity, shares in self.holdings.items():
            todaysIndex = getToday(todayymd, equity)
            if todaysIndex == 'a':
                continue
            availableData = equity.array[0:todaysIndex+1]
            if sellSignal(equity, availableData) and self.holdings[equity] > 0:
                self.sell(equity, todaysIndex)

    def plotEquity(self):
        ax1 = plt.subplot(2, 1, 1)
        x = self.equityHistory.keys()
        y = self.equityHistory.values()
        ax1.plot(x, y, 'b-', label = 'Equity')

        x = self.cashHistory.keys()
        y = self.cashHistory.values()
        #ax1.plot(x, y, 'r-', label = 'Cash')
        
        ax1.legend(loc='best')

        ax2 = plt.subplot(2, 1, 2)
        x = self.bhhistory.keys()
        y = self.bhhistory.values()
        ax2.plot(x, y, 'b-', label = 'Buy and Hold')
        
        plt.show()

    def printResults(self):
        
        percentChange = ((self.totalEquity/self.startingEquity)-1)*100
        print("Percent Change: " + str(percentChange))

        bhStart = self.bhhistory[min(self.bhhistory.keys())]
        bhEnd = self.bhhistory[max(self.bhhistory.keys())]

        bhPercentChange = (bhEnd - bhStart)*100/bhStart
        print("Buy and Hold Percent Change: " + str(bhPercentChange))

    
        
        

        
    
        
