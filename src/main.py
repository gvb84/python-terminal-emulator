#!/usr/bin/env python3

import sys, argparse

from PySide.QtCore import *
from PySide.QtGui import *

import terminal
import gui

arg_ns = None

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

		global arg_ns
		if arg_ns.terminal_enabled:
			frame = gui.TerminalWidget(self, "/bin/sh")
			self.tabs.addTab(frame, 'Terminal #1')
		#frame = gui.TerminalWidget(self, "/bin/sh")
		#self.tabs.addTab(frame, 'Terminal #2')

		self.splitter = QSplitter()

		self.splitter.addWidget(self.tabs)

		self.tabs2 = QTabWidget(self)
		self.tabs2.setDocumentMode(True)
		self.tabs2.setTabsClosable(True)
		self.tabs2.setMovable(True)
		self.splitter.addWidget(self.tabs2)

		if arg_ns.terminal_enabled:
			frame = gui.TerminalWidget(self, "/usr/bin/vim")
			self.tabs2.addTab(frame, 'Terminal #3')

		#self.setCentralWidget(self.tabs)
		self.setCentralWidget(self.splitter)
		self.splitter.setOrientation(Qt.Vertical)
		self.splitter.setSizes([1, 1])

		self.show()

	def sizeHint(self):
		return QSize(800, 600)

def run():
	parser = argparse.ArgumentParser(description="Santarago Labs Pentest Framework")
	parser.add_argument("--disable-terminal", help="disable terminal feature", action="store_false", dest="terminal_enabled")
	global arg_ns
	arg_ns = parser.parse_args()

	if arg_ns.terminal_enabled:
		td = terminal.driver.TerminalDriver()

	app = QApplication(sys.argv)

	if arg_ns.terminal_enabled:
		app.td = td

	main = Main()
	app.exec_()

if __name__ == "__main__":
	run()
