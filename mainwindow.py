#!/usr/bin/env python
#coding: utf-8

from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import Qt
import os, random

from preview import Preview
from toolproperties import ToolProperties
from mainwidget import MainWidget
from palette import Palette

from dialogs import *


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
		self.com.overCanvas.connect(self.setImagePosition)

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

		tools = ["selection", "pencil", "eraser", "colorpicker", "fill", "gradient", "exchange"]
		connects = [self.setSelectionTool, self.setPencilTool, self.setEraserTool, self.setColorPickerTool, self.setFillTool, self.setGradientTool, self.setExchangeTool]
		shortcuts = ['Z', 'X', 'C', 'A', 'S', 'D', '']

		for i in range(len(tools)):
			a = QtGui.QAction(QtGui.QIcon( os.path.join("themes", self.data.theme, tools[i] + ".png") ), self.data.getText("tools", tools[i]) + " (" + shortcuts[i] + ")", self.tools)
			a.setCheckable(True)
			a.setShortcut(shortcuts[i])
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
			if j == 6:
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
		connects = [self.showNewFileDialog, self.openFile, self.saveFile, self.saveFileAs, self.close]

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
		ids = ["undo", "redo", "selectall", "deselect", "invert", "cut", "copy", "paste", "clear", "preferences"]
		icons = ["edit-undo.png", "edit-redo.png", "", "", "", "edit-cut.png", "edit-copy.png", "edit-paste.png", "edit-clear.png", "document-properties.png"]
		shortcuts = ['Ctrl+Z', 'Ctrl+Y', "", "", "", 'Ctrl+X', 'Ctrl+C', 'Ctrl+V', 'Del', '']
		connects = [self.undo, self.redo, 0, 0, 0, self.cut, self.copy, self.paste, self.clear, self.showPreferences]

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
		l.insert(6,0)
		l.insert(11,0)

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
		connects = [self.showHelp, self.showAboutDialog]

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

		scrollBar.setValue((scrollBar.maximum() - scrollBar.minimum()) / 2)

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
			self.statusBar.insertWidget(0, self.imagePosLabel, 0)
			self.imagePosLabel.show()
			#self.imagePosLabel.move(self.statusBar.width()/2,self.imagePosLabel.y())

	def hideImagePosition(self):

		self.statusBar.removeWidget(self.imagePosLabel)

	def setImagePosition(self, x, y):

		self.imagePosLabel.setText("  Pos: (" + str(x) + ", " + str(y) + ")")
	
	def showNewFileDialog(self):

		d = NewFileDialog(self.data, self)

	def showHelp(self):

		url = QtCore.QUrl("http://nataczajohnson.wix.com/pixs2pics#!page3/cee5")
		QtGui.QDesktopServices.openUrl(url)

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

		if self.data.posHistory > 0:
			self.data.posHistory -= 1
			self.data.image = QtGui.QImage(self.data.history[self.data.posHistory])
			self.com.updateCanvas.emit()
			self.com.resizeCanvas.emit()

	def redo(self):

		if self.data.posHistory < len(self.data.history)-1:
			self.data.posHistory += 1
			self.data.image = QtGui.QImage(self.data.history[self.data.posHistory])
			self.com.updateCanvas.emit()
			self.com.resizeCanvas.emit()

	def cut(self):

		self.com.cutImage.emit()

	def copy(self):

		self.com.copyImage.emit()

	def paste(self):

		clipboard = QtGui.QApplication.clipboard()
		if not clipboard.image().isNull():
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

		if self.onClickPalette:
			if event.delta() > 0:
				self.zoomIn()
			else:
				self.zoomOut()

		super(MainWindow, self).wheelEvent(event)

	def closeEvent(self, event):

		reply = QtGui.QMessageBox.warning(self, self.data.getText("dialog_exit", "title"),
			self.data.getText("dialog_exit", "message"),
			QtGui.QMessageBox.Save | QtGui.QMessageBox.Discard | QtGui.QMessageBox.Cancel,
			QtGui.QMessageBox.Save)
		if reply == QtGui.QMessageBox.Discard:
			event.accept()
		elif reply == QtGui.QMessageBox.Cancel:
			event.ignore()  
			return 
		elif reply == QtGui.QMessageBox.Save:
			self.saveFile()
			event.accept()

		self.data.saveDefaults()

		super(MainWindow, self).closeEvent(event)
