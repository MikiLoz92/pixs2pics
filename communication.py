#!/usr/bin/env python
#coding: utf-8

from PyQt4 import QtCore

class Communication(QtCore.QObject):
	"""
	La clase Communication hace de puente entre diferentes
	instancias de todo el programa.
	"""

	newImage = QtCore.pyqtSignal()

	updateCanvas = QtCore.pyqtSignal()
	resizeCanvas = QtCore.pyqtSignal()

	copyImage = QtCore.pyqtSignal()
	cutImage = QtCore.pyqtSignal()
	pasteImage = QtCore.pyqtSignal()
	clearImage  = QtCore.pyqtSignal()

	updateColor = QtCore.pyqtSignal()
	updateColorDeg = QtCore.pyqtSignal()

	updateTool = QtCore.pyqtSignal()

	zoom = QtCore.pyqtSignal()

	colorPickerOn = QtCore.pyqtSignal()
	colorPickerOff = QtCore.pyqtSignal()

	enterCanvas = QtCore.pyqtSignal()
	leaveCanvas = QtCore.pyqtSignal()