from Config import *
from StockCore.StockDB import ShenzhenStockDB
from PriceSource import PriceSource

class Market:
	def __init__(self):
		self.users = []
		self.price_sources = {}
		self.count = 0
		self.date = None
		self.trading_fee = 0.1

		# Add all shenzhen stock to market price source
		db = ShenzhenStockDB()
		company_list = db.GetCompanyList()
		for ticker in company_list.keys():
			print 'Loading:', ticker
			sz = PriceSource(ticker)
			self.AddPriceSource(sz)

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


	def Buy(self, user, stockname, volume):
		trading_fee = 0.8 / 1000

		price = self.GetPrice(stockname)
		print 'User:%s (%.2f) \t is trying to buy %s(%d) \t at price %.2f' % (user.name, user.money, stockname, volume, price)
		cost = volume * price * (1 + trading_fee)
		if cost > user.money:
			print 'Insufficient fund'
			return False
		else:
			user.money = user.money - cost
			if not user.stocks.has_key(stockname):
				user.stocks[stockname] = volume
			else:
				user.stocks[stockname] = user.stocks[stockname] + volume
			return True

	def Sell(self, user, stockname, volume):
		trading_fee = 0.8 / 1000
		tax_fee = 1 / 1000

		holdvolume = user.stocks.get(stockname)
		if not holdvolume or holdvolume < volume:
			print 'Insufficient stock to sell'
			return False
		else:
			price = self.GetPrice(stockname)
			cash = volume * price * (1 - trading_fee - tax_fee)
			user.stocks[stockname] = user.stocks[stockname] - volume
			user.money = user.money + cash
			print 'User:', user.name, ' is selling ', volume, 'at price ', price
			return True


	def GetPrice(self, stockname):
		price_source = self.GetPriceSource(stockname)
		if price_source == None:
			return None

		# current return high price
		# print dir(price_source.GetPrice(self.date))
		if price_source.GetPrice(self.date) == None:
			print 'Market:No trading data for ', self.date
			return None
		else:
			return price_source.GetPrice(self.date)
			# return price_source.GetPrice(self.date)

	def GetHistoryPrice(self, stockname):
		price_source = self.GetPriceSource(stockname)
		if price_source == None:
			return None

		return price_source.GetHistoryPrice(self.start_date, self.date)

	# private method
	def GetPriceSource(self, stockname):
		'''Return price of specific stock'''
		if self.date == None:
			print 'Market:Date is None.'
			return None
		# stock_prices = {'GOOG': 50 + self.count, 'APPL': 100 + self.count}
		price_source = self.price_sources.get(stockname)
		if price_source == None:
			print 'Market:Can not find this stockname.'
			return None
		return price_source
