# -*- coding: utf-8 -*-

# dataKey = ['公司代码','公司简称','公司全称','英文名称','注册地址','A股代码','A股简称','A股上市日期','A股总股本','A股流通股本','B股代码','B股简称','B股上市日期','B股总股本','B股流通股本','地区','省份']
# classKey = ['name','abbr','fullName','enName','addr','aCode','aAbbr','aDate']

key=[
    ('公司代码','code'),
    ('公司简称','abbr'),
    ('公司全称','fullName'),
    ('英文名称','enName'),
    ('注册地址','addr'),
    ('A股代码','aCode'),
    ('A股简称','aAbbr'),
    ('A股上市日期','aDate'),
    ('A股总股本','aAll'),
    ('A股流通股本','aAvail'),
    ('B股代码','bCode'),
    ('B股简称','bAbbr'),
    ('B股上市日期','bDate'),
    ('B股总股本','bAll'),
    ('B股流通股本','bAvail'),
    ('地区','region'),
    ('省份','province'),
    ('城市','city'),
    ('所属行业','area'),
    ('公司网址','website'),
    ]

dataKey = [i[0] for i in key]
classKey = [i[1] for i in key]

class Company:
    def __init__(self, ticker=None):
        self.ticker = ticker
        self.fullName = ''
        self.records = []

    def Append(self, dayRecord):
        self.records.insert(0, dayRecord)

    def GetProperty(self, propMap, startDate=None, endDate=None):
        '''
        propMap is a function to specify which property will be return.
        '''
        if startDate and endDate:
            dic = []
            for i in self.records:
                if i.date >= startDate and i.date <= endDate:
                    dic.append(propMap(i))
        else:
            dic = [propMap(i) for i in self.records]
        return dic

    def GetDayRecord(self, startDate=None, endDate=None):
        return self.GetProperty(lambda(x):x, startDate, endDate)

    def GetDate(self, startDate=None, endDate=None):
        return self.GetProperty(lambda(x):x.intDate(), startDate, endDate)

    def GetOpen(self, startDate=None, endDate=None):
        return self.GetProperty(lambda(x):x.open, startDate, endDate)

    def GetHigh(self, startDate=None, endDate=None):
        return self.GetProperty(lambda(x):x.high, startDate, endDate)

    def GetLow(self, startDate=None, endDate=None):
        return self.GetProperty(lambda(x):x.low, startDate, endDate)

    def GetVolume(self, startDate=None, endDate=None):
        return self.GetProperty(lambda(x):x.volume, startDate, endDate)

    def PrintInfo(self):
        for classField in self.__dict__.keys():
            if classField in classKey:
                chineseField = dataKey[classKey.index(classField)]
                print chineseField,':',self.__dict__[classField]

            elif classField == 'records':
                print classField,':','Length of records %d' % len(self.records)
            else:
                print classField,':',self.__dict__[classField]

    def GetAll(self):
        '''
        All market of this stock
        '''
        return int(self.aAll.replace(',',''))

    def GetAvailable(self):
        '''
        Available market of this stock
        '''
        return int(self.aAvail.replace(',',''))
            

import datetime

class DayRecord:
    '''
    Record for everyday transaction data.
    '''
    def __init__(self, date, openP, high, low, close, volume, adjclose):
        # self.date = parseDate(date)
        self.date = date
        # self.open, high, close, low is left here for
        # compatability issue
        self.open = float(openP)
        self.openPrice = self.open
        self.high = float(high)
        self.highPrice = self.high
        self.low = float(low)
        self.lowPrice = self.low
        self.close = float(close)
        self.closePrice = self.close
        self.volume = int(volume)
        self.adjclose = float(adjclose)
        
    def intDate(self):
        return int(self.date.strftime('%Y%m%d'))

def parseDate(formatStr):
    return datetime.datetime.strptime(formatStr.strip('"'), '%d-%b-%y')
