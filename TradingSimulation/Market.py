class Market:
	def __init__(self):
		self.users = []
		self.count = 0

	def GenerateNewPrice(self):  # Method for generating market price
		self.count = self.count + 1
		pass

	def UserAction(self):
		for user in self.users:
			user.Action()

	def AddUser(self, user):
		self.users.append(user)
		user.market = self

	def GetPrice(self, stockname):
		stock_prices = {'GOOG': 50 + self.count, 'APPL': 100 + self.count}
		return stock_prices[stockname]

