#!/usr/bin/env python
#coding: utf-8

import sys

from PyQt4 import QtGui, QtCore, QtOpenGL
from PyQt4.QtCore import Qt

try:
    from OpenGL import GL

except ImportError:
    print "Error: pyOpenGL must be installed if you want to use OpenGL acceleration."
    sys.exit(1)


class RubberBand(QtGui.QRubberBand):

	def __init__(self, origin, data, parent=None):

		super(RubberBand, self).__init__(QtGui.QRubberBand.Rectangle, parent)

		self.data = data
		print origin

		self.origin = QtCore.QPoint(origin)
		self.finished = False
		self.moving = False
		self.image = None
		self.rect = QtCore.QRect()

	def setGeometry(self, x, y, w, h): # Todos los argumentos son el imagen, no en el Canvas

		self.rect = QtCore.QRect(x, y, w, h)
		super(RubberBand, self).setGeometry( x * self.data.zoom - 1, y * self.data.zoom - 1, w * self.data.zoom + 2, h * self.data.zoom + 2 )

		


## Vista/View
class Canvas(QtGui.QLabel):
	"""
	La clase Canvas representa el lienzo donde pintaremos.
	Se expande de tamaño a medida que aumentamos el zoom.
	"""

	def __init__(self, w, h, data, com, color, parent=None):

		#super(Canvas, self).__init__(QtOpenGL.QGLFormat(QtOpenGL.QGL.SampleBuffers), parent)
		super(Canvas, self).__init__(parent)

		self.setBackgroundRole(QtGui.QPalette.Base)
		self.setAttribute(Qt.WA_TranslucentBackground)
		self.setMouseTracking(True)
		self.setObjectName("Canvas")

		self.com = com
		self.com.zoomIn.connect(self.calcNewSelectionGeometry)
		self.com.zoomOut.connect(self.calcNewSelectionGeometry)
		self.com.updateCanvas.connect(self.update)
		self.com.updateTool.connect(self.cancelSelection)
		self.com.newImage.connect(self.resizeToNewImage)
		self.parent = parent
		self.data = data

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
					# Crear una nueva selección
					self.selection = RubberBand(QtCore.QPoint(x, y), self.data, self)
				else:
					if self.selection.rect.contains(QtCore.QPoint(x, y)):
						# Mover selección
						self.selection.moving = True
						#self.selectionGrabPoint = pos
						self.selectionGrabPoint = QtCore.QPoint(x - self.selection.rect.x(), y - self.selection.rect.y())
					else:
						if self.selection.image != None:
							# Pintamos la imagen seleccionada en la imagen final
							self.applySelection()
						self.selection = RubberBand(QtCore.QPoint(x, y), self.data, self)
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
			if event.button() == Qt.LeftButton or event.button() == Qt.RightButton:
				self.lastPoint = QtCore.QPoint(x,y)
				painter = QtGui.QPainter(self.data.image)
				painter.setPen(QtGui.QPen(self.data.bgColor, self.data.pencilSize, QtCore.Qt.SolidLine, QtCore.Qt.SquareCap, QtCore.Qt.MiterJoin))
				painter.drawPoint(x,y)
				self.drawing = True

		# Pipeta de color
		elif self.data.currentTool == 4:
			if event.button() == Qt.LeftButton:
				self.data.changePrimaryColor( QtGui.QColor(self.data.image.pixel(QtCore.QPoint(x,y))) )
			elif event.button() == Qt.RightButton:
				self.data.changeSecondaryColor( QtGui.QColor(self.data.image.pixel(QtCore.QPoint(x,y))) )
			self.com.updateColor.emit()

		# Cubo
		elif self.data.currentTool == 5:
			if event.button() == Qt.LeftButton:
				self.fillImage( (x, y), self.data.primaryColor, self.data.image.pixel(x,y), self.data.image )
			elif event.button() == Qt.RightButton:
				self.fillImage( (x, y), self.data.secondaryColor, self.data.image.pixel(x,y), self.data.image )
			self.data.addHistoryStep()
			self.com.updateCanvas.emit()

		# Degradado
		elif self.data.currentTool == 6:

			if event.button() == Qt.LeftButton:

				if self.data.DegPoint == 0:
					self.data.DegPoint = (x,y)
					self.data.save_color = QtGui.QColor( self.data.image.pixel(x,y) )
					self.data.color_deg_1.setAlpha(self.data.DegAlpha)
					if self.data.DegState == 1:
						self.data.image.setPixel(x,y,self.data.color_deg_1.rgba())
					elif self.data.DegState == 2:
						self.data.image.setPixel(x,y,self.data.color_deg_1.rgb())

				elif (x,y) != self.data.DegPoint :
					if self.data.DegState == 1:
						i = self.Grad2Colors((x,y))
						if i==0:
							self.data.DegPoint = 0
					elif self.data.DegState == 2:
						i = self.GradColorAlpha((x,y))
						if i==0:
							self.data.DegPoint = 0

			elif event.button() == QtCore.Qt.RightButton:

				#Degradado - Cancelar primera selección
				if self.data.currentTool==6 and self.data.DegPoint!=0:
					x, y = self.data.DegPoint
					self.data.image.setPixel(x,y,self.data.save_color.rgba())
					self.data.DegPoint = 0

		# Mover canvas
		if event.button() == Qt.MiddleButton:
			self.grabPoint = event.pos()

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
				if not self.selection.finished:
					self.selecting = True
					self.calcNewSelectionGeometry(event.pos().x(), event.pos().y())
				if self.selection.moving:
					self.moveSelection(event.pos().x(), event.pos().y())
				
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

		# Goma
		elif self.data.currentTool == 3:
			if event.buttons() == Qt.LeftButton or event.buttons() == Qt.RightButton:
				print "Borrando"
				endPoint = QtCore.QPoint(x,y)
				painter = QtGui.QPainter(self.data.image)
				painter.setPen(QtGui.QPen(self.data.bgColor, self.data.pencilSize,	Qt.SolidLine, Qt.SquareCap, Qt.MiterJoin))
				painter.setCompositionMode(QtGui.QPainter.CompositionMode_Source)
				painter.drawLine(self.lastPoint, endPoint)
				self.com.updateCanvas.emit()
				self.lastPoint = QtCore.QPoint(endPoint)

		if event.buttons() == Qt.MiddleButton:
			
			self.move(self.mapToParent(event.pos() - self.grabPoint))

			print "event pos:", self.mapToParent(pos).x(), "parent.width:", self.parent.width(), "width:", self.width()
			if (self.mapToParent(pos).x() + self.width() - self.grabPoint.x()) > (self.parent.width() ):
				self.move(self.parent.width()-self.width(), self.y())
			elif (self.mapToParent(pos).x() - self.grabPoint.x()) < 0:
				self.move(0, self.y())
			if (self.mapToParent(pos).y() + self.height() - self.grabPoint.y()) > (self.parent.height() ):
				self.move(self.x(), self.parent.height()-self.height())
			elif (self.mapToParent(pos).y() - self.grabPoint.y()) < 0:
				self.move(self.x(), 0)

		self.update()
			
	def mouseReleaseEvent(self, event):

		pos = event.pos()
		x = pos.x() / self.data.zoom # x de la imagen
		y = pos.y() / self.data.zoom # y de la imagen

		# Selección
		if self.data.currentTool == 0 and event.button() == QtCore.Qt.LeftButton:
			
			if self.selecting:
				print "Selection made starting at (" + str(self.selection.origin.x()) + ", " + str(self.selection.origin.y()) + ") and ending at (" + str(x) + ", " + str(y) + ") (both included)"
				self.selection.finished = True
				self.selection.image = self.data.image.copy(self.selection.rect)
				painter = QtGui.QPainter(self.data.image)
				painter.setCompositionMode(QtGui.QPainter.CompositionMode_Source)
				painter.fillRect(self.selection.rect, self.data.bgColor)
				print "Filling selection rect with bgColor"
			else:
				if self.selection != None and self.selection.finished:
					print "Moved selection"
				else:
					print "No selection was made"
					self.selection = None
			self.selecting = False

		# Lápiz
		elif self.data.currentTool == 1 and self.drawing:
			if event.button() == Qt.LeftButton or event.button() == Qt.RightButton:
				self.data.addHistoryStep()
	
	def paintEvent(self, event):
		
		#super(Canvas, self).paintEvent(event)

		painter = QtGui.QPainter(self)

		# Transparency
		if self.data.bgColor == QtGui.QColor(0,0,0,0):
			painter.fillRect(self.rect(), QtGui.QBrush(QtGui.QImage("images/transparent.png")))
		
		# Image
		painter.drawImage(self.rect(), self.data.image)

		# Selection
		if not self.selecting and self.selection != None and self.selection.finished and self.selection.image != None:
			rect = QtCore.QRect(self.selection.rect.topLeft()*self.data.zoom, self.selection.rect.size()*self.data.zoom)
			painter.drawImage(rect, self.selection.image)

		# Pixel Grid
		if self.data.grid and self.data.zoom > 3:
			r = self.data.bgColor.red()
			g = self.data.bgColor.green()
			b = self.data.bgColor.blue()
			gridColor = QtGui.QColor(255-r, 255-g, 255-b, 255)
			pen = QtGui.QPen(gridColor)
			if self.data.zoom < 9:
				pen.setStyle(Qt.SolidLine)
			else:
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

	def applySelection(self):

		print "Applying selection"
		painter = QtGui.QPainter(self.data.image)
		painter.drawImage(self.selection.rect.topLeft(), self.selection.image)
		self.data.addHistoryStep()
		self.selection.hide()
		self.selection = None

	def cancelSelection(self):

		if self.selection != None:
			print "Canceling selection"
			painter = QtGui.QPainter(self.data.image)
			painter.drawImage(self.selection.rect.topLeft(), self.selection.image)
			self.data.addHistoryStep()
			self.selection.hide()
			self.selection = None

	def resizeToNewImage(self):

		if self.selection != None:
			self.selection.hide()
			self.selection = None
		self.resize(self.data.image.width(), self.data.image.height())
		self.setPixmap(QtGui.QPixmap.fromImage(self.data.image))
		self.data.zoom = 1
		self.com.updateCanvas.emit()

	def fillImage(self, begin, paint, current, imagen):
		if paint.rgb() == current :
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

	def Grad2Colors(self, pf):

		pi = self.data.DegPoint
		alpha = self.data.DegAlpha
		print pi,pf

		if pf[0] == pi[0]:

			Var_y = pf[1] - pi[1]
			if Var_y > 0 :
				dy = +1
			elif Var_y < 0 :
				dy = -1
			else:
				return 0

			color1 = self.data.color_deg_1.getRgb()
			color2 = self.data.color_deg_2.getRgb()
			print color1,color2

			Var_r = color2[0] - color1[0]
			dr = float(Var_r)/abs(Var_y)
			Var_g = color2[1] - color1[1]
			dg = float(Var_g)/abs(Var_y)
			Var_b = color2[2] - color1[2]
			db = float(Var_b)/abs(Var_y)
			print dr, dg, db

			for i in range(1,abs(Var_y)+1):
				R = color1[0] + i*dr
				G = color1[1] + i*dg
				B = color1[2] + i*db
				R = int( round(R) )
				G = int( round(G) )
				B = int( round(B) )
				print R,G,B

				tmp_c = QtGui.QColor(R,G,B,alpha)
				print "changed color"
				self.data.image.setPixel(pi[0],pi[1]+i*dy,tmp_c.rgba())

			return 0

		elif pf[1] == pi[1]:

			Var_x = pf[0] - pi[0]
			if Var_x > 0 :
				dx = +1
			elif Var_x < 0 :
				dx = -1
			else:
				return 0

			color1 = self.data.color_deg_1.getRgb()
			color2 = self.data.color_deg_2.getRgb()
			print color1,color2

			Var_r = color2[0] - color1[0]
			dr = float(Var_r)/abs(Var_x)
			Var_g = color2[1] - color1[1]
			dg = float(Var_g)/abs(Var_x)
			Var_b = color2[2] - color1[2]
			db = float(Var_b)/abs(Var_x)
			print dr, dg, db

			for i in range(1,abs(Var_x)+1):
				R = color1[0] + i*dr
				G = color1[1] + i*dg
				B = color1[2] + i*db
				R = int( round(R) )
				G = int( round(G) )
				B = int( round(B) )
				print R,G,B

				tmp_c = QtGui.QColor(R,G,B,alpha)
				self.data.image.setPixel(pi[0]+i*dx,pi[1],tmp_c.rgba())
			return 0

		else:
			return 1

	def GradColorAlpha(self, pf):

		pi = self.data.DegPoint
		alpha = self.data.DegAlpha
		print pi,pf

		if pf[0] == pi[0]:

			Var_y = pf[1] - pi[1]
			if Var_y > 0 :
				dy = +1
			elif Var_y < 0 :
				dy = -1
			else:
				return 0

			color = self.data.color_deg_1
			da = 255/abs(Var_y)

			for i in range(1,abs(Var_y)+1):

				color.setAlpha(255-da*i)
				print "changed color"
				self.data.image.setPixel(pi[0],pi[1]+i*dy,color.rgba())

			return 0

		elif pf[1] == pi[1]:

			Var_x = pf[0] - pi[0]
			if Var_x > 0 :
				dx = +1
			elif Var_x < 0 :
				dx = -1
			else:
				return 0

			color = self.data.color_deg_1
			da = 255/abs(Var_x)

			for i in range(1,abs(Var_x)+1):

				color.setAlpha(255-da*i)
				print "changed color"
				self.data.image.setPixel(pi[0]+i*dx,pi[1],color.rgba())

			return 0

		else:
			return 1

	def calcNewSelectionGeometry(self, xevent, yevent):

		# En la imagen
		x = xevent / self.data.zoom
		y = yevent / self.data.zoom

		if x >= self.selection.origin.x() and y >= self.selection.origin.y():
			self.selection.setGeometry( self.selection.origin.x(), self.selection.origin.y(), x - self.selection.origin.x() + 1, y - self.selection.origin.y() + 1 )
		elif x < self.selection.origin.x() and y >= self.selection.origin.y():
			self.selection.setGeometry( x, self.selection.origin.y(), self.selection.origin.x() - x + 1, y - self.selection.origin.y() + 1 )
		elif x < self.selection.origin.x() and y < self.selection.origin.y():
			self.selection.setGeometry( x, y, self.selection.origin.x() - x + 1, self.selection.origin.y() - y + 1 )
		elif x >= self.selection.origin.x() and y < self.selection.origin.y():
			self.selection.setGeometry( self.selection.origin.x(), y, x - self.selection.origin.x() + 1, self.selection.origin.y() - y + 1 )
		else:
			self.selection.setGeometry( xorig, yorig, 1, 1 )

		self.selection.show()

	def moveSelection(self, xevent, yevent):

		# En la imagen
		x = xevent / self.data.zoom
		y = yevent / self.data.zoom

		xx = self.selectionGrabPoint.x()
		yy = self.selectionGrabPoint.y()

		self.selection.setGeometry(x - xx, y - yy, self.selection.rect.width(), self.selection.rect.height())