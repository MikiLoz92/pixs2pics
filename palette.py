#!/usr/bin/env python
#coding: utf-8

from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import Qt
import random


class CurrentColor(QtGui.QLabel):

	def __init__(self, primary, data, com, Parent=None):

		super(CurrentColor, self).__init__()

		self.parent = Parent
		self.data = data
		self.com = com
		self.com.updateColor.connect(self.update)
		self.primary = primary

		if primary:
			self.color = self.data.primaryColor
			self.setObjectName("PrimaryColor")
		else:
			self.color = self.data.secondaryColor
			self.setObjectName("SecondaryColor")

		self.setStyleSheet("background-color: " + self.color.name() + ";")
		self.setFixedHeight(24)

	def mouseMoveEvent(self, e):

		mimeData = QtCore.QMimeData()
		mimeData.setColorData(self.color)

		drag = QtGui.QDrag(self)
		drag.setMimeData(mimeData)
		drag.setHotSpot(e.pos() - self.rect().topLeft())

		dropAction = drag.start(QtCore.Qt.MoveAction)

	def mouseReleaseEvent(self, e):

		if e.button() == Qt.LeftButton:
			c = QtGui.QColorDialog.getColor(self.color)
			if c.isValid():
				if self.primary: self.data.changePrimaryColor(c)
				else: self.color = self.data.changeSecondaryColor(c)

	def update(self):

		if self.primary:
			self.color = self.data.primaryColor
			self.setStyleSheet("background-color: " + self.color.name() + ";")
		else:
			self.color = self.data.secondaryColor
			self.setStyleSheet("background-color: " + self.color.name() + ";")
		
		super(CurrentColor, self).update()


class Color(QtGui.QFrame):
	"""
	Una QFrame cuadrada que representa un color de la paleta.
	"""

	def __init__(self, position, color, data, com, Parent=None):

		super(Color, self).__init__(Parent)

		self.parent = Parent
		self.data = data
		self.com = com

		self.position = position
		self.color = QtGui.QColor(color[0], color[1], color[2])

		self.setObjectName("Color")
		self.setFixedSize(12, 12)
		self.setStyleSheet("background-color: " + self.color.name() + ";")

		self.setAcceptDrops(True)

	def mousePressEvent(self, e):

		if e.button() == Qt.LeftButton:
			self.data.changePrimaryColor(self.color)
		elif e.button() == Qt.RightButton:
			self.data.changeSecondaryColor(self.color)
		elif e.button() == Qt.MidButton:
			c = QtGui.QColorDialog.getColor(self.color)
			if c.isValid():
				self.changeColor(c)

	"""
	def mouseMoveEvent(self, e):

		mimeData = QtCore.QMimeData()
		mimeData.setColorData(self.color)

		drag = QtGui.QDrag(self)
		drag.setMimeData(mimeData)
		drag.setHotSpot(e.pos() - self.rect().topLeft())

		dropAction = drag.start(QtCore.Qt.MoveAction)

		self.changeColor(QtGui.QColor(0,0,0))
	"""

	def dragEnterEvent(self, e):

		if e.mimeData().hasColor():
			e.accept()

	def dropEvent(self, e):

		self.changeColor(QtGui.QColor(e.mimeData().colorData()))

		e.setDropAction(QtCore.Qt.CopyAction)
		e.accept()

	def update(self):

		self.setStyleSheet("background-color: " + self.color.name() + ";")
		super(Color, self).update()

	def changeColor(self, c):

		self.color = c
		self.data.palette[self.position] = [c.red(), c.green(), c.blue()]
		self.update()

class Palette (QtGui.QWidget):

	def __init__(self, data, com, Parent=None):

		super(Palette, self).__init__(Parent)

		self.parent = Parent
		self.data = data
		self.com = com
		self.setObjectName("Palette")

		palette = QtGui.QGridLayout()
		for i in range(5):
			for j in range(12):
				palette.addWidget(Color(i*12+j, self.data.palette[i*12+j], self.data, self.com), i, j)
				"""
				if i > 1:
					palette.addWidget(Color(True, self.data, self.com), i, j)
				else:
					palette.addWidget(Color(False, self.data, self.com), i, j)
				"""
		palette.setSpacing(1)

		hbox = QtGui.QHBoxLayout()
		hbox.addWidget(CurrentColor(True, self.data, self.com))
		hbox.addWidget(CurrentColor(False, self.data, self.com))
		hbox.setSpacing(2)
		#hbox.setSizeConstraint(QtGui.QLayout.SetMaximumSize)

		vbox = QtGui.QVBoxLayout()
		vbox.addLayout(hbox)
		vbox.addLayout(palette)
		vbox.setSpacing(2)
		#vbox.setSizeConstraint(QtGui.QLayout.SetMaximumSize)

		self.setLayout(vbox)
		self.setSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Maximum)
