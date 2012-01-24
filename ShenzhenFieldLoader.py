# -*- coding: utf-8 -*-

import BeautifulSoup
from entity import Company, classKey

class ShenzhenFieldLoader():
    def loadFromXmlRow(self, xmlRow):
        c = Company()
        dataVal = xmlRow.findAll('td')
        for i in xrange(len(dataVal)):
            if i < len(classKey) and classKey[i] != '':
                c.__dict__[classKey[i]] = dataVal[i].text
        return c

    def load(self):
        return self.loadFromPlainTxt()
        # self.loadFromXmlFile()

    def loadFromPlainTxt(self):
        txtFile = open('sjCompanyData.txt')
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
        

    def loadFromXmlFile(self):
        '''
        从xls载入数据
        仅有股票信息，无具体交易信息
        '''
        f = open('s深圳交易所.xls')
        soup = BeautifulSoup.BeautifulSoup(f)
        titleRow = soup.find('tr', {'class':'cls-data-tr-head'})
        dataRows = soup.findAll('tr',{'class':'cls-data-tr'})
        companys = {}
        fields = self.loadField(titleRow)
        for i in dataRows:
            c = self.loadFromXmlRow(i)
            companys[c.code] = c
        return companys


    def loadField(self, titleRow):
        fields = []
        xmlFields = titleRow.findAll('td',{'class':'cls-data-th'})
        for i in xmlFields:
            field = i.text.replace(' ','')
            fields.append(field)
        return fields        
