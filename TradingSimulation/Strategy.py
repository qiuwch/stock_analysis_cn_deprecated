import math

class GreedyStrategy:
	def __init__(self):
		pass

	def SetContext(self, market, user):
		self.market = market
		self.user = user

	def Action(self):
		user = self.user
		market = self.market

		stocknames = market.price_sources.keys()

		print stocknames

		scores = [self.StockScore(stock_name) for stock_name in stocknames]
		

	def Choose(self):

		pass

	def StockScore(self, stockname):
		return 0

class SimpleStrategy:
	def __init__(self):
		pass

	def SetContext(self, market, user):
		# all public information of markdet and user
		# should be observable to trading strategy

		# history data can be available, but future data not available
		self.market = market
		self.user = user

	def Action(self):
		user = self.user
		market = self.market

		stockname = '000001.SZ'
		# print market.GetPrice(stockname)
		stockprice = market.GetPrice(stockname)
		prices = market.GetHistoryPrice(stockname)

		# Use all the money to buy
		if stockprice != None:
			volume = math.floor(user.money / (stockprice * 100)) * 100
			if volume != 0: 
				self.user.Buy(stockname, volume)
		else:
			return

		# self.user.Sell(stockname, volume)
		

		'''
		volume = (user.money / 2) / market.GetPrice('GOOG')
		if volume > 0:
			self.user.Buy('GOOG', volume)
		volume = (user.money / 2) / market.GetPrice('APPL')
		if volume > 0:
			self.user.Buy('APPL', volume)
		'''
		# self.user.Sell('GOOG', 200)


