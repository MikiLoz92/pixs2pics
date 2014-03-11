#!/usr/bin/env python
#coding: utf-8

"""
PixelART: Editor de Pixel Art

Autores:
	Alicia Guindulain
	Antonio Peris
	Luis Moyà
	Natasha -
	Miguel Vera
"""

import sys

from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import Qt

from image import Image
from communication import Communication
from dialogs import NewFileDialog
from mainwidget import MainWidget
from canvas import Canvas
from mainwindow import MainWindow


def readCSS(fname):
	f = open(fname)
	return f.read()


## Controlador
if __name__ == '__main__':

	app = QtGui.QApplication(sys.argv)
	com = Communication()
	im = Image(com)
	mw = MainWindow(im, com)
	mw.setStyleSheet(readCSS("style.css"))

	sys.exit(app.exec_())