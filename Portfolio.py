from Signals import *
from Datafile import *
import matplotlib.pyplot as plt

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
        
    def long(self, equity, todayIndex):
        if self.numUnitsHolding < 0:
            raise Exception("negative units holding")
        if self.numUnitsHolding < self.maxUnits - 5:
            #holding size by equal percent of equity
            pricePerShare = equity.array[todayIndex][5]
            cashPerUnit = int(self.totalEquity/self.maxUnits)
            equalEquity = int(cashPerUnit*0.95/pricePerShare)
            
            #holding size in units with ATR (N)
            unitSize = int(0.01*self.totalEquity/(equity.array[todayIndex][8]*5))

            #number of shares to buy should be minimum of the above to prevent negative cash
            numShares = min(equalEquity, unitSize)
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

    def update(self, todayymd):
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
               self.totalEquity += int(equity.array[getToday(todayymd, equity)][5]*shares)
               if self.verbose:
                 print(equity.name + ": " + str(shares) + "@" + str(equity.array[getToday(todayymd, equity)][5]))
            if self.verbose:
                 print("Cash: " + str(self.cash))
                 print("Units Holding: " + str(self.numUnitsHolding))

            #update historical stats
            self.equityHistory[ymdtodt(todayymd)] = self.totalEquity
            self.cashHistory[ymdtodt(todayymd)] = self.cash
            self.numUnitsHoldingHistory[ymdtodt(todayymd)] = self.numUnitsHolding
        if self.verbose:
            print("Equity: $" + str(self.totalEquity))

    def sell(self, equity, todaysIndex):
        pricePerShare = equity.array[todaysIndex][5]
        numShares = self.holdings[equity]
        print("Sold " + str(numShares) + " of " + equity.name + " for " + str(pricePerShare))
        
        self.cash += numShares*pricePerShare
        self.holdings[equity] = 0
        self.numUnitsHolding -= equity.unitsHolding
        equity.unitsHolding = 0
        for date, price in equity.purchases:
            equity.purchases.remove((date, price))
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
        ax1.plot(x, y, 'r-', label = 'Cash')
        
        ax1.legend(loc='best')

        ax2 = plt.subplot(2, 1, 2)
        x = self.numUnitsHoldingHistory.keys()
        y = self.numUnitsHoldingHistory.values()
        ax2.plot(x, y, 'b-', label = 'Units Holding')
        
        plt.show()

    def printResults(self):
        
        percentChange = ((self.totalEquity/self.startingEquity)-1)*100
        print("Percent Change: " + str(percentChange))

        maxCashUsed = min([x for x in self.cashHistory.values()])
        print("Max Cash Used: " + str(maxCashUsed))
        
        

        
    
        
