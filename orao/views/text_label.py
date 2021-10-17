import pygame
from .view import View
from ..chargen import chargen_draw_str


class TextLabel(View):
	def __init__(self, text):
		self.init_surface(pygame.Surface((len(text)*8, 8), depth=24))
		chargen_draw_str(self.surf, 0,0, text, color=(0xff, 0xcc, 0x00))
