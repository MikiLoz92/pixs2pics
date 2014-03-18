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

		dimensionGroup = QtGui.QGroupBox("Dimension")
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

		backgroundGroup = QtGui.QGroupBox("Background")
		backgroundLayout = QtGui.QVBoxLayout()
		r1 = QtGui.QRadioButton("Transparent")
		r1.setChecked(True)
		self.r2 = QtGui.QRadioButton("Color:")
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
		self.setWindowTitle("Create new image")
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

		dimensionGroup = QtGui.QGroupBox("New dimension")
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
		self.setWindowTitle("Create new image")
		self.show()

	def accept(self):
	
		self.parent.resizeImage(self.width.value(), self.height.value())
		super(ResizeImageDialog,self).accept()