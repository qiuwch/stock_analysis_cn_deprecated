# -*- coding: utf-8 -*-

import BeautifulSoup

from Config import *
from StockCore.entity import Company, classKey

class ShenzhenFieldLoader():
    def LoadCompany(self, ticker):
        # this deprecated function load data from online service
        companys = self.Load()
        c = companys.get(ticker)
        if len(c.records) == 0:
            from YahooDataLoader import YahooDataLoader
            YahooDataLoader.LoadCompanyHistoryFromLocalCache(c, 2011, 2012)
        return c

    def Load(self):
        return self.LoadFromPlainTxt()
        # self.loadFromXmlFile()

    def LoadFromPlainTxt(self):
        txtFile = open(SHENZHEN_COMPANY_INFO, 'r')
        fieldLine = txtFile.readline()
        fieldCnVals = fieldLine.split(':')
        
        dataLine = txtFile.readline()
        companys = {}
        while dataLine:
            c = Company()
            dataVals = dataLine.split(':')
            for i in xrange(len(dataVals)):
                c.__dict__[classKey[i]] = dataVals[i]
            dataLine = txtFile.readline()
            c.ticker = c.code + '.SZ'
            companys[c.ticker] = c
        txtFile.close()
        return companys
        

    def LoadFromXmlFile(self):
        '''
        从xls载入数据
        仅有股票信息，无具体交易信息
        '''
        f = open('s深圳交易所.xls')
        soup = BeautifulSoup.BeautifulSoup(f)
        titleRow = soup.find('tr', {'class':'cls-data-tr-head'})
        dataRows = soup.findAll('tr',{'class':'cls-data-tr'})
        companys = {}
        fields = self.LoadField(titleRow)
        for i in dataRows:
            c = self.LoadFromXmlRow(i)
            companys[c.code] = c
        return companys


    def LoadField(self, titleRow):
        fields = []
        xmlFields = titleRow.findAll('td',{'class':'cls-data-th'})
        for i in xmlFields:
            field = i.text.replace(' ','')
            fields.append(field)
        return fields     

    def LoadFromXmlRow(self, xmlRow):
        c = Company()
        dataVal = xmlRow.findAll('td')
        for i in xrange(len(dataVal)):
            if i < len(classKey) and classKey[i] != '':
                c.__dict__[classKey[i]] = dataVal[i].text
        return c   
