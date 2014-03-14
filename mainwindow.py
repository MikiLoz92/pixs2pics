#!/usr/bin/env python
#coding: utf-8

from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import Qt
from mainwidget import MainWidget
from dialogs import *
from canvas import *
from image import *

import random

class Color(QtGui.QFrame):
	"""
	"""

	def __init__(self, Parent=None):

		super(Color, self).__init__(Parent)

		self.color = QtGui.QColor( random.randint(0,255), random.randint(0,255),random.randint(0,255) )
		self.setFixedSize(16,16)
		self.setPalette(QtGui.QPalette(self.color))
		self.setAutoFillBackground(True)

	def paintEvent(self, e):

	
		painter = QtGui.QPainter(self)	
		painter.setBackgroundMode(Qt.OpaqueMode)
		brush = QtGui.QBrush(self.color)
		painter.setBrush(brush)
		painter.fillRect(0,0,self.width(),self.height(),brush)

		super(Color, self).paintEvent(e)

	def mousePressEvent(self, e):

		if e.button() == Qt.LeftButton:
			self.setFrameStyle(QtGui.QFrame.Box)
			self.setFrameShadow(QtGui.QFrame.Plain)
			self.setLineWidth(2)
		elif e.button() == Qt.RightButton:
			c = QtGui.QColorDialog.getColor(self.color, self)
			if c.isValid():
				self.color = c
				self.update()

			      
## Vista/View
class MainWindow(QtGui.QMainWindow):
	"""
	La clase MainWindow es la ventana principal del programa.
	"""

	def __init__(self, image, com):

		super(MainWindow,self).__init__()
		self.com = com

		self.resize(640,480)
		self.setWindowTitle("PixelArt")
		self.statusBar = self.statusBar().showMessage("Ready")

		self.menuBar = self.createMenuBar()

		self.mainWidget = MainWidget(128, 96, image, com, Qt.red, self)
		
		selectAction = QtGui.QAction(QtGui.QIcon('images/marquee.png'), 'Select (W)', self)
		pencilAction = QtGui.QAction(QtGui.QIcon('images/pencil.png'), 'Pencil (N)', self)
		zoomInAction = QtGui.QAction(QtGui.QIcon('images/zoomin.png'), 'Zoom In (+)', self)
		zoomInAction.setShortcut("+")
		zoomInAction.triggered.connect(self.mainWidget.canvas.zoomIn)
		zoomOutAction = QtGui.QAction(QtGui.QIcon('images/zoomout.png'), 'Zoom Out (+)', self)
		zoomOutAction.setShortcut("-")
		zoomOutAction.triggered.connect(self.mainWidget.canvas.zoomOut)
		toolbar = QtGui.QToolBar()
		toolbar.addAction(selectAction)
		toolbar.addAction(pencilAction)
		toolbar.addAction(zoomInAction)
		toolbar.addAction(zoomOutAction)
		self.addToolBar(Qt.LeftToolBarArea, toolbar)

		# El Widget alrededor del cual gira la MainWindow es mainWidget
		self.setCentralWidget(self.mainWidget)

		# Creamos los DockWidgets de la derecha
		self.createDockWidgets()

		# Podemos fijar o dejar libre la Toolbar
		toolbar.setMovable(False)
		toolbar.setOrientation(Qt.Vertical)

		self.show()

	def createMenuBar(self):

		menubar = self.menuBar()
		fileMenu = menubar.addMenu('&File')
		editMenu = menubar.addMenu('&Edit')
		helpMenu = menubar.addMenu('&Help')
		fileActions = self.createFileActions()
		editActions = self.createEditActions()
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

		return menubar

	def createFileActions(self):

		# Llistes de propietats (de cada acció)
		icons = ["document-new.png", "document-open.png", "document-save.png", "document-save-as.png", "application-exit.png"]
		labels = ["&New", "&Open", "&Save", "Save &As...", "&Exit"]
		shortcuts = ['Ctrl+N', 'Ctrl+O', 'Ctrl+S', 'Ctrl+Shift+S', 'Ctrl+Q']
		statusTips = [ "Create a new image", "Open an existing image", "Save the current image", "Saves as a new image", "Exit application"]
		connects = [self.showNewFileDialog,self.openFile,self.saveFile,0,QtGui.qApp.quit]

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

	def createDockWidgets(self):

		self.paletteDW = QtGui.QDockWidget("Palette", self)
		self.paletteDW.setAllowedAreas(Qt.RightDockWidgetArea)
		self.paletteDW.setFeatures(QtGui.QDockWidget.NoDockWidgetFeatures)

		self.palette = QtGui.QWidget()
		grid = QtGui.QGridLayout()
		grid.setSizeConstraint(QtGui.QLayout.SetMaximumSize)
		self.palette.setLayout(grid)
		grid.setOriginCorner(Qt.TopLeftCorner)
		
		i = 0
		j = 0
		for k in range(16):
			c = Color(self)
			grid.addWidget(c,j,i)
			i += 1
			if j == 0 and i > 7:
				j = 1
				i = 0

		grid.setSpacing(0)
		#d.setSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
		#d.setFixedSize(grid.minimumSize())
		self.paletteDW.setWidget(self.palette)

		self.addDockWidget(Qt.RightDockWidgetArea, self.paletteDW)

		d = QtGui.QDockWidget("Tool Properties", self)
		d.setAllowedAreas(Qt.RightDockWidgetArea)
		self.addDockWidget(Qt.RightDockWidgetArea, d)

	def createNewImage(self):

		self.mainWidget.canvas = Canvas(32, 32, Image(self.com), self.com, Qt.green, self)

	def showNewFileDialog(self):

		d = NewFileDialog(self)

	def openFile(self):
		
		fileName = QtGui.QFileDialog.getOpenFileName(self,
					"Open an existing image",
					"/home",
					"Images (*.bmp, *.gif, *.png, *.xpm *.jpg);;All Files (*)")
		if fileName:
			print fileName

	def saveFile(self):

		fileName = QtGui.QFileDialog.getSaveFileName(self,
					"Save the current image", 
					"", 
					"*.bmp;;*.gif;;*.png;;*.xpm;;*.jpg")

