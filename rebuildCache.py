#!/usr/bin/python

import os

pathName = 'SZ'
companyList = os.listdir(pathName)
print 'Downloaded companys %d' % len(companyList)
# print companyList

f = open('rebuildSzList.txt', 'w')

fieldLine = 'ticker,startYear,years\n'
f.writelines(fieldLine)

for companyName in companyList:
    years = os.listdir('%s/%s' % (pathName, companyName))
    if len(years) == 0:
        continue
    years = [int(year.split('.')[0]) for year in years]
    years.sort()
    companyLine = [companyName, str(years[0])] + [str(year) for year in years]
    companyLine =  ','.join(companyLine)
    f.writelines(companyLine)
    f.writelines('\n')
f.close()    
    # print companyLine

