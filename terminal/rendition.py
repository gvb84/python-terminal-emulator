"""
generate the color scheme with the code below

def generate_colors():
	# System colors
	dim_colors = [(0,0,0), (135, 0, 0), (0, 135, 0), (135, 135, 0),
		(0, 0, 135), (135, 0, 135), (0, 135, 135), (135, 135, 135)]
	normal_colors = [(46, 52, 54), (204, 0, 0), (78, 154, 6), (196, 160, 0),
		(52, 101, 164), (117, 80, 123), (6, 152, 154), (211, 215, 207)]
	bright_colors = [(85, 87, 83), (239, 41, 41), (138, 226, 52), (252, 233, 79),
		(114, 159, 207), (173, 127, 168), (52, 226, 226), (255,255,255)]

	# Create color arrays for normal mode
	fore_colors = [(255,255,255)] + dim_colors + normal_colors + bright_colors + bright_colors
	back_colors = [(0,0,0)] + normal_colors + bright_colors

	# Create color array for 256-color mode
	colors = normal_colors + bright_colors

	values = [0x00, 0x5f, 0x87, 0xaf, 0xd7, 0xff]
	for red in values:
		for green in values:
			for blue in values:
				color = (red, green, blue)
				colors.append(color)

	values = [0x08, 0x12, 0x1c, 0x26, 0x30, 0x3a, 0x44, 0x4e, 0x58, 0x62, 0x6c, 0x76, 0x80, 0x8a, 0x94, 0x9e,
		0xa8, 0xb2, 0xbc, 0xc6, 0xd0, 0xda, 0xe4, 0xee]
	for gray in values:
		color = (gray, gray, gray)
		colors.append(color)

	def genstringforcolors(colors):
		s2 = []
		i = 0
		for c in colors:
			if i > 0 and i % 5 == 0:
				s2.append("\n\t")
			s2.append("(%3i,%3i,%3i), " % (c[0],c[1],c[2]))
			i = i + 1
		return "".join(s2)[:-2]

	print "colors = [\n\t%s\n]" % genstringforcolors(colors)
	print "back_colors = [\n\t%s\n]" % genstringforcolors(back_colors)
	print "fore_colors = [\n\t%s\n]" % genstringforcolors(fore_colors)

generate_colors()
"""
colors = [
	( 46, 52, 54), (204,  0,  0), ( 78,154,  6), (196,160,  0), ( 52,101,164), 
	(117, 80,123), (  6,152,154), (211,215,207), ( 85, 87, 83), (239, 41, 41), 
	(138,226, 52), (252,233, 79), (114,159,207), (173,127,168), ( 52,226,226), 
	(255,255,255), (  0,  0,  0), (  0,  0, 95), (  0,  0,135), (  0,  0,175), 
	(  0,  0,215), (  0,  0,255), (  0, 95,  0), (  0, 95, 95), (  0, 95,135), 
	(  0, 95,175), (  0, 95,215), (  0, 95,255), (  0,135,  0), (  0,135, 95), 
	(  0,135,135), (  0,135,175), (  0,135,215), (  0,135,255), (  0,175,  0), 
	(  0,175, 95), (  0,175,135), (  0,175,175), (  0,175,215), (  0,175,255), 
	(  0,215,  0), (  0,215, 95), (  0,215,135), (  0,215,175), (  0,215,215), 
	(  0,215,255), (  0,255,  0), (  0,255, 95), (  0,255,135), (  0,255,175), 
	(  0,255,215), (  0,255,255), ( 95,  0,  0), ( 95,  0, 95), ( 95,  0,135), 
	( 95,  0,175), ( 95,  0,215), ( 95,  0,255), ( 95, 95,  0), ( 95, 95, 95), 
	( 95, 95,135), ( 95, 95,175), ( 95, 95,215), ( 95, 95,255), ( 95,135,  0), 
	( 95,135, 95), ( 95,135,135), ( 95,135,175), ( 95,135,215), ( 95,135,255), 
	( 95,175,  0), ( 95,175, 95), ( 95,175,135), ( 95,175,175), ( 95,175,215), 
	( 95,175,255), ( 95,215,  0), ( 95,215, 95), ( 95,215,135), ( 95,215,175), 
	( 95,215,215), ( 95,215,255), ( 95,255,  0), ( 95,255, 95), ( 95,255,135), 
	( 95,255,175), ( 95,255,215), ( 95,255,255), (135,  0,  0), (135,  0, 95), 
	(135,  0,135), (135,  0,175), (135,  0,215), (135,  0,255), (135, 95,  0), 
	(135, 95, 95), (135, 95,135), (135, 95,175), (135, 95,215), (135, 95,255), 
	(135,135,  0), (135,135, 95), (135,135,135), (135,135,175), (135,135,215), 
	(135,135,255), (135,175,  0), (135,175, 95), (135,175,135), (135,175,175), 
	(135,175,215), (135,175,255), (135,215,  0), (135,215, 95), (135,215,135), 
	(135,215,175), (135,215,215), (135,215,255), (135,255,  0), (135,255, 95), 
	(135,255,135), (135,255,175), (135,255,215), (135,255,255), (175,  0,  0), 
	(175,  0, 95), (175,  0,135), (175,  0,175), (175,  0,215), (175,  0,255), 
	(175, 95,  0), (175, 95, 95), (175, 95,135), (175, 95,175), (175, 95,215), 
	(175, 95,255), (175,135,  0), (175,135, 95), (175,135,135), (175,135,175), 
	(175,135,215), (175,135,255), (175,175,  0), (175,175, 95), (175,175,135), 
	(175,175,175), (175,175,215), (175,175,255), (175,215,  0), (175,215, 95), 
	(175,215,135), (175,215,175), (175,215,215), (175,215,255), (175,255,  0), 
	(175,255, 95), (175,255,135), (175,255,175), (175,255,215), (175,255,255), 
	(215,  0,  0), (215,  0, 95), (215,  0,135), (215,  0,175), (215,  0,215), 
	(215,  0,255), (215, 95,  0), (215, 95, 95), (215, 95,135), (215, 95,175), 
	(215, 95,215), (215, 95,255), (215,135,  0), (215,135, 95), (215,135,135), 
	(215,135,175), (215,135,215), (215,135,255), (215,175,  0), (215,175, 95), 
	(215,175,135), (215,175,175), (215,175,215), (215,175,255), (215,215,  0), 
	(215,215, 95), (215,215,135), (215,215,175), (215,215,215), (215,215,255), 
	(215,255,  0), (215,255, 95), (215,255,135), (215,255,175), (215,255,215), 
	(215,255,255), (255,  0,  0), (255,  0, 95), (255,  0,135), (255,  0,175), 
	(255,  0,215), (255,  0,255), (255, 95,  0), (255, 95, 95), (255, 95,135), 
	(255, 95,175), (255, 95,215), (255, 95,255), (255,135,  0), (255,135, 95), 
	(255,135,135), (255,135,175), (255,135,215), (255,135,255), (255,175,  0), 
	(255,175, 95), (255,175,135), (255,175,175), (255,175,215), (255,175,255), 
	(255,215,  0), (255,215, 95), (255,215,135), (255,215,175), (255,215,215), 
	(255,215,255), (255,255,  0), (255,255, 95), (255,255,135), (255,255,175), 
	(255,255,215), (255,255,255), (  8,  8,  8), ( 18, 18, 18), ( 28, 28, 28), 
	( 38, 38, 38), ( 48, 48, 48), ( 58, 58, 58), ( 68, 68, 68), ( 78, 78, 78), 
	( 88, 88, 88), ( 98, 98, 98), (108,108,108), (118,118,118), (128,128,128), 
	(138,138,138), (148,148,148), (158,158,158), (168,168,168), (178,178,178), 
	(188,188,188), (198,198,198), (208,208,208), (218,218,218), (228,228,228), 
	(238,238,238)
]

back_colors = [
	(  0,  0,  0), ( 46, 52, 54), (204,  0,  0), ( 78,154,  6), (196,160,  0), 
	( 52,101,164), (117, 80,123), (  6,152,154), (211,215,207), ( 85, 87, 83), 
	(239, 41, 41), (138,226, 52), (252,233, 79), (114,159,207), (173,127,168), 
	( 52,226,226), (255,255,255)
]

fore_colors = [
	(255,255,255), (  0,  0,  0), (135,  0,  0), (  0,135,  0), (135,135,  0), 
	(  0,  0,135), (135,  0,135), (  0,135,135), (135,135,135), ( 46, 52, 54), 
	(204,  0,  0), ( 78,154,  6), (196,160,  0), ( 52,101,164), (117, 80,123), 
	(  6,152,154), (211,215,207), ( 85, 87, 83), (239, 41, 41), (138,226, 52), 
	(252,233, 79), (114,159,207), (173,127,168), ( 52,226,226), (255,255,255), 
	( 85, 87, 83), (239, 41, 41), (138,226, 52), (252,233, 79), (114,159,207), 
	(173,127,168), ( 52,226,226), (255,255,255)
]

from . import screen

def get_colors(rendition):
	fg = bg = None
	if rendition & screen.GFX_BG:
		bg = colors[(rendition >> 24) & 0xff]	
	else:
		bg = back_colors[(rendition >> 24) & 0x1f]
	if rendition & screen.GFX_FG:
		if ((rendition >> 16) & 0xff) < 16:
			if rendition & screen.GFX_BOLD:
				fg = fore_colors[((rendition >> 16)&7)+17]
			else:
				fg = fore_colors[((rendition >> 16) & 0xf) + 9]
		else:
			fg = colors[(rendition >> 16) & 0xff]
	elif (rendition & 0x1f0000) == 0 or (rendition & screen.GFX_DIM):
		fg = fore_colors[(rendition >> 16) & 0x1f]
	elif rendition & screen.GFX_BOLD:
		fg = fore_colors[((rendition >> 16) & 0x1f) + 16]
	else:
		fg = fore_colors[((rendition >> 16) & 0x1f) + 8]
	if rendition & screen.GFX_INV:
		fg, bg = bg, fg
	return fg, bg