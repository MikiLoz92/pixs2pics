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

	def __init__(self, w, h, image, com, color, parent=None):

		super(Canvas, self).__init__()
		self.qimage = QtGui.QImage(w,h,QtGui.QImage.Format_RGB32)

		self.setPixmap(QtGui.QPixmap.fromImage(self.qimage))

		self.parent = parent
		self.width = w
		self.height = h
		#self.setSizePolicy(QtGui.QSizePolicy.Fixed,QtGui.QSizePolicy.Fixed)
		#self.repaint()
		#self.setFixedSize(w, h)
		self.zoom = 1
		#self.setBackgroundRole(QtGui.QPalette.Base)
		#self.setAutoFillBackground(True)

		#self.setAttribute(QtCore.Qt.WA_StaticContents)
		self.myPenWidth = 1
		self.myPenColor = color
		self.image = image
		self.com = com
		self.com.dadesActualitzada.connect(self.actualitzar)
		#self.com.zoomIn.connect(self.zoomIn)

	def actualitzar(self):

		self.update()

	def mousePressEvent(self, event):

		if event.button() == QtCore.Qt.LeftButton:
			pos = event.pos()
			x = pos.x() - pos.x()*(self.zoom-1)/self.zoom
			y = pos.y() - pos.y()*(self.zoom-1)/self.zoom
			self.image.afegirpunt(QtCore.QPoint(x,y))
			self.update()

	def mouseMoveEvent(self, event):

		if (event.buttons() & QtCore.Qt.LeftButton):
			pos = event.pos()
			x = pos.x() - pos.x()*(self.zoom-1)/self.zoom
			y = pos.y() - pos.y()*(self.zoom-1)/self.zoom
			self.image.afegirpunt(QtCore.QPoint(x,y))
			self.update()

	def mouseReleaseEvent(self, event):

		if event.button() == QtCore.Qt.LeftButton:
			pos = event.pos()
			x = pos.x() - pos.x()*(self.zoom-1)/self.zoom
			y = pos.y() - pos.y()*(self.zoom-1)/self.zoom
			self.image.afegirpunt(QtCore.QPoint(x,y))
			self.update()

	def zoomIn(self):

		if self.zoom < 7:
			self.zoom += 1
			self.setFixedSize(self.width*self.zoom, self.height*self.zoom)
			self.actualitzar()

	def zoomOut(self):

		if self.zoom > 1:
			self.zoom -= 1
			self.setFixedSize(self.width*self.zoom, self.height*self.zoom)
			self.actualitzar()

	def paintEvent(self, event):
		
		painter = QtGui.QPainter(self)
		painter.scale(self.zoom,self.zoom)		
		painter.setBackgroundMode(Qt.OpaqueMode)
		brush = QtGui.QBrush(Qt.white)
		painter.setBrush(brush)
		painter.fillRect(0,0,self.width,self.height,brush)

		painter.setPen(QtGui.QPen(self.myPenColor, self.myPenWidth,
			QtCore.Qt.SolidLine, QtCore.Qt.FlatCap, QtCore.Qt.MiterJoin))
		for punt in self.image.lpunts:
			painter.drawPoint(punt)