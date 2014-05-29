#!/usr/bin/env python
#coding: utf-8

import ConfigParser

from PyQt4 import QtGui, QtCore
from translation import *
from brushes import *

## Model / Modelo
class Data:
	"""
	La clase Data contiene todos los datos, parámetros y configuraciones
	de la aplicación. Por ejemplo, contiene la lista de píxeles pintados en
	la imagen con su correspondiente color. También guarda las variables de
	la anchura del làpiz, los colores en la paleta, el color seleccionado
	actualmente, la altura y anchura de la imagen, etc.
	"""

	color = QtCore.Qt.red

	palette = []
	defaultPalette = [[14, 53, 75], [0, 76, 115], [18, 121, 174], [49, 162, 238], [136, 199, 234], [27, 52, 43],
	                  [30, 85, 55], [69, 145, 26], [121, 191, 29], [190, 222, 44], [69, 18, 18], [113, 31, 31],
	                  [184, 37, 53], [220, 81, 115], [255, 159, 182], [39, 20, 67], [105, 28, 99], [173, 81, 185],
	                  [184, 152, 208], [53, 48, 36], [89, 66, 40], [140, 92, 77], [208, 128, 112], [229, 145, 49],
	                  [247, 176, 114], [252, 215, 142], [0, 0, 0], [33, 33, 33], [79, 79, 79], [179, 179, 179],
	                  [255, 255, 255], [37, 42, 46], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0],
	                  [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0],
	                  [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0],
	                  [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0],
	                  [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]]

	selection = None

	gradient = None

	currentTool = 1

	zoom = 1

	defaultFileName = ""

	colorPicker = False

	ximage = 0
	yimage = 0

	DegState = 1
	DegPoint = 0
	color_deg_1 = QtGui.QColor(QtCore.Qt.white)
	color_deg_2 = QtGui.QColor(QtCore.Qt.black)
	DegAlpha = 255
	save_color = 0

	def __init__(self, com):

		self.com = com

		# Cargamos TODA la configuración
		self.loadDefaults()

		# Cargamos la Paleta
		self.loadPalette()

		# Creamos la QImage
		self.newImage(32,32,QtGui.QColor(255,255,255))

		# Creamos los cursores
		self.pencilCur = QtGui.QCursor(QtGui.QPixmap("images/cursors/penicon.png"), 2, 17)
		self.colorPickerCur = QtGui.QCursor(QtGui.QPixmap("images/cursors/droppericon.png"), 2, 17)
		self.eraserCur = QtGui.QCursor(QtGui.QPixmap("images/cursors/erasericon.png"), 2, 17)
		self.fillCur = QtGui.QCursor(QtGui.QPixmap("images/cursors/fillicon.png"), 1, 14)

		# Generar Bitmaps
		self.circles, self.brushes = createBrushes()

	def loadImage(self, fileName):

		self.defaultFileName = fileName
		self.image = QtGui.QImage(fileName).convertToFormat(QtGui.QImage.Format_ARGB32_Premultiplied)
		if self.image.hasAlphaChannel():
			self.bgColor = QtGui.QColor(0,0,0,0)
		else:
			self.bgColor = QtGui.QColor(255,255,255)
		self.zoom = 1
		self.com.newImage.emit()

	def newImage(self, w, h, bg):

		self.defaultFileName = ""
		self.image = QtGui.QImage(w, h, QtGui.QImage.Format_ARGB32_Premultiplied)
		self.image.fill(bg)
		self.bgColor = bg
		self.zoom = 1
		self.history = [QtGui.QImage(self.image)]
		self.posHistory = 0
		self.com.newImage.emit()
		self.com.updateCanvas.emit()
		self.com.resizeCanvas.emit()

	def paintPoint(self, x, y, color):

		"""
		# Cuadrado
		erasing = (self.currentTool == 2)
		if erasing:
			size = self.eraserSize
		else:
			size = self.pencilSize
		if size%2 == 0: size += 1

		ran = range(-(size-(size/2+1)), size/2+1)

		for i in ran:
			for j in ran:
				self.image.setPixel(x+i, y+j, color.rgba())
		"""
		"""
		# Circular
		erasing = (self.currentTool == 2)
		if erasing:
			m = self.tips[self.eraserSize-1]
			radius = self.eraserSize - 1
		else:
			m = self.tips[self.pencilSize-1]
			radius = self.pencilSize - 1

		for i in range(len(m)):
			for j in range(len(m[i])):
				xx = x+radius-i
				yy = y+radius-j
				if m[i][j] and xx >= 0 and xx < self.image.width() and yy >= 0 and yy < self.image.height():
					self.image.setPixel(xx, yy, color.rgba())
		"""
		"""
		# Qt Ellipses
		erasing = (self.currentTool == 2)
		if erasing: size = (self.eraserSize-1)*2
		else: size = (self.pencilSize-1)*2
		if size > 0:
			painter = QtGui.QPainter(self.image)
			painter.setPen(color);
			painter.setBrush(color);
			path = QtGui.QPainterPath()
			path.addEllipse(QtCore.QRectF(x-size/2,y-size/2,size,size))
			painter.drawPath(path)
		else:
			self.image.setPixel(x, y, color.rgba())
		"""

		# Bitmaps
		erasing = (self.currentTool == 2)
		if erasing:
			m = self.brushes[self.eraserSize-1]
			radius = self.eraserSize - 1
		else:
			m = self.brushes[self.pencilSize-1]
			radius = self.pencilSize - 1
		painter = QtGui.QPainter(self.image)
		painter.setPen(color)
		painter.setCompositionMode(QtGui.QPainter.CompositionMode_Source)
		painter.drawPixmap(QtCore.QPoint(x-radius, y-radius), self.brushes[radius])


	def createBitmaps(self):

		l = []
		l2 = []
		for i in range(9):
			size = i*2
			bitmap = QtGui.QBitmap(size+1, size+1)
			bitmap.clear()
			painter = QtGui.QPainter(bitmap)
			if i == 0: painter.drawPoint(0,0)
			else:
				path = QtGui.QPainterPath()
				path.addEllipse(QtCore.QRectF(0,0,size,size))
				painter.setBrush(QtGui.QColor(0,0,0))
				painter.setPen(QtGui.QColor(0,0,0));
				painter.drawPath(path)
			l.append(bitmap)
			im = bitmap.toImage()
			bmp = []
			for j in range(size+1):
				bmp.append([])
				for k in range(size+1):
					if im.pixel(j, k) == QtGui.QColor(0,0,0).rgb():
						bmp[j].append(True)
					else:
						bmp[j].append(False)
			l2.append(bmp)
		return l

	def changePrimaryColor(self, c):

		#self.color = c
		self.primaryColor = c
		self.com.updateColor.emit()

	def changeSecondaryColor(self, c):

		self.secondaryColor = c
		self.com.updateColor.emit()

	def addHistoryStep(self):

		if self.posHistory != len(self.history)-1:
			self.history = self.history[:self.posHistory+1]
		self.history.append(QtGui.QImage(self.image))
		
		self.posHistory += 1

	def resizeSelection(self, xevent, yevent):

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

	def undo(self): # TODO
		pass

	def redo(self): # TODO
		pass

	def flipHorizontally(self):

		if self.selection != None:
			self.selection.image = self.selection.image.mirrored(True, False)
		else:
			self.image = self.image.mirrored(True, False)
			self.addHistoryStep()

	def flipVertically(self):

		if self.selection != None:
			self.selection.image = self.selection.image.mirrored(False, True)
		else:
			self.image = self.image.mirrored(False, True)
			self.addHistoryStep()

	def rotate90CW(self):

		transform = QtGui.QTransform().rotate(90)
		if self.selection != None:
			self.selection.image = self.selection.image.transformed(transform)
			self.selection.setGeometry(self.selection.rect.x(), self.selection.rect.y(), self.selection.image.width(), self.selection.image.height())
		else:
			self.image = self.image.transformed(transform)
			self.addHistoryStep()

	def rotate90CCW(self):

		transform = QtGui.QTransform().rotate(270)
		if self.selection != None:
			self.selection.image = self.selection.image.transformed(transform)
			self.selection.setGeometry(self.selection.rect.x(), self.selection.rect.y(), self.selection.image.width(), self.selection.image.height())
		else:
			self.image = self.image.transformed(transform)
			self.addHistoryStep()

	def rotate180(self):

		transform = QtGui.QTransform().rotate(180)
		if self.selection != None:
			self.selection.image = self.selection.image.transformed(transform)
		else:
			self.image = self.image.transformed(transform)
			self.addHistoryStep()

	def resizeImage(self, width, height):
		
		self.image = self.image.scaled(width, height)
		self.addHistoryStep()
		self.com.newImage.emit()
		self.com.resizeCanvas.emit()

	def resizeCanvas(self, width, height):

		im = self.image
		self.image = QtGui.QImage(width, height, QtGui.QImage.Format_ARGB32_Premultiplied)
		self.image.fill(self.bgColor)
		painter = QtGui.QPainter(self.image)
		painter.drawImage(QtCore.QPoint(0,0,), im)
		self.addHistoryStep()
		self.com.updateCanvas.emit()
		self.com.resizeCanvas.emit()

	def setPencilSize(self, size):

		if size < 10 and size > 0:
			self.pencilSize = size
			self.com.updatePencilSize.emit(self.pencilSize)

	def setEraserSize(self, size):

		if size < 10 and size > 0:
			self.eraserSize = size
			self.com.updateEraserSize.emit(self.eraserSize)

	def getText(self, sect, ident): # Get some text in the current language

		return self.tdatabase.getText(self.lang, sect, ident).decode("utf-8").replace("\\n", "\n")

	def getTextInLang(self, lang, sect, ident): # Get some text in a specific language

		return self.tdatabase.getText(lang, sect, ident).decode("utf-8")

	def setDefault(self, sect, ident, value):

		try:
			self.cp.set(sect, ident, value)
		except ConfigParser.NoSectionError:
			print "Trying to set \"" + ident + "\" to \"" + str(value) + "\" on section \"" + sect + "\", but given section does not exist. Creating section."
			self.cp.add_section(sect)
			self.cp.set(sect, ident, value)

		f = open("defaults.cfg", "w")
		self.cp.write(f)
		f.close()

	def getDefault(self, sect, ident, default):

		try:
			return self.cp.get(sect, ident)
		except ConfigParser.NoSectionError:
			print "Trying to get value from option \"" + ident + "\" on section \"" + sect + "\", but no section with that name exists. Returning default value."
			return default
		except ConfigParser.NoOptionError:
			print "Trying to get value from option \"" + ident + "\" on section \"" + sect + "\", but specified option does not exist within that section. Returning default value."
			return default

	def getBoolDefault(self, sect, ident, default):

		try:
			return self.cp.getboolean(sect, ident)
		except ValueError:
			print "Trying to get boolean value from option \"" + ident + "\" on section \"" + sect + "\", but given option value is not boolean."
		except ConfigParser.NoSectionError:
			print "Trying to get boolean value from option \"" + ident + "\" on section \"" + sect + "\", but no section with that name exists. Returning default value."
			return default
		except ConfigParser.NoOptionError:
			print "Trying to get boolean value from option \"" + ident + "\" on section \"" + sect + "\", but specified option does not exist within that section. Returning default value."
			return default

	def getIntDefault(self, sect, ident, default):

		try:
			return self.cp.getint(sect, ident)
		except ValueError:
			print "Trying to get integer value from option \"" + ident + "\" on section \"" + sect + "\", but given option value is not an integer."
		except ConfigParser.NoSectionError:
			print "Trying to get integer value from option \"" + ident + "\" on section \"" + sect + "\", but no section with that name exists. Returning default value."
			return default
		except ConfigParser.NoOptionError:
			print "Trying to get integer value from option \"" + ident + "\" on section \"" + sect + "\", but specified option does not exist within that section. Returning default value."
			return default

	def getFloatDefault(self, sect, ident, default):

		try:
			return self.cp.getfloat(sect, ident)
		except ValueError:
			print "Trying to get float value from option \"" + ident + "\" on section \"" + sect + "\", but given option value is not a floating point number."
		except ConfigParser.NoSectionError:
			print "Trying to get float value from option \"" + ident + "\" on section \"" + sect + "\", but no section with that name exists. Returning default value."
			return default
		except ConfigParser.NoOptionError:
			print "Trying to get float value from option \"" + ident + "\" on section \"" + sect + "\", but specified option does not exist within that section. Returning default value."
			return default

	def loadDefaults(self):

		self.cp = ConfigParser.ConfigParser()
		self.cp.read("defaults.cfg")

		self.loadDefaultsLanguage()
		self.loadDefaultsGrid()
		self.loadDefaultsColor()
		self.loadDefaultsTheme()
		self.loadDefaultsPencil()
		self.loadDefaultsEraser()

	def loadDefaultsLanguage(self):

		self.tdatabase = TDatabase()
		lang = self.getDefault("language", "lang", "en")
		if lang in self.tdatabase.langAvailable:
			self.lang = lang
		else:
			self.lang = "en"

	def loadDefaultsGrid(self):

		self.grid = self.getBoolDefault("grid", "grid", False)
		self.matrixGrid = self.getBoolDefault("grid", "matrix_grid", False)
		self.matrixGridWidth = self.getIntDefault("grid", "matrix_grid_width", 16)
		self.matrixGridHeight = self.getIntDefault("grid", "matrix_grid_height", 16)

	def loadDefaultsColor(self):

		self.primaryColor = QtGui.QColor(self.getIntDefault("color", "primary_color", QtCore.Qt.color1))
		self.secondaryColor = QtGui.QColor(self.getIntDefault("color", "secondary_color", QtCore.Qt.color0))

	def loadDefaultsTheme(self):

		self.theme = self.getDefault("theme", "theme", "aquamarine")

	def loadDefaultsPencil(self):

		self.pencilSize = self.getIntDefault("pencil", "size", 1)
		self.secondaryColorEraser = self.getBoolDefault("pencil", "secondary_color_eraser", False)

	def loadDefaultsEraser(self):

		self.eraserSize = self.getIntDefault("eraser", "size", 1)

	def saveDefaults(self):

		self.setDefault("color", "primary_color", self.primaryColor.rgb())
		self.setDefault("color", "secondary_color", self.secondaryColor.rgb())

		self.setDefault("pencil", "size", self.pencilSize)
		self.setDefault("pencil", "secondary_color_eraser", self.secondaryColorEraser)
		self.setDefault("eraser", "size", self.eraserSize)

		self.savePalette()

	def loadPalette(self):

		try:
			f = open("palette.cfg", 'r')
		except IOError:
			print "Cannot open palette.cfg, falling back to default palette."
			self.palette = self.defaultPalette
			return

		l = f.readlines()
		for i in l:
			colors = i[:-1].split(' ')
			red = int(colors[0])
			green = int(colors[1])
			blue = int(colors[2])
			self.palette.append([red, green, blue])
		f.close()

	def savePalette(self):

		f = open("palette.cfg", 'w')
		for i in self.palette:
			f.write(str(i[0]) + " " + str(i[1]) + " " + str(i[2]) + "\n")
		f.close()