from PySide.QtCore import *
from PySide.QtGui import *

from . import font
from terminal import emulator, screen, rendition


class TerminalWidget(QWidget):
	def __init__(self, parent, cmd="/bin/sh"):
		QWidget.__init__(self, parent)
		layout = QBoxLayout(QBoxLayout.TopToBottom)
		self.setLayout(layout)
		self.w = TerminalRenderWidget(self, cmd)
		layout.addWidget(self.w)
		self.b = QStatusBar()
		layout.addWidget(self.b)
		l = QLabel("wut")
		#l.setPixmap(QPixmap("exit.png"))
		self.b.addPermanentWidget(l)
		layout.setContentsMargins(1, 1, 1, 1)

	def update_title(self, title):
		print("!!!%s"% title)
		return
		self.b.showMessage(title)

class TerminalRenderWidget(QAbstractScrollArea):

	def __init__(self, parent=None, cmd="/bin/sh"):
		super(TerminalRenderWidget, self).__init__(parent)

		self.setFrameStyle(QFrame.NoFrame)
		self.historySize = 0

		self.rows, self.cols = 25, 80 
		self.emulator = emulator.Emulator(self.rows, self.cols)
		self.emulator.set_update_callback(self.update_screen)
		self.emulator.set_title_callback(parent.update_title)
		self.emulator.set_data_callback(self.update_data)
		self.terminal_id = QApplication.instance().td.startTerminal("/bin/sh", [], self)
		

		self.font = font.MonoFont("Monospace", 10)

		self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
		self.setViewportMargins(2, 2, 2, 2)

		p = QPalette(self.palette())
		p.setColor(QPalette.Background, Qt.black)
		self.setPalette(p)
		self.setAutoFillBackground(True)

		# XXX platform dependent
		self.ctrl = Qt.ControlModifier

		self.cursorRow = 0
		self.blink = False
		self.cursorBlink = QTimer()
		self.cursorBlink.setInterval(500)
		self.cursorBlink.setSingleShot(False)
		self.cursorBlink.timeout.connect(self.cursorBlinkEvent)
		self.cursorBlink.start()
		self.caretVisible = False
		self.blink = False

	def exited(self, ok):
		print("process exited!!?")

	def renderCursor(self):
		self.viewport().update(0, self.cursorRow * self.font.charHeight,
			self.viewport().size().width(), self.font.charHeight)
		self.cursorRow = self.emulator.cursor.y
		self.viewport().update(0, self.cursorRow * self.font.charHeight,
			self.viewport().size().width(), self.font.charHeight)

	def cursorBlinkEvent(self):
		self.blink = not self.blink
		self.renderCursor()

	def update_screen(self):
		self.viewport().update()

	def update_data(self, data):
		pass

	def event(self, event):
		t = event.type()
		if t == QEvent.KeyPress and (event.key() == Qt.Key_Tab or event.key() == Qt.Key_Backtab):
			self.keyPressEvent(event)
			return True
		if t == QEvent.ShortcutOverride and event.key() >= Qt.Key_A and event.key() <= Qt.Key_Z:
			if (event.modifiers() & (self.ctrl | Qt.AltModifier | Qt.ShiftModifier)) == self.ctrl:
				event.accept()
				return True
		return super(TerminalRenderWidget, self).event(event)

	def getKeyModifierString(self, mod):
		if (mod & (self.ctrl | Qt.ShiftModifier | Qt.AltModifier)) == (Qt.ShiftModifier):
			return ";2"
		if (mod & (self.ctrl | Qt.ShiftModifier | Qt.AltModifier)) == (Qt.AltModifier):
			return ";3"
		if (mod & (self.ctrl | Qt.ShiftModifier | Qt.AltModifier)) == (Qt.ShiftModifier | Qt.AltModifier):
			return ";4"
		if (mod & (self.ctrl | Qt.ShiftModifier | Qt.AltModifier)) == (self.ctrl):
			return ";5"
		if (mod & (self.ctrl | Qt.ShiftModifier | Qt.AltModifier)) == (Qt.ShiftModifier | self.ctrl):
			return ";6"
		if (mod & (self.ctrl | Qt.ShiftModifier | Qt.AltModifier)) == (Qt.AltModifier | self.ctrl):
			return ";7"
		if (mod & (self.ctrl | Qt.ShiftModifier | Qt.AltModifier)) == (Qt.ShiftModifier | Qt.AltModifier | self.ctrl):
			return ";8"
		return ""

	def keyPressEvent(self, event):
		key_data = {
			Qt.Key_F5:"15",
			Qt.Key_F6:"17",
			Qt.Key_F7:"18",
			Qt.Key_F8:"19",
			Qt.Key_F9:"20",
			Qt.Key_F10:"21",
			Qt.Key_F11:"23",
			Qt.Key_F12:"24",
			Qt.Key_Delete:"3",
		}
		arrow_keys = {
			Qt.Key_Up:"A",
			Qt.Key_Down:"B",
			Qt.Key_Right:"C",
			Qt.Key_Left:"D"
		}
		ctrl = self.ctrl
		alt = Qt.AltModifier
		shift = Qt.ShiftModifier
		mods = event.modifiers()
		modstr = self.getKeyModifierString(mods)
		key = event.key()
		text = event.text()
		data = None
		if key in arrow_keys:
			if mods & (ctrl|alt|shift):
				data = "\033[%s%c" % (modstr, arrow_keys[key])
			else:
				data = "\033[%c" % arrow_keys[key]
			#XXX if cursor_keys option set
			
		if key in key_data:
			data = "\033[%s%s~" % (key_data[key], modstr)
		elif key == Qt.Key_Backspace:
			data = "\x7f"
		elif key == Qt.Key_Tab:
			data = "\t"
		elif key == Qt.Key_Backtab:
			data = "\033[Z"
		elif key >= Qt.Key_A and key <= Qt.Key_Z and (mods & (ctrl|alt|shift))==ctrl:
			try:
				data =  "%c" % (chr(key-ord('A')+1))
				#data = "%c" % (chr(key - Qt.Key_A) + 1)
			except Exception as e:
				print(e)
				print(key - Qt.Key_A)
				print(key, ord('A'), key-ord('A')+1, chr(key-ord('A')+1))
		elif len(text) > 0:
			data = event.text()
			if len(text) == 1 and text >= ' ' and text <= '~' and mods & alt:
				data = "\033" + data	

		self.send_input(data)
		if not data:
			return	

		#self.verticalScrollBar().setValue(0)

	def send_input(self, data):
		QApplication.instance().td.sendInput(self.terminal_id, data)
		self.update_screen()

	def data(self, data):
		self.emulator.input_data(data)
		self.update_screen()
			
	def mousePressEvent(self, event):
		pass

	def mouseMoveEvent(self, event):
		pass

	def mouseReleaseEvent(self, event):
		pass

	def mouseDoubleClickEvent(self, event):
		pass

	def focusInEvent(self, event):
		self.caretVisible = True
		self.blink = True
		self.cursorBlink.stop()
		self.cursorBlink.start()
		self.renderCursor()

	def focusOutEvent(self, event):
		self.caretVisible = False
		self.renderCursor()

	def get_colors(self, gfx):
		fg, bg = rendition.get_colors(gfx)
		fg = QColor(*fg) if fg else Qt.white
		bg = QColor(*bg) if bg else Qt.black
		return fg, bg

	def paintRow(self, y, row, rowgfx):
		p = QPainter(self.viewport())
		p.setFont(self.font.font)

		# render background
		bg, fg = Qt.black, Qt.white
		length = 0
		current = None
		x = 0 
		for i in range(0, self.cols):
			gfx = rowgfx[i]	

			# invert colors when rendering the cursor
			if self.blink and self.caretVisible and self.emulator.cursor.visible and \
				self.emulator.cursor.y == y and self.emulator.cursor.x == i:
				gfx ^= rendition.GFX_INV

			if gfx != current:
				if length > 0:
					p.fillRect(x * self.font.charWidth, y * self.font.charHeight,
						length * self.font.charWidth, self.font.charHeight, bg)
					x = x + length
					length = 0	
				current = gfx
				fg, bg = self.get_colors(gfx)
			length = length + 1
		if length > 0:
			p.fillRect(x * self.font.charWidth, y * self.font.charHeight,
				length * self.font.charWidth, self.font.charHeight, bg)

		# render foreground
		bg, fg = Qt.black, Qt.white
		length = 0
		current = None
		x = 0 
		for i in range(0, self.cols):
			gfx = rowgfx[i]
			if gfx != current:
				if length > 0:
					line = "".join(row[x:i])
					p.setPen(fg)
					p.drawText(x * self.font.charWidth, y * self.font.charHeight + self.font.charOffset + self.font.ascent, line)
					if gfx & rendition.GFX_BOLD:
						p.setFont(self.font.bold)
					elif gfx & rendition.GFX_UL:
						p.setFont(self.font.under)
					else:
						p.setFont(self.font.font)
					x = x + length
					length = 0	
				current = gfx
				fg, bg = self.get_colors(gfx)
			length = length + 1
		if length > 0:
			line = "".join(row[x:i])
			p.setPen(fg)
			p.drawText(x * self.font.charWidth, y * self.font.charHeight + self.font.charOffset + self.font.ascent, line)

		# draw disabled cursor as the screen's not active right now
		if not self.caretVisible and self.emulator.cursor.y == y:

			if self.emulator.cursor.x == len(rowgfx):
				fg, bg = self.get_colors(rowgfx[self.emulator.cursor.x-1])
			elif self.emulator.cursor.x > len(rowgfx):
				print(self.emulator.cursor.x, len(rowgfx))
				print(rowgfx)
				raise Exception("")
			else:
				fg, bg = self.get_colors(rowgfx[self.emulator.cursor.x])
			p.setPen(fg)
			p.drawRect(x * self.font.charWidth, y * self.font.charHeight, self.font.charWidth -1, self.font.charHeight - 1)


	def paintEvent(self, event):
		p = QPainter(self.viewport())
		p.setFont(self.font.font)
		p.fillRect(event.rect(), Qt.black)

		yofs = self.verticalScrollBar().value()
		y = event.rect().y()
		bot = y + event.rect().height()
		top = int(y / self.font.charHeight)
		bot = int((bot / self.font.charHeight) + 1)

		screen = self.emulator.screen
		for y in range(0, self.rows):
			self.paintRow(y, screen.cells[y], screen.gfx[y])

	def closeRequest(self):
		print("clooooooooose")
		#self.process.kill()

	def resizeEvent(self, event):
		sz = event.size()
		self.resize(sz.width(), sz.height())

	def resize(self, w, h):
		self.cols = int(w / self.font.charWidth)
		self.rows = int(h / self.font.charHeight)
		#self.verticalScrollBar().setPageStep(self.rows)
		#self.verticalScrollBar().setRange(-self.historySize, 0)
		self.emulator.resize(self.rows, self.cols)
		QApplication.instance().td.resizeTerminal(self.terminal_id, self.rows, self.cols)
