
from PyQt4 import QtGui

class GraphicsCompanyItem(QtGui.QWidget)
    def __init__(self):
        QtGui.QWidget.__init__(self)
        mainLayout = QtGui.QGridLayout(self)

        view = QtGui.QGraphicsView()
        scene = QtGui.QGraphicsScene()
        view.setScene(scene)
        
        mainLayout.addItem(view)
        
        
    
