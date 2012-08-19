#!/usr/bin/python
from Config import *
from PyQt4 import QtGui
from GraphicsWidget import GraphicsAxisItem, GraphicsDayRecordItem, GraphicsCompanyInfoItem, GraphcisRecordInfoPanel

BIGNUM = 1000000

class GraphicsCompanyTimeSeries(QtGui.QGraphicsItemGroup):
    ## Property methods
    def SetLineColor(self, color):
        '''
        Set stock history value line color
        For better visualization to multiple stocks simultaneously
        '''
        self.lineColor = color

    ## public methods
    def __init__(self, c, recordInfoPanel=None):
        QtGui.QGraphicsItemGroup.__init__(self)

        # set up internal data structure
        self.lineColor = None
        self.company = c
        self.start_date = None
        self.end_date = None

        self.dayrecord_infopanel = GraphcisRecordInfoPanel()
        # self.dayrecord_infopanel.setPos(400, 30)
        # self.scene.addItem(self.dayrecord_infopanel)
        self.addToGroup(self.dayrecord_infopanel)
        
        self.setHandlesChildEvents(False) # allow children to handle hover event
        # self.setAcceptHoverEvents(True)

        if len(c.records) == 0:
            print 'Warning: No records for %s:%s' % (c.ticker, c.fullName)
        else:
            print 'Records of %s:%s is %d' % (c.ticker, c.fullName, len(c.records))

    def SetKVisible(self, visible):
        pass

    def SetXRange(self, start_date, end_date):
        self.start_date = start_date
        self.end_date = end_date
        self.Update()

    ## Private methods
    def Update(self):
        if self.start_date == None or self.end_date == None:
            return

        n = 0
        for record in self.company.records:
            if record.date < self.start_date or record.date > self.end_date:
                continue
            n = n+1
            record_item = GraphicsDayRecordItem.CreateFromRecord(record)
            record_item.setPos(GraphicsDayRecordItem.paintWidth * n, 0)
            if self.dayrecord_infopanel != None:
                record_item.info_panel = self.dayrecord_infopanel
            self.addToGroup(record_item)
        
    def paint(self, painter, option, widget=None):
        QtGui.QGraphicsItemGroup.paint(self, painter, option, widget)
        if self.company == None or len(self.company.records) == 0:
            return
        x1 = GraphicsDayRecordItem.paintWidth / 2
        r = self.company.records[0]
        val1 = - (r.openPrice + r.closePrice) / 2 * 100
        for r in self.company.records:
            val2 = - (r.openPrice + r.closePrice) / 2 * 100
            x2 = x1 + GraphicsDayRecordItem.paintWidth
            # print 'point (%d, %d, %d, %d)' % (x1, val1, x2, val2)
            # painter.drawLine(x1, val1, x2, val2)
            val1 = val2
            x1 = x2

