#!/usr/bin/env python
#coding: utf-8

## Modelo
class Image:
	"""
	La clase Image contiene todos los datos de la imagen que muestran las vistas.
	De momento solo contiene información de la posición de cada punto que tiene color, 
	pero dentro de poco debería contener información de color de todos y cada uno de
	los píxeles del lienzo.
	"""

	def __init__(self, com):

		self.lpunts = []
		self.com = com
		 
	def afegirpunt(self, pos):
		
		if pos not in self.lpunts:
			self.lpunts.append(pos)
			self.com.dadesActualitzada.emit()