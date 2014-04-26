#!/usr/bin/env python
#coding: utf-8

from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import Qt
import random

from mainwidget import MainWidget
from dialogs import ResizeImageDialog, NewFileDialog, Preferences
from palette import Palette


class Preview (QtGui.QDockWidget):

	def __init__(self, title, data, com, Parent=None):

		super(Preview, self).__init__(title, Parent)

		self.data = data
		self.com = com
		self.parent = Parent
		self.setAllowedAreas(Qt.RightDockWidgetArea)

		self.label = QtGui.QLabel()
		self.label.setPixmap(QtGui.QPixmap.fromImage(self.data.image))
		self.layout = QtGui.QHBoxLayout()
		self.layout.addWidget(self.label)
		self.label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
		self.layout.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
		self.setWidget(self.label)
		self.update()

		self.com.updateCanvas.connect(self.update)

	def update(self):

		super(Preview, self).update()
		if self.data.image.width() > 128 or self.data.image.height() > 128:
			imatge = self.data.image.scaled(128, 128, Qt.KeepAspectRatio)
			self.label.setPixmap(QtGui.QPixmap.fromImage(imatge))
		else:
			self.label.setPixmap(QtGui.QPixmap.fromImage(self.data.image))

		print "Updating Preview"

	def setPixmap(self):

		if self.data.image.width() > 128 or self.data.image.height() > 128:
			imatge = self.data.image.scaled(128, 128, Qt.KeepAspectRatio)
			self.label.setPixmap(QtGui.QPixmap.fromImage(imatge))
		else:
			self.label.setPixmap(QtGui.QPixmap.fromImage(self.data.image))


class ToolProperties (QtGui.QDockWidget):

	def __init__(self, title, data, com, Parent=None):

		super(ToolProperties, self).__init__(title, Parent)

		self.data = data
		self.com = com
		self.parent = Parent
		self.setAllowedAreas(Qt.RightDockWidgetArea)
		self.setFeatures(QtGui.QDockWidget.NoDockWidgetFeatures)

		# Llista de widgets (configuració de cada eina del programa)
		self.widgets = self.createWidgets()
		self.com.updateTool.connect(self.updateWidget)

		self.updateWidget()

	def createWidgets(self):

		# Creem una llista amb tots el widgets i la retornem
		l = []

		l.append(QtGui.QWidget())
		l.append(self.createPencilWidget())
		l.append(QtGui.QWidget())
		l.append(QtGui.QWidget())
		l.append(QtGui.QWidget())
		l.append(QtGui.QWidget())
		l.append(self.createGradientWidget())

		return l

	def createPencilWidget(self):

		w = QtGui.QWidget()
		hbox = QtGui.QHBoxLayout()

		pencilSizeLabel = QtGui.QLabel("Size:")
		slider = QtGui.QSlider(QtCore.Qt.Horizontal, self)
		slider.setValue(self.data.pencilSize)
		self.pencilSize = QtGui.QLabel(str(self.data.pencilSize))

		slider.setMaximum(9)
		slider.setMinimum(1)
		slider.setPageStep(1)
		slider.valueChanged.connect(self.setPencilSize)

		hbox.addWidget(pencilSizeLabel)
		hbox.addWidget(slider)
		hbox.addWidget(self.pencilSize)
		hbox.setAlignment(QtCore.Qt.AlignTop)

		w.setLayout(hbox)

		return w

	def setPencilSize(self, size):

		self.pencilSize.setText(str(size))
		self.data.pencilSize = size

	def createGradientWidget(self):

		w = QtGui.QWidget()
		grid = QtGui.QGridLayout()

		label1 = QtGui.QLabel("Color 1:", self)
		label2 = QtGui.QLabel("Color 2:", self)
		self.color1 = DegColor(self.data, self.com, self.data.color_deg_1, 1)
		self.color2 = DegColor(self.data, self.com, self.data.color_deg_2, 2)

		self.color1.com.updateColorDeg.connect(self.setColorDeg)
		self.color1.com.updateColorDeg.connect(self.setColorDeg)

		grid.addWidget(label1,1,1)
		grid.addWidget(self.color1,1,3)
		grid.addWidget(label2,3,1)
		grid.addWidget(self.color2,3,3)
		grid.setRowMinimumHeight(0,3)
		grid.setRowMinimumHeight(2,3)
		grid.setColumnMinimumWidth(0,3)
		grid.setColumnMinimumWidth(2,3)
		grid.setColumnStretch(4,1)
		grid.setRowStretch(4,1)

		w.setLayout(grid)

		return w

	def setColorDeg(self, index):
		if index == 1:
			self.data.color_deg_1 == self.color1.color
		if index == 2:
			self.data.color_deg_2 == self.color2.color

	def updateWidget(self):

		self.setWidget(self.widgets[self.data.currentTool])
		print self.data.currentTool


class PenSizeValueLabel(QtGui.QLabel):

	def setText(self, text):

		super(PenSizeValueLabel, self).setText(str(text))


class CurrentColor(QtGui.QLabel):

	def __init__(self, data, com, Parent=None):

		super(CurrentColor, self).__init__(Parent)

		self.data = data
		self.com = com
		self.color = QtGui.QColor( random.randint(0,255), random.randint(0,255),random.randint(0,255) )
		self.setFixedSize(32,32)
		self.setPalette(QtGui.QPalette(self.color))
		self.setAutoFillBackground(True)
		self.parent = Parent
		self.data.color = self.color

		self.com.updateColor.connect(self.update)

	def paintEvent(self, e):

		painter = QtGui.QPainter(self)	
		painter.setBackgroundMode(Qt.OpaqueMode)
		brush = QtGui.QBrush(self.color)
		painter.setBrush(brush)
		painter.fillRect(0,0,self.width(),self.height(),brush)

		super(CurrentColor, self).paintEvent(e)

	def mousePressEvent(self, e):

		if e.button() == Qt.LeftButton:
			c = QtGui.QColorDialog.getColor(self.color, self)
			if c.isValid():
				self.data.color = c
				self.com.updateColor.emit()

	def update(self):

		self.color = self.data.color
		super(CurrentColor, self).update()


class Color(QtGui.QFrame):
	"""
	"""

	def __init__(self, data, com, Parent=None):

		super(Color, self).__init__(Parent)

		self.data = data
		self.com = com
		self.color = QtGui.QColor( random.randint(0,255), random.randint(0,255),random.randint(0,255) )
		self.setFixedSize(16,16)
		self.setPalette(QtGui.QPalette(self.color))
		self.setAutoFillBackground(True)
		self.parent = Parent

	def paintEvent(self, e):

	
		painter = QtGui.QPainter(self)	
		painter.setBackgroundMode(Qt.OpaqueMode)
		brush = QtGui.QBrush(self.color)
		painter.setBrush(brush)
		painter.fillRect(0,0,self.width(),self.height(),brush)

		super(Color, self).paintEvent(e)

	def mousePressEvent(self, e):

		if e.button() == Qt.LeftButton:
			#self.setFrameStyle(QtGui.QFrame.Box)
			#self.setFrameShadow(QtGui.QFrame.Plain)
			#self.setLineWidth(2)
			self.data.color = self.color
			self.com.updateColor.emit()
		elif e.button() == Qt.RightButton:
			c = QtGui.QColorDialog.getColor(self.color, self)
			if c.isValid():
				self.color = c
				self.update()

class DegColor(Color):

	def __init__(self, data, com, color, index, Parent = None):

		super(DegColor,self).__init__(data, com, Parent)

		self.color = color
		self.indx = index

	def mousePressEvent(self, e):

		if e.button() == Qt.LeftButton:
			c = QtGui.QColorDialog.getColor(self.color, self)
			if c.isValid():
				self.color = c
				self.update()
				self.com.updateColorDeg.emit(self.index)


