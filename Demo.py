#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Load all company infos from ShenZhen data.
'''

import pickle
import DataLoader.ShenzhenFieldLoader


def findMaxRemain(companys):
    findMax(companys, lambda(x): x.intAAll() - x.intAAvail())

def findMaxAAvail(companys):
    findMax(companys, lambda(x): x.intAAvail())

def findMaxAAll(companys):
    findMax(companys, lambda(x): x.intAAll())

def findMax(companys, func):
    max = 0
    maxI = 0
    for i in xrange(len(companys)):
        company = companys[i]
        val = func(company)
        if val > max:
            max = val
            maxI = i
    print max
    companys[maxI].printInfo()

if __name__ == '__main__':
    loader = DataLoader.ShenzhenFieldLoader.ShenzhenFieldLoader()
    companys = loader.Load()
    company = loader.LoadCompany('000001.SZ')
    price = [r.closePrice for r in company.records]

    from pylab import *
    n = len(price)
    plot(range(n), price)
    show()
    print dir(company.records[0])




