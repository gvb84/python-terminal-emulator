from PyQt5.QtGui import QFont, QFontMetricsF

class MonoFont:
	def __init__(self, name, size):
		self.font = QFont(name, size)
		self.font.setKerning(False)
		self.ascent = int(QFontMetricsF(self.font).ascent())
		self.charWidth = QFontMetricsF(self.font).width("X")
		self.charHeight = int(QFontMetricsF(self.font).height())
		self.charOffset = 0 # can introduce extra linespacing here

		self.bold = QFont(self.font)
		self.bold.setBold(True)

		self.under = QFont(self.font)
		self.under.setUnderline(True)

		# align character width properly
		if self.charWidth % 1.0 < 0.5:
			adjust = -(self.charWidth % 1.0)
		else:
			adjust = 1.0 - (self.charWidth % 1.0)

		self.charWidth += adjust
		self.font.setLetterSpacing(QFont.AbsoluteSpacing, adjust)
		self.bold.setLetterSpacing(QFont.AbsoluteSpacing, adjust)
		self.under.setLetterSpacing(QFont.AbsoluteSpacing, adjust)

	
