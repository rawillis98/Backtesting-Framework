import numpy as np
import os, sys, datetime, gc
from Datafile import *
from Portfolio import *
from Signals import *

path = r'C:\Users\ricwi\Documents\Projects\Project 1 - Turtle Rules\SP 500 Data'
daysOffset = 60
verbose = False
cash = 30000
maxUnits = 30
portfolio = Portfolio(cash, maxUnits, verbose)
            
files = [Datafile(os.path.join(d, x)) for d, dirs, files in os.walk(path) for x in files]
for file in files:
    file.calcN()
print("Calculated N")
minDate = files[0].array[0][0]
maxDate = minDate

#find minDate and maxDate of trading data
for file in files:
    for row in file.array:
        date = row[0]
        if date < minDate:
            minDate = date
        if date > maxDate:
            maxDate = date

minDate = ymdtodt(minDate)
maxDate = ymdtodt(maxDate)

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
                        portfolio.long(equity, todaysRow)
                elif equity in portfolio.holdings.keys() and len(availableData) > daysOffset:
                    if increaseSignal(equity, availableData):
                        portfolio.long(equity, todaysRow)
        portfolio.checkForSell(todayymd)
        portfolio.update(todayymd)
        if verbose:
            print()
    except:
        portfolio.update(todayymd)
        portfolio.printResults()
        portfolio.plotEquity()
        sys.exit(0)
    gc.collect()
    
    today +=datetime.timedelta(days=1)
portfolio.printResults()
portfolio.plotEquity()

    


