#!/usr/bin/env python
#coding: utf-8

from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import Qt
import os, random

from mainwidget import MainWidget
from dialogs import *
from palette import Palette, Color


class Preview (QtGui.QDockWidget):

	def __init__(self, title, data, com, Parent=None):

		super(Preview, self).__init__(title, Parent)

		self.data = data
		self.com = com
		self.parent = Parent
		self.setAllowedAreas(Qt.RightDockWidgetArea)
		self.setFeatures(QtGui.QDockWidget.NoDockWidgetFeatures)

		self.label = QtGui.QLabel()
		self.label.setPixmap(QtGui.QPixmap.fromImage(self.data.image))
		self.label.setObjectName("Preview")
		self.label.setSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Maximum)
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

		#print "Updating Preview"

	def setPixmap(self):

		if self.data.image.width() > 128 or self.data.image.height() > 128:
			imatge = self.data.image.scaled(128, 128, Qt.KeepAspectRatio)
			self.label.setPixmap(QtGui.QPixmap.fromImage(imatge))
		else:
			self.label.setPixmap(QtGui.QPixmap.fromImage(self.data.image))

class SizeLabel (QtGui.QLabel):

	def setValue(self, value):

		self.setText(str(value))


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
		l.append(self.createEraserWidget())
		l.append(QtGui.QWidget())
		l.append(QtGui.QWidget())
		#l.append(self.createGradientWidget())
		l.append(QtGui.QWidget())

		return l

	def createPencilWidget(self):

		w = QtGui.QWidget()
		w.setObjectName("ToolProperties")
		w.setSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Minimum)
		vbox = QtGui.QVBoxLayout()

		hbox1 = QtGui.QHBoxLayout()

		pencilSizeLabel = QtGui.QLabel(self.data.getText("tool_properties_pencil", "size"))
		slider = QtGui.QSlider(QtCore.Qt.Horizontal, self)
		slider.setValue(self.data.pencilSize)
		self.pencilSize = SizeLabel(str(self.data.pencilSize))

		slider.setMaximum(9)
		slider.setMinimum(1)
		slider.setPageStep(1)
		slider.setValue(self.data.pencilSize)
		slider.valueChanged.connect(self.data.setPencilSize)
		slider.valueChanged.connect(self.pencilSize.setValue)
		self.com.updatePencilSize.connect(slider.setValue)

		hbox1.addWidget(pencilSizeLabel)
		hbox1.addWidget(slider)
		hbox1.addWidget(self.pencilSize)

		"""
		hbox2 = QtGui.QHBoxLayout()
		hbox2.addWidget(QtGui.QLabel("Alpha:"))
		alpha = QtGui.QSpinBox()
		alpha.setMinimum(0)
		alpha.setMaximum(255)
		alpha.setValue(255)
		alpha.valueChanged.connect(self.setPencilAlpha)
		alpha.setSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
		hbox2.addWidget(alpha)
		"""
		hbox2 = QtGui.QHBoxLayout()
		print self.data.getText("tool_properties_pencil", "eraser")
		eraser = QtGui.QCheckBox(self.data.getText("tool_properties_pencil", "eraser"), self)
		eraser.setChecked(self.data.secondaryColorEraser)
		eraser.toggled.connect(self.toggleSecondaryColorEraser)
		hbox2.addWidget(eraser)

		vbox.setAlignment(QtCore.Qt.AlignTop)

		vbox.addLayout(hbox1)
		vbox.addLayout(hbox2)
		w.setLayout(vbox)

		return w

	def setPencilSize(self, size):

		self.pencilSize.setText(str(size))
		self.data.pencilSize = size

	def setPencilAlpha(self, alpha):

		self.data.pencilAlpha = alpha

	def toggleSecondaryColorEraser(self):

		self.data.secondaryColorEraser = not self.data.secondaryColorEraser

	def createEraserWidget(self):

		w = QtGui.QWidget()
		w.setSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Minimum)
		vbox = QtGui.QVBoxLayout()

		hbox = QtGui.QHBoxLayout()

		eraserSizeLabel = QtGui.QLabel(self.data.getText("tool_properties_pencil", "size"))
		slider = QtGui.QSlider(QtCore.Qt.Horizontal, self)
		slider.setValue(self.data.eraserSize)
		self.eraserSize = SizeLabel(str(self.data.eraserSize))

		slider.setMaximum(9)
		slider.setMinimum(1)
		slider.setPageStep(1)
		slider.setValue(self.data.eraserSize)
		slider.valueChanged.connect(self.data.setEraserSize)
		slider.valueChanged.connect(self.eraserSize.setValue)
		self.com.updateEraserSize.connect(slider.setValue)

		hbox.addWidget(eraserSizeLabel)
		hbox.addWidget(slider)
		hbox.addWidget(self.eraserSize)

		vbox.setAlignment(QtCore.Qt.AlignTop)

		vbox.addLayout(hbox)
		w.setLayout(vbox)

		return w

	def setEraserSize(self, size):

		self.eraserSize.setText(str(size))
		self.data.eraserSize = size

	def createGradientWidget(self):

		w = QtGui.QWidget()
		grid = QtGui.QGridLayout()

		self.label1 = QtGui.QLabel("Color 1:", self)
		self.label2 = QtGui.QLabel("Color 2:", self)
		self.label3 = QtGui.QLabel("Transparencia:", self)
		self.color1 = DegColor(self.data, self.com, self.data.color_deg_1, 1)
		self.color2 = DegColor(self.data, self.com, self.data.color_deg_2, 2)

		self.DegOp1 = QtGui.QRadioButton("2 Colores")
		self.DegOp2 = QtGui.QRadioButton("1 color a Transparente")
		self.DegOp1.setChecked(True)

		self.AlphaSpin = QtGui.QSpinBox(self) 
		self.AlphaSpin.setMinimum(0)
		self.AlphaSpin.setMaximum(255)
		self.AlphaSpin.setValue(255)
		self.AlphaSpin.valueChanged.connect(self.setAlphaValue)

		hbox = QtGui.QHBoxLayout()
		hbox.addWidget(self.label3)
		hbox.addWidget(self.AlphaSpin)
		hbox.setAlignment(QtCore.Qt.AlignTop)

		self.DegOp1.clicked.connect(self.changeDegState)
		self.DegOp2.clicked.connect(self.changeDegState)

		self.color1.com.updateColorDeg.connect(self.setColorDeg1)
		self.color2.com.updateColorDeg.connect(self.setColorDeg2)

		grid.addWidget(self.label1,1,1)
		grid.addWidget(self.color1,1,3)
		grid.addWidget(self.label2,3,1)
		grid.addWidget(self.color2,3,3)
		grid.addLayout(hbox,5,1,1,3)
		grid.addWidget(self.DegOp1,7,1,1,3)
		grid.addWidget(self.DegOp2,9,1,1,3)

		grid.setRowMinimumHeight(0,3)
		grid.setRowMinimumHeight(2,3)
		grid.setRowMinimumHeight(4,3)
		grid.setRowMinimumHeight(6,8)
		grid.setColumnMinimumWidth(0,3)
		grid.setColumnMinimumWidth(2,3)
		grid.setColumnMinimumWidth(4,1)
		grid.setRowStretch(12,1)

		w.setLayout(grid)

		return w

	def setColorDeg1(self):
		self.data.color_deg_1 = self.color1.color

	def setColorDeg2(self):
		self.data.color_deg_2 = self.color2.color

	def setAlphaValue(self,alpha):
		self.data.DegAlpha = alpha
		print "alpha",alpha

	def changeDegState(self):
		if self.DegOp1.isChecked():
			self.data.DegState = 1
			self.color2.show()
			self.label2.show()
			self.label3.show()
			self.AlphaSpin.show()
		elif self.DegOp2.isChecked():
			self.data.DegState = 2
			self.color2.hide()
			self.label2.hide()
			self.label3.hide()
			self.AlphaSpin.hide()

	def updateWidget(self):

		self.setWidget(self.widgets[self.data.currentTool])
		print self.data.currentTool


