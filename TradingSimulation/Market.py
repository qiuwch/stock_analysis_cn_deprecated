class Market:
	def __init__(self):
		self.users = []
		self.price_sources = {}
		self.count = 0
		self.date = None

	def SetDate(self, date):
		self.date = date
		print 'Market date:', self.date

	def AddUser(self, user):
		self.users.append(user)
		user.market = self

	def UserAction(self):
		for user in self.users:
			user.Action()

	def AddPriceSource(self, price_source):
		'''Price source for each stock'''
		self.price_sources[price_source.ticker] = price_source

	def GetPrice(self, stockname):
		'''Return price of specific stock'''
		if self.date == None:
			print 'Market:Date is None.'
			return None
		# stock_prices = {'GOOG': 50 + self.count, 'APPL': 100 + self.count}
		price_source = self.price_sources.get(stockname)
		if price_source == None:
			print 'Market:Can not find this stockname.'
			return None

		# current return high price
		# print dir(price_source.GetPrice(self.date))
		if price_source.GetPrice(self.date) == None:
			print 'Market:No trading data for ', self.date
			return None
		else:
			return price_source.GetPrice(self.date).high
			# return price_source.GetPrice(self.date)

