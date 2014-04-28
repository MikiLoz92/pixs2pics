#!/usr/bin/env python
#coding: utf-8

"""
PixelART: Editor de Pixel Art

Autores:
	Alicia Guindulain
	Antonio Peris
	Luis Mollá
	Natacza Johnson
	Miguel Vera
"""

import sys

from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import Qt

from mainwindow import MainWindow
from communication import Communication
from data import Data


def readCSS(fname):
	f = open(fname)
	return f.read()


## Controlador
if __name__ == '__main__':

	app = QtGui.QApplication(sys.argv)
	com = Communication()
	data = Data(com)
	mw = MainWindow(data, com)

	customFnt = "Lato-Reg.ttf"
	if QtGui.QFontDatabase().addApplicationFont(customFnt) < 0:
		print "Warning: Could not load custom font" + customFnt + ", falling back to default font."
	else:
		fnt = QtGui.QFont("Lato", 10)
		app.setFont(fnt)
	mw.setStyleSheet(readCSS("style.css"))

	sys.exit(app.exec_())