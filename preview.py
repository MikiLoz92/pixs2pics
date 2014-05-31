#!/usr/bin/env python
#coding: utf-8

from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import Qt

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

	def setPixmap(self):

		if self.data.image.width() > 128 or self.data.image.height() > 128:
			imatge = self.data.image.scaled(128, 128, Qt.KeepAspectRatio)
			self.label.setPixmap(QtGui.QPixmap.fromImage(imatge))
		else:
			self.label.setPixmap(QtGui.QPixmap.fromImage(self.data.image))