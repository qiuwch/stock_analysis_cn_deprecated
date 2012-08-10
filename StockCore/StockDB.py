#!/usr/bin/python
from Config import *
from entity import *

class ShenzhenStockDB:
	def __init__(self):
		print "Construct DB"

	def GetStock(self, ticker):
		''' From ShenzhenFieldLoader '''
		txt_file = open(SHENZHEN_COMPANY_INFO, 'r')
		field_line = txt_file.readline()
		filed_cn_vals = field_line.split(':')

		data_line = txt_file.readline()
		companys = {}
		while data_line:
			c = Company()
			data_vals = data_line.split(':')
			for i in xrange(len(data_vals)):
				c.__dict__[classKey[i]] = data_vals[i]

			data_line = txt_file.readline()
			c.ticker = c.code + '.SZ'
			companys[c.ticker] = c
		txt_file.close()

		# c = companys[ticker + '.SZ']
		c = companys[ticker]
		start_year = 2001
		end_year = 2013

		for year in range(start_year, end_year):
			suffix = c.ticker.split('.')[1]
			record_filename = os.path.join(SZ_DATA_DIR, c.ticker, '%s.txt' % year)
			# f = open('%s/%s/%s.txt' % (suffix, c.ticker, year), 'r')
			if os.access(record_filename, os.R_OK):
				f = open(record_filename, 'r')
				filed_line = f.readline().strip('\r\n')
				fields = field_line.split(',')
				data_line = f.readline().strip('\r\n')
				while data_line:
					# print data_line
					[date, open_price, high_price, low_price, close_price, volume, adj_close] = data_line.split(',')
					record = DayRecord(date, open_price, high_price, low_price, close_price, volume, adj_close)
					c.Append(record)
					data_line = f.readline().strip('\r\n')
				f.close()
		return c

if __name__ == '__main__':
	db = ShenzhenStockDB()	
	c = db.GetStock('000001')
	c.PrintInfo()
	print c
