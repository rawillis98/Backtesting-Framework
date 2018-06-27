from Datafile import *
from pytrends.request import TrendReq
import sys, os
import pandas as pd

def getIOT():
    pytrends = TrendReq(hl = 'en-US', tz = 360)
    kw_list = ["debt"]
    pytrends.build_payload(kw_list, cat = 0, timeframe = 'today 5-y', geo = '', gprop = '')
    iot = pytrends.interest_over_time()
    return iot

def buySignal(equity, data, today, iot): #returns true if we should buy stock
    n = 4

    dates = list(iot.index)
    debts = list(iot['debt'])
    for i in range(len(dates)):
        date = dates[i]
        debt = debts[i]
        if today.year == date.year:
            if today.month == date.month:
                if today.day-5 == date.day:
                    avg = 0
                    for j in range(0, n):
                        avg += debts[i-j]/4
                    if debt < avg:
                        return True
        else:
            return False

def sellSignal(equity, data, iot):
    return True