class MainWindow(QtGui.QMainWindow):
	"""
	La clase MainWindow es la ventana principal del programa.
	"""

	def __init__(self, data, com):

		super(MainWindow,self).__init__()

		self.com = com
		self.data = data

		self.onClickPalette = False
		self.resize(640,480)
		self.setWindowTitle("Pix2Pics")
		self.statusBar = self.statusBar().showMessage("Ready")
		self.menuBar = self.createMenuBar()
		self.toolBar = self.createToolBar()
		self.createDockWidgets()
		self.mainWidget = MainWidget(128, 96, data, com, Qt.red, self)

		# El Widget alrededor del cual gira la MainWindow es mainWidget
		self.setCentralWidget(self.mainWidget)

		self.show()

	def createToolBarActions(self):

		# Llista d'accions
		l = []

		self.tools = QtGui.QActionGroup(self)

		self.selectionAction = QtGui.QAction(QtGui.QIcon('images/selection.png'), 'Select (W)', self.tools)
		self.selectionAction.setCheckable(True)
		self.selectionAction.toggled.connect(self.setSelectionTool)
		l.append(self.selectionAction)

		self.pencilAction = QtGui.QAction(QtGui.QIcon('images/pencil.png'), 'Pencil (N)', self.tools)
		self.pencilAction.setCheckable(True)
		self.pencilAction.toggled.connect(self.setPencilTool)
		self.pencilAction.toggle()
		l.append(self.pencilAction)

		self.brushAction = QtGui.QAction(QtGui.QIcon('images/brush.png'), 'Brush (B)', self.tools)
		self.brushAction.setCheckable(True)
		self.brushAction.toggled.connect(self.setBrushTool)
		l.append(self.brushAction)

		self.eraserAction = QtGui.QAction(QtGui.QIcon('images/eraser.png'), 'Eraser (E)', self.tools)
		self.eraserAction.setCheckable(True)
		self.eraserAction.toggled.connect(self.setEraserTool)
		l.append(self.eraserAction)

		self.colorPickerAction = QtGui.QAction(QtGui.QIcon('images/dropper.png'), 'Color Picker (C)', self.tools)
		self.colorPickerAction.setCheckable(True)
		self.colorPickerAction.toggled.connect(self.setColorPickerTool)
		l.append(self.colorPickerAction)

		self.zoomInAction = QtGui.QAction(QtGui.QIcon('images/zoomin.png'), 'Zoom In (+)', self.tools)
		self.zoomInAction.setShortcut("+")
		self.zoomInAction.triggered.connect(self.zoomIn)
		l.append(self.zoomInAction)

		self.zoomOutAction = QtGui.QAction(QtGui.QIcon('images/zoomout.png'), 'Zoom Out (+)', self.tools)
		self.zoomOutAction.setShortcut("-")
		self.zoomOutAction.triggered.connect(self.zoomOut)
		l.append(self.zoomOutAction)

		self.fillAction = QtGui.QAction(QtGui.QIcon('images/fill.png'), 'Fill (F)', self.tools)
		self.fillAction.setCheckable(True)
		self.fillAction.toggled.connect(self.setFillTool)
		l.append(self.fillAction)

		self.fillAction = QtGui.QAction(QtGui.QIcon('images/gradient.png'), 'Gradient (D)', self.tools)
		self.fillAction.setCheckable(True)
		self.fillAction.toggled.connect(self.setDegTool)
		l.append(self.fillAction)

		return l

	def createToolBar(self):

		toolBar = QtGui.QToolBar()
		l = self.createToolBarActions()

		for i in l:
			toolBar.addAction(i)

		toolBar.setMovable(False)
		toolBar.setOrientation(Qt.Vertical)
		self.addToolBar(Qt.LeftToolBarArea, toolBar)

		return toolBar

	def createFileActions(self):

		# Llistes de propietats (de cada acció)
		icons = ["document-new.png", "document-open.png", "document-save.png", "document-save-as.png", "application-exit.png"]
		labels = ["&New", "&Open", "&Save", "Save &As...", "&Exit"]
		shortcuts = ['Ctrl+N', 'Ctrl+O', 'Ctrl+S', 'Ctrl+Shift+S', 'Ctrl+Q']
		statusTips = [ "Create a new image", "Open an existing image", "Save the current image", "Saves as a new image", "Exit application"]
		connects = [self.showNewFileDialog,self.openFile,self.saveFile,self.saveFileAs,QtGui.qApp.quit]
		#connects = [0,0,0,0,0]

		# Llista d'accions
		l = []

		for i in range(len(labels)):
			a = QtGui.QAction(QtGui.QIcon("images/" + icons[i]), labels[i], self)
			a.setShortcut(shortcuts[i])
			a.setStatusTip(statusTips[i])
			if connects[i] != 0: a.triggered.connect(connects[i])
			l.append(a)

		# Insertem els zeros que simbolitzen separadors
		l.insert(4,0)

		return l

	def createEditActions(self):

		# Llistes de propietats (de cada acció)
		icons = ["edit-undo.png", "edit-redo.png", "edit-cut.png", "edit-copy.png", "edit-paste.png", "edit-clear.png", "document-properties.png"]
		labels = ["&Undo", "&Redo", "Cu&t", "&Copy", "&Paste", "C&lear", "&Preferences"]
		shortcuts = ['Ctrl+Z', 'Ctrl+Y', 'Ctrl+X', 'Ctrl+C', 'Ctrl+V', 'Del', '']
		statusTips = ["Undo the last action", "Redo the last action", "Cut a part of the image", "Copy a part of the image", "Paste an image into this one", "Clear out a part of the image", "Open the preferences dialog"]
		connects = [0,0,0,0,0,0, self.showPreferences]

		# Llista d'accions
		l = []

		for i in range(len(labels)):
			a = QtGui.QAction(QtGui.QIcon("images/" + icons[i]), labels[i], self)
			a.setShortcut(shortcuts[i])
			a.setStatusTip(statusTips[i])
			if connects[i] != 0: a.triggered.connect(connects[i])
			l.append(a)

		# Insertem els zeros que simbolitzen separadors
		l.insert(2,0)
		l.insert(7,0)

		return l

	def createImageActions(self):

		# Llistes de propietats (de cada acció)
		icons = ["resize-image.png"]
		labels = ["&Resize..."]
		shortcuts = ['Ctrl+R']
		statusTips = ["Adjust the image size"]
		connects = [self.showResizeImageDialog]

		# Llista d'accions
		l = []

		for i in range(len(labels)):
			a = QtGui.QAction(QtGui.QIcon("images/" + icons[i]), labels[i], self)
			a.setShortcut(shortcuts[i])
			a.setStatusTip(statusTips[i])
			if connects[i] != 0: a.triggered.connect(connects[i])
			l.append(a)

		return l

	def createHelpActions(self):

		# Llistes de propietats (de cada acció)
		icons = ["help-contents.png", "help-about.png"]
		labels = ["&Contents", "&About"]
		shortcuts = ['Ctrl+H', 'Ctrl+B']
		statusTips = ["Show the Help dialog", "About PixelART..."]
		connects = [0, self.showAboutDialog]

		# Llista d'accions
		l = []

		for i in range(len(labels)):
			a = QtGui.QAction(QtGui.QIcon("images/" + icons[i]), labels[i], self)
			a.setShortcut(shortcuts[i])
			a.setStatusTip(statusTips[i])
			l.append(a)

		# Insertem els zeros que simbolitzen separadors
		l.insert(1,0)

		return l

	def createMenuBar(self):
		
		menubar = self.menuBar()
		fileMenu = menubar.addMenu('&File')
		editMenu = menubar.addMenu('&Edit')
		imageMenu = menubar.addMenu('&Image')
		helpMenu = menubar.addMenu('&Help')
		fileActions = self.createFileActions()
		editActions = self.createEditActions()
		imageActions = self.createImageActions()
		helpActions = self.createHelpActions()
		for i in fileActions:
			if i == 0: fileMenu.addSeparator()
			else: fileMenu.addAction(i)
		for i in editActions:
			if i == 0: editMenu.addSeparator()
			else: editMenu.addAction(i)
		for i in helpActions:
			if i == 0: helpMenu.addSeparator()
			else: helpMenu.addAction(i)
		for i in imageActions:
			if i == 0: imageMenu.addSeparator()
			else: imageMenu.addAction(i)

		return menubar
		
	def createDockWidgets(self):
		
		# Palette widget

		self.palette = QtGui.QDockWidget("Palette", self)
		self.palette.setAllowedAreas(Qt.RightDockWidgetArea)
		self.palette.setFeatures(QtGui.QDockWidget.NoDockWidgetFeatures)

		paletteWidget = QtGui.QWidget()
		hbox = QtGui.QHBoxLayout()
		grid = QtGui.QGridLayout()

		self.currentColor = CurrentColor(self.data, self.com, self)
		
		i = 0
		j = 0
		for k in range(12):
			c = Color(self.data, self.com, self)
			grid.addWidget(c,j,i)
			i += 1
			if j == 0 and i > 5:
				j = 1
				i = 0

		hbox.addWidget(self.currentColor)
		hbox.addLayout(grid)
		hbox.setSizeConstraint(QtGui.QLayout.SetMaximumSize)
		grid.setSizeConstraint(QtGui.QLayout.SetMaximumSize)
		hbox.setSpacing(0)
		grid.setSpacing(0)
		paletteWidget.setLayout(hbox)

		paletteWidgetNew = Palette(self.data, self.com)

		self.palette.setWidget(paletteWidget)
		#self.palette.setWidget(paletteWidgetNew) # NUEVA Paleta

		self.addDockWidget(Qt.RightDockWidgetArea, self.palette)

		# Tool Properties widget

		self.toolProperties = ToolProperties("Tool Properties", self.data, self.com)
		self.addDockWidget(Qt.RightDockWidgetArea, self.toolProperties)

		# Preview

		self.preview = Preview("Preview", self.data, self.com, self)
		self.addDockWidget(Qt.RightDockWidgetArea, self.preview)
		
	def zoomIn(self):

		if self.data.zoom < 25:
			self.data.zoom += 2
			#self.mainWidget.canvas.setFixedSize(self.data.image.width()*self.data.zoom, self.data.image.height()*self.data.zoom)
			self.scaleImage(self.data.zoom)
			self.mainWidget.canvas.update()

	def zoomOut(self):

		if self.data.zoom > 1:
			self.data.zoom -= 2
			#self.mainWidget.canvas.setFixedSize(self.data.image.width()*self.data.zoom, self.data.image.height()*self.data.zoom)
			self.scaleImage(self.data.zoom)
			self.mainWidget.canvas.update()

	def scaleImage(self, zoom):
		
		self.mainWidget.canvas.resize(zoom * self.mainWidget.canvas.pixmap().size())

		self.adjustScrollBar(self.mainWidget.horizontalScrollBar(), zoom)
		self.adjustScrollBar(self.mainWidget.verticalScrollBar(), zoom)
		
	def adjustScrollBar(self, scrollBar, zoom):

		scrollBar.setValue(int(zoom * scrollBar.value() + ((zoom - 1) * scrollBar.pageStep()/2)))
		print zoom

	def showResizeImageDialog(self):

		d = ResizeImageDialog(self)

	def resizeImage(self, width, height):
		
		self.data.image = self.data.image.scaled(width, height)
		self.com.newImage.emit()
		
	def setPencilSize(self, size):

		self.pencilSize.setText(str(size))
		self.data.pencilSize = size

	def setSelectionTool(self):

		self.data.currentTool = 0
		self.com.updateTool.emit()

	def setPencilTool(self):

		self.data.currentTool = 1
		self.com.updateTool.emit()

	def setBrushTool(self):

		self.data.currentTool = 2
		self.com.updateTool.emit()

	def setEraserTool(self):

		self.data.currentTool = 3
		self.com.updateTool.emit()

	def setColorPickerTool(self):

		self.data.currentTool = 4
		self.com.updateTool.emit()

	def setFillTool(self):

		self.data.currentTool = 5
		self.com.updateTool.emit()

	def setDegTool(self):

		self.data.currentTool = 6
		self.com.updateTool.emit()

	def showNewFileDialog(self):

		d = NewFileDialog(self)

	def showAboutDialog(self):

		d = QtGui.QMessageBox.about(self, "About Pix2Pics...", "Pix2Pics is a Pixel Art that serves all purposes, from creating sprites and tiles to editing simple images.")
		d.show()

	def showPreferences(self):

		d = Preferences(self)

	def newImage(self, w, h):

		self.data.newImage(w, h)

	def openFile(self):
		
		fileName = QtGui.QFileDialog.getOpenFileName(self,
					"Open an existing image",
					"/home",
					"Images (*.bmp *.gif *.png *.xpm *.jpg);;All Files (*)")
		if fileName:
			#print fileName
			self.data.loadImage(fileName)

	def saveFile(self):

		if self.data.defaultFileName == "":
			self.saveFileAs()
		else:	
			self.data.image.save(self.data.defaultFileName)

	def saveFileAs(self):

		d = QtGui.QFileDialog()
		fileName, filterName = d.getSaveFileNameAndFilter(self,
					"Save the current image", 
					"", 
					"*.bmp;;*.gif;;*.png;;*.xpm;;*.jpg")
		self.data.image.save(fileName+filterName[1:])
		self.data.defaultFileName = fileName + filterName[1:]

	def keyPressEvent(self, event):

		super(MainWindow, self).keyPressEvent(event)

		if event.key() == Qt.Key_Control:
			self.onClickPalette = True
			QtCore.QCoreApplication.instance().setOverrideCursor(self.data.colorPickerCur)
			self.grabMouse()

	def keyReleaseEvent(self, event):

		super(MainWindow, self).keyReleaseEvent(event)

		if event.key() == Qt.Key_Control:
			self.onClickPalette = False
			QtCore.QCoreApplication.instance().restoreOverrideCursor()
			self.releaseMouse()

	def mousePressEvent(self, event):

		super(MainWindow, self).mousePressEvent(event)

		# --- Paleta "onClick" ---
		# Cuando pulsamos Ctrl y hacemos click con el mouse creamos una captura de pantalla.
		# Luego de esa captura extraemos el color en la posición del cursor y lo establecemos
		# como color principal.
		if event.button() == QtCore.Qt.LeftButton and self.onClickPalette:
			widget = QtCore.QCoreApplication.instance().desktop().screen()
			im = QtGui.QPixmap.grabWindow(widget.winId()).toImage() # Captura de pantalla
			c = QtGui.QColor(im.pixel(QtGui.QCursor.pos())) # Cogemos el color de la posición del cursor
			self.data.changeColor(c) # Cambiamos el color actual por el que hemos cogido

			# im.save("desktop.png") # Guardar la captura de pantalla en un archivo
			# print "Getting color " + c.red(), c.green(), c.blue() + " from screen" # Comprueba qué color coge

	def mouseMoveEvent(self, event):

		super(MainWindow, self).mouseMoveEvent(event)
		# Lo mismo de antes pero para cuando el ratón se mueve
		if self.onClickPalette and event.buttons() == QtCore.Qt.LeftButton:
			widget = QtCore.QCoreApplication.instance().desktop().screen()
			im = QtGui.QPixmap.grabWindow(widget.winId()).toImage()
			c = QtGui.QColor(im.pixel(QtGui.QCursor.pos()))
			self.data.changeColor(c)