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
		price = self.market.GetPrice(stockname)
		print 'User:%s (%.2f) \t is trying to buy %s(%d) \t at price %.2f' % (self.name, self.money, stockname, volume, price)
		if volume * price > self.money:
			print 'Insufficient fund'
			return False
		else:
			self.money = self.money - volume * price
			if not self.stocks.has_key(stockname):
				self.stocks[stockname] = volume
			else:
				self.stocks[stockname] = self.stocks[stockname] + volume
			return True


	def Sell(self, stockname, volume):
		holdvolume = self.stocks.get(stockname)
		if not holdvolume or holdvolume < volume:
			print 'Insufficient stock to sell'
		else:
			price = self.market.GetPrice(stockname)
			self.money = self.money + volume * price
			print 'User:', self.name, ' is selling ', volume, 'at price ', price

	def Action(self):
		self.strategy.Action()

	def PrintInfo(self):
		stock_string = [self.STOCK_INFO % (stockname, self.stocks[stockname], self.market.GetPrice(stockname)) \
				for stockname in self.stocks.keys()]
		wealth = self.money
		for stockname in self.stocks.keys():
			wealth = wealth + self.stocks[stockname] * self.market.GetPrice(stockname)
		print self.USER_INFO % (self.name, self.money, ''.join(stock_string), wealth)

	