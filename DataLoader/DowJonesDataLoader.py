from entity import DayRecord, Company
class DowJonesDataLoader():
    @classmethod
    def load(cls):
        f = open('data/DJ30_1985_2003.txt')
        companys = {}
        recordCount = 0
        line = f.readline()

        while line and line != '':
            recordCount = recordCount + 1
            [uid, date, openPrice, highPrice, lowPrice, closePrice, volume, adjClose, ticker] = line.split(';')
            ticker = ticker.strip('\r\n"')
            record = DayRecord(date, openPrice, highPrice, lowPrice, closePrice, volume, adjClose)
            if not ticker in companys:
                c = Company(ticker)
                companys[ticker] = c
            else:
                c = companys[ticker]
            c.Append(record)
            line = f.readline()
        print recordCount
        return companys
    
        
