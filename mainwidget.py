#!/usr/bin/env python
#coding: utf-8

from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import Qt
from canvas import Canvas


class MainWidget(QtGui.QTabWidget):

	def __init__(self, data, com, Parent=None):

		super(MainWidget, self).__init__()

		self.com = com
		self.data = data
		self.parent = Parent

		self.com.updateCanvas.connect(self.updateIcon)
		self.com.resizeCanvas.connect(self.updateIcon)

		scrollArea1 = ScrollArea(data, com, self)
		scrollArea2 = ScrollArea(data, com, self)
		self.addTab(scrollArea1, "Image1")
		self.addTab(scrollArea2, "Image2")
		if self.count() == 0:

			self.setStyleSheet("QTabWidget::pane { border-top: 0; }")

	def updateIcon(self):

		print "hholas"
		self.setTabIcon(self.currentIndex(), QtGui.QIcon(QtGui.QPixmap.fromImage(self.data.image)))


class ScrollArea(QtGui.QScrollArea):
	"""
	La clase ScrollArea es una derivada de la clase QScrollArea.
	En este widget se pone, centrado, el lienzo del dibujo (Canvas).
	Además, éste es el widget alrededor del cual se centra la MainWindow.
	"""

	def __init__(self, data, com, Parent=None):

		super(ScrollArea,self).__init__()

		self.com = com
		self.data = data
		self.canvas = Canvas(data, com, self)
		self.parent = Parent

		self.setBackgroundRole(QtGui.QPalette.Dark)
		self.setObjectName("ScrollArea")
		self.setWidget(self.canvas)
	
	def resizeEvent(self, event):

		super(ScrollArea,self).resizeEvent(event)
		self.calcNewCanvasGeometry()

	def paintEvent(self, event):

		super(ScrollArea,self).paintEvent(event)
		self.calcNewCanvasGeometry()

	def calcNewCanvasGeometry(self):
		
		g = self.frameGeometry()
		w = g.width()
		h = g.height()

		if self.canvas.width() < w:
			self.canvas.move( (w-self.data.image.width()*self.data.zoom)/2 , self.canvas.y() )
		if self.canvas.height() < h:
			self.canvas.move( self.canvas.x(), (h-self.data.image.height()*self.data.zoom)/2 )

	def wheelEvent(self, event):

		#super(ScrollArea, self).wheelEvent(event)
		
		if self.parent.parent.onClickPalette:
			self.parent.parent.wheelEvent(event)
		else:
			super(ScrollArea, self).wheelEvent(event)