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
        date = int(equity.array[row][0])
        if int(todayymd) == date:
            return row
        elif int(todayymd) < date:
            return 'a'


class Datafile:
    def __init__(self, file):
        self.array = genfromtxt(file, delimiter=',')
        self.fullpath = file
        self.name = file.split("\\")[7].split("_")[1].split(".")[0]
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
            O = self.array[i][2]
            H = self.array[i][3]
            L = self.array[i][4]
            C = self.array[i][5]
            PDC = self.array[i-1][5]

            TR = max([H-L, H-PDC, PDC - L])
            self.array[i][7] = TR
        N = 0
        for i in range(0, 20):
            N += self.array[i][7]/20
        self.array[19][8] = N
        for i in range(20, len(self.array)):
            PDN = self.array[i-1][8]
            TR = self.array[i][7]
            N = (19*PDN + TR)/20
            self.array[i][8] = N
        
        

            






















    
