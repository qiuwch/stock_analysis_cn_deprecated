class SimpleStrategy:
	def __init__(self):
		pass

	def SetContext(self, market, user):
		self.market = market
		self.user = user

	def Action(self):
		user = self.user
		market = self.market
		volume = (user.money / 2) / market.GetPrice('GOOG')
		if volume > 0:
			self.user.Buy('GOOG', volume)
		volume = (user.money / 2) / market.GetPrice('APPL')
		if volume > 0:
			self.user.Buy('APPL', volume)
		# self.user.Sell('GOOG', 200)


