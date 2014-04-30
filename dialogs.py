#!/usr/bin/env python
#coding: utf-8

from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import Qt

## Vista/View
class NewFileDialog(QtGui.QDialog):
	"""
	La ventanita que se abre cuando queremos crear un archivo nuevo.
	"""

	def __init__(self, Parent=None):

		super(NewFileDialog,self).__init__(Parent)
		self.parent = Parent

		dimensionGroup = QtGui.QGroupBox(self.parent.data.getText("dialog_new_image", "dimension"))
		dimensionLayout = QtGui.QVBoxLayout()
		self.width = QtGui.QSpinBox(dimensionGroup)
		self.width.setValue(32)
		self.width.setMinimum(1)
		self.width.setMaximum(1024)
		self.height = QtGui.QSpinBox(dimensionGroup)
		self.height.setValue(32)
		self.height.setMinimum(1)
		self.height.setMaximum(1024)
		dimensionLayout.addWidget(self.width)
		dimensionLayout.addWidget(self.height)
		dimensionGroup.setLayout(dimensionLayout)

		backgroundGroup = QtGui.QGroupBox(self.parent.data.getText("dialog_new_image", "background"))
		backgroundLayout = QtGui.QVBoxLayout()
		r1 = QtGui.QRadioButton(self.parent.data.getText("dialog_new_image", "transparent"))
		r1.setChecked(True)
		self.r2 = QtGui.QRadioButton(self.parent.data.getText("dialog_new_image", "color"))
		self.cButton = QtGui.QPushButton()
		self.cButton.clicked.connect(self.getColor)
		colorLayout = QtGui.QHBoxLayout()
		colorLayout.addWidget(self.r2)
		colorLayout.addWidget(self.cButton)
		backgroundLayout.addWidget(r1)
		#backgroundLayout.addWidget(r2)
		backgroundLayout.addLayout(colorLayout)
		backgroundGroup.setLayout(backgroundLayout)

		buttonBox = QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.Ok | QtGui.QDialogButtonBox.Cancel)
		#buttonBox.accepted.connect(self.accept)
		buttonBox.accepted.connect(self.accept)
		buttonBox.rejected.connect(self.reject)
		mainLayout = QtGui.QVBoxLayout()
		mainLayout.addWidget(dimensionGroup)
		mainLayout.addWidget(backgroundGroup)
		mainLayout.addWidget(buttonBox)
		self.setLayout(mainLayout)
		self.setWindowTitle(self.parent.data.getText("dialog_new_image", "title"))
		self.initUI()

		# Definim les senyals
		newfile = pyqtSignal([int],[int],['QColor'])

	def initUI(self):

		self.show()

	def getColor(self):

		color = QtGui.QColorDialog.getColor(Qt.green, self)
		if color.isValid(): 
			self.r2.setChecked(True)
			self.cButton.setStyleSheet("QPushButton {"
										"background: " + color.name() +";"
										"}")
			self.cButton.setText(color.name())
			self.cButton.setPalette(QtGui.QPalette(color))
			self.cButton.setAutoFillBackground(True)

	def accept(self):

		self.parent.newImage(self.width.value(), self.height.value())
		super(NewFileDialog, self).accept()


class ResizeImageDialog (QtGui.QDialog):

	def __init__(self, Parent=None):

		super(ResizeImageDialog, self).__init__(Parent)

		self.parent = Parent

		dimensionGroup = QtGui.QGroupBox(self.parent.data.getText("dialog_resize", "dimension"))
		dimensionLayout = QtGui.QVBoxLayout()

		self.width = QtGui.QSpinBox(dimensionGroup)
		self.width.setMinimum(1)
		self.width.setMaximum(1024)
		self.width.setValue(Parent.data.image.width())
		self.height = QtGui.QSpinBox(dimensionGroup)
		self.height.setMinimum(1)
		self.height.setMaximum(1024)
		self.height.setValue(Parent.data.image.height())

		dimensionLayout.addWidget(self.width)
		dimensionLayout.addWidget(self.height)
		dimensionGroup.setLayout(dimensionLayout)
		
		buttonBox = QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.Ok | QtGui.QDialogButtonBox.Cancel)
		buttonBox.accepted.connect(self.accept)
		buttonBox.rejected.connect(self.reject)

		mainLayout = QtGui.QVBoxLayout()
		mainLayout.addWidget(dimensionGroup)
		mainLayout.addWidget(buttonBox)

		self.setLayout(mainLayout)
		self.setWindowTitle(self.parent.data.getText("dialog_resize", "title"))
		self.show()

	def accept(self):
	
		self.parent.resizeImage(self.width.value(), self.height.value())
		super(ResizeImageDialog,self).accept()


