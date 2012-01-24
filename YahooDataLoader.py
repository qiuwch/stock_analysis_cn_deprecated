import ystockquote
from entity import DayRecord

class YahooDataLoader():
    def __init__(self):
        pass

    @classmethod
    def load(cls, ticker):
        return ystockquote.get_price(ticker)

    @classmethod
    def loadHistory(cls, ticker, start_date, end_date):
        return ystockquote.get_historical_prices(ticker, start_date, end_date)

    @classmethod
    def loadCompanyHistory(cls, c, start_date, end_date):
        lines = ystockquote.get_historical_prices(c.ticker, start_date, end_date)
        fieldLine = lines[0]
        print fieldLine
        dataLines = lines[1:]
        for dataLine in dataLines:
            [date, openPrice, highPrice, lowPrice, closePrice, volume, adjClose] = dataLine
            record = DayRecord(date, openPrice, highPrice, lowPrice, closePrice, volume, adjClose)
            c.Append(record)
        return lines



if __name__ == '__main__':
    from ShenzhenFieldLoader import ShenzhenFieldLoader
    loader = ShenzhenFieldLoader()
    companys = loader.loadFromPlainTxt()
    c = companys.values()[0]

    # print YahooDataLoader.load('GOOG')
    # print YahooDataLoader.loadHistory('002132.SZ', '20110101', '20120101')
    # print YahooDataLoader.loadHistory('000916.SZ', '20110101', '20120101')
    print c.fullName
    print YahooDataLoader.loadCompanyHistory(c, '20110101', '20120101')
    
