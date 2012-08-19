#!/usr/bin/python
from PyQt4 import QtGui, QtCore

class GraphicsAnimation(QtGui.QWidget):
	def __init__(self):
		# super(MainWindow, self).__init__(parent)
		QtGui.QWidget.__init__(self)

		# self.timer = QtCore.QTimer(self)
		# self.timer.timeout.connect(self.Tick)
		# fps = 30
		# self.timer.start(int(1000 / fps))

	# def Tick(self):
	#	print 'Ticking...'

class UIThread(QtCore.QThread):
	def __init__(self):
		QtCore.QThread.__init__(self)


class Animator(QtCore.QThread):
	def __init__(self):
		print 'Construct Animator'
		QtCore.QThread.__init__(self)
		self.timer = QtCore.QTimer(self)
		fps = 30
		self.timer.timeout.connect(self.Tick)
		self.timer.start(int(1000 / fps))
		self.count = 0

	def Tick(self):
		print 'Ticking', self.count
		self.count = self.count + 1
		self.win.setWindowTitle(str(self.count))
		
if __name__ == '__main__':
	import sys

	app = QtGui.QApplication(sys.argv)

	win = GraphicsAnimation()
	win.show()

	# uithread = UIThread()
	# uithread.run()

	print 'Construct animator'
	animator = Animator()
	animator.win = win

	app.exec_()
