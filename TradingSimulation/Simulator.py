class Simulator:
	def __init__(self, market):
		# stocksource 
		self.market = market

	def MainLoop(self):
		for i in range(100):
			self.Tick()

	def Initialize(self):
		for user in self.market.users:
			user.strategy.SetContext(self.market, user)

	def Tick(self):
		self.market.GenerateNewPrice()
		self.market.UserAction()

	def Simulate(self):
		self.Initialize()
		self.MainLoop()
		for user in self.market.users:
			user.PrintInfo()

