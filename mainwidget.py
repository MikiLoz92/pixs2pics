#!/usr/bin/env python
#coding: utf-8

from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import Qt
from canvas import Canvas

## Vista/View
class MainWidget(QtGui.QScrollArea):
	"""
	La clase MainWidget es una derivada de la clase QScrollArea.
	En este widget se pone, centrado, el lienzo del dibujo (Canvas).
	Además, éste es el widget alrededor del cual se centra la MainWindow.
	"""

	def __init__(self, w, h, data, com, color, Parent=None):

		super(MainWidget,self).__init__()

		self.com = com
		self.data = data
		self.canvas = Canvas(w, h, data, com, color, self)

		self.setBackgroundRole(QtGui.QPalette.Dark)
		self.setObjectName("MainWidget")
		self.setWidget(self.canvas)
	"""
	def resizeEvent(self, event):

		super(MainWidget,self).resizeEvent(event)
		self.calcNewCanvasGeometry()

	def paintEvent(self, event):

		super(MainWidget,self).paintEvent(event)
		self.calcNewCanvasGeometry()

	def calcNewCanvasGeometry(self):
		
		g = self.frameGeometry()
		w = g.width()
		h = g.height()

		if self.canvas.width() < w:
			self.canvas.move( (w-self.data.image.width()*self.data.zoom)/2 , self.canvas.y() )
		if self.canvas.height() < h:
			self.canvas.move( self.canvas.x(), (h-self.data.image.height()*self.data.zoom)/2 )
	"""