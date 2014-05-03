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
		self.setMouseTracking(True)
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
		self.com.enterCanvas.emit()

	def leaveEvent(self, event): # Si el ratón se va, lo reiniciamos

		super(Canvas, self).leaveEvent(event)
		self.unsetCursor()
		self.com.leaveCanvas.emit()

	def mousePressEvent(self, event):

		pos = event.pos()
		x = pos.x() / self.data.zoom # x de la imagen
		y = pos.y() / self.data.zoom # y de la imagen

		# Selección
		if self.data.currentTool == 0:
			if event.button() == Qt.LeftButton:
				if not self.selection:
					self.selOriginOnImage = QtCore.QPoint( x, y )
					self.selOriginOnCanvas = QtCore.QPoint( x * self.data.zoom - 1, y * self.data.zoom - 1)
					self.selection = RubberBand(self.data, self)
			elif event.button() == Qt.RightButton:
				pass

		# Lápiz
		elif self.data.currentTool == 1:
			self.lastPoint = QtCore.QPoint(x,y)
			painter = QtGui.QPainter(self.data.image)
			if event.button() == Qt.LeftButton:
				painter.setPen(QtGui.QPen(self.data.primaryColor, self.data.pencilSize,	Qt.SolidLine, Qt.SquareCap, Qt.MiterJoin))
				painter.drawPoint(x,y)
				self.drawing = True
			elif event.button() == Qt.RightButton:
				painter.setPen(QtGui.QPen(self.data.secondaryColor, self.data.pencilSize,	Qt.SolidLine, Qt.SquareCap, Qt.MiterJoin))
				painter.drawPoint(x,y)
				self.drawing = True

		# Goma
		elif self.data.currentTool == 3:
			print "Borrandooooo, me paso el día borrandoooo"

		# Pipeta de color
		elif self.data.currentTool == 4:
			if event.button() == Qt.LeftButton:
				self.data.changePrimaryColor( QtGui.QColor(self.data.image.pixel(QtCore.QPoint(x,y))) )
			elif event.button() == Qt.RightButton:
				self.data.changeSecondaryColor( QtGui.QColor(self.data.image.pixel(QtCore.QPoint(x,y))) )
			self.updateColor.emit()

		# Cubo
		elif self.data.currentTool == 5:
			self.fillImage( (x, y), self.data.primaryColor, self.data.image.pixel(x,y), self.data.image )
			self.com.updateCanvas.emit()

		# Degradado
		elif self.data.currentTool == 6:
			if self.data.DegPoint == 0:
				self.data.DegPoint = (x,y)
			else:
				if DegState == 1:
					self.Grad2Color(self, (x,y))

		self.update()

		# DEBUG
		# print self.width(), self.height()
		# print self.data.image.width(), self.data.image.height()
		# print x,y

	def mouseMoveEvent(self, event):

		pos = event.pos()
		x = pos.x() / self.data.zoom # x de la imagen
		y = pos.y() / self.data.zoom # y de la imagen

		# Selección
		if self.data.currentTool == 0:
			if event.buttons() == Qt.LeftButton:
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
		
		# Lápiz
		elif self.data.currentTool == 1:
			endPoint = QtCore.QPoint(x,y)
			painter = QtGui.QPainter(self.data.image)
			if event.buttons() == Qt.LeftButton:
				painter.setPen(QtGui.QPen(self.data.primaryColor, self.data.pencilSize,	Qt.SolidLine, Qt.SquareCap, Qt.MiterJoin))
				painter.drawLine(self.lastPoint, endPoint)
				self.com.updateCanvas.emit()
				self.lastPoint = QtCore.QPoint(endPoint)
			elif event.buttons() == Qt.RightButton:
				painter.setPen(QtGui.QPen(self.data.secondaryColor, self.data.pencilSize,	Qt.SolidLine, Qt.SquareCap, Qt.MiterJoin))
				painter.drawLine(self.lastPoint, endPoint)
				self.com.updateCanvas.emit()
				self.lastPoint = QtCore.QPoint(endPoint)

		self.update()
			
	def mouseReleaseEvent(self, event):

		pos = event.pos()
		x = pos.x() / self.data.zoom # x de la imagen
		y = pos.y() / self.data.zoom # y de la imagen

		# Selección
		if self.data.currentTool == 0 and event.button() == QtCore.Qt.LeftButton:
			if self.selecting:
				print "Selection made starting at (" + str(self.selOriginOnImage.x()) + ", " + str(self.selOriginOnImage.y()) + ") and ending at (" + str(x) + ", " + str(y) + ")"
			else:
				print "No selection was made"
			self.selection.hide()
			self.selecting = False
			self.selection = None
			self.selOriginOnImage = None
			self.selOriginOnCanvas = None

		# Lápiz
		elif self.data.currentTool == 1 and self.drawing:
			if event.button() == Qt.LeftButton or event.button() == Qt.RightButton:
				if self.data.posHistory != len(self.data.history)-1:
					self.data.history = self.data.history[:self.data.posHistory+1]
				self.data.history.append(QtGui.QImage(self.data.image))
				self.data.posHistory += 1
				self.update()

		
	
	def paintEvent(self, event):
		
		#super(Canvas, self).paintEvent(event)
		
		# Image
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
			for i in range(w)[1:]:
				painter.drawLine(i*self.data.zoom, 0, i*self.data.zoom, h*self.data.zoom)
			for i in range(h)[1:]:
				painter.drawLine(0, i*self.data.zoom, w*self.data.zoom, i*self.data.zoom)

		# Matrix Grid
		if self.data.matrixGrid and self.data.zoom >= 3:
			painter.setPen(QtGui.QColor(127,67,167,128))
			w = self.data.image.width()
			h = self.data.image.height()
			for i in range(w)[1:]:
				if i % self.data.matrixGridWidth == 0:
					print i
					painter.drawLine(i*self.data.zoom, 0, i*self.data.zoom, h*self.data.zoom)
			for i in range(h)[1:]:
				if i % self.data.matrixGridHeight == 0:
					painter.drawLine(0, i*self.data.zoom, w*self.data.zoom, i*self.data.zoom)
		
	def drawLineTo(self, endPoint):

		painter = QtGui.QPainter(self.data.image)
		painter.setPen(QtGui.QPen(self.data.primaryColor, self.data.pencilSize,
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

	def fillImage(self, begin, paint, current, imagen):
		if paint.rgb() == current :
			print paint.rgb()
			print current
			print "pass activated"
		else:
			queue = [begin]
			for x,y in queue:
				if imagen.pixel(x,y) == current:
					cond = True
					nodes = [(x,y)]
					xt = x-1
					while xt>=0 and cond: 
						cond = imagen.pixel(xt,y)==current
						if cond:
							nodes.append( (xt,y) ) 
							xt = xt-1

					cond = True
					xt = x+1
					while xt<imagen.width() and cond : 
						cond = imagen.pixel(xt,y)==current
						if cond:
							nodes.append( (xt,y) ) 
							xt = xt+1

					for xp,yp in nodes:
						imagen.setPixel(xp,yp,paint.rgb())
						if yp<imagen.width()-1:
							if imagen.pixel(xp,yp+1) == current: 
								queue.append( (xp,yp+1) )
						if yp>0:
							if imagen.pixel(xp,yp-1) == current:
								queue.append( (xp,yp-1) )

	def Grad2Colors(self,pf):
		pi = self.data.DegPoint[0]
		if pf[0] == pi[0]:
			Var_y = self.data.DegPoint[1] - pf[1]
			if Var_y > 0 :
				dy = +1
			elif Var_y < 0 :
				dy = -1
			else:
				pass
			color1 = self.data.color_deg_1.getRgb()
			color2 = self.data.color_deg_2.getRgb()
			Var_r = color1[0] - color[0]
			dr = float(Var_r)/abs(Var_y)
			Var_g = color1[1] - color[1]
			dg = float(Var_r)/abs(Var_y)
			Var_b = color1[2] - color[2]
			db = float(Var_r)/abs(Var_y)
			for i in range(1,Var_y-1):
				R = color1[0] + i*dr
				G = color1[1] + i*dg
				B = color1[2] + i*db
				tmp_c = QtGui.QColor(R,G,B,255)
				self.data.image.setPixel(pi[0],pi[1]+i*dy,tmp_c.rgb())
		elif pf[1] == pi[1]:
			pass
		elif imagen.pixel(x,y) == current :
			imagen.setPixel(x,y,paint.rgb())
			self.fillImage(x+1, y, paint, current, imagen)
			self.fillImage(x, y+1, paint, current, imagen)
			self.fillImage(x-1, y, paint, current, imagen)
			self.fillImage(x, y-1, paint, current, imagen)

		