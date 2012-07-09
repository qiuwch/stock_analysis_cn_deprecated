class Market:
	def __init__(self):
		self.users = []
		self.price_sources = {}
		self.count = 0
		self.date = None

	def SetDate(self, date):
		self.date = date
		print 'Market date:', self.date

	def UserAction(self):
		for user in self.users:
			user.Action()

	def AddUser(self, user):
		self.users.append(user)
		user.market = self

	def AddPriceSource(self, price_source):
		self.price_sources[price_source.ticker] = price_source

	def GetPrice(self, stockname):
		if self.date == None:
			print 'Market:Date is None.'
			return None
		# stock_prices = {'GOOG': 50 + self.count, 'APPL': 100 + self.count}
		price_source = self.price_sources.get(stockname)
		if price_source == None:
			print 'Market:Can not find this stockname.'
			return None

		return price_source.GetPrice(self.date)

