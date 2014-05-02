#!/usr/bin/env python
#coding: utf-8

from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import Qt
import random

from flowlayout import FlowLayout


class CurrentColor(QtGui.QLabel):

	def __init__(self, primary, data, com, Parent=None):

		super(CurrentColor, self).__init__()

		self.parent = Parent
		self.data = data
		self.com = com
		self.com.updateColor.connect(self.update)
		self.primary = primary

		if primary: self.color = self.data.primaryColor
		else: self.color = self.data.secondaryColor

		self.setFixedHeight(24)
		self.setPalette(QtGui.QPalette(self.color))
		self.setAutoFillBackground(True)

	def paintEvent(self, e):

		painter = QtGui.QPainter(self)	
		painter.setBackgroundMode(Qt.OpaqueMode)
		brush = QtGui.QBrush(self.color)
		painter.setBrush(brush)
		painter.fillRect(0,0,self.width(),self.height(),brush)

		super(CurrentColor, self).paintEvent(e)

	def mouseReleaseEvent(self, e):

		if e.button() == Qt.LeftButton:
			c = QtGui.QColorDialog.getColor(self.color, self)
			if c.isValid():
				if self.primary: self.data.changePrimaryColor(c)
				else: self.color = self.data.changeSecondaryColor(c)

	def update(self):

		if self.primary: self.color = self.data.primaryColor
		else: self.color = self.data.secondaryColor
		
		super(CurrentColor, self).update()


class Color(QtGui.QFrame):
	"""
	Una QFrame cuadrada que representa un color de la paleta.
	"""

	def __init__(self, data, com, Parent=None):

		super(Color, self).__init__(Parent)

		self.parent = Parent
		self.data = data
		self.com = com

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
			self.data.changePrimaryColor(self.color)
		elif e.button() == Qt.RightButton:
			c = QtGui.QColorDialog.getColor(self.color, self)
			if c.isValid():
				self.color = c
				self.update()


class Palette (QtGui.QWidget):

	def __init__(self, data, com, Parent=None):

		super(Palette, self).__init__(Parent)

		self.parent = Parent
		self.data = data
		self.com = com

		"""
		palette = QtGui.QGridLayout()
		palette.setSpacing(0)
		palette.setSizeConstraint(QtGui.QLayout.SetMaximumSize)
		i = 0
		j = 0
		for k in range(16):
			c = Color(self.data, self.com, self)
			palette.addWidget(c,j,i)
			i += 1
			if j == 0 and i > 7:
				j = 1
				i = 0
		"""

		
		palette = FlowLayout()
		for i in range(random.randint(20,50)):
			palette.addWidget(Color(self.data, self.com))
		palette.setSpacing(0)
		

		hbox = QtGui.QHBoxLayout()
		hbox.addWidget(CurrentColor(True, self.data, self.com))
		hbox.addWidget(CurrentColor(False, self.data, self.com))
		hbox.setSpacing(0)
		hbox.setSizeConstraint(QtGui.QLayout.SetMaximumSize)

		vbox = QtGui.QVBoxLayout()
		vbox.addLayout(hbox)
		vbox.addLayout(palette)
		vbox.setSpacing(0)
		vbox.setSizeConstraint(QtGui.QLayout.SetMaximumSize)

		self.setLayout(vbox)
