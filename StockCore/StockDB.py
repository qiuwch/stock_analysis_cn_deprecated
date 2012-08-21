#!/usr/bin/python
# -*- encoding: utf-8 -*-
from DbConfig import *
from Entity import *

class ShenzhenStockDB:
	'''
	Usage:
	from StockCore.StockDB import ShenzhenStockDB
	db = ShenzhenStockDB()
	ticker = '000001.SZ'
	db.GetStock(ticker)
	'''
	def __init__(self):
		self.company_list = {}
		pass

	def GetCompanyList(self):
		if not self.company_list:
			# lazy load
			txt_file = open(SHENZHEN_COMPANY_INFO, 'r')
			field_line = txt_file.readline()
			filed_cn_vals = field_line.split(':')

			data_line = txt_file.readline()
			while data_line:
				c = Company()
				data_vals = data_line.split(':')
				for i in xrange(len(data_vals)):
					c.__dict__[classKey[i]] = data_vals[i]

				data_line = txt_file.readline()
				c.ticker = c.code + '.SZ'
				self.company_list[c.ticker] = c
			txt_file.close()
		return self.company_list

	def GetStock(self, ticker):
		''' Refactor from ShenzhenFieldLoader '''
		company_list = self.GetCompanyList()

		# c = companys[ticker + '.SZ']
		c = company_list[ticker]
		start_year = 2001
		end_year = 2013

		dates = []

		for year in range(end_year, start_year, -1): # TODO: range(start_year, end_year):
			suffix = c.ticker.split('.')[1]
			record_filename = os.path.join(SZ_DATA_DIR, c.ticker, '%s.txt' % year)
			# f = open('%s/%s/%s.txt' % (suffix, c.ticker, year), 'r')
			if os.access(record_filename, os.R_OK):
				f = open(record_filename, 'r')
				field_line = f.readline().strip('\r\n')
				fields = field_line.split(',')
				data_line = f.readline().strip('\r\n')
				while data_line:
					# print data_line
					[date, open_price, high_price, low_price, close_price, volume, adj_close] = data_line.split(',')
					record = DayRecord(date, open_price, high_price, low_price, close_price, volume, adj_close)
					dates.append(record.date) # TODO: change to more efficient way
					c.Insert(record)  # TODO: change this to append
					data_line = f.readline().strip('\r\n')
				f.close()

		if dates:
			c.min_date = min(dates)
			c.max_date = max(dates)
		else:
			print "StockDB:stock info of %s is empty" % c.ticker

		return c

if __name__ == '__main__':
	db = ShenzhenStockDB()	
	c = db.GetStock('000001.SZ')
	c.PrintInfo()

	companys = db.GetCompanyList()
	print len(companys)
	print(dir(c))

	company_area = {}
	area_name = {}
	for c in companys.values():
		[key, val] =  c.area.split(' ')
		if None == company_area.get(key):
			company_area[key] = []
			area_name[key] = val
		company_area[key].append(c)

	print len(company_area.keys())
	for key in company_area.keys():
		print area_name[key], len(company_area[key])

	from PyQt4 import QtGui, QtCore

	app = QtGui.QApplication([])

	tree_widget = QtGui.QTreeWidget()
	tree_widget.show()
	tree_widget.setColumnCount(2)
	tree_widget.setHeaderLabel(QtCore.QString.fromUtf8('行业分类'))
	# TODO: can only set one column now

	category_keys = company_area.keys()
	for category_idx in range(len(category_keys)):
		category_key = category_keys[category_idx]
		category_item = QtGui.QTreeWidgetItem()
		category_item.setText(0, QtCore.QString.fromUtf8(area_name[category_key]))
		category_item.setText(1, str(len(company_area[category_key])))
		tree_widget.insertTopLevelItem(category_idx, category_item)

		for company_idx in range(len(company_area[category_key])):
			company_item = QtGui.QTreeWidgetItem()
			c = company_area[category_key][company_idx]
			company_item.setText(0, QtCore.QString.fromUtf8(c.ticker))
			company_item.setText(1, QtCore.QString.fromUtf8(c.abbr))

			category_item.insertChild(company_idx, company_item)

	app.exec_()

		




