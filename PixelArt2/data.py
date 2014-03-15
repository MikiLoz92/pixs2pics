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
	pencilSize = 2
	brushSize = 3
	zoom = 1

	def __init__(self, com):

		self.image = QtGui.QImage(32,32,QtGui.QImage.Format_RGB32)
		#self.image = QtGui.QImage("images/zapdos.png")
