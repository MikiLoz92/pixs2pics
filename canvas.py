#!/usr/bin/env python
#coding: utf-8

from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import Qt


class RubberBand(QtGui.QRubberBand):

	def __init__(self, data, parent=None):

		self.data = data

		super(RubberBand, self).__init__(QtGui.QRubberBand.Rectangle, parent)

	"""
	def resizeEvent(self, event):

		super(RubberBand, self).resizeEvent(event)
		w = (event.size().width()/self.data.zoom + 1) * self.data.zoom
		h = (event.size().height()/self.data.zoom + 1) * self.data.zoom
		self.resize(w, h)
	"""

	"""
	def paintEvent(self, event):

		rect = event.rect()
		x = (rect.x() + rect.width()) / self.data.zoom
		y = (rect.y() + rect.height()) / self.data.zoom
		self.resize(x*self.data.zoom+1+5, y*self.data.zoom+1+5)

		super(RubberBand, self).paintEvent(QtGui.QPaintEvent(self.rect()))
	"""
	


## Vista/View
class Canvas(QtGui.QLabel):
	"""
	La clase Canvas representa el lienzo donde pintaremos.
	Se expande de tamaño a medida que aumentamos el zoom.
	"""

	def __init__(self, w, h, data, com, color, parent=None):

		super(Canvas, self).__init__()

		self.setBackgroundRole(QtGui.QPalette.Base)
		self.setAttribute(Qt.WA_TranslucentBackground)
		#self.setSizePolicy(QtGui.QSizePolicy.Ignored, QtGui.QSizePolicy.Ignored)
		#self.setScaledContents(True)

		self.com = com
		self.com.updateCanvas.connect(self.update)
		self.com.newImage.connect(self.resizeToNewImage)
		self.parent = parent
		self.data = data
		#self.image = data.image
		self.data.image.fill(QtGui.qRgb(255, 255, 255))
		self.setPixmap(QtGui.QPixmap.fromImage(self.data.image))
		self.drawing = False
		self.selecting = False
		self.selection = None

	def enterEvent(self, event): # Cuando entra el ratón en el Canvas cambiamos el cursor

		super(Canvas, self).enterEvent(event)
		if not self.data.colorPicker:
			self.setCursor(self.data.pencilCur)

	def leaveEvent(self, event): # Si el ratón se va, lo reiniciamos

		super(Canvas, self).leaveEvent(event)
		self.unsetCursor()

	def mousePressEvent(self, event):

		pos = event.pos()
		x = pos.x() / self.data.zoom # x de la imagen
		y = pos.y() / self.data.zoom # y de la imagen

		if event.button() == QtCore.Qt.LeftButton:
			if self.data.currentTool == 0:
				if not self.selection:
					self.selOriginOnImage = QtCore.QPoint( x, y )
					self.selOriginOnCanvas = QtCore.QPoint( x * self.data.zoom - 1, y * self.data.zoom - 1)
					self.selection = RubberBand(self.data, self)
			elif self.data.currentTool == 1:
				self.lastPoint = QtCore.QPoint(x,y)
				painter = QtGui.QPainter(self.data.image)
				painter.setPen(QtGui.QPen(self.data.color, self.data.pencilSize,
								QtCore.Qt.SolidLine, QtCore.Qt.SquareCap, QtCore.Qt.MiterJoin))
				painter.drawPoint(x,y)
				self.drawing = True
			elif self.data.currentTool == 5:
				self.fillImage( x, y, self.data.color, self.data.image.pixel(x,y), self.data.image )
			elif self.data.currentTool == 4:
				self.data.color = QtGui.QColor(self.data.image.pixel(QtCore.QPoint(x,y)))
				self.com.updateColor.emit()
			elif self.data.currentTool == 3:
				print "Borrandooooo, me paso el día borrandoooo"

			self.update()

		# DEBUG
		print self.width(), self.height()
		print self.data.image.width(), self.data.image.height()
		print x,y

	def mouseMoveEvent(self, event):

		if (event.buttons() and QtCore.Qt.LeftButton) and self.drawing:
			pos = event.pos()
			x = self.data.image.width() * pos.x() / ( self.data.image.width() * self.data.zoom )
			y = self.data.image.height() * pos.y() / ( self.data.image.height() * self.data.zoom )
			self.drawLineTo(QtCore.QPoint(x,y))
			self.update()

		if (event.buttons() and QtCore.Qt.LeftButton and self.data.currentTool == 0):

			self.selecting = True

			w = (event.pos().x()-self.selOriginOnCanvas.x()) / self.data.zoom * self.data.zoom
			h = (event.pos().y()-self.selOriginOnCanvas.y()) / self.data.zoom * self.data.zoom
			x = event.pos().x() / self.data.zoom * self.data.zoom - 1
			y = event.pos().y() / self.data.zoom * self.data.zoom - 1

			if event.pos().x() >= self.selOriginOnCanvas.x() + 1 and event.pos().y() >= self.selOriginOnCanvas.y() + 1:
				#print "Cuadrante 4"
				self.selection.setGeometry( self.selOriginOnCanvas.x(), self.selOriginOnCanvas.y(), w+self.data.zoom+2, h+self.data.zoom+2)
			elif event.pos().x() < self.selOriginOnCanvas.x() + 1 and event.pos().y() >= self.selOriginOnCanvas.y() + 1:
				#print "Cuadrante 3"
				self.selection.setGeometry( x, self.selOriginOnCanvas.y(), (self.selOriginOnImage.x()+1)*self.data.zoom + 1 - x, h+self.data.zoom+2)
			elif event.pos().x() < self.selOriginOnCanvas.x() + 1 and event.pos().y() < self.selOriginOnCanvas.y() + 1:
				#print "Cuadrante 2"
				self.selection.setGeometry( x, y, (self.selOriginOnImage.x()+1)*self.data.zoom + 1 - x, (self.selOriginOnImage.y()+1)*self.data.zoom + 1 - y)
			elif event.pos().x() >= self.selOriginOnCanvas.x() + 1 and event.pos().y() < self.selOriginOnCanvas.y() + 1:
				#print "Cuadrante 1"
				self.selection.setGeometry( self.selOriginOnCanvas.x(), y, w+self.data.zoom+2, (self.selOriginOnImage.y()+1)*self.data.zoom + 1 - y)

			self.selection.show()
			#print "Origin x:", self.selOriginOnCanvas.x(), ", y:", self.selOriginOnCanvas.y(), "w:", w, ", h:", h
			#print "Event x:", event.pos().x(), ", y:", event.pos().y()
			
			

	def mouseReleaseEvent(self, event):

		if event.button() == QtCore.Qt.LeftButton and self.drawing:
			pos = event.pos()
			x = self.data.image.width() * pos.x() / ( self.data.image.width() * self.data.zoom )
			y = self.data.image.height() * pos.y() / ( self.data.image.height() * self.data.zoom )
			self.drawLineTo(QtCore.QPoint(x,y))
			self.drawing = False
			self.update()

		if event.button() == QtCore.Qt.LeftButton and self.data.currentTool == 0:
			x = event.pos().x() / self.data.zoom
			y = event.pos().y() / self.data.zoom
			if self.selecting:
				print "Selection made starting at (" + str(self.selOriginOnImage.x()) + ", " + str(self.selOriginOnImage.y()) + ") and ending at (" + str(x) + ", " + str(y) + ")"
			else:
				print "No selection was made"
			self.selection.hide()
			self.selecting = False
			self.selection = None
			self.selOriginOnImage = None
			self.selOriginOnCanvas = None
	
	def paintEvent(self, event):
		
		#super(Canvas, self).paintEvent(event)
		
		#self.setFixedSize(self.data.image.width()*self.data.zoom, self.data.image.height()*self.data.zoom)
		painter = QtGui.QPainter(self)
		painter.drawImage(self.rect(), self.data.image)

		# Pixel Grid
		if self.data.grid and self.data.zoom > 3:
			if self.data.zoom < 9:
				pen = QtGui.QPen(QtGui.QColor(0,0,0,64))
				pen.setStyle(Qt.SolidLine)
			else:
				pen = QtGui.QPen(QtGui.QColor(0,0,0,128))
				pen.setStyle(Qt.DotLine)
			painter.setPen(pen)
			w = self.data.image.width()
			h = self.data.image.height()
			for i in range(w):
				painter.drawLine(i*self.data.zoom, 0, i*self.data.zoom, h*self.data.zoom)
			for i in range(h):
				painter.drawLine(0, i*self.data.zoom, w*self.data.zoom, i*self.data.zoom)
		
	def drawLineTo(self, endPoint):

		painter = QtGui.QPainter(self.data.image)
		painter.setPen(QtGui.QPen(self.data.color, self.data.pencilSize,
			QtCore.Qt.SolidLine, QtCore.Qt.SquareCap, QtCore.Qt.MiterJoin))
		painter.drawLine(self.lastPoint, endPoint)
		self.modified = True
		self.com.updateCanvas.emit()

		#self.update()
		self.lastPoint = QtCore.QPoint(endPoint)

	def resizeToNewImage(self):

		self.resize(self.data.image.width(), self.data.image.height())
		self.setPixmap(QtGui.QPixmap.fromImage(self.data.image))
		self.data.zoom = 1
		self.com.updateCanvas.emit()

	def fillImage(self, x, y, paint, current, imagen):
		if x<0 or y<0 or x>imagen.width() or y>imagen.height():
			pass
		elif imagen.pixel(x,y) == current :
			imagen.setPixel(x,y,paint.rgb())
			self.fillImage(x+1, y, paint, current, imagen)
			self.fillImage(x, y+1, paint, current, imagen)
			self.fillImage(x-1, y, paint, current, imagen)
			self.fillImage(x, y-1, paint, current, imagen)

		