#!/usr/bin/python
# -*- coding: utf-8 -*-

from PyQt4 import QtGui
import sys
from YahooDataLoader import YahooDataLoader
from GraphicsCompanyView import GraphicsCompanyView

BIGNUM = 1000000

def loadCompanyData():
    from ShenzhenFieldLoader import ShenzhenFieldLoader
    loader = ShenzhenFieldLoader()
    companys = loader.loadFromPlainTxt()
    c = companys.values()[0]
    # c.PrintInfo()
    # YahooDataLoader.loadCompanyHistoryFromInternet(c, '20110101', '20120101')
    print c.ticker
    YahooDataLoader.loadCompanyHistoryFromLocalCache(c, 2011, 2012)
    # c.PrintInfo()
    return c

def main():
    # load data
    c = loadCompanyData()

    app = QtGui.QApplication(sys.argv)

    # set up scene container
    scene = QtGui.QGraphicsScene()

    # set up scene contents

    # set up dayRecordInfoPanel
    dayRecordInfoPanel = GraphcisRecordInfoPanel()
    dayRecordInfoPanel.setPos(400, 30)
    scene.addItem(dayRecordInfoPanel)

    maxPrice = 0
    minPrice = BIGNUM
    n = 0
    for record in c.records:
        n = n+1
        recordItem = GraphicsDayRecordItem.CreateFromRecord(record)
        print n
        recordItem.setPos(GraphicsDayRecordItem.paintWidth * n, 0)
        recordItem.infoPanel = dayRecordInfoPanel
        scene.addItem(recordItem)
        maxPrice = max(maxPrice, record.high)
        minPrice = min(minPrice, record.low)
        
    companyInfoItem = GraphicsCompanyInfoItem(c)
    companyInfoItem.setPos(0, 30)
    scene.addItem(companyInfoItem)

    # add axis to scene
    xWidth = GraphicsDayRecordItem.paintWidth*n
    xMarker = [i for i in range(0, xWidth, 100)]
    xMarker.append(xWidth)
    xAxis = GraphicsAxisItem(xMarker, xaxis=True, yaxis=False)
    minPrice = int(minPrice * 100)
    maxPrice = int(maxPrice * 100)
    yMarker = [i for i in range(min(minPrice,0), maxPrice, int(maxPrice-minPrice)/10)]
    yMarker.append(maxPrice)
    yAxis = GraphicsAxisItem(yMarker, yaxis=True, xaxis=False)
    scene.addItem(xAxis)
    scene.addItem(yAxis)

    # set up view widget
    w = QtGui.QGraphicsView()
    w.setScene(scene)
    w.resize(250, 150)
    w.move(300, 300)
    w.setWindowTitle('Sample')
    w.show()
    sys.exit(app.exec_())
    
if __name__ == '__main__':
    main()

