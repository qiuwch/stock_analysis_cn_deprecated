#!/usr/bin/python
from PyQt4 import QtGui, QtCore

class MainWindow(QtGui.QMainWindow):
    def __init__(self, *args):
        QtGui.QMainWindow.__init__(self, *args)

        self.mainWidget = QtGui.QWidget(self)
        self.setCentralWidget(self.mainWidget)
        
        # build main container
        self.mainLayout = QtGui.QVBoxLayout(self.mainWidget)

        # build menu
        self.menu = QtGui.QWidget()
        self.buildMenu()
        print 'Build menu success.'

        # load data
        self.loadData()

        
        
    def buildMenu(self):
        menuLayout = QtGui.QHBoxLayout(self.menu)

        btn1 = QtGui.QPushButton('Menu btn 1')
        btn2 = QtGui.QPushButton('Menu btn 2')

        menuLayout.addWidget(btn1)
        menuLayout.addWidget(btn2)

        self.mainLayout.addWidget(self.menu)

    def loadData(self):
        pass

def main(argv):
    app = QtGui.QApplication(argv)
    win = MainWindow()
    win.show()

    app.exec_()

if __name__ == '__main__':
    import sys
    main(sys.argv)
        
        
    
