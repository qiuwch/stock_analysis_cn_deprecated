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
    ('省份','')]

dataKey = [i[0] for i in key]
classKey = [i[1] for i in key]

class Company:
    def __init__(self, ticker):
        self.ticker = ticker
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
        return self.getProperty(lambda(x):x, startDate, endDate)

    def GetDate(self, startDate=None, endDate=None):
        return self.getProperty(lambda(x):x.intDate(), startDate, endDate)

    def GetOpen(self, startDate=None, endDate=None):
        return self.getProperty(lambda(x):x.open, startDate, endDate)

    def GetHigh(self, startDate=None, endDate=None):
        return self.getProperty(lambda(x):x.high, startDate, endDate)

    def GetLow(self, startDate=None, endDate=None):
        return self.getProperty(lambda(x):x.low, startDate, endDate)

    def GetVolume(self, startDate=None, endDate=None):
        return self.getProperty(lambda(x):x.volume, startDate, endDate)

    def PrintInfo(self):
        for i in self.__dict__.keys():
            field = dataKey[classKey.index(i)]
            print field,':',self.__dict__[i]

    def intAAll(self):
        '''
        All market of this stock
        '''
        return int(self.aAll.replace(',',''))

    def intAAvail(self):
        '''
        Available market of this stock
        '''
        return int(self.aAvail.replace(',',''))

        
def loadFromXml(xmlRow):
    c = Company()
    dataVal = xmlRow.findAll('td')
    for i in xrange(len(dataVal)):
        if i < len(classKey) and classKey[i] != '':
            c.__dict__[classKey[i]] = dataVal[i].text
    return c
        
