#!/usr/bin/python
# -*- coding: utf-8 -*-

from PyQt4 import QtGui, QtCore

# from entity import DayRecord

class GraphicsAxisItem(QtGui.QGraphicsItem):
    marginWidth = 30
    def __init__(self, marker=None, xaxis=True, yaxis=True):
        QtGui.QGraphicsItem.__init__(self)
        if None == marker:
            self.marker = [0]
        else:
            self.marker = marker
        self.xaxis = xaxis
        self.yaxis = yaxis
        self.maxVal = max(self.marker)
        self.minVal = min(self.marker)

    def SetXRange(self, start_date, end_date):
        pass

    def SetMarker(self, marker):
        self.marker = marker
        self.maxVal = max(marker)
        self.minVal = min(marker)
        self.update()

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
            # return QtCore.QRectF(-marginWidth, -self.minVal, marginWidth*2 + 1, -(self.maxVal+marginWidth))
            return QtCore.QRectF(-marginWidth, -(self.maxVal + marginWidth), marginWidth*2 + 1, self.maxVal - self.minVal + 2*marginWidth)
        else:
            return QtCore.QRectF(min(-marginWidth, self.minVal),\
                                 min(-marginWidth, self.minVal),\
                                 max(marginWidth*2+1, self.maxVal),\
                                 max(marginWidth*2+1, self.MaxVal))


class GraphicsCompanyInfoItem(QtGui.QGraphicsItem):
    textHeight = 20
    def __init__(self, c):
        QtGui.QGraphicsItem.__init__(self)
        self.c = c
        self.w = 300
        self.h = 60

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
        # print dir(self)
        return QtCore.QRectF(0, 0, self.w, self.h)


class GraphicsDayRecordItem(QtGui.QGraphicsItem):
    paintWidth = 10
    @classmethod
    def CreateFromRecord(cls, r):
        recordItem = GraphicsDayRecordItem(r.open, r.high, r.low, r.close, r.date)
        recordItem.record = r
        return recordItem

    def __init__(self, openPrice, highPrice, lowPrice, closePrice, date):
        QtGui.QGraphicsItem.__init__(self)

        self.setAcceptHoverEvents(True)
        self.openPrice = openPrice * 100
        self.highPrice = highPrice * 100
        self.lowPrice = lowPrice * 100
        self.closePrice = closePrice * 100
        self.date = date
        self.info_panel = None
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
        # print 'up:%s down:%s' % (up, down)

        h = up - down
        painter.setPen(penColor)
        painter.drawRect(0, down, width, h)
        # x, y, w, h
        centerPosX = width / 2 
        painter.drawLine(centerPosX, down, centerPosX, self.lowPrice)
        painter.drawLine(centerPosX, up, centerPosX, self.highPrice)
        # x1, y1, x2, y2


    def boundingRect(self):
        '''
        inhereted
        Return bouding rect of this control (absolute coordinate of rectangle)
        '''
        h = self.highPrice - self.lowPrice
        return QtCore.QRectF(0, -self.highPrice, self.paintWidth, h)

    def hoverEnterEvent(self, event):
        '''
        inhereted
        Handle hover event
        '''
        # print 'Hover the item'
        # print dir(event)
        # print dir(event.lastScenePos())
        mouse_pos = event.lastScenePos()
        if self.info_panel != None:
            self.info_panel.setPos(mouse_pos.x(), mouse_pos.y())
            self.info_panel.ShowInfo(self)

class GraphcisRecordInfoPanel(QtGui.QGraphicsItem):
    textHeight = 20
    def __init__(self):
        QtGui.QGraphicsItem.__init__(self)
        self.record = None
        self.h = 60
        self.w = 300

    def paint(self, painter, option, widget=None):
        if None == self.record:
            return
        import datetime
        textHeight = GraphicsCompanyInfoItem.textHeight
        fields = \
               [['日期', self.record.date.strftime('%Y-%m-%d')],
                ['开盘价', self.record.openPrice],
                ['收盘价', self.record.closePrice],
                ['今日最低', self.record.lowPrice],
                ['今日最高', self.record.highPrice]]
        # draw bouding box
        self.h = len(fields) * textHeight + 10
        painter.drawRect(0, 0, self.w, self.h)

        # draw record info
        offY = 0
        for f in fields:
            offY = offY + textHeight
            painter.drawText(QtCore.QPointF(5,offY), QtCore.QString.fromUtf8('%s:%s' % (f[0], f[1])))


    def ShowInfo(self, dayRecordItem):
        self.record = dayRecordItem.record
        self.update() # make ui to refresh

    def boundingRect(self):
        return QtCore.QRectF(0, 0, self.w, self.h)

