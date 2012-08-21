class User:
	"""docstring for User"""
	USER_INFO = '''
	name:      %s
	money:     %d
	stocks:    %s
	wealth:  %.2f
	'''

	STOCK_INFO = '''
	stock name: %s   volume: %d   current price: %f'''

	def __init__(self, name, money, strategy):
		self.name = name
		self.money = money
		self.strategy = strategy
		self.stocks = {}
		self.market = None

	def Buy(self, stockname, volume):
		self.market.Buy(self, stockname, volume)

	def Sell(self, stockname, volume):
		self.market.Sell(self, stockname, volume)

	def Action(self):
		self.strategy.Action()

	def PrintInfo(self):
		stock_string = [self.STOCK_INFO % (stockname, self.stocks[stockname], self.market.GetPrice(stockname)) \
				for stockname in self.stocks.keys()]
		wealth = self.money
		for stockname in self.stocks.keys():
			wealth = wealth + self.stocks[stockname] * self.market.GetPrice(stockname)
		print self.USER_INFO % (self.name, self.money, ''.join(stock_string), wealth)

	