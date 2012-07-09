class SimpleStrategy:
	def __init__(self):
		pass

	def SetContext(self, market, user):
		self.market = market
		self.user = user

	def Action(self):
		user = self.user
		market = self.market

		stockname = '000001.SZ'
		volume = user.money / market.GetPrice(stockname)
		self.user.Buy(stockname, volume)

		'''
		volume = (user.money / 2) / market.GetPrice('GOOG')
		if volume > 0:
			self.user.Buy('GOOG', volume)
		volume = (user.money / 2) / market.GetPrice('APPL')
		if volume > 0:
			self.user.Buy('APPL', volume)
		'''
		# self.user.Sell('GOOG', 200)


