
chars = None

def chargen_init(char_data):
	global chars
	chars = char_data


def chargen_draw_char(surf, px, py, ch, color=(0, 255, 0), bg=(0, 0, 0)):
	char_loc = (ord(ch) - 32) * 8
	for y in range(8):
		c = chars[char_loc + y]
		for x in range(8):
			if (c >> x) & 1:
				surf.set_at((px + x, py + y), color)
			else:
				surf.set_at((px + x, py + y), bg)


def chargen_draw_str(surf, px, py, str, color=(0, 255, 0), bg=(0, 0, 0)):
	for x in range(len(str)):
		chargen_draw_char(surf, px + x * 8, py, str[x], color=color, bg=bg)
