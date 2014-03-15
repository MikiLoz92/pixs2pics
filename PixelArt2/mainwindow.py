#!/usr/bin/env python
#coding: utf-8

from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import Qt
from mainwidget import MainWidget
from dialogs import ResizeImageDialog
import random

class PenSizeValueLabel(QtGui.QLabel):

	def setText(self, text):

		super(PenSizeValueLabel, self).setText(str(text))

class CurrentColor(QtGui.QLabel):

	def __init__(self, Parent=None):

		super(CurrentColor, self).__init__(Parent)

		self.color = QtGui.QColor( random.randint(0,255), random.randint(0,255),random.randint(0,255) )
		self.setFixedSize(32,32)
		self.setPalette(QtGui.QPalette(self.color))
		self.setAutoFillBackground(True)
		self.parent = Parent

	def paintEvent(self, e):

		painter = QtGui.QPainter(self)	
		painter.setBackgroundMode(Qt.OpaqueMode)
		brush = QtGui.QBrush(self.color)
		painter.setBrush(brush)
		painter.fillRect(0,0,self.width(),self.height(),brush)
		self.parent.data.color = self.color

		super(CurrentColor, self).paintEvent(e)

	def mousePressEvent(self, e):

		if e.button() == Qt.LeftButton:
			c = QtGui.QColorDialog.getColor(self.color, self)
			if c.isValid():
				self.color = c
				self.update()


class Color(QtGui.QFrame):
	"""
	"""

	def __init__(self, Parent=None):

		super(Color, self).__init__(Parent)

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
			self.parent.currentColor.color = self.color
			self.parent.currentColor.update()
		elif e.button() == Qt.RightButton:
			c = QtGui.QColorDialog.getColor(self.color, self)
			if c.isValid():
				self.color = c
				self.update()


class MainWindow(QtGui.QMainWindow):
	"""
	La clase MainWindow es la ventana principal del programa.
	"""

	def __init__(self, data, com):

		super(MainWindow,self).__init__()

		self.com = com
		self.data = data

		self.resize(640,480)
		self.setWindowTitle("PixelArt")
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

		self.selectAction = QtGui.QAction(QtGui.QIcon('images/marquee.png'), 'Select (W)', self)
		l.append(self.selectAction)

		self.pencilAction = QtGui.QAction(QtGui.QIcon('images/pencil.png'), 'Pencil (N)', self)
		l.append(self.pencilAction)

		self.zoomInAction = QtGui.QAction(QtGui.QIcon('images/zoomin.png'), 'Zoom In (+)', self)
		self.zoomInAction.setShortcut("+")
		self.zoomInAction.triggered.connect(self.zoomIn)
		l.append(self.zoomInAction)

		self.zoomOutAction = QtGui.QAction(QtGui.QIcon('images/zoomout.png'), 'Zoom Out (+)', self)
		self.zoomOutAction.setShortcut("-")
		self.zoomOutAction.triggered.connect(self.zoomOut)
		l.append(self.zoomOutAction)

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
		#connects = [self.showNewFileDialog,self.openFile,self.saveFile,0,QtGui.qApp.quit]
		connects = [0,0,0,0,0]

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
		icons = ["edit-undo.png", "edit-redo.png", "edit-cut.png", "edit-copy.png", "edit-paste.png", "edit-clear.png"]
		labels = ["&Undo", "&Redo", "Cu&t", "&Copy", "&Paste", "C&lear"]
		shortcuts = ['Ctrl+Z', 'Ctrl+Y', 'Ctrl+X', 'Ctrl+C', 'Ctrl+V', 'Del']
		statusTips = ["Undo the last action", "Redo the last action", "Cut a part of the image", "Copy a part of the image", "Paste an image into this one", "Clear out a part of the image"]
		connects = [0,0,0,0,0,0]

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

		self.palette = QtGui.QDockWidget("Palette", self)
		self.palette.setAllowedAreas(Qt.RightDockWidgetArea)
		self.palette.setFeatures(QtGui.QDockWidget.NoDockWidgetFeatures)

		paletteWidget = QtGui.QWidget()
		hbox = QtGui.QHBoxLayout()
		grid = QtGui.QGridLayout()

		self.currentColor = CurrentColor(self)
		
		i = 0
		j = 0
		for k in range(12):
			c = Color(self)
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

		self.palette.setWidget(paletteWidget)
		self.addDockWidget(Qt.RightDockWidgetArea, self.palette)

		self.toolProperties = QtGui.QDockWidget("Tool Properties", self)
		self.toolProperties.setAllowedAreas(Qt.RightDockWidgetArea)
		self.palette.setFeatures(QtGui.QDockWidget.NoDockWidgetFeatures)

		toolPropertiesWidget = QtGui.QWidget()
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
		toolPropertiesWidget.setLayout(hbox)
		hbox.setAlignment(QtCore.Qt.AlignTop)

		self.toolProperties.setWidget(toolPropertiesWidget)
		self.addDockWidget(Qt.RightDockWidgetArea, self.toolProperties)

	def zoomIn(self):

		if self.data.zoom < 15:
			self.data.zoom += 1
			#self.mainWidget.canvas.setFixedSize(self.data.image.width()*self.data.zoom, self.data.image.height()*self.data.zoom)
			self.scaleImage(self.data.zoom)
			self.mainWidget.canvas.update()

	def zoomOut(self):

		if self.data.zoom > 1:
			self.data.zoom -= 1
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

	def setPencilSize(self, size):

		self.pencilSize.setText(str(size))
		self.data.pencilSize = size