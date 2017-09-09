#!/usr/bin/env python3

import os
import sys
from PySide.QtCore import *
from PySide.QtGui import *

import terminal
import gui

class Main(QMainWindow):
	def __init__(self, parent=None):
		super(Main, self).__init__(parent)
		self.setWindowTitle("blabla")

		self.fileMenu = QMenu("&File", self)
		self.menuBar().addMenu(self.fileMenu)

		self.tabs = QTabWidget(self)
		self.tabs.setDocumentMode(True)
		self.tabs.setTabsClosable(True)
		self.tabs.setMovable(True)

		frame = gui.TerminalWidget(self)
		self.tabs.addTab(frame, 'Terminal #1')
		frame = gui.TerminalWidget(self)
		self.tabs.addTab(frame, 'Terminal #2')
		frame = gui.TerminalWidget(self)
		self.tabs.addTab(frame, 'Terminal #3')

		self.setCentralWidget(self.tabs)

		self.show()

	def sizeHint(self):
		return QSize(800, 600)

if __name__ == "__main__":
	app = QApplication(sys.argv)
	main = Main()
	app.exec_()
