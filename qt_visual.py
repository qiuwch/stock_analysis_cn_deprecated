#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
from PyQt4 import QtGui, QtCore
from YahooDataLoader import YahooDataLoader
# from entity import DayRecord

BIGNUM = 1000000

class GraphicsAxisItem(QtGui.QGraphicsItem):
    marginWidth = 30
    def __init__(self, marker, xaxis=True, yaxis=True):
        QtGui.QGraphicsItem.__init__(self)
        self.marker = marker
        self.xaxis = xaxis
        self.yaxis = yaxis
        self.maxVal = max(marker)
        self.minVal = min(marker)

    def paint(self, painter, option, widget=None):
        # m = QtGui.QMatrix()
        # m.scale(1, -1)
        # painter.setMatrix(m)

        if self.xaxis:
            painter.drawLine(self.minVal, 0, self.maxVal, 0)
            for x in self.marker:
                painter.drawLine(x, -3, x, 3)
                painter.drawText(QtCore.QPointF(x-10, 20), QtCore.QString.fromUtf8(str(x)))
        if self.yaxis:
            painter.drawLine(0, -self.minVal, 0, -self.maxVal)
            for y in self.marker:
                painter.drawLine(-3, -y, 3, -y)
                painter.drawText(QtCore.QPointF(-GraphicsAxisItem.marginWidth, -y), QtCore.QString.fromUtf8(str(y)))

    def boundingRect(self):
        marginWidth = GraphicsAxisItem.marginWidth
        # QRectF(x, y, w, h)  
        if self.xaxis:
            return QtCore.QRectF(self.minVal-GraphicsAxisItem.marginWidth, -marginWidth, self.maxVal+marginWidth, marginWidth*2 + 1)
        elif self.yaxis:
            return QtCore.QRectF(-marginWidth, -self.minVal, marginWidth*2 + 1, -(self.maxVal+marginWidth))
        else:
            return QtCore.QRectF(min(-marginWidth, self.minVal),\
                                 min(-marginWidth, self.minVal),\
                                 max(marginWidth*2+1, self.maxVal),\
                                 max(marginWidth*2+1, self.MaxVal))

class GraphicsCompanyInfoItem(QtGui.QGraphicsItem):
    textHeight = 20
    def __init__(self, c):
        QtGui.QGraphicsItem.__init__(self)
        self.h = 60
        self.w = 300
        self.c = c

    def paint(self, painter, option, widget=None):
        fields = \
               [['公司名', self.c.fullName],
                ['公司代码', self.c.ticker],
                ['所属行业', self.c.area]]

        # draw bouding box
        self.h = len(fields) * GraphicsCompanyInfoItem.textHeight + 10
        painter.drawRect(0, 0, self.w, self.h)

        # draw company info
        offY = 0
        for f in fields:
            offY = offY + GraphicsCompanyInfoItem.textHeight
            painter.drawText(QtCore.QPointF(5,offY), QtCore.QString.fromUtf8('%s:%s' % (f[0], f[1])))


    def boundingRect(self):
        return QtCore.QRectF(0, 0, self.w, self.h)

class GraphicsDayRecordItem(QtGui.QGraphicsItem):
    paintWidth = 5
    @classmethod
    def CreateFromRecord(cls, r):
        recordItem = GraphicsDayRecordItem(r.open, r.high, r.low, r.close)
        return recordItem
        
    def __init__(self, openPrice, highPrice, lowPrice, closePrice):
        QtGui.QGraphicsItem.__init__(self)
        self.openPrice = openPrice * 100
        self.highPrice = highPrice * 100
        self.lowPrice = lowPrice * 100
        self.closePrice = closePrice * 100
        # self.paintWidth = 10

    def paint(self, painter, option, widget=None):
        painter.scale(1, -1)
        
        # painter.drawRect(0, self.lowPrice, 10, self.highPrice - self.lowPrice)
        width = GraphicsDayRecordItem.paintWidth
        if (self.closePrice > self.openPrice):
            # raise today, red
            penColor = QtGui.QColor(255, 0, 0)
            up = self.closePrice
            down = self.openPrice
        elif (self.closePrice < self.openPrice):
            penColor = QtGui.QColor(0, 255, 0)
            up = self.openPrice
            down = self.closePrice
        else:
            penColor = QtGui.QColor(0, 0, 0)
            up = down = self.openPrice
        print 'up:%s down:%s' % (up, down)
            
        h = up - down
        painter.setPen(penColor)
        painter.drawRect(0, down, width, h)
        # x, y, w, h
        centerPosX = width / 2 
        painter.drawLine(centerPosX, down, centerPosX, self.lowPrice)
        painter.drawLine(centerPosX, up, centerPosX, self.highPrice)
        # x1, y1, x2, y2


    def boundingRect(self):
        h = self.highPrice - self.lowPrice
        return QtCore.QRectF(0, -self.highPrice, self.paintWidth, h)

def loadCompanyData():
    from ShenzhenFieldLoader import ShenzhenFieldLoader
    loader = ShenzhenFieldLoader()
    companys = loader.loadFromPlainTxt()
    c = companys.values()[0]
    # c.PrintInfo()
    YahooDataLoader.loadCompanyHistory(c, '20110101', '20120101')
    # c.PrintInfo()
    return c

def main():
    app = QtGui.QApplication(sys.argv)

    # set up scene container
    scene = QtGui.QGraphicsScene()

    # set up scene contents
    # rect = QtGui.QGraphicsRectItem(10, 10, 30, 30, scene=scene)
    # rect = QtGui.QGraphicsRectItem(10, 10, 30, 30)
    # recordItem = GraphicsDayRecordItem(10, 20, 5, 15)
    # scene.addItem(rect)
    # scene.addItem(recordItem)

    c = loadCompanyData()
    n = 0

    maxPrice = 0
    minPrice = BIGNUM
    for record in c.records:
        n = n+1
        recordItem = GraphicsDayRecordItem.CreateFromRecord(record)
        print n
        recordItem.setPos(GraphicsDayRecordItem.paintWidth * n, 0)
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

