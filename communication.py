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
	updateColor = QtCore.pyqtSignal()
	updateColorDeg = QtCore.pyqtSignal()
	updateTool = QtCore.pyqtSignal()
	zoomIn = QtCore.pyqtSignal()
	zoomOut = QtCore.pyqtSignal()
	colorPickerOn = QtCore.pyqtSignal()
	colorPickerOff = QtCore.pyqtSignal()
	enterCanvas = QtCore.pyqtSignal()
	leaveCanvas = QtCore.pyqtSignal()