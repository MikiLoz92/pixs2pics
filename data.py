#!/usr/bin/env python
#coding: utf-8

from PyQt4 import QtGui, QtCore

## Model / Modelo
class Data:
	"""
	La clase Data contiene todos los datos, parámetros y configuraciones
	de la aplicación. Por ejemplo, contiene la lista de píxeles pintados en
	la imagen con su correspondiente color. También guarda las variables de
	la anchura del làpiz, los colores en la paleta, el color seleccionado
	actualmente, la altura y anchura de la imagen, etc.
	"""

	color = QtCore.Qt.red
	pencilSize = 1
	brushSize = 3
	brushStyle = 0
	currentTool = 1
	zoom = 1
	defaultFileName = ""
	colorPicker = False
	color_deg_1 = QtCore.Qt.white
	color_deg_2 = QtCore.Qt.black

	def __init__(self, com):

		self.com = com

		# Creamos la QImage
		self.image = QtGui.QImage(32,32,QtGui.QImage.Format_ARGB32)

		# Creamos los cursores
		self.pencilCur = QtGui.QCursor(QtGui.QPixmap("images/pencilCur.png"), 0, 23)
		self.colorPickerCur = QtGui.QCursor(QtGui.QPixmap("images/dropperCur.png"), 0, 23)

	def loadImage(self, fileName):

		self.defaultFileName = fileName
		self.image = QtGui.QImage(fileName).convertToFormat(QtGui.QImage.Format_ARGB32)
		self.zoom = 1
		self.com.newImage.emit()

	def newImage(self, w, h):

		self.defaultFileName = ""
		self.image = QtGui.QImage(w, h, QtGui.QImage.Format_ARGB32)
		self.image.fill(QtGui.qRgb(255, 255, 255))
		self.zoom = 1
		self.com.newImage.emit()

	def changeColor(self, c):

		self.color = c
		self.com.updateColor.emit()