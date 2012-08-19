#!/usr/bin/python
import datetime
from Config import *
from StockCore.Formatter import DateFormatter
from StockCore.StockDB import ShenzhenStockDB

class PriceSource:
	def __init__(self, ticker):
		# from DataLoader.ShenzhenFieldLoader import ShenzhenFieldLoader
		# loader = ShenzhenFieldLoader()
		self.ticker = ticker
		self.db = ShenzhenStockDB()
		self.source = self.db.GetStock(ticker)
		# self.source = loader.LoadCompany(ticker)  # this version load data from internet, not local cache

	def GetPrice(self, date):
		date_key = DateFormatter.Format(date) # TODO: fix this buggy code.
		# print date_key
		# print self.source.prices
		return self.source.prices.get(date_key)
		# return 1

if __name__ == '__main__':
	'''
	Unit test
	'''
	source = PriceSource('000001.SZ')
	date = datetime.datetime(2011, 6, 1)
	delta = datetime.timedelta(1)
	date = date + delta

	price_record = source.GetPrice(date)
	print price_record
	print dir(price_record)
	print price_record.closePrice
