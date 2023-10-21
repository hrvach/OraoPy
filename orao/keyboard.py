# -*- coding: utf8 -*-

# defines orao keyboard

import pygame, numpy

_kbd = {
	0x83FE: (112, 240, 185, 39), 0x83FF: (45, 48),    # [p đ š ;]  [-  0]
	0x85FE: (232, 230, 190, 43), 0x85FF: (8, 94),     # [č ć ž :]  [BS ^]
	0x86FE: (102, 104, 103, 110), 0x86FF: (98, 118),  # [f h g n]  [b  v]
	0x877E: (100, 97, 115, 122), 0x877F: (120, 99),   # [d a s z]  [x  c]
	0x87BE: (108, 106, 107, 109), 0x87BF: (44, 46),   # [l j k m]  [,  .]
	0x87DE: (101, 113, 119, 49), 0x87DF: (50, 51),    # [e q w l]  [2  3]
	0x87EE: (111, 105, 117, 55), 0x87EF: (56, 57),    # [o i u 7]  [8  9]
	0x87F6: (114, 121, 116, 54), 0x87F7: (53, 52),    # [r y t 6]  [5  4]
	0x87FA: (282, 283, 284, pygame.K_RCTRL), 0x87FD: (13, pygame.K_LCTRL),  # [f1f2f3f4] [cr l_ctrl]
	0x87FC: (pygame.K_LEFT, pygame.K_UP, pygame.K_DOWN, pygame.K_RIGHT),
	0x87FB: (32, pygame.K_RSHIFT) # [spc l_shift]
}

def listener(event, cpu):
	if event.type in [pygame.KEYDOWN, pygame.KEYUP]:
		for address, keycodes in _kbd.items():
			keys = list(map(pygame.key.get_pressed().__getitem__, keycodes))
			cpu.memory[address] = ~numpy.dot(keys, [16, 32, 64, 128][:len(keys)]) & 0xFF

