#!/usr/bin/python
#-*-  coding: utf-8 -*-

class HistoryDownloadParm():
    maxYear = 2013
    def __init__(self):
        self.startYear = 2000
        self.endYear = HistoryDownloadParm.maxYear
        self.current = self.startYear
        self.finished = []
        self.failed = []

class PlainTextImporter():
    def __init__(self):
        pass

class PlainTextExporter():
    def __init__(self):
        pass

    def ExportCompany(self, c):
        pass

    def DownloadCompanyList(self, companys):
        import os
        # process exsiting data
        finishedData = {}
        if os.access('szList.txt', os.F_OK):
            fCompanyList = open('szList.txt', 'r')
            line = fCompanyList.readline().strip('\r\n')
            # this line is field line
            print 'Content of szList.txt'
            line = fCompanyList.readline().strip('\r\n')
            # this is first line of data
            while line:
                print line
                lineFields = line.split(',')
                ticker = lineFields[0]
                startYear = int(lineFields[1])
                availYears = [int(i) for i in lineFields[2:]]
                finishedData[ticker] = [startYear] + availYears
                line = fCompanyList.readline().strip('\r\n')
            fCompanyList.close()
        
        # download new data
        fCompanyList = open('szList.txt', 'w+')
        fieldLine = 'ticker,startYear,years\n'
        fCompanyList.writelines(fieldLine)
        count = 0
        totalCount = len(companys)
        for c in companys:
            print 'Processing %d:%d' % (count, totalCount)
            parm = HistoryDownloadParm()
            if finishedData.has_key(c.ticker):
                alreadyFinished = finishedData[c.ticker]
                parm.startYear = int(alreadyFinished[0])
                # use the first element to store start year.
                parm.finished = parm.finished + alreadyFinished[1:]

            self.DownloadCompanyData(c, parm)
            print 'Finished download', parm.finished
            print 'Failed download', parm.failed

            companyField = [str(i) for i in parm.finished]
            if len(companyField) == 0:
                companyField = [c.ticker, str(HistoryDownloadParm.maxYear)]
            else:
                companyField = [c.ticker, companyField[0]] + companyField
            # ticker, startYear, finishedYear
            companyLine = ','.join(companyField)
            # print companyLine
            fCompanyList.writelines(companyLine)
            fCompanyList.writelines('\n')
            fCompanyList.flush()
            count = count + 1
            
        fCompanyList.close()

    def DownloadCompanyData(self, c, parm):
        import os
        import ystockquote
        import sys

        pathName = c.ticker
        if not os.access(pathName, os.F_OK):
            os.mkdir(pathName)

        print 'Downloading %s , %s:' % (c.ticker, c.fullName),
        for year in range(parm.startYear, parm.endYear):
            # print parm.finished
            print year,
            if year in parm.finished:
                print 'skipped',
                continue
            parm.current = year
            sys.stdout.flush()
            
            lines = ystockquote.get_historical_prices(c.ticker, '%s0101' % year, '%s1231' % year)

            fieldLine = lines[0]
            if len(fieldLine) < 5:
                parm.failed.append(year)
                print 'failed',
                continue

            f = open('%s/%s.txt' % (pathName, year), 'w')

            strFieldLine = ','.join(fieldLine)
            dataLines = lines[1:]

            f.writelines(strFieldLine)
            f.writelines('\n')

            for dataLine in dataLines:
                strDataLine = ','.join(dataLine)
                f.writelines(strDataLine)
                f.writelines('\n')

            f.close()
            parm.finished.append(year)
            print 'done',
        print '...'


if __name__ == '__main__':
    from ShenzhenFieldLoader import ShenzhenFieldLoader
    loader = ShenzhenFieldLoader()
    companys = loader.loadFromPlainTxt()
    # companys = companys.values()[0:2]
    companys = companys.values()


    parm = HistoryDownloadParm()
    exporter = PlainTextExporter()
    exporter.DownloadCompanyList(companys)
    
    
