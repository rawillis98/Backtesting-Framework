from numpy import genfromtxt
import numpy as np
import datetime

def utodt(unixDate):
    return datetime.datetime.fromtimestamp(int(unixDate)).strftime('%Y-%m-%d %H:%M:%S')

def ymdtodt(ymd):
    ymd = str(ymd)
    return datetime.date(int(ymd[0:4]), int(ymd[4:6]), int(ymd[6:8]))

def dttoymd(dt):
    ymd = str(dt.year)
    if dt.month < 10:
        ymd += "0"
        ymd += str(dt.month)
    else:
        ymd += str(dt.month)
    if dt.day < 10:
        ymd += "0"
        ymd += str(dt.day)
    else:
        ymd += str(dt.day)
    return ymd

def getToday(todayymd, equity):    
    for row in range(0, len(equity.array)):
        date = int(equity.rowtoymd(row))
        if int(todayymd) == date:
            return row
    return 'a'


class Datafile:
    def __init__(self, file):
        self.array = genfromtxt(file, delimiter=',')
        self.array = np.flipud(self.array)
        self.array = np.delete(self.array, len(self.array)-1, 0)
        self.fullpath = file
        self.name = "SPY"
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
            open_ = 3
            high_ = 4
            low_ = 5
            close_ = 6
            tr_ = 8
            n_ = 9
            
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
            PDN = self.array[i-1][n_]
            TR = self.array[i][tr_]
            N = (19*PDN + TR)/20
            self.array[i][n_] = N
    def rowtoymd(self, row):
        ymd = ""
        ymd += str(int(self.array[row][2]))
        month = str(int(self.array[row][0]))
        if len(month) == 1:
            ymd+= "0" + month
        else:
            ymd += month

        day = str(int(self.array[row][1]))
        if len(day) == 1:
            ymd+= "0" + day
        else:
            ymd += day
        return ymd

        
        
        

            






















    