class GraphicsCompanyView(QtGui.QWidget):
    '''
    CompanyView control used to show trading history in static or dynamic form
    '''
    ## Property methods
    def SetXRange(self, start_date, end_date):
        '''
        Only show data within this range
        '''
        print 'Set start date to:', start_date
        print 'Set end date to:', end_date
        self.start_date = start_date
        self.end_date = end_date
        self.x_axis.SetXRange(start_date, end_date)

        self.Update()

    def SetYRange(self):
        '''
        Not important yet.
        '''
        pass
    
    def SetSource(self, companyList):
        self.companyInfos = []
        for c in companyList:
            self.appendCompany(c)
        self.Update()

    def AddCompany(self, c):
        self.appendCompany(c)
        self.Update()

    ## private methods
    def __init__(self):
        # internal data structure
        self.companyInfos = []
        self.yAxisMaxPrice = 0
        self.yAxisMinPrice = BIGNUM
        self.xAxisN = 0
        self.start_date = None
        self.end_date = None
        
        QtGui.QWidget.__init__(self)
        # build main layout
        mainLayout = QtGui.QGridLayout(self)

        # build main view of graph
        self.view = QtGui.QGraphicsView()
        self.scene = QtGui.QGraphicsScene()
        self.view.setScene(self.scene)
        mainLayout.addWidget(self.view)

        # build axis of company view
        self.x_axis = None
        self.y_axis = None
        # self.buildAxis()

        # build record info panel
        self.dayRecordInfoPanel = None
        # self.buildRecordInfoPanel()

    def wheelEvent(self, event):
        '''
        Inhereted
        Support mouse wheel event to zoom in/out
        '''
        QtGui.QWidget.wheelEvent(self, event)
        # print event.delta()

    def buildAxis(self):
        '''
        Add axis to scene
        Use date string to index history data
        '''
        self.x_axis = GraphicsAxisItem(xaxis=True, yaxis=False)
        self.y_axis = GraphicsAxisItem(yaxis=True, xaxis=False)
        
        self.scene.addItem(self.x_axis)
        self.scene.addItem(self.y_axis)

    def updateAxis(self):
        # update yAxisValue
        self.yAxisMaxPrice = 0
        self.yAxisMinPrice = BIGNUM
        
        for companyInfo in self.companyInfos:
            [c, maxPrice, minPrice] = companyInfo
            self.yAxisMaxPrice = max(maxPrice, self.yAxisMaxPrice)
            self.yAxisMinPrice = min(minPrice, self.yAxisMinPrice)
        self.xAxisN = len(c.records)

        xWidth = GraphicsDayRecordItem.paintWidth * self.xAxisN
        xMarker = [i for i in range(0, xWidth, 100)]
        xMarker.append(xWidth)
        self.x_axis.SetMarker(xMarker)

        yAxisMax = int(self.yAxisMaxPrice * 100)
        yAxisMin = int(self.yAxisMinPrice * 100)

        print 'yAxisMin:%d  yAxisMax:%d' % (yAxisMin, yAxisMax)
        
        # yMarker = [i for i in range(min(yAxisMin, 0), yAxisMax, int(yAxisMax-yAxisMin)/10)]
        yMarker = [i for i in range(min(yAxisMin, 0), yAxisMax, 20)]
        yMarker.append(yAxisMax)        
        self.y_axis.SetMarker(yMarker)


    def appendCompany(self, c):
        companyMaxPrice = 0
        companyMinPrice = BIGNUM
        for record in c.records:
            companyMaxPrice = max(companyMaxPrice, record.highPrice)
            companyMinPrice = min(companyMinPrice, record.lowPrice)
        self.companyInfos.append([c, companyMaxPrice, companyMinPrice])

    def BuildCompanyInfoItem(self, c):
        companyInfoItem = GraphicsCompanyInfoItem(c)
        companyInfoItem.setPos(0, 30)
        self.scene.addItem(companyInfoItem)

    def Update(self):
        '''
        Refresh the GraphicsCompanyView control
        '''
        self.scene.clear()
        
        self.buildAxis()
        self.updateAxis()
        
        for companyInfo in self.companyInfos:
            [c, maxPrice, minPrice] = companyInfo
            self.BuildCompanyInfoItem(c)
            companyTimeSeries = GraphicsCompanyTimeSeries(c, self.dayRecordInfoPanel)
            companyTimeSeries.SetXRange(self.start_date, self.end_date)
            self.scene.addItem(companyTimeSeries)
            # c.PrintInfo()

    ## public methods
    def ZoomIn(self):
        '''
        Zoom in to see more details
        '''
        self.view.scale(1.1, 1.1)
        print 'Zoom in'

    def ZoomOut(self):
        print 'Zoom out'
        self.view.scale(0.9, 0.9)



        
def test():
    '''
    Unit test code for testing GraphicsCompanyView Control
    '''
    ## Old protocol
    # from ShenzhenFieldLoader import ShenzhenFieldLoader
    # from YahooDataLoader import YahooDataLoader
    # loader = ShenzhenFieldLoader()
    # companys = loader.loadFromPlainTxt()
    
    ## New protocol
    
    from StockCore.StockDB import ShenzhenStockDB
    db = ShenzhenStockDB()
    c = db.GetStock('000001.SZ')

    ## Test add multiple companys
    # showCompanys = []
    # for i in range(0, 10):
    #     showCompanys.append(companys.values()[i])
    # for c in showCompanys:
    #     YahooDataLoader.loadCompanyHistoryFromLocalCache(c, 2011, 2012)

    import sys
    app = QtGui.QApplication(sys.argv)

    w = GraphicsCompanyView()
    w.AddCompany(c)
    # w.SetXRange()    
    w.setWindowTitle('Sample')
    w.show()

    from PyQt4 import QtCore
    class Animator(QtCore.QThread):
        def __init__(self):
            print 'Construct Animator'
            QtCore.QThread.__init__(self)
            self.timer = QtCore.QTimer(self)
            # fps = 30
            interval = 1
            self.timer.timeout.connect(self.Tick)
            self.timer.start(int(1000 * interval))
            self.count = 0

        def Tick(self):
            print 'Ticking', self.count
            self.count = self.count + 1
            # self.win.setWindowTitle(str(self.count))
            delta = datetime.timedelta(1)
            end_date = self.win.end_date + delta
            self.win.SetXRange(self.win.start_date, end_date)

    import datetime
    from StockCore.Formatter import DateFormatter
    start_date = c.records[0].date
    end_date = start_date
    w.SetXRange(start_date, end_date)

    animator = Animator()
    animator.win = w
    sys.exit(app.exec_())

    # run animation to show the progress of market trade


if __name__ == '__main__':
    test()
