#!/usr/bin/python
'''
MainWindow from stock price visualization.
'''
from PyQt4 import QtGui, QtCore
from QtGui.GraphicsCompanyView import GraphicsCompanyView
from QtGui.GraphicsCompanyList import GraphicsCompanyList, CompanyListSource

class MainWindow(QtGui.QMainWindow):
    def __init__(self, *args):
        QtGui.QMainWindow.__init__(self, *args)

        # internal data structure
        self.companys = None
        self.selectedCompany = None
        self.loadComapnyListData()
        
        self.mainWidget = QtGui.QWidget(self)
        self.setCentralWidget(self.mainWidget)
        
        # build main container
        self.mainLayout = QtGui.QVBoxLayout(self.mainWidget)


        # build company list
        self.companyList = GraphicsCompanyList()
        self.companyList.AddSelectionChangeHandler(self.SelectionChangedHandler)
        self.companyList.SetSource(CompanyListSource(self.companys.values()))

        # build company data view
        self.buildCompanyView()
        self.mainLayout.addWidget(self.companyView)
        print 'Build main data view success.'

        # build menu
        self.menu = QtGui.QWidget()
        self.buildMenu()
        self.mainLayout.addWidget(self.menu)
        print 'Build menu success.'

    def show(self):
        QtGui.QMainWindow.show(self)
        if self.companyList != None:
            self.companyList.show()

    def buildCompanyView(self):
        self.companyView = GraphicsCompanyView()
        
    def buildMenu(self):
        menuLayout = QtGui.QHBoxLayout(self.menu)

        btn1 = QtGui.QPushButton('Zoom in')
        btn2 = QtGui.QPushButton('Zoom out')
        QtCore.QObject.connect(btn1, QtCore.SIGNAL('clicked()'), self.companyView.ZoomIn)
        QtCore.QObject.connect(btn2, QtCore.SIGNAL('clicked()'), self.companyView.ZoomOut)

        menuLayout.addWidget(btn1)
        menuLayout.addWidget(btn2)

    def loadComapnyListData(self):
        from DataLoader.ShenzhenFieldLoader import ShenzhenFieldLoader
        loader = ShenzhenFieldLoader()
        self.companys = loader.loadFromPlainTxt()

    def SelectionChangedHandler(self, selectedWidgets):
        self.selectedCompany = []
        for widget in selectedWidgets:
            c = widget.company
            self.selectedCompany.append(c)
            if len(c.records) == 0:
                from YahooDataLoader import YahooDataLoader
                YahooDataLoader.loadCompanyHistoryFromLocalCache(c, 2011, 2012)
        self.companyView.SetSource(self.selectedCompany)
        
    

def main(argv):
    app = QtGui.QApplication(argv)

    # main window
    win = MainWindow()
    win.show()

    app.exec_()

if __name__ == '__main__':
    import sys
    main(sys.argv)
        
        
    
