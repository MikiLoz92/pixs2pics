#!/usr/bin/env python
#coding: utf-8

from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import Qt

## Vista/View
class Canvas(QtGui.QLabel):
	"""
	La clase Canvas representa el lienzo donde pintaremos.
	Se expande de tamaño a medida que aumentamos el zoom.
	"""

	def __init__(self, w, h, data, com, color, parent=None):

		super(Canvas, self).__init__()

		self.setBackgroundRole(QtGui.QPalette.Base)
		self.setSizePolicy(QtGui.QSizePolicy.Ignored, QtGui.QSizePolicy.Ignored)
		self.setScaledContents(True)

		self.com = com
		self.com.updateCanvas.connect(self.update)
		self.parent = parent
		self.data = data
		self.image = data.image
		self.image.fill(QtGui.qRgb(255, 255, 255))
		self.setPixmap(QtGui.QPixmap.fromImage(self.image))
		self.drawing = False

	def mousePressEvent(self, event):

		if event.button() == QtCore.Qt.LeftButton:
			if self.data.currentTool == 1:
				pos = event.pos()
				x = self.image.width() * pos.x() / ( self.image.width() * self.data.zoom )
				y = self.image.height() * pos.y() / ( self.image.height() * self.data.zoom )
				self.lastPoint = QtCore.QPoint(x,y)
				self.drawLineTo(QtCore.QPoint(x,y))
				self.drawing = True
			elif self.data.currentTool == 4:
				pos = event.pos()
				x = self.image.width() * pos.x() / ( self.image.width() * self.data.zoom )
				y = self.image.height() * pos.y() / ( self.image.height() * self.data.zoom )
				self.data.color = QtGui.QColor(self.image.pixel(QtCore.QPoint(x,y)))
				self.com.updateColor.emit()
				print "ASDASRF"
				#self.mainWidget.update()
			self.update()

	def mouseMoveEvent(self, event):

		if (event.buttons() and QtCore.Qt.LeftButton) and self.drawing:
			pos = event.pos()
			x = self.image.width() * pos.x() / ( self.image.width() * self.data.zoom )
			y = self.image.height() * pos.y() / ( self.image.height() * self.data.zoom )
			self.drawLineTo(QtCore.QPoint(x,y))
			self.update()

	def mouseReleaseEvent(self, event):

		if event.button() == QtCore.Qt.LeftButton and self.drawing:
			pos = event.pos()
			x = self.image.width() * pos.x() / ( self.image.width() * self.data.zoom )
			y = self.image.height() * pos.y() / ( self.image.height() * self.data.zoom )
			self.drawLineTo(QtCore.QPoint(x,y))
			self.drawing = False
			self.update()
	
	def paintEvent(self, event):
		
		#super(Canvas, self).paintEvent(event)
		
		#self.setFixedSize(self.image.width()*self.data.zoom, self.image.height()*self.data.zoom)
		painter = QtGui.QPainter(self)
		painter.drawImage(self.rect(), self.image)
		

	def drawLineTo(self, endPoint):

		painter = QtGui.QPainter(self.image)
		painter.setPen(QtGui.QPen(self.data.color, self.data.pencilSize,
			QtCore.Qt.SolidLine, QtCore.Qt.SquareCap, QtCore.Qt.MiterJoin))
		painter.drawLine(self.lastPoint, endPoint)
		self.modified = True

		#self.update()
		self.lastPoint = QtCore.QPoint(endPoint)