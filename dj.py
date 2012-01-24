#!/usr/bin/python
'''
Load Dow Jones Data
TODO: abstract data functions
'''

from DowJonesDataLoader import DowJonesDataLoader

if __name__ == '__main__':
    companys = DowJonesDataLoader.load()
    for c in companys.values():
        c.PrintInfo()


'''
Function to analysis dove jones market data
'''
# def main():
#     f = open('DJ30 1985 2003.txt')
# 
#     companys = {}
#     count = 0
#     line = f.readline()
# 
#     while line and line != '':
#         count = count + 1
#         [uid, date, openP, high, low, close, volume, adjclose, ticker] = line.split(';')
#         ticker = ticker.strip('\r\n"')
#         r = DayRecord(date, openP, high, low, close, volume, adjclose)
#         if not ticker in companys:
#             c = Company(ticker)
#             companys[ticker] = c
#         else:
#             c = companys[ticker]
#         c.Append(r)
#         line = f.readline()
#     print count
#     return companys
# 
# if __name__ == '__main__':
#     companys = main()
#     c = companys['ibm']
#     c.PrintInfo()
# 
