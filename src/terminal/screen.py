import array

from . import rendition

class Screen:
	def __init__(self, rows, cols):
		self.reset(rows, cols)

	def reset(self, rows, cols):
		self.cols = cols
		self.rows = rows
		self.cells = []
		self.gfx = []
		self.empty_line = array.array("u", u" "*cols)
		self.empty_gfx = array.array("I", [0]*cols)
		
		for i in range(0, rows):
			self.cells.append(array.array("u", self.empty_line))
			self.gfx.append(array.array("I", self.empty_gfx))

	def scroll_up(self, scroll_top, scroll_bottom, alt, current_gfx):
		top_screen = self.cells.pop(scroll_top)
		top_gfx = self.gfx.pop(scroll_top)
		if scroll_top == 0 and scroll_bottom == self.rows -1 and alt:
			top_screen = array.array("u", self.empty_line)
			top_gfx = array.array("I", self.empty_gfx)
		else:
			top_screen[0:self.cols] = array.array("u", self.empty_line)
			top_gfx[0:self.cols] = array.array("I", self.empty_gfx)
		for i in range(0, self.cols):
			top_gfx[i] = current_gfx
		self.cells.insert(scroll_bottom, top_screen) 
		self.gfx.insert(scroll_bottom, top_gfx)

	def resize(self, rows, cols):
		if rows > self.rows:
			for row in range(self.rows, rows):
				self.cells.append(array.array("u", self.empty_line))
				self.gfx.append(array.array("I", self.empty_gfx))
		elif rows < self.rows:
			self.cells = self.cells[:rows]
			self.gfx = self.gfx[:rows]
		if cols > self.cols:
			for row in range(0, rows):
				for col in range(self.cols, cols):
					self.cells[row].append(u" ")
					self.gfx[row].append(0)
			self.empty_line = array.array("u", u" "*cols)
			self.empty_gfx = array.array("I", [0]*cols)
		elif cols < self.cols:
			for row in range(0, rows):
				self.cells[row] = self.cells[row][0:cols]
				self.gfx[row] = self.gfx[row][0:cols]
			self.empty_line = self.empty_line[0:cols]
			self.empty_gfx = self.empty_gfx[0:cols]
		self.rows = rows
		self.cols = cols

	def write_char(self, cursor, ch, gfx):
		self.cells[cursor.y][cursor.x] = ch	
		self.gfx[cursor.y][cursor.x] = gfx | rendition.GFX_WRITTEN

	def erase_rectangle(self, top_row, left_col, bot_row, right_col, gfx=0): # XXX: need to pass in active rendition
		for y in range(top_row, bot_row):
			if y < 0 or y >= self.rows:
				continue
			for x in range(left_col, right_col):
				if x < 0 or x >= self.cols:
					continue
				self.cells[y][x] = u" " 
				self.gfx[y][x] = gfx
