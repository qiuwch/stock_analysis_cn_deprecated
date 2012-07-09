class Simulator:
	def __init__(self, market):
		# stocksource 
		self.market = market
		self.date = None

	def MainLoop(self):
		for i in range(100):
			self.Tick()

	def Initialize(self):
		for user in self.market.users:
			user.strategy.SetContext(self.market, user)

	def Tick(self):
		weekday = self.date.isoweekday()
		if weekday == 6 or weekday == 7:
			print 'Simulator:Skip weekends'
		else:
			# self.market.GenerateNewPrice()
			self.market.SetDate(self.date)
			self.market.UserAction()

		import datetime
		delta = datetime.timedelta(1)
		self.date = self.date + delta

	def Simulate(self):
		if not self.start_date == None:
			self.date = self.start_date
		else:
			print 'Simulator:Set start date first.'
			return

		self.Initialize()
		self.MainLoop()
		for user in self.market.users:
			user.PrintInfo()

