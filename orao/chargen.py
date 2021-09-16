
chars = None

def chargen_init(char_data):
	global chars
	chars = char_data


def chargen_draw_char(surf, px, py, ch):
	char_loc = (ord(ch) - 32) * 8
	for y in range(8):
		c = chars[char_loc + y]
		for x in range(8):
			if (c >> x) & 1:
				surf.set_at((px + x, py + y), (0, 255, 0))
			else:
				surf.set_at((px + x, py + y), (0, 0, 0))


def chargen_draw_str(surf, px, py, str):
	for x in range(len(str)):
		chargen_draw_char(surf, px + x * 8, py, str[x])
