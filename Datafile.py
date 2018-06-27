from numpy import genfromtxt
import numpy as np
import datetime, time
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
def utodt(unixDate):
    return datetime.datetime.fromtimestamp(int(unixDate))

def ymdtodt(ymd):
    return datetime.datetime.fromtimestamp(int(ymd))

def dttoymd(dt):
    return time.mktime(dt.timetuple())
     

def getToday(todayymd, equity):
    for row in range(1, len(equity.array)):
        date = int(equity.array[row][0])
        if int(todayymd) == date:
            return row
        elif int(todayymd) < date:
            return 'a'


class Datafile:
    def __init__(self, file):
        self.array = genfromtxt(file, delimiter=',')
        self.fullpath = file
        self.name = file.split("\\")[7]
        self.purchases = []
        self.stop = 'a'
        self.unitsHolding = 0
        self.lastBreakoutIndex = 'a'
        self.reasonForBuying = ""
        self.system1 = False
        self.system2 = False
        
    def calcN(self):
        self.array = np.append(self.array, np.zeros((len(self.array), 2)), axis=1)
        for i in range(1, len(self.array)):
            O = self.array[i][open_]
            H = self.array[i][high_]
            L = self.array[i][low_]
            C = self.array[i][close_]
            PDC = self.array[i-1][close_]

            TR = max([H-L, H-PDC, PDC - L])
            self.array[i][tr_] = TR
        N = 0
        for i in range(0, 20):
            N += self.array[i][tr_]/20
        self.array[19][n_] = N
        for i in range(20, len(self.array)):
            PDN = self.array[i-1][8]
            TR = self.array[i][7]
            N = (19*PDN + TR)/20
            self.array[i][n_] = N
        
        

            






















    
