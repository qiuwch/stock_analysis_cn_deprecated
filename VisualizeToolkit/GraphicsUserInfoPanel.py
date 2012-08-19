#!/usr/bin/python
# -*- coding: utf-8 -*-
from Config import *
from PyQt4 import QtCore, QtGui

class GraphicsStockList(QtGui.QWidget):
	def __init__(self):
		QtGui.QWidget.__init__(self)

		self.layout = QtGui.QVBoxLayout()
		self.stock_layout = QtGui.QGridLayout()
		self.BuildTitle()

		lbl_stocks = QtGui.QLabel(QtCore.QString.fromUtf8('持有股票'))
		self.layout.addWidget(lbl_stocks)
		self.layout.addLayout(self.stock_layout)

		self.setLayout(self.layout)
		self.stock_list = {}
		self.stock_control = {}
		self.date = None

	def BuildTitle(self):
		lbl_stock_ticker = QtGui.QLabel(QtCore.QString.fromUtf8('代码'))
		lbl_stock_amount = QtGui.QLabel(QtCore.QString.fromUtf8('持有量'))
		lbl_stock_price = QtGui.QLabel(QtCore.QString.fromUtf8('现价'))
		lbl_stock_total = QtGui.QLabel(QtCore.QString.fromUtf8('总值'))

		# add table title
		self.stock_layout.addWidget(lbl_stock_ticker, 0, 0)
		self.stock_layout.addWidget(lbl_stock_amount, 0, 1)
		self.stock_layout.addWidget(lbl_stock_price, 0, 2)
		self.stock_layout.addWidget(lbl_stock_total, 0, 3)


	def UpdateStock(self, stock_ticker, stock_amount):
		stock_price = 0
		if None != self.date:
			from StockCore.StockDB import ShenzhenStockDB
			from StockCore.Formatter import DateFormatter
			db = ShenzhenStockDB()
			c = db.GetStock(stock_ticker)
			date_key = DateFormatter.Format(self.date)
			stock_price_record = c.prices.get(date_key)
			if None != stock_price_record:
				stock_price = stock_price_record.closePrice
			
		stock_total = stock_amount * stock_price

		# Update internal data
		self.stock_list[stock_ticker] = (stock_amount, stock_price, stock_total)
		self.stock_value = sum([item[2] for item in self.stock_list.values()])

		if None == self.stock_control.get(stock_ticker):
			# Create new controls
			lbl_stock_ticker = QtGui.QLabel(stock_ticker)
			lbl_stock_amount = QtGui.QLabel(str(stock_amount))
			lbl_stock_price = QtGui.QLabel(str(stock_price))
			lbl_stock_total = QtGui.QLabel(str(stock_total))

			# store UI controls for update operation
			control_dict = {'amount':lbl_stock_amount, 'price':lbl_stock_price, 'total':lbl_stock_total}
			self.stock_control[stock_ticker] = control_dict

			n = len(self.stock_list)
			# include one line of header, so first line is 1
			self.stock_layout.addWidget(lbl_stock_ticker, n, 0)
			self.stock_layout.addWidget(lbl_stock_amount, n, 1)
			self.stock_layout.addWidget(lbl_stock_price, n, 2)
			self.stock_layout.addWidget(lbl_stock_total, n, 3)
		else:
			stock_control = self.stock_control.get(stock_ticker)
			lbl_stock_amount = stock_control.get('amount')
			lbl_stock_price = stock_control.get('price')
			lbl_stock_total = stock_control.get('total')

			lbl_stock_amount.setText(str(stock_amount))
			lbl_stock_price.setText(str(stock_price))
			lbl_stock_total.setText(str(stock_total))

	def Clear(self):
		# self.stock_layout.clear() # This is not working
		self.layout.removeWidget(self.stock_layout)
		self.stock_layout = QtGui.QGridLayout()

		self.BuildTitle()

	def SetDate(self, date):
		self.date = date


class GraphicsUserInfoPanel(QtGui.QWidget):
	def __init__(self):
		QtGui.QWidget.__init__(self)

		self.lbl_name = QtGui.QLabel()
		self.lbl_money = QtGui.QLabel()
		self.lbl_wealth = QtGui.QLabel()
		self.lbl_date = QtGui.QLabel()
		
		layout = QtGui.QFormLayout()
		layout.addRow(QtCore.QString.fromUtf8('日期'), self.lbl_date)
		layout.addRow(QtCore.QString.fromUtf8('用户名'), self.lbl_name)
		layout.addRow(QtCore.QString.fromUtf8('现金'), self.lbl_money)

		self.stock_list = GraphicsStockList()
		layout.addRow(self.stock_list)

		layout.addRow(QtCore.QString.fromUtf8('总资产'), self.lbl_wealth)
		self.setLayout(layout)


	def SetBasicInfo(self, name, money):
		self.lbl_name.setText(name)
		self.lbl_money.setText(str(money))
		self.money = money

	def UpdateStock(self, stock_ticker, stock_amount):
		self.stock_list.UpdateStock(stock_ticker, stock_amount)
		self.lbl_wealth.setText(str(self.money + self.stock_list.stock_value))

	def ClearStock(self):
		self.stock_list.Clear()

	def SetDate(self, date):
		from StockCore.Formatter import DateFormatter
		self.lbl_date.setText(DateFormatter.Format(date))
		self.stock_list.SetDate(date)


def test():
	'''
	Unit test code for GraphicsUserInfoPanel
	'''	
	app = QtGui.QApplication([])
	userinfo_panel = GraphicsUserInfoPanel()
	import datetime
	date = datetime.datetime(2011, 1, 6)
	userinfo_panel.SetDate(date)
	userinfo_panel.SetBasicInfo('qiuwch', 10000)
	userinfo_panel.UpdateStock('000001.SZ', 1000)
	userinfo_panel.show()
	app.exec_()


if __name__ == '__main__':
	test()