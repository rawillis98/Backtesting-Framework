import numpy as np
import os, sys, datetime, gc
from Datafile import *
from Portfolio import *
from Signals import *

open_ = 1
high_ = 2
low_ = 3
close_ = 4
tr_ = 6
n_ = 7

path = r'C:\Users\ricwi\Documents\Projects\Project 3 - Google Trends\Data'
weeksOffset = 6
daysOffset = 4
verbose = False
cash = 30000
maxUnits = 30
portfolio = Portfolio(cash, maxUnits, verbose)
            
files = [Datafile(os.path.join(d, x)) for d, dirs, files in os.walk(path) for x in files]
minDate = files[0].rowtoymd(1)
maxDate = minDate

#find minDate and maxDate of trading data
for file in files:
    for row in range(0, len(file.array)):
        date = file.rowtoymd(row)
        if date < minDate:
            minDate = date
        if date > maxDate:
            maxDate = date

minDate = ymdtodt(20120212)
maxDate = ymdtodt(maxDate)

today = minDate + datetime.timedelta(weeks = weeksOffset)

iot = getIOT()

while(today<maxDate):
    try:
        if verbose:
            print(today)
        #Check for buy signals in S&P 500
        for equity in files:
            todayymd = dttoymd(today)
            todaysRow = getToday(todayymd, equity)
            portfolio.checkForSell(todayymd, iot)
            portfolio.update(todayymd, files[0])
            if todaysRow != 'a':
                availableData = equity.array[0:todaysRow+1]
                buySignal(equity, availableData, today, iot)
                if not equity in portfolio.holdings.keys() and len(availableData) > daysOffset:
                    if buySignal(equity, availableData, today, iot):
                        portfolio.long(equity, todaysRow)
        today +=datetime.timedelta(days=1)
        gc.collect()
        if verbose:
            print()
    except KeyboardInterrupt:
        portfolio.update(todayymd, files[0])
        portfolio.printResults()
        portfolio.plotEquity()
        sys.exit(0)
    
    
portfolio.printResults()
portfolio.plotEquity()

    


