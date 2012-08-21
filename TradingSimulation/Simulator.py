#!/usr/bin/python
from Config import *
from VisualizeToolkit.GraphicsUserInfoPanel import GraphicsUserInfoPanel
from PyQt4 import QtCore, QtGui

class Simulator:
	k_linebreak = '--------------------------------'
	def __init__(self, market):
		# stocksource 
		self.market = market
		self.date = None

		# Use QTimer to implement animation function
		# to get rid of time.sleep
		self.timer = QtCore.QTimer()
		self.timer.timeout.connect(self.Tick)
		

	def MainLoop(self):
		# ms_interval = 10
		ms_interval = 1
		self.timer.start(ms_interval)
		# Old implementation
		# for i in range(100):
		# 	self.Tick()
		# 	import time
		# 	time.sleep(1)

	def Initialize(self):
		self.SetupUI()
		for user in self.market.users:
			user.strategy.SetContext(self.market, user)

	def Tick(self):
		print Simulator.k_linebreak
		weekday = self.date.isoweekday()
		if weekday == 6 or weekday == 7:
			print 'Simulator:Skip weekends'
		else:
			# self.market.GenerateNewPrice()
			self.market.SetDate(self.date)
			self.market.UserAction()
			self.UpdateUI()

		import datetime
		delta = datetime.timedelta(1)
		self.date = self.date + delta

		if self.date > self.end_date:
			self.timer.stop()

	def SetupUI(self):
		user = self.market.users[0]
		self.userinfo_panel = GraphicsUserInfoPanel() 
		# if this is not a class member, will be gc at the end of this function
		self.userinfo_panel.SetBasicInfo(user.name, user.money)
		self.userinfo_panel.show()

	def UpdateUI(self):
		# self.userinfo_panel.ClearStock()
		self.userinfo_panel.SetDate(self.date)
		user = self.market.users[0]
		self.userinfo_panel.SetBasicInfo(user.name, user.money)
		for stock_ticker in user.stocks.keys():
			stock_amount = user.stocks[stock_ticker]
			self.userinfo_panel.UpdateStock(stock_ticker, stock_amount)

	def Simulate(self):
		if not self.start_date == None:
			self.date = self.start_date
			self.market.start_date = self.start_date
		else:
			print 'Simulator:Set start date first.'
			return

		self.Initialize()
		self.MainLoop()
		for user in self.market.users:
			user.PrintInfo()
			print 'End of simulation'

def test():
	'''
	Unit test for Simulator
	'''
	from Simulator import Simulator
	from Strategy import SimpleStrategy
	from Market import Market
	from User import User
	# from Gui import Gui
	from PriceSource import PriceSource
	import datetime
	from PyQt4 import QtGui
	app = QtGui.QApplication([])

	strategy = SimpleStrategy()

	name = 'Weichao Qiu'
	initial_money = 10000
	user = User(name, initial_money, strategy)

	# sz01 = PriceSource('000001.SZ')

	market = Market()
	# market.AddPriceSource(sz01)  # Done by ctor of Market class
	market.AddUser(user)

	simulator = Simulator(market)
	# simulator.gui = Gui()

	simulator.start_date = datetime.datetime(2011, 1, 10)
	simulator.end_date = datetime.datetime(2011, 3, 15)
	# simulator.end_date = simulator.start_date + datetime.timedelta(180)
	# simulate for 6 months
	# simulator.end_date = datetime.datetime.now()
	simulator.Simulate()  # Begin simulation

	print 'end of simulation'

	app.exec_()

if __name__ == '__main__':
	test()

