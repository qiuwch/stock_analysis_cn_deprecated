'''
Record for everyday transaction data.
'''
class DayRecord:
    def __init__(self, date, openP, high, low, close, volume, adjclose):
        self.date = parseDate(date)
        self.open = float(openP)
        self.high = float(high)
        self.low = float(low)
        self.close = float(close)
        self.volume = int(volume)
        self.adjclose = float(adjclose)
        
    def intDate(self):
        return int(self.date.strftime('%Y%m%d'))