class Preferences (QtGui.QDialog):

	def  __init__(self, data, com, Parent=None):

		super(Preferences, self).__init__(Parent)
		self.data = data
		self.com = com
		self.parent = Parent

		# El QStackedWidget es un tipo de widget muy útil que tiene diferentes "páginas" y podemos ir cambiando entre ellas
		# con sólo llamar a un método. En nuestro caso, conectamos (el signal que emite el QListWidget al cambiar de sección)
		# -> (al método self.changeCurrentView, que cambia la página del QStackedWidget).

		self.view = QtGui.QStackedWidget()
		self.view.addWidget(self.createLanguageView())
		self.view.addWidget(self.createUICustomizationView())
		self.view.addWidget(self.createMatrixGridView())
		#self.view.addWidget(self.createKeyboardShorcutsView()) # Si se descomenta da un SEGFAULT
		#self.view.addWidget(self.createDefaultsView()) # Si se descomenta da un SEGFAULT

		self.preferences = QtGui.QListWidget()
		self.preferences.addItem("Language")
		self.preferences.addItem("UI Customization")
		self.preferences.addItem("Matrix grid")
		self.preferences.addItem("Keyboard shortcuts")
		self.preferences.addItem("Defaults")
		self.preferences.setCurrentRow(0)
		self.preferences.currentItemChanged.connect(self.changeCurrentView)
		self.preferences.setFixedWidth(self.preferences.sizeHintForColumn(0) + 24)

		self.buttonBox = QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.Ok | QtGui.QDialogButtonBox.Cancel)
		self.buttonBox.accepted.connect(self.accept)
		self.buttonBox.rejected.connect(self.reject)

		self.hbox = QtGui.QHBoxLayout()
		self.hbox.addWidget(self.preferences)
		self.hbox.addWidget(self.view)

		self.vbox = QtGui.QVBoxLayout()
		self.vbox.addLayout(self.hbox)
		self.vbox.addWidget(self.buttonBox)

		self.setLayout(self.vbox)
		self.setWindowTitle("Preferences")
		self.adjustSize()
		self.show()

	def changeCurrentView(self):

		self.view.setCurrentIndex(self.preferences.currentRow())

	def createLanguageView(self):

		# Widget de ejemplo

		g = QtGui.QGroupBox("Language")

		w = QtGui.QWidget()

		vbox = QtGui.QVBoxLayout()

		self.language = QtGui.QComboBox()

		for i in self.data.tdatabase.d.keys():
			self.language.addItem(self.data.tdatabase.d[i].name)
			self.langCode = self.data.tdatabase.d[i].code
			#self.language.setCurrentIndex()

		vbox.addWidget(self.language)
		vbox.setStretch(1,1)
		vbox.setAlignment(Qt.AlignTop)

		w.setLayout(vbox)

		g.setLayout(vbox)

		return g

	def createUICustomizationView(self):

		g = QtGui.QGroupBox("UI Customization")

		vbox = QtGui.QVBoxLayout()
		vbox.addWidget(QtGui.QComboBox())
		vbox.setStretch(1,1)
		vbox.setAlignment(Qt.AlignTop)

		g.setLayout(vbox)

		return g

	def createKeyboardShorcutsView(self):

		return

	def createMatrixGridView(self):

		g = QtGui.QGroupBox("Matrix grid dimension")

		vbox = QtGui.QVBoxLayout()
		
		self.matrixGridWidth = QtGui.QSpinBox()
		self.matrixGridWidth.setMinimum(1)
		self.matrixGridWidth.setMaximum(1024)
		self.matrixGridWidth.setValue(self.data.matrixGridWidth)
		self.matrixGridHeight = QtGui.QSpinBox()
		self.matrixGridHeight.setMinimum(1)
		self.matrixGridHeight.setMaximum(1024)
		self.matrixGridHeight.setValue(self.data.matrixGridHeight)

		vbox.addWidget(self.matrixGridWidth)
		vbox.addWidget(self.matrixGridHeight)
		vbox.setStretch(1,1)
		vbox.setAlignment(Qt.AlignTop)

		g.setLayout(vbox)

		return g

	def createDefaultsView(self):

		return

	def accept(self):

		if self.language != self.data.lang:
			QtGui.QMessageBox.information(self, "Language settings changed", "You will have to close Pix2Pics for the language settings to apply.")


		self.data.matrixGridWidth = self.matrixGridWidth.value()
		self.data.matrixGridHeight = self.matrixGridHeight.value()

		self.com.updateCanvas.emit()
		super(Preferences, self).accept()