#!/usr/bin/env python3

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

	print("colors = [\n\t%s\n]" % genstringforcolors(colors))
	print("back_colors = [\n\t%s\n]" % genstringforcolors(back_colors))
	print("fore_colors = [\n\t%s\n]" % genstringforcolors(fore_colors))

generate_colors()
