from . import ctrl, esc, cursor, screen

class Emulator:
	def __init__(self, rows=80, cols=25, debug=True):

		# configure two supported screens and cursors
		self.cols, self.rows = cols, rows
		self.screens = [screen.Screen(rows, cols), screen.Screen(rows, cols)]
		self.cursors = [cursor.Cursor(0,0), cursor.Cursor(0, 0)]

		# set currently active screen, cursor, scroll region and graphics rendition settings
		self.screen = self.screens[0]
		self.cursor = self.cursors[0]
		self.scroll_bottom = rows - 1
		self.scroll_top = 0
		self.gfx = 0

		# vars for parser state machine of escape sequences etc	
		self.escape_str = ""
		self.in_escape = False   	# in escape sequence
		self.in_csi = False	 	# in Control Sequence Introducer

		# xterm set title support
		self.current_title = None	# currently set title
		self.set_title = False	 	# set window title
		self.ignore_title = True 	# ignore setting of window title

		# misc settings
		self.tabstop = 8		# amount of spaces in a tab
		self.draw_lines = False  	# line drawing mode
		self.insert_mode = False	# insert mode for drawing characters
		self.cursor_keys = False	# interpet cursor keys on numpad as keys or not

		# references to callback functions
		self.callback_data = None	# respond with data to f.e. a specific CSI sequence
		self.callback_update = None	# let caller know there's new data available
		self.callback_title = None	# inform caller of updated window title
	
		# debug log support
		self.debug = debug
		self.debuglog = []
		self.debugloglen = 256		# maximum number of lines stored in self.debuglog

		# control character dispatch
		self.ctrl_dispatch = {
			ctrl.BEL : self.bell,
			ctrl.BS : self.backspace,
			ctrl.HT : self.htab,
			ctrl.LF : self.lf,
			ctrl.VT : self.lf,
			ctrl.FF : self.lf,
			ctrl.CR : self.cr,
			ctrl.SO : self.shift_out,
			ctrl.SI : self.shift_in,
		}

		# escape sequence dispatcher for CSI escape sequences as per VT102
		self.csi_dispatch = {
			esc.ICH : self.insert_chars,
			esc.CUU : self.cursor_up,
			esc.CUD : self.cursor_down,
			esc.CUF : self.cursor_forward,
			esc.CUB : self.cursor_back,
			esc.CNL : self.cursor_next_line,
			esc.CPL : self.cursor_prev_line,
			esc.CHA : self.cursor_halign,
			esc.CUP : self.cursor_set,
			esc.ED : self.erase_data,
			esc.EL : self.erase_in_line,
			esc.IL : self.insert_lines,
			esc.DL : self.delete_lines,
			esc.DCH : self.delete_characters,
			esc.ECH : self.erase_characters,
			esc.HPR : self.cursor_forward,
			esc.DA : self.report_da,
			esc.VPA : self.cursor_set,
			#esc.VPR : self.vertical_position_relative,
			#esc.HVP : self.hvposition,
			esc.TBC : self.tabulation_clear,
			esc.SM : self.set_mode,
			esc.RM : self.reset_mode,
			esc.SGR : self.select_gfx,
			esc.DSR : self.report_status,
			esc.DECSTBM : self.scroll_region,
			esc.HPA : self.cursor_halign,
			#esc.RIS : self.reset,
			#esc.IND : self.index,
			#esc.RI : self.rindex,
			#esc.NEL : self.nextline,
			esc.DECSC : self.cursor_save,
			esc.DECRC : self.cursor_restore,
		}

		# charset setting identifiers used for non "standard" escape sequences etc
		self.charset = [" ", "#", "%", "(", ")", "*", "+"]

		# replace key chars with values when in line drawing mode
		self.line_draw_map = {
			u"j": u"\xe2\x94\x98",
			u"k": u"\xe2\x94\x90",
			u"l": u"\xe2\x94\x8c",
			u"m": u"\xe2\x94\x94",
			u"n": u"\xe2\x94\xbc",
			u"q": u"\xe2\x94\x80",
			u"t": u"\xe2\x94\x9c",
			u"u": u"\xe2\x94\xa4",
			u"v": u"\xe2\x94\xb4",
			u"w": u"\xe2\x94\xac",
			u"x": u"\xe2\x94\x82",
		}

	def set_update_callback(self, cb):
		self.callback_update = cb

	def set_data_callback(self, cb):
		self.callback_data = cb

	def set_title_callback(self, cb):
		self.callback_title = cb

	def update_callback(self):
		if self.callback_update:
			self.callback_update()

	def data_callback(self, data):
		if self.callback_data:
			self.callback_data(data)

	def title_callback(self, title):
		if title == self.current_title:
			return
		self.current_title = title
		if self.callback_title:
			self.callback_title(self.current_title)

	def shift_in(self):
		raise Exception("shift in")

	def shift_out(self):
		raise Exception("shift out")

	def bell(self):
		pass

	def backspace(self):
		if self.cursor.x > 0:
			self.cursor.x = self.cursor.x - 1

	def htab(self):
		self.cursor.x = self.cursor.x + self.tabstop - (self.cursor.x % self.tabstop)
		if self.cursor.x > self.cols:
			self.cursor.x = self.cols

	def cursor_save(self, *params):
		print("Save cursor1")
		#raise Exception("save cursor")
	
	def cursor_restore(self, *params):
		print("Save cursor2")
		#raise Exception("restore cursor")

	def insert_lines(self, count=None):
		pass

	def insert_chars(self, count=None):
		#raise Exception("todo")
		pass

	def cursor_up(self, count=None):
		self.cursor.y += count or 1
		self.fix_cursors()

	def cursor_down(self, count=None):
		self.cursor.y -= count or 1
		self.fix_cursors()

	def cursor_forward(self, count=None):
		self.cursor.x += count or 1
		self.fix_cursors()

	def cursor_back(self, count=None):
		self.cursor.x -= count or 1
		self.fix_cursors()

	def cursor_next_line(self, count=None):
		self.cursor_down(count)
		self.cursor.x = 0

	def cursor_prev_line(self, count=None):
		self.cursor_up(count)
		self.cursor.x = 0

	def cursor_halign(self, param=None):
		raise Exception("!!!!", param)
		if param:
			self.cursor.x = param - 1
			self.fix_cursors()

	def cursor_set(self, y = None, x = None):
		x = 0 if not x or x == 0 else x - 1
		y = 0 if not y or y == 0 else y - 1
		self.cursor.x = x
		self.cursor.y = y
		self.fix_cursors()

	def fix_cursor_bounds(self, cursor):
		if cursor.x > self.cols:
			cursor.x = self.cols
		if cursor.y >= self.rows:
			cursor.y = self.rows - 1

	def fix_cursors(self):
		self.fix_cursor_bounds(self.cursors[0])
		self.fix_cursor_bounds(self.cursors[1])

	def delete_lines(self, count):
		raise Exception("delete lines")

	def delete_characters(self, *params):
		raise Exception("delete characters")

	def report_da(self, *params):
		self.data_callback("\033[?1;2c")

	def is_alternative_screen(self):
		return self.screen == self.screens[1]
	
	def set_mode(self, *params):
		if len(params) < 0:
			return
		private = False
		if params[-1] == "?":
			private = True
			params = params[:-1]
		for p in params:
			if p == 4:
				self.insert_mode = True
			elif p == 1049 or p == 47 and not self.is_alternative_screen():
				self.screen = self.screen[1]
				self.cursor = self.cursor[1]
			elif p == 1:
				self.cursor_keys = True
			elif p == 2:
				pass
			elif p == 7:
				pass
			elif p == 12:
				pass
			elif p == 25:
				raise Exception("visible cursor")
				self.cursor.visible = True
			elif p == 0:
				pass
			else:
				raise Exception("set mode unkonwn: %s" % p)


	def reset_mode(self, *params):
		if len(params) < 0:
			return
		private = False
		if params[-1] == "?":
			private = True
			params = params[:-1]
		for p in params:
			if p == 4:
				self.insert_mode = False 
			elif p == 1049 or p == 47 and self.is_alternative_screen():
				self.screen = self.screen[0]
				self.cursor = self.cursor[0]
			elif p == 1:
				self.cursor_keys = False
			elif p == 2:
				pass
			elif p == 7:
				pass
			elif p == 12:
				pass
			elif p == 25:
				raise Exception("not visible cursor")
				self.cursor.visible = False
			elif p == 0:
				pass
			else:
				raise Exception("set mode unkonwn: %s" % p)

	def report_status(self, param=None):
		if not param or param not in [5, 6]:
			return
		if param == 5:
			self.data_callback("\033[0n")
		elif param == 6:
			self.data_callback("\033[%d;%dR" % (self.cursor.y + 1, self.cursor.x + 1))

	def scroll_region(self, *params):
		if len(params) < 2:
			return

		self.scroll_top = params[0] - 1
		self.scroll_bottom = params[1] - 1
		if self.scroll_top < 0:
			self.scroll_top = 0
		elif self.scroll_top >= self.rows:
			self.scroll_top = self.rows - 1
		if self.scroll_bottom < 0:
			self.scroll_bottom = 0
		elif self.scroll_bottom >= self.rows:
			self.scroll_bottom = self.rows - 1

	def select_gfx(self, *params):
		i = 0
		lp = len(params)
		# ISO-8613-3 support for 256-colors is implemented
		# 24-bit color support is not implemented
		if (lp == 0):
			raise Exception("no args to gfx")
		while i < lp:
			p = params[i]
			if p == 0:
				# default graphics rendition
				self.gfx = 0
			elif p >= 1 and p <= 9:
				# set a style
				self.gfx &= ~0xff
				self.gfx |= 1 << (p - 1)
			elif p >= 21 and p <= 29:
				# clear a style
				self.gfx &= ~(1 << (p - 21))
			elif p >= 30 and p <= 37:
				self.gfx &= ~(0x00FF0000 | screen.GFX_FG)
				self.gfx |= ((p - 29) << 16)
			elif p == 38 and i + 2 < len(params):
				if params[i+1] == 5:
					self.gfx &= ~0x00ff0000
					self.gfx |= screen.GFX_FG
					self.gfx |= (params[i+2] & 0xff) << 16
					i = i + 2
			elif p == 39:
				self.gfx &= ~(0x00ff0000 | screen.GFX_FG)
			elif p >= 40 and p <= 47:
				self.gfx &= ~(0xFF000000 | screen.GFX_BG)
				self.gfx |= ((p - 39) << 24)
			elif p == 48 and i + 2 < len(params):
				if params[i+1] == 5:
					self.gfx &= ~0x00ff0000
					self.gfx |= screen.GFX_BG
					self.gfx |= (params[i+2] & 0xff) << 24
					i = i + 2
			elif p == 49:
				self.gfx &= ~(0xff000000 | screen.GFX_BG)
			elif p >= 90 and p <= 97:
				self.gfx &= ~(0x00ff0000 | screen.GFX_FG)
				self.gfx |= ((p - 81) << 16)
			elif p >= 100 and p <= 107:
				self.gfx &= ~(0xff000000 | screen.GFX_BG)
				self.gfx |= ((p - 91) << 16)
			else:
				raise Exception("unsupported gfx rendition %i" % p)
			i = i + 1

	def tabulation_clear(self, param = 0):
		if param == 0:
			self.tabstops.discard(self.cursor.x)
		elif param == 3:
			self.tabstops = set()

	def erase_characters(self, count=None):
		if not count or count == 0:
			count = 1
		self.screen.erase_rectangle(self.cursor.y, self.cursor.x, self.cursor.y + 1, self.x + count, self.gfx)

	def erase_in_line(self, param = None):
		if not param:
			param = 0
		if param == 0:
			self.screen.erase_rectangle(self.cursor.y, self.cursor.x, self.cursor.y + 1, self.cols, self.gfx)
		elif param == 1:
			self.screen.erase_rectangle(self.cursor.y, 0, self.cursor.y + 1, self.cursor.x + 1, self.gfx)
		elif param == 2:
			self.screen.erase_rectangle(self.cursor.y, 0, self.cursor.y + 1, self.cols, self.gfx)

	def erase_data(self, param = None):
		if not param:
			param = 0
		if param == 0:
			self.screen.erase_rectangle(self.cursor.y, self.cursor.x, self.cursor.y + 1, self.cols, self.gfx)
			self.screen.erase_rectangle(self.cursor.y + 1, 0, self.rows, self.cols, self.gfx)
		elif param == 1:
			self.screen.erase_rectangle(0, 0, self.cursor.y, self.cols, self.gfx)
			self.screen.erase_rectangle(self.cursor.y, 0, self.cursor.y + 1, self.cursor.x + 1, self.gfx)
		elif param == 2:
			self.screen.erase_rectangle(0, 0, self.rows, self.cols, self.gfx)
			self.cursor.x, self.cursor.y = 0, 0

	def resize(self, rows, cols):
		if rows == self.rows and cols == self.cols:
			return
		self.screens[0].resize(rows, cols)
		self.screens[1].resize(rows, cols)
		self.scroll_top = 0
		self.scroll_bottom = rows - 1
		self.rows = rows
		self.cols = cols
		self.fix_cursors()

	def lf(self):
		if self.cursor.y >= self.scroll_bottom:
			self.screen.scroll_up(self.scroll_top, self.scroll_bottom, self.is_alternative_screen(), self.gfx)
		else:
			self.cursor.y += 1

	def cr(self):
		self.cursor.x = 0

	def newline(self):
		self.lf()
		self.cursor.x = 0

	def write_char(self, ch):
		if self.cursor.x >= self.cols:
			self.newline()

		if self.draw_lines:
			if ch in self.linemap:
				ch = self.linemap[ch]

		if self.insert_mode:
			self.insert_chars([1])

		self.screen.write_char(self.cursor, ch, self.gfx)
		self.cursor.x += 1

		self.update_callback()

	def parse_escape_sequence(self, data):
		l = len(data)
		if l == 0:
			# XXX log
			raise Exception("unhandled escape seq")
			return

		if data[0] != "[":
			# ignore numpad handling
			if data[0] in ["=", ">"]:
				return
			else:
				raise Exception("unhandled data %s" % data)

		seq = data[1:-1]
		mode = ord(data[-1])
		option = None
		if len(seq) > 1 and seq[0] in ["?", ">", "!"]:
			option = seq[0]
			seq = seq[1]
		try:
			if len(seq) > 0:
				params = [int(x) for x in seq.split(";")]
			else:
				params = [0]
		except Exception as e:
			params = [0]

		if mode not in self.csi_dispatch:
			s="".join(["%x " % ord(x) for x in data])
			s2="".join(["%c " % ord(x) for x in data])
			self.write_debug_logdata("! unknown CSI: %s [%s]" % (s2, s))
			return

		if not option:
			self.csi_dispatch[mode](*params)
		else:
			self.csi_dispatch[mode](*params, option)
		self.write_debug_logdata("ESC %s -> %s" % (data, self.csi_dispatch[mode]))

	def write_debug_logdata(self, data):
		if not self.debug:
			return
		data = data.splitlines()
		for line in data:
			self.debuglog.append(line)
		ld = len(self.debuglog)
		if ld > self.debugloglen:
			self.debuglog = self.debuglog[ld - self.debugloglen:]

	def parse_data(self, data):
		for c in data:
			oc = ord(c)
			if self.set_title:
				if oc != ctrl.BEL:
					self.escape_str += c
					continue
				if self.ignore_title == False:
					self.title_callback(self.escape_str)
				self.escape_str = ""
				self.set_title = False
				continue
			elif oc in self.ctrl_dispatch:
				self.ctrl_dispatch[oc]()
				continue
			elif self.in_escape and not self.in_csi:
				self.escape_str += c
				l = len(self.escape_str)
				if l == 1 and c == "[":
					self.in_csi = True
					continue	
				elif l == 1 and c != "[" and c != "]" and c not in self.charset:
					self.parse_escape_sequence(self.escape_str)
					self.escape_str = ""
					self.in_escape = False
					continue
				elif l == 2 and self.escape_str[0] in self.charset:
					if self.escape_str == "(0":
						self.draw_lines = True
					else:
						self.draw_lines = False
					self.escape_str = ""
					self.in_escape = False	
					continue
				elif l > 1 and self.escape_str[0] == "]" and c == ";":
					self.set_title = True
					try:
						param = [int(x) for x in self.escape_str[1:-1].split(";")]
					except:
						param = [0]
					if len(param) == 0 or param[0]==0 or param[0] == 2:
						self.ignore_title = False
					else:
						self.ignore_title = True
					self.in_escape = False
					self.escape_str = ""
					continue
			elif self.in_csi:
				self.escape_str += c
				if oc >= ord("@") and oc <= ord("~"):
					self.parse_escape_sequence(self.escape_str)
					self.in_csi = False
					self.in_escape = False
					self.escape_str = ""
				continue
			elif oc == ctrl.ESC:
				self.in_escape = True
				continue
			else:
				self.write_char(c)

	def input_data(self, data):
		try:
			data = data.decode(encoding="utf8")
			self.parse_data(data)
		except Exception as e:
			self.write_debug_logdata(e)
