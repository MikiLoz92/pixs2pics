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
		self.rubber = None

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
				if not self.rubber:
					#self.rubberOrigin = event.pos()
					self.rubberOrigin = QtCore.QPoint( x * self.data.zoom - 1, y * self.data.zoom - 1)
					self.rubber = RubberBand(self.data, self)
					self.rubber.setGeometry(QtCore.QRect(self.rubberOrigin, QtCore.QSize()))
					self.rubber.show()
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
			#self.rubber.setGeometry(QtCore.QRect(self.rubberOrigin, event.pos()).normalized())
			x = (event.pos().x()-self.rubberOrigin.x()) / self.data.zoom * self.data.zoom
			y = (event.pos().y()-self.rubberOrigin.y()) / self.data.zoom * self.data.zoom
			print "Origin x:", self.rubberOrigin.x(), ", y:", self.rubberOrigin.y(), "x:", x, ", y:", y
			self.rubber.setGeometry( self.rubberOrigin.x(), self.rubberOrigin.y(), x+self.data.zoom+2, y+self.data.zoom+2 )
			

	def mouseReleaseEvent(self, event):

		if event.button() == QtCore.Qt.LeftButton and self.drawing:
			pos = event.pos()
			x = self.data.image.width() * pos.x() / ( self.data.image.width() * self.data.zoom )
			y = self.data.image.height() * pos.y() / ( self.data.image.height() * self.data.zoom )
			self.drawLineTo(QtCore.QPoint(x,y))
			self.drawing = False
			self.update()

		if event.button() == QtCore.Qt.LeftButton and self.data.currentTool == 0:
			self.rubber.hide()
			self.rubber = None
			self.rubberOrigin = None
	
	def paintEvent(self, event):
		
		#super(Canvas, self).paintEvent(event)
		
		#self.setFixedSize(self.data.image.width()*self.data.zoom, self.data.image.height()*self.data.zoom)
		painter = QtGui.QPainter(self)
		painter.drawImage(self.rect(), self.data.image)
		
		#self.com.updateCanvas.emit()
		
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

		