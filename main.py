import numpy as np
import os, sys, datetime
from Datafile import *
from Portfolio import *
from Signals import *
import gc

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

path = r'C:\Users\ricwi\Documents\Projects\Project 2 - Crypto Turtle\Data'
daysOffset = 60
verbose = False
cash = 30000
maxUnits = 10
portfolio = Portfolio(cash, maxUnits, verbose)
            
files = [Datafile(os.path.join(d, x)) for d, dirs, files in os.walk(path) for x in files]
print("Read files in")
for file in files:
    file.calcN()
print("Calculated N")
minDate = files[0].array[1][0]
maxDate = files[0].array[-1][0]

#find minDate and maxDate of trading data
for file in files:
    for i in range(1, len(file.array)):
        row = file.array[i]
        try: int(date = row[0])
        except: continue
        if date < minDate:
            minDate = date
        if date > maxDate:
            maxDate = date
print(minDate)
print(maxDate)
minDate = ymdtodt(minDate)
maxDate = ymdtodt(maxDate)
#minDate = datetime.datetime(2015, 2, 6, 5, 0)
#maxDate = datetime.datetime(2015, 2, 7, 5, 0)

print(minDate)
print(maxDate)
bhprice = 0
today = minDate + datetime.timedelta(days=daysOffset)
    
while(today<maxDate):
    try:
        if verbose:
            print(today)
        #Check for buy signals in S&P 500
        for equity in files:
            todayymd = dttoymd(today)
            todaysRow = getToday(todayymd, equity)
            if todaysRow != 'a':
                availableData = equity.array[0:todaysRow+1]
                if not equity in portfolio.holdings.keys() and len(availableData) > daysOffset:
                    if buySignal(equity, availableData):
                        for date, price in equity.purchases:
                            equity.purchases.remove((date, price))
                        portfolio.long(equity, todaysRow)
                elif equity in portfolio.holdings.keys() and len(availableData) > daysOffset:
                    if increaseSignal(equity, availableData):
                        portfolio.long(equity, todaysRow)
                bhprice = equity.array[todaysRow][close_]
        portfolio.update(todayymd, bhprice)
        portfolio.checkForSell(todayymd)
        
        if verbose:
            print()
    except KeyboardInterrupt:
        portfolio.update(todayymd, bhprice)
        portfolio.printResults()
        portfolio.plotEquity()
        sys.exit(0)
    
    today +=datetime.timedelta(minutes=1)
    gc.collect()
portfolio.printResults()
portfolio.plotEquity()

    


