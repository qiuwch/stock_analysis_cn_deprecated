#!/usr/bin/python
import datetime
from Config import *
from StockCore.DbConfig import *
from StockCore.Formatter import DateFormatter
from StockCore.StockDB import ShenzhenStockDB

class PriceSource:
	def __init__(self, ticker):
		self.ticker = ticker

		# Deprecated implementation
		# from DataLoader.ShenzhenFieldLoader import ShenzhenFieldLoader
		# loader = ShenzhenFieldLoader()
		# self.db = ShenzhenStockDB()
		# self.source = self.db.GetStock(ticker)
		# self.source = loader.LoadCompany(ticker)  # this version load data from internet, not local cache

		start_year = 2001
		end_year = 2013

		self.history_price = {}

		for year in range(end_year, start_year, -1): # TODO: range(start_year, end_year):
			suffix = self.ticker.split('.')[1]
			record_filename = os.path.join(SZ_DATA_DIR, self.ticker, '%s.txt' % year)

			if os.access(record_filename, os.R_OK):
				f = open(record_filename, 'r')
				field_line = f.readline().strip('\r\n')
				fields = field_line.split(',')
				data_line = f.readline().strip('\r\n')
				while data_line:
					# print data_line
					[date, open_price, high_price, low_price, close_price, volume, adj_close] = data_line.split(',')
					self.history_price[date] = float(high_price)
					data_line = f.readline().strip('\r\n')
				f.close()

		'''
		if dates:
			c.min_date = min(dates)
			c.max_date = max(dates)
		else:
			print "StockDB:stock info of %s is empty" % c.ticker
		'''

	def GetPrice(self, date):
		date_key = DateFormatter.Format(date) # TODO: fix this buggy code.
		# print date_key
		# print self.source.prices
		
		# Deprecated implementation
		# entry = self.source.prices.get(date_key)

		# if entry:
		# 	return entry.high
		# else:
		#	return None
		return self.history_price.get(date_key)

	def GetHistoryPrice(self, start_date, end_date):
		# TODO: this implementation is really slow, refactor
		# start_date = self.source.min_date

		date = start_date
		delta = datetime.timedelta(1)
		time_range = []

		while date <= end_date:
			time_range.append(date)
			date = date + delta

		prices = {}
		for date in time_range:
			date_key = DateFormatter.Format(date)
			if None != self.GetPrice(date):
				prices[date_key] = self.GetPrice(date)

		print len(prices.keys())
		return prices


		 	





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