class PenSizeValueLabel(QtGui.QLabel):

	def setText(self, text):

		super(PenSizeValueLabel, self).setText(str(text))


class DegColor(Color):

	def __init__(self, data, com, color, index, Parent = None):

		super(DegColor,self).__init__(False, data, com, Parent)

		self.color = color
		self.index = index

	def mousePressEvent(self, e):

		if e.button() == Qt.LeftButton:
			c = QtGui.QColorDialog.getColor(self.color, self)
			if c.isValid():
				self.color = c
				self.update()
				self.com.updateColorDeg.emit()


class MainWindow(QtGui.QMainWindow):
	"""
	La clase MainWindow es la ventana principal del programa.
	"""

	def __init__(self, data, com):

		super(MainWindow,self).__init__()

		self.com = com
		self.data = data

		self.com.enterCanvas.connect(self.showImagePosition)
		self.com.leaveCanvas.connect(self.hideImagePosition)

		self.onClickPalette = False
		self.resize(800,480)
		self.setWindowTitle(self.data.getText("pix2pics", "title"))
		self.statusBar = self.statusBar()
		self.menuBar = self.createMenuBar()
		self.toolBar = self.createToolBar()
		self.createDockWidgets()
		self.mainWidget = MainWidget(128, 96, data, com, Qt.red, self)

		self.imagePosLabel = QtGui.QLabel()
		self.imagePosLabel.setObjectName("ImagePosLabel")

		# El Widget alrededor del cual gira la MainWindow es mainWidget
		self.setCentralWidget(self.mainWidget)

		self.show()

	def createPopupMenu(self):

		pass # Reimplementando esta función conseguimos que no se creen los menús popup cuando hacemos click derecho en toolbars/dockwidgets.

	def createToolBarActions(self):

		# Llista d'accions
		l = []

		self.tools = QtGui.QActionGroup(self)

		#tools = ["selection", "pencil", "eraser", "colorpicker", "fill", "gradient", "exchange"]
		tools = ["selection", "pencil", "eraser", "colorpicker", "fill", "gradient"]
		#connects = [self.setSelectionTool, self.setPencilTool, self.setEraserTool, self.setColorPickerTool, self.setFillTool, self.setGradientTool, self.setExchangeTool]
		connects = [self.setSelectionTool, self.setPencilTool, self.setEraserTool, self.setColorPickerTool, self.setFillTool, self.setGradientTool]

		for i in range(len(tools)):
			a = QtGui.QAction(QtGui.QIcon( os.path.join("themes", self.data.theme, tools[i] + ".png") ), self.data.getText("tools", tools[i]), self.tools)
			a.setCheckable(True)
			if connects[i] != 0: a.toggled.connect(connects[i])
			l.append(a)

		a = QtGui.QAction(QtGui.QIcon( os.path.join("themes", self.data.theme, "zoomin.png") ), self.data.getText("tools", "zoomin"), self.tools)
		a.setShortcut("Ctrl++")
		a.triggered.connect(self.zoomIn)
		l.append(a)

		a = QtGui.QAction(QtGui.QIcon( os.path.join("themes", self.data.theme, "zoomout.png") ), self.data.getText("tools", "zoomout"), self.tools)
		a.setShortcut("Ctrl+-")
		a.triggered.connect(self.zoomOut)
		l.append(a)

		l[self.data.currentTool].setChecked(True)

		return l

	def createToolBar(self):

		toolBar = QtGui.QToolBar()
		l = self.createToolBarActions()

		j = 0
		for i in l:
			toolBar.addAction(i)
			#if j == 6:
			if j == 5:
				toolBar.addSeparator()
			j += 1

		toolBar.setMovable(False)
		toolBar.setOrientation(Qt.Vertical)
		self.addToolBar(Qt.LeftToolBarArea, toolBar)

		return toolBar

	def createFileActions(self):

		# Llistes de propietats (de cada acció)
		ids = ["new", "open", "save", "saveas", "exit"]
		icons = ["document-new.png", "document-open.png", "document-save.png", "document-save-as.png", "application-exit.png"]
		shortcuts = ['Ctrl+N', 'Ctrl+O', 'Ctrl+S', 'Ctrl+Shift+S', 'Ctrl+Q']
		connects = [self.showNewFileDialog, self.openFile, self.saveFile, self.saveFileAs, QtGui.qApp.quit]

		# Llista d'accions
		l = []

		for i in range(len(ids)):
			a = QtGui.QAction(QtGui.QIcon("images/" + icons[i]), self.data.getText("menu_file_labels", ids[i]), self)
			a.setShortcut(shortcuts[i])
			a.triggered.connect(self.restoreFocus)
			a.setStatusTip(self.data.getText("menu_file_status_tips", ids[i]))
			if connects[i] != 0: a.triggered.connect(connects[i])
			l.append(a)

		# Insertem els zeros que simbolitzen separadors
		l.insert(4,0)

		return l

	def createEditActions(self):

		# Llistes de propietats (de cada acció)
		ids = ["undo", "redo", "cut", "copy", "paste", "clear", "preferences"]
		icons = ["edit-undo.png", "edit-redo.png", "edit-cut.png", "edit-copy.png", "edit-paste.png", "edit-clear.png", "document-properties.png"]
		shortcuts = ['Ctrl+Z', 'Ctrl+Y', 'Ctrl+X', 'Ctrl+C', 'Ctrl+V', 'Del', '']
		connects = [self.undo, self.redo, self.cut, self.copy, self.paste, self.clear, self.showPreferences]

		# Llista d'accions
		l = []

		for i in range(len(ids)):
			a = QtGui.QAction(QtGui.QIcon("images/" + icons[i]), self.data.getText("menu_edit_labels", ids[i]), self)
			a.setShortcut(shortcuts[i])
			a.triggered.connect(self.restoreFocus)
			a.setStatusTip(self.data.getText("menu_edit_status_tips", ids[i]))
			if connects[i] != 0: a.triggered.connect(connects[i])
			l.append(a)

		# Insertem els zeros que simbolitzen separadors
		l.insert(2,0)
		l.insert(7,0)

		return l

	def createViewActions(self):

		# Llistes de propietats (de cada acció)
		ids = ["pixel_grid", "matrix_grid"]
		icons = ["", ""]
		shortcuts = ['Ctrl+G', 'Ctrl+M']
		connects = [self.setPixelGrid, self.setMatrixGrid]

		# Llista d'accions
		l = []

		for i in range(len(ids)):
			a = QtGui.QAction(QtGui.QIcon("images/" + icons[i]), self.data.getText("menu_view_labels", ids[i]), self)
			a.setShortcut(shortcuts[i])
			a.triggered.connect(self.restoreFocus)
			a.setStatusTip(self.data.getText("menu_view_status_tips", ids[i]))
			if connects[i] != 0: a.triggered.connect(connects[i])
			a.setCheckable(True)
			l.append(a)

		# Insertem els zeros que simbolitzen separadors
		l.insert(2,0)

		# Algunas opcionas son chekables, lo consideramos:
		l[0].setCheckable(True)
		if self.data.grid: l[0].setChecked(True)
		l[1].setCheckable(True)
		if self.data.matrixGrid: l[1].setChecked(True)

		return l

	def createTransformActions(self):

		# Llistes de propietats (de cada acció)
		ids = ["flip_hor", "flip_ver", "rotate_cw", "rotate_ccw", "rotate_180", "resize", "resize_canvas"]
		icons = ["", "", "", "", "", "", ""]
		shortcuts = ['', '', '', '', '', '', '']
		connects = [self.flipHorizontally,self.flipVertically,self.rotate90CW,self.rotate90CCW,self.rotate180,self.showResizeImageDialog,self.showResizeCanvasDialog]

		# Llista d'accions
		l = []

		for i in range(len(ids)):
			a = QtGui.QAction(QtGui.QIcon("images/" + icons[i]), self.data.getText("menu_transform_labels", ids[i]), self)
			a.setShortcut(shortcuts[i])
			a.triggered.connect(self.restoreFocus)
			a.setStatusTip(self.data.getText("menu_transform_status_tips", ids[i]))
			if connects[i] != 0: a.triggered.connect(connects[i])
			l.append(a)

		l.insert(2,0)
		l.insert(6,0)

		return l

	def createHelpActions(self):

		# Llistes de propietats (de cada acció)
		ids = ["contents", "about"]
		icons = ["help-contents.png", "help-about.png"]
		shortcuts = ['F1', 'Ctrl+B']
		connects = [0, self.showAboutDialog]

		# Llista d'accions
		l = []

		for i in range(len(ids)):
			a = QtGui.QAction(QtGui.QIcon("images/" + icons[i]), self.data.getText("menu_help_labels", ids[i]), self)
			a.setShortcut(shortcuts[i])
			a.triggered.connect(self.restoreFocus)
			a.setStatusTip(self.data.getText("menu_help_status_tips", ids[i]))
			if connects[i] != 0: a.triggered.connect(connects[i])
			l.append(a)

		# Insertem els zeros que simbolitzen separadors
		l.insert(1,0)

		return l

	def restoreFocus(self):

		self.releaseMouse()
		self.releaseKeyboard()
		QtCore.QCoreApplication.instance().restoreOverrideCursor()

	def createMenuBar(self):
		
		menubar = self.menuBar()
		fileMenu = menubar.addMenu(self.data.getText("menu", "file"))
		editMenu = menubar.addMenu(self.data.getText("menu", "edit"))
		viewMenu = menubar.addMenu(self.data.getText("menu", "view"))
		transformMenu = menubar.addMenu(self.data.getText("menu", "transform"))
		helpMenu = menubar.addMenu(self.data.getText("menu", "help"))
		fileActions = self.createFileActions()
		editActions = self.createEditActions()
		viewActions = self.createViewActions()
		transformActions = self.createTransformActions()
		helpActions = self.createHelpActions()
		for i in fileActions:
			if i == 0: fileMenu.addSeparator()
			else: fileMenu.addAction(i)
		for i in editActions:
			if i == 0: editMenu.addSeparator()
			else: editMenu.addAction(i)
		for i in viewActions:
			if i == 0: viewMenu.addSeparator()
			else: viewMenu.addAction(i)
		for i in helpActions:
			if i == 0: helpMenu.addSeparator()
			else: helpMenu.addAction(i)
		for i in transformActions:
			if i == 0: transformMenu.addSeparator()
			else: transformMenu.addAction(i)

		return menubar
		
	def createDockWidgets(self):
		
		# Palette widget

		self.palette = QtGui.QDockWidget(self.data.getText("dock_widgets", "palette"), self)
		self.palette.setAllowedAreas(Qt.RightDockWidgetArea)
		self.palette.setFeatures(QtGui.QDockWidget.NoDockWidgetFeatures)

		paletteWidget = Palette(self.data, self.com)

		self.palette.setWidget(paletteWidget)
		self.palette.setSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Minimum)

		self.addDockWidget(Qt.RightDockWidgetArea, self.palette)

		# Tool Properties widget

		self.toolProperties = ToolProperties(self.data.getText("dock_widgets", "tool_properties"), self.data, self.com)
		self.addDockWidget(Qt.RightDockWidgetArea, self.toolProperties)
		self.palette.setSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Expanding)

		# Preview

		self.preview = Preview(self.data.getText("dock_widgets", "preview"), self.data, self.com, self)
		self.addDockWidget(Qt.RightDockWidgetArea, self.preview)
		
	def zoomIn(self):

		if self.data.zoom < 25:
			self.data.zoom += 1
			#self.mainWidget.canvas.setFixedSize(self.data.image.width()*self.data.zoom, self.data.image.height()*self.data.zoom)
			self.scaleImage(self.data.zoom)
			self.mainWidget.canvas.update()
			self.com.zoom.emit()

	def zoomOut(self):

		if self.data.zoom > 1:
			self.data.zoom -= 1
			#self.mainWidget.canvas.setFixedSize(self.data.image.width()*self.data.zoom, self.data.image.height()*self.data.zoom)
			self.scaleImage(self.data.zoom)
			self.mainWidget.canvas.update()
			self.com.zoom.emit()

	def scaleImage(self, zoom):
		
		#self.mainWidget.canvas.resize(zoom * self.data.image.size())
		self.com.resizeCanvas.emit()

		self.adjustScrollBar(self.mainWidget.horizontalScrollBar(), zoom)
		self.adjustScrollBar(self.mainWidget.verticalScrollBar(), zoom)
		
	def adjustScrollBar(self, scrollBar, zoom):


		#scrollBar.setValue(int(zoom * scrollBar.value() + ((zoom - 1) * scrollBar.pageStep()/2)))
		scrollBar.setValue((scrollBar.maximum() - scrollBar.minimum()) / 2)
		print scrollBar.minimum()
		print scrollBar.maximum()
		print zoom

	def flipHorizontally(self):

		self.data.flipHorizontally()
		self.com.updateCanvas.emit()

	def flipVertically(self):

		self.data.flipVertically()
		self.com.updateCanvas.emit()

	def rotate90CW(self):

		self.data.rotate90CW()
		self.com.updateCanvas.emit()
		if not self.data.selection:
			self.com.newImage.emit()
		
	def rotate90CCW(self):

		self.data.rotate90CCW()
		self.com.updateCanvas.emit()
		if not self.data.selection:
			self.com.newImage.emit()

	def rotate180(self):

		self.data.rotate180()
		self.com.updateCanvas.emit()

	def showResizeImageDialog(self):

		d = ResizeImageDialog(self)

	def showResizeCanvasDialog(self):

		d = ResizeCanvasDialog(self)

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

	def setEraserTool(self):

		self.data.currentTool = 2
		self.com.updateTool.emit()

	def setColorPickerTool(self):

		self.data.currentTool = 3
		self.com.updateTool.emit()

	def setFillTool(self):

		self.data.currentTool = 4
		self.com.updateTool.emit()

	def setGradientTool(self):

		self.data.currentTool = 5
		self.com.updateTool.emit()

	def setExchangeTool(self):

		self.data.currentTool = 6
		self.com.updateTool.emit()

	def showImagePosition(self):

		if self.imagePosLabel.isHidden():
			self.imagePosLabel.setText( str(self.data.ximage) + str(self.data.yimage) )
			self.statusBar.addWidget(self.imagePosLabel)
			self.imagePosLabel.show()
			self.imagePosLabel.move(self.statusBar.width()/2,self.imagePosLabel.y())

	def hideImagePosition(self):

		self.statusBar.removeWidget(self.imagePosLabel)
	
	def showNewFileDialog(self):

		d = NewFileDialog(self.data, self)

	def showAboutDialog(self):

		d = QtGui.QMessageBox.about(self, self.data.getText("dialog_about", "title"), self.data.getText("dialog_about", "description"))

	def showPreferences(self):

		d = Preferences(self.data, self.com, self)

	def newImage(self, w, h):

		self.data.newImage(w, h)

	def openFile(self):
		
		fileName = QtGui.QFileDialog.getOpenFileName(self,
					self.data.getText("dialog_open", "title"),
					"/home",
					self.data.getText("dialog_open", "images") + u" (*.bmp *.gif *.png *.xpm *.jpg);;" + self.data.getText("dialog_open", "all_files") + u" (*)")
		if fileName:
			self.data.loadImage(fileName)

	def saveFile(self):

		if self.data.defaultFileName == "":
			self.saveFileAs()
		else:	
			self.data.image.save(self.data.defaultFileName)

	def saveFileAs(self):

		d = QtGui.QFileDialog()
		fileName, filterName = d.getSaveFileNameAndFilter(self,
					self.data.getText("dialog_save", "title"), 
					"", 
					"*.bmp;;*.gif;;*.png;;*.xpm;;*.jpg")
		self.data.image.save(fileName+filterName[1:])
		self.data.defaultFileName = fileName + filterName[1:]

	def undo(self):

		print "Undo"
		if self.data.posHistory > 0:
			self.data.posHistory -= 1
			print self.data.posHistory
			self.data.image = QtGui.QImage(self.data.history[self.data.posHistory])
			self.com.updateCanvas.emit()
			print self.data.history

	def redo(self):

		print "Redo"
		if self.data.posHistory < len(self.data.history)-1:
			self.data.posHistory += 1
			self.data.image = QtGui.QImage(self.data.history[self.data.posHistory])
			self.com.updateCanvas.emit()

	def cut(self):

		self.com.cutImage.emit()

	def copy(self):

		self.com.copyImage.emit()

	def paste(self):

		clipboard = QtGui.QApplication.clipboard()
		if not clipboard.image().isNull():
			print self.tools.actions()[0].setChecked(True)
			self.com.pasteImage.emit()
			self.com.updateCanvas.emit()

	def clear(self):

		self.com.clearImage.emit()

	def setPixelGrid(self):

		self.data.grid = not self.data.grid
		self.com.updateCanvas.emit()
		self.data.setDefault("grid", "grid", self.data.grid)

	def setMatrixGrid(self):

		self.data.matrixGrid = not self.data.matrixGrid
		self.com.updateCanvas.emit()
		self.data.setDefault("grid", "matrix_grid", self.data.matrixGrid)

	def keyPressEvent(self, event):

		print "KeyPress"
		super(MainWindow, self).keyPressEvent(event)

		if event.key() == Qt.Key_Control:
			self.onClickPalette = True
			QtCore.QCoreApplication.instance().setOverrideCursor(self.data.colorPickerCur)
			self.com.onClickPalette.emit()
			self.grabMouse()
			#self.grabKeyboard()

		elif event.key() == Qt.Key_Plus:
			if self.data.currentTool == 1:
				self.data.setPencilSize(self.data.pencilSize+1)
			elif self.data.currentTool == 2:
				self.data.setEraserSize(self.data.eraserSize+1)

		elif event.key() == Qt.Key_Minus:
			if self.data.currentTool == 1:
				self.data.setPencilSize(self.data.pencilSize-1)
			elif self.data.currentTool == 2:
				self.data.setEraserSize(self.data.eraserSize-1)

		else:
			QtCore.QCoreApplication.instance().restoreOverrideCursor()
			self.releaseMouse()
			self.releaseKeyboard()


	def keyReleaseEvent(self, event):

		super(MainWindow, self).keyReleaseEvent(event)

		if event.key() == Qt.Key_Control:
			self.onClickPalette = False
			QtCore.QCoreApplication.instance().restoreOverrideCursor()
			self.releaseMouse()
			self.releaseKeyboard()

	def mousePressEvent(self, event):

		super(MainWindow, self).mousePressEvent(event)

		# --- Paleta "onClick" ---
		# Cuando pulsamos Ctrl y hacemos click con el mouse creamos una captura de pantalla.
		# Luego de esa captura extraemos el color en la posición del cursor y lo establecemos
		# como color principal.
		if self.onClickPalette:
			widget = QtCore.QCoreApplication.instance().desktop().screen()
			im = QtGui.QPixmap.grabWindow(widget.winId()).toImage() # Captura de pantalla
			c = QtGui.QColor(im.pixel(QtGui.QCursor.pos())) # Cogemos el color de la posición del cursor
			if event.button() == Qt.LeftButton:
				print c.red(), c.green(), c.blue()
				self.data.changePrimaryColor(c) # Cambiamos el color primario actual por el que hemos cogido
			elif event.button() == Qt.RightButton:
				self.data.changeSecondaryColor(c) # Cambiamos el color secundario actual por el que hemos cogido
			# im.save("desktop.png") # Guardar la captura de pantalla en un archivo
			# print "Getting color " + c.red(), c.green(), c.blue() + " from screen" # Comprueba qué color coge

	def mouseMoveEvent(self, event):

		super(MainWindow, self).mouseMoveEvent(event)

		# Lo mismo de antes pero para cuando el ratón se mueve
		if self.onClickPalette:
			widget = QtCore.QCoreApplication.instance().desktop().screen()
			im = QtGui.QPixmap.grabWindow(widget.winId()).toImage() # Captura de pantalla
			c = QtGui.QColor(im.pixel(QtGui.QCursor.pos())) # Cogemos el color de la posición del cursor
			if event.buttons() == Qt.LeftButton:
				self.data.changePrimaryColor(c) # Cambiamos el color primario actual por el que hemos cogido
			elif event.buttons() == Qt.RightButton:
				self.data.changeSecondaryColor(c) # Cambiamos el color secundario actual por el que hemos cogido

	def wheelEvent(self, event):
		print "wheelEvent"

		if self.onClickPalette:
			print "wheelEvent2"
			if event.delta() > 0:
				self.zoomIn()
			else:
				self.zoomOut()

		super(MainWindow, self).wheelEvent(event)

	def closeEvent(self, event):

		self.data.setDefault("color", "primary_color", self.data.primaryColor.rgb())
		self.data.setDefault("color", "secondary_color", self.data.secondaryColor.rgb())

		self.data.savePalette()

		super(MainWindow, self).closeEvent(event)
