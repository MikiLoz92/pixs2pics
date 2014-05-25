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

import sys, os

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
	app.setWindowIcon(QtGui.QIcon("images/icon.gif"))
	com = Communication()
	data = Data(com)

	if data.theme != "default-light" and data.theme != "default-dark":
		customFnt = "Lato-Reg.ttf"
		if QtGui.QFontDatabase().addApplicationFont(os.path.join("fonts", customFnt)) < 0:
			print "Warning: Could not load custom font" + customFnt + ", falling back to default font."
		else:
			fnt = QtGui.QFont("Lato", 10)
			app.setFont(fnt)

	if os.path.isdir(os.path.join("themes", data.theme)):
		css = os.path.join("themes", data.theme, "style.css")
		if os.path.isfile(css):
			mw = MainWindow(data, com)
			mw.setStyleSheet(readCSS(css))
		else:
			mw = MainWindow(data, com)
	else:
		print "Couldn't find theme " + data.theme + ", falling back to default-light."
		data.theme = "default-light"
		mw = MainWindow(data, com)

	sys.exit(app.exec_())