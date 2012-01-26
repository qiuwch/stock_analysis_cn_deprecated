#!/usr/bin/python
import sys
from PyQt4 import QtGui, QtCore

class MainWindow(QtGui.QMainWindow):
    def __init__(self, *args):
        apply(QtGui.QMainWindow.__init__, (self, ) + args)
        self.mainWidget = QtGui.QWidget(self)

        self.vlayout = QtGui.QVBoxLayout(self.mainWidget)

        self.frame = QtGui.QWidget()
        self.hlayout = QtGui.QHBoxLayout(self.frame)

        # self.vlayout.addWidget(self.hlayout)
        btn1 = QtGui.QPushButton('Button 1')
        btn2 = QtGui.QPushButton('Button 2')
        self.hlayout.addWidget(btn1)
        self.hlayout.addWidget(btn2)

        self.lsv = QtGui.QListWidget(self.mainWidget)
        # self.lsv.addColumn('First column')
        self.lsv.setSelectionMode(QtGui.QAbstractItemView.MultiSelection)
        self.lsv.addItem(QtGui.QListWidgetItem('One'))
        self.lsv.addItem(QtGui.QListWidgetItem('Two'))
        self.lsv.addItem(QtGui.QListWidgetItem('Three'))

        self.bn = QtGui.QPushButton('Push me', self.mainWidget)

        self.vlayout.addWidget(self.lsv)
        self.vlayout.addWidget(self.bn)
        self.vlayout.addWidget(self.frame)

        QtCore.QObject.connect(self.bn, QtCore.SIGNAL('clicked()'), self.lsv, QtCore.SLOT('clear()'))
        # QtCore.QObject.connect(self.bn, 'clicked()', self.lsv, 'invertSelection()')
        self.setCentralWidget(self.mainWidget)

def main(args):
    app = QtGui.QApplication(args)
    win = MainWindow()
    win.show()

    app.connect(app, QtCore.SIGNAL('lastWindowClosed()'),
                app, QtCore.SLOT('quit()'))
    app.exec_()

if __name__ == '__main__':
    main(sys.argv)

    
                            
        
