#!/usr/bin/python
from Simulator import Simulator
from Strategy import SimpleStrategy
from Market import Market
from User import User

strategy = SimpleStrategy()

name = 'qiuwch'
initial_money = 10000
user = User(name, initial_money, strategy)

market = Market()
market.AddUser(user)

simulator = Simulator(market)
simulator.Simulate()  # Begin simulation