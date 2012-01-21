#!/usr/bin/python
'''
Load Dow Jones Data
TODO: abstract data functions
'''
import datetime
from IPython import embed

class DayRecord:
    def __init__(self, date, openP, high, low, close, volume, adjclose):
        self.date = parseDate(date)
        self.open = float(openP)
        self.high = float(high)
        self.low = float(low)
        self.close = float(close)
        self.volume = int(volume)
        self.adjclose = float(adjclose)
        
    def intDate(self):
        return int(self.date.strftime('%Y%m%d'))

class Company:
    def __init__(self, ticker):
        self.ticker = ticker
        self.records = []

    def append(self, dayRecord):
        self.records.insert(0, dayRecord)

    def getProperty(self, propMap, startDate=None, endDate=None):
        if startDate and endDate:
            dic = []
            for i in self.records:
                if i.date >= startDate and i.date <= endDate:
                    dic.append(propMap(i))
        else:
            dic = [propMap(i) for i in self.records]
        return dic

    def dayRecord(self, startDate=None, endDate=None):
        return self.getProperty(lambda(x):x, startDate, endDate)

    def date(self, startDate=None, endDate=None):
        return self.getProperty(lambda(x):x.intDate(), startDate, endDate)

    def open(self, startDate=None, endDate=None):
        return self.getProperty(lambda(x):x.open, startDate, endDate)
    
    def high(self, startDate=None, endDate=None):
        return self.getProperty(lambda(x):x.high, startDate, endDate)
    
    def low(self, startDate=None, endDate=None):
        return self.getProperty(lambda(x):x.low, startDate, endDate)

    def close(self, startDate=None, endDate=None):
        return self.getProperty(lambda(x):x.close, startDate, endDate)

    def volume(self, startDate=None, endDate=None):
        return self.getProperty(lambda(x):x.volume, startDate, endDate)

def parseDate(formatStr):
    return datetime.datetime.strptime(formatStr.strip('"'), '%d-%b-%y')

def main():
    f = open('DJ30 1985 2003.txt')

    companys = {}
    count = 0
    line = f.readline()

    while line and line != '':
        count = count + 1
        [id, date, openP, high, low, close, volume, adjclose, ticker] = line.split(';')
        ticker = ticker.strip('\r\n"')
        r = DayRecord(date, openP, high, low, close, volume, adjclose);
        if not ticker in companys:
            c = Company(ticker)
            companys[ticker] = c
        else:
            c = companys[ticker]
        c.append(r)
        line = f.readline()
    print count
    return companys

if __name__ == '__main__':
    companys = main()
