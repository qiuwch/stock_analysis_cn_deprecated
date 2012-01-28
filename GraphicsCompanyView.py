#!/usr/bin/python
from PyQt4 import QtGui

from GraphicsWidget import GraphicsAxisItem, GraphicsDayRecordItem, GraphicsCompanyInfoItem, GraphcisRecordInfoPanel

BIGNUM = 1000000

class GraphicsCompanyTimeSeries(QtGui.QGraphicsItemGroup):
    def __init__(self, c, recordInfoPanel=None):
        QtGui.QGraphicsItemGroup.__init__(self)

        self.company = c
        self.setHandlesChildEvents(False)
        # self.setAcceptHoverEvents(True)
        if len(c.records) == 0:
            print 'Warning: No records for %s:%s' % (c.ticker, c.fullName)
        else:
            print 'Records of %s:%s is %d' % (c.ticker, c.fullName, len(c.records))
        n = 0
        for record in c.records:
            n = n+1
            recordItem = GraphicsDayRecordItem.CreateFromRecord(record)
            recordItem.setPos(GraphicsDayRecordItem.paintWidth * n, 0)
            if recordInfoPanel != None:
                recordItem.infoPanel = recordInfoPanel
            self.addToGroup(recordItem)

    def paint(self, painter, option, widget=None):
        QtGui.QGraphicsItemGroup.paint(self, painter, option, widget)
        x1 = GraphicsDayRecordItem.paintWidth / 2
        r = self.company.records[0]
        val1 = - (r.openPrice + r.closePrice) / 2 * 100
        for r in self.company.records:
            val2 = - (r.openPrice + r.closePrice) / 2 * 100
            x2 = x1 + GraphicsDayRecordItem.paintWidth
            # print 'point (%d, %d, %d, %d)' % (x1, val1, x2, val2)
            painter.drawLine(x1, val1, x2, val2)
            val1 = val2
            x1 = x2
        


class GraphicsCompanyView(QtGui.QWidget):
    def __init__(self):
        # internal data structure
        self.companyInfos = []
        self.yAxisMaxPrice = 0
        self.yAxisMinPrice = BIGNUM
        self.xAxisN = 0
        
        QtGui.QWidget.__init__(self)
        # build main layout
        mainLayout = QtGui.QGridLayout(self)

        # build main view of graph
        self.view = QtGui.QGraphicsView()
        self.scene = QtGui.QGraphicsScene()
        self.view.setScene(self.scene)
        mainLayout.addWidget(self.view)

        # build axis of company view
        self.xAxis = None
        self.yAxis = None
        self.buildAxis()

        # build record info panel
        self.dayRecordInfoPanel = None
        self.buildRecordInfoPanel()

    def buildAxis(self):
        # add axis to scene
        self.xAxis = GraphicsAxisItem(xaxis=True, yaxis=False)
        self.yAxis = GraphicsAxisItem(yaxis=True, xaxis=False)
        
        self.scene.addItem(self.xAxis)
        self.scene.addItem(self.yAxis)

    def updateAxis(self):
        # update axis

        xWidth = GraphicsDayRecordItem.paintWidth * self.xAxisN
        xMarker = [i for i in range(0, xWidth, 100)]
        xMarker.append(xWidth)
        self.xAxis.SetMarker(xMarker)

        yAxisMax = int(self.yAxisMaxPrice * 100)
        yAxisMin = int(self.yAxisMinPrice * 100)

        print 'yAxisMin:%d  yAxisMax:%d' % (yAxisMin, yAxisMax)
        
        # yMarker = [i for i in range(min(yAxisMin, 0), yAxisMax, int(yAxisMax-yAxisMin)/10)]
        yMarker = [i for i in range(min(yAxisMin, 0), yAxisMax, 20)]
        yMarker.append(yAxisMax)        
        self.yAxis.SetMarker(yMarker)

        # print xMarker
        # print yMarker

    def Update(self):
        self.updateAxis()

        for companyInfo in self.companyInfos:
            [c, maxPrice, minPrice] = companyInfo
            self.buildCompanyInfoItem(c)
            companyTimeSeries = GraphicsCompanyTimeSeries(c, self.dayRecordInfoPanel)
            self.scene.addItem(companyTimeSeries)
            # c.PrintInfo()
    
    def AddCompany(self, c):
        companyMaxPrice = 0
        companyMinPrice = BIGNUM
        for record in c.records:
            companyMaxPrice = max(companyMaxPrice, record.highPrice)
            companyMinPrice = min(companyMinPrice, record.lowPrice)
        self.companyInfos.append([c, companyMaxPrice, companyMinPrice])
        # print self.companyInfos

        # update yAxisValue
        self.yAxisMaxPrice = 0
        self.yAxisMinPrice = BIGNUM
        
        for companyInfo in self.companyInfos:
            [c, maxPrice, minPrice] = companyInfo
            self.yAxisMaxPrice = max(maxPrice, self.yAxisMaxPrice)
            self.yAxisMinPrice = min(minPrice, self.yAxisMinPrice)

        self.xAxisN = len(c.records)

    def buildCompanyInfoItem(self, c):
        companyInfoItem = GraphicsCompanyInfoItem(c)
        companyInfoItem.setPos(0, 30)
        self.scene.addItem(companyInfoItem)


    def buildRecordInfoPanel(self):
        # set up dayRecordInfoPanel
        self.dayRecordInfoPanel = GraphcisRecordInfoPanel()
        self.dayRecordInfoPanel.setPos(400, 30)
        self.scene.addItem(self.dayRecordInfoPanel)
        

        
def test():
    from ShenzhenFieldLoader import ShenzhenFieldLoader
    from YahooDataLoader import YahooDataLoader
    loader = ShenzhenFieldLoader()
    companys = loader.loadFromPlainTxt()

    showCompanys = []
    for i in range(0, 10):
        showCompanys.append(companys.values()[i])

    for c in showCompanys:
        YahooDataLoader.loadCompanyHistoryFromLocalCache(c, 2011, 2012)
    # c1 = companys.values()[0]
    # YahooDataLoader.loadCompanyHistoryFromLocalCache(c1, 2011, 2012)
    # c2 = companys.values()[1]
    # YahooDataLoader.loadCompanyHistoryFromLocalCache(c2, 2011, 2012)
    
    import sys
    app = QtGui.QApplication(sys.argv)

    w = GraphicsCompanyView()
    for c in showCompanys:
        w.AddCompany(c)
    w.Update()
    w.setWindowTitle('Sample')
    w.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    test()
