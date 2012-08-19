#!/usr/bin/python
from Simulator import Simulator
from Strategy import SimpleStrategy
from Market import Market
from User import User
from Gui import Gui
from PriceSource import PriceSource
import datetime

strategy = SimpleStrategy()

name = 'Weichao Qiu'
initial_money = 10000
user = User(name, initial_money, strategy)

sz01 = PriceSource('000001.SZ')

market = Market()
market.AddPriceSource(sz01)
market.AddUser(user)

simulator = Simulator(market)
# simulator.gui = Gui()

simulator.start_date = datetime.datetime(2011, 1, 10)
simulator.Simulate()  # Begin simulation
