#!/usr/bin/python
from PyQt4 import QtGui, QtCore

class GraphicsCompanySelectionItem(QtGui.QWidget):
    def __init__(self, company, parent=None):
        QtGui.QWidget.__init__(self)

        if None != parent:
            self.parent = parent
        self.company = company
        vlayout = QtGui.QHBoxLayout(self)
        labelName = QtGui.QLabel(QtCore.QString.fromUtf8(company.abbr))
        removeButton = QtGui.QPushButton('X')
        vlayout.addWidget(labelName)
        vlayout.addWidget(removeButton)

        QtCore.QObject.connect(removeButton, QtCore.SIGNAL('clicked()'), self.RemoveFromSelection)

    def RemoveFromSelection(self):
        # print self.parent()
        # print self.parent().layout()
        # self.parent().layout().addWidget(QtGui.QButton('test'))
        if None != self.parent:
            self.parent.removeWidget(self)
            # self.parent.update()

class GraphicsCompanySelectionList(QtGui.QWidget):
    def __init__(self):
        QtGui.QWidget.__init__(self)
        # self.layout = QtGui.QFormLayout(self)
        self.layout = QtGui.QFormLayout()
        self.setLayout(self.layout)
        self.selectedTicker = []

    def Add(self, selectionItem):
        if selectionItem.company.ticker in self.selectedTicker:
            return
        else:
            self.layout.addRow(selectionItem)
            selectionItem.parent = self.layout
            self.selectedTicker.append(selectionItem.company.ticker)

def test():
    app = QtGui.QApplication([])

    w = GraphicsCompanySelectionList()
    item = GraphicsCompanySelectionItem(None)
    w.Add(item)
    w.show()
    
    app.exec_()

if __name__=='__main__':
    test()
