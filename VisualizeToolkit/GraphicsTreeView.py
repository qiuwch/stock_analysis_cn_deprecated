#!/usr/bin/python
# -*- encoding: utf-8 -*-
from PyQt4 import QtGui, QtCore

app = QtGui.QApplication([])

tree_widget = QtGui.QTreeWidget()
tree_widget.show()
tree_widget.setColumnCount(1)
tree_widget.setHeaderLabel(QtCore.QString.fromUtf8('行业分类'))

n = 
item = QtGui.QTreeWidgetItem()
item.setText(0, 'test')
tree_widget.insertTopLevelItem(0, item)

new_item = QtGui.QTreeWidgetItem('second')
item.insertChild(0, new_item)

app.exec_()
