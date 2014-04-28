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

	def  __init__(self, Parent=None):

		super(Preferences, self).__init__(Parent)
		self.parent = Parent

		# El QStackedWidget es un tipo de widget muy útil que tiene diferentes "páginas" y podemos ir cambiando entre ellas
		# con sólo llamar a un método. En nuestro caso, conectamos (el signal que emite el QListWidget al cambiar de sección)
		# -> (al método self.changeCurrentView, que cambia la página del QStackedWidget).

		self.view = QtGui.QStackedWidget()
		self.view.addWidget(self.createLanguageView())
		self.view.addWidget(self.createUICustomizationView())
		#self.view.addWidget(self.createKeyboardShorcutsView()) # Si se descomenta da un SEGFAULT
		#self.view.addWidget(self.createDefaultsView()) # Si se descomenta da un SEGFAULT
		self.view.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)

		self.preferences = QtGui.QListWidget()
		self.preferences.addItem("Language")
		self.preferences.addItem("UI Customization")
		self.preferences.addItem("Keyboard shortcuts")
		self.preferences.addItem("Defaults")
		self.preferences.setCurrentRow(0)
		self.preferences.currentItemChanged.connect(self.changeCurrentView)
		self.preferences.setFixedWidth(self.preferences.sizeHintForColumn(0) + 24)
		#self.preferences.setFixedHeight(self.preferences.sizeHintForRow(0)*self.preferences.count()+24)
		self.preferences.setSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Minimum)
		#self.preferences.setFixedSize(self.preferences.minimumSize())
		#self.preferences.setSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Preferred)

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

	def createLanguageView(self):

		# Widget de ejemplo

		g = QtGui.QGroupBox()

		w = QtGui.QWidget()

		vbox = QtGui.QVBoxLayout()
		#vbox.addWidget(QtGui.QLabel("Hola"))
		#vbox.addWidget(QtGui.QLabel("Adios"))
		vbox.addWidget(QtGui.QComboBox())
		vbox.setStretch(1,1)
		vbox.setAlignment(Qt.AlignTop)

		w.setLayout(vbox)

		g.setLayout(vbox)
		g.setTitle("Language")

		return g

	def createUICustomizationView(self):

		# Widget de ejemplo

		w = QtGui.QWidget()

		vbox = QtGui.QVBoxLayout()
		vbox.addWidget(QtGui.QLabel("Ra, Ra, Rasputin"))
		vbox.addWidget(QtGui.QLabel("Lover of the Russian queen"))
		vbox.addWidget(QtGui.QLabel("There was a cat that really was gone"))
		vbox.addWidget(QtGui.QLabel("Ra, Ra, Rasputin"))
		vbox.addWidget(QtGui.QLabel("Russia's greatest love machine"))
		vbox.addWidget(QtGui.QLabel("It was a shame how he carried on"))

		w.setLayout(vbox)

		return w

	def createKeyboardShorcutsView(self):

		return

	def createDefaultsView(self):

		return

	def changeCurrentView(self):

		self.view.setCurrentIndex(self.preferences.currentRow())