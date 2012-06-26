#!/usr/bin/python
from PyQt4 import QtGui, QtCore
from DataSource import CompanyListSource
from GraphicsSelectionList import GraphicsCompanySelectionList, GraphicsCompanySelectionItem

class GraphicsCompanyListItem(QtGui.QListWidgetItem):
    def __init__(self, company):
        QtGui.QListWidgetItem.__init__(self)
        self.company = company
        self.setText(QtCore.QString.fromUtf8(company.fullName))

class GraphicsSearchBox(QtGui.QLineEdit):
    def __init__(self):
        QtGui.QLineEdit.__init__(self)
        QtCore.QObject.connect(self, QtCore.SIGNAL("textChanged(QString)"), self.Search)
        self.source = None
        self.queryHandler = []

    def Search(self, newStr):
        queryStr = newStr.toUtf8()
        if None == self.source:
            return

        queryResult = self.source.Query(queryStr)

        for f in self.queryHandler:
            apply(f, [queryResult])
        # print queryResult
        return queryResult


    def AddQueryHandler(self, handler):
        self.queryHandler.append(handler)

    def RemoveQueryHandler(self, handler):
        self.queryHandler.remove(handler)

    def SetSource(self, source):
        self.source = source

class GraphicsQueryResult(QtGui.QListWidget):
    def __init__(self):
        QtGui.QListWidget.__init__(self)
        QtCore.QObject.connect(self, QtCore.SIGNAL('itemSelectionChanged()'), self.updateSelection)
        self.selectionChangeHandler = []
        self.setSelectionMode(QtGui.QAbstractItemView.MultiSelection)

    # def selectionChanged(self, selected, deselected):
    # pass

    def AddSelectionChangeHandler(self, func):
        self.selectionChangeHandler.append(func)

    def RemoveSelectionChangeHandler(self, func):
        self.selectionChangeHandler.remove(func)

    def updateSelection(self):
        print 'emit selection change signal, count of handlers %d ' % len(self.selectionChangeHandler)
        for func in self.selectionChangeHandler:
            apply(func, [self.selectedItems()])
        
        
class GraphicsCompanyList(QtGui.QWidget):
    def __init__(self):
        QtGui.QWidget.__init__(self)

        self.mainLayout = QtGui.QVBoxLayout(self)
        self.searchBox = GraphicsSearchBox()

        # searchBox = QtGui.QLineEdit()
        self.mainLayout.addWidget(self.searchBox)

        self.queryResultWidget = GraphicsQueryResult()
        # QtCore.QObject.connect(self.queryResultWidget, QtCore.SIGNAL('itemSelectionChanged()'), self.updateSelection)
        
        self.mainLayout.addWidget(self.queryResultWidget)
        self.searchBox.AddQueryHandler(self.QueryResultHandler)

        self.selectedCompanyList = GraphicsCompanySelectionList()
        self.mainLayout.addWidget(self.selectedCompanyList)
        
        self.AddSelectionChangeHandler(self.SelectionChangedHandler)
        # self.searchBox.RemoveQueryHandler(self.Update)

    def SetSource(self, source):
        self.searchBox.SetSource(source)

    def SelectionChangedHandler(self, selectedWidgets):
        print 'Selection changed counts of selected companys %d' % len(selectedWidgets)
        for widget in selectedWidgets:
            self.selectedCompanyList.Add(GraphicsCompanySelectionItem(widget.company))
        # self.selectedCompanyListContainer.update()

    def AddSelectionChangeHandler(self, func):
        # self.selectionChangeHandler.append(func)
        self.queryResultWidget.AddSelectionChangeHandler(func)

    def RemoveSelectionChangeHandler(self, func):
        # self.selectionChangeHandler.remove(func)
        self.queryResultWidget.RemoveSelectionChangeHandler(func)
        
    def QueryResultHandler(self, queryResult):
        # print queryResult
        self.queryResultWidget.clear()
        print 'Number of returned query result %d' % len(queryResult)
        for c in queryResult:
            companyListItem = GraphicsCompanyListItem(c)
            self.queryResultWidget.addItem(companyListItem)



def test():
    import sys
    app = QtGui.QApplication(sys.argv)

    from ShenzhenFieldLoader import ShenzhenFieldLoader
    loader = ShenzhenFieldLoader()
    companys = loader.loadFromPlainTxt()

    companyList = GraphicsCompanyList()
    companyList.SetSource(CompanyListSource(companys.values()))
    companyList.show()

    app.exec_()

if __name__ == '__main__':
    test()

    
        
        
