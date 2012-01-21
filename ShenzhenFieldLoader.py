# -*- coding: utf-8 -*-

import BeautifulSoup
import Company

class ShenzhenFieldLoader():
    def loadVal(self, dataRow):
        c = Company.loadFromXml(dataRow)
        return c

    def load(self):
        '''
        从xls载入数据
        仅有股票信息，无具体交易信息
        '''
        f = open('s深圳交易所.xls')
        soup = BeautifulSoup.BeautifulSoup(f)
        titleRow = soup.find('tr', {'class':'cls-data-tr-head'})
        dataRows = soup.findAll('tr',{'class':'cls-data-tr'})
        companys = []
        fields = self.loadField(titleRow)
        for i in dataRows:
            c = self.loadVal(i)
            companys.append(c)
        return companys


    def loadField(self, titleRow):
        fields = []
        xmlFields = titleRow.findAll('td',{'class':'cls-data-th'})
        for i in xmlFields:
            field = i.text.replace(' ','')
            fields.append(field)
        return fields        
