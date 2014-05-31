#!/usr/bin/env python
#coding: utf-8

from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import Qt

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
		l.append(self.createGradientWidget())
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

		eraserSizeLabel = QtGui.QLabel(self.data.getText("tool_properties_eraser", "size"))
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

		self.v = QtGui.QVBoxLayout()

		v2 = QtGui.QVBoxLayout()

		self.btn1 = QtGui.QRadioButton(self.data.getText("tool_properties_gradient", "horizontal"))
		self.btn2 = QtGui.QRadioButton(self.data.getText("tool_properties_gradient", "vertical"))
		self.btn1.setChecked(True)

		self.btn1.clicked.connect( lambda : self.changeDegDir('H') )
		self.btn2.clicked.connect( lambda : self.changeDegDir('V') )

		h = QtGui.QHBoxLayout()

		self.label = QtGui.QLabel("Transparencia:", self)

		self.AlphaSpin = QtGui.QSpinBox(self) 
		self.AlphaSpin.setMinimum(0)
		self.AlphaSpin.setMaximum(255)
		self.AlphaSpin.setValue(255)
		self.AlphaSpin.valueChanged.connect(self.setAlphaValue)

		h.addWidget(self.label)
		h.addWidget(self.AlphaSpin)
		tmp = QtGui.QWidget()
		tmp.setLayout(h) 

		self.check = QtGui.QCheckBox("Color a Transparente")
		self.check.stateChanged.connect(self.changeDegState)

		v2.addWidget(self.btn1)
		v2.addWidget(self.btn2)
		tmp2 = QtGui.QWidget()
		tmp2.setLayout(v2) 

		self.v.addWidget(tmp2) 
		#self.v.addWidget(tmp)
		#self.v.addWidget(self.check)

		w = QtGui.QWidget()
		w.setLayout(self.v)
		self.v.addStretch()

		return w


	def changeDegDir(self, state):
		if self.btn1.isChecked():
			self.data.DegDir = 'H'
		elif self.btn2.isChecked():
			self.data.DegDir = 'V'

	def changeDegState(self):
		if self.check.isChecked():
			self.data.DegState = 1
		else:
			self.data.DegState = 2

	def setAlphaValue(self):
		self.data.DegAlpha = self.AlphaSpin.value()
		print self.data.DegAlpha

	def updateWidget(self):
		self.setWidget(self.widgets[self.data.currentTool])