#!/usr/bin/env python
#coding: utf-8

from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import Qt
import random

from flowlayout import FlowLayout


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
			self.data.changeColor(self.color)
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

		self.flow = FlowLayout()

		#cList = []
		for i in range(random.randint(20,50)):
			#cList.append(Color())
			self.flow.addWidget(Color(self.data, self.com))

		self.flow.setSpacing(0)
		self.setLayout(self.flow)