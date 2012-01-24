# -*- coding: utf-8 -*-

import BeautifulSoup
# from entity import Company


def loadField(titleRow):
    fields = []
    xmlFields = titleRow.findAll('td',{'class':'cls-data-th'})
    for i in xmlFields:
        field = i.text.replace(' ','')
        fields.append(field)
    return fields        

f = open('s深圳交易所.xls')

txtDataFile = open('sjCompanyData.txt', 'w')


soup = BeautifulSoup.BeautifulSoup(f)
titleRow = soup.find('tr', {'class':'cls-data-tr-head'})
dataRows = soup.findAll('tr',{'class':'cls-data-tr'})

fields = loadField(titleRow)
fieldLine = ':'.join(fields)
print fieldLine
txtDataFile.writelines(fieldLine.encode('utf-8'))
txtDataFile.writelines('\n')

for xmlRow in dataRows:
    xmlDataVal = xmlRow.findAll('td')
    textDataVal = [i.text for i in xmlDataVal]
    dataLine = ':'.join(textDataVal)
    txtDataFile.writelines(dataLine.encode('utf-8'))
    txtDataFile.writelines('\n')
    print dataLine

txtDataFile.close()    


