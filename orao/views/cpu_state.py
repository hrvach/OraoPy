import pygame
from .view import View
from ..chargen import chargen_draw_str


class CPUState(View):

	def __init__(self):
		self.init_surface(pygame.Surface((2 * 8 * 8, 3 * 8), depth=24))
		#self.set_smooth_scale()

	def draw_text(self, x, y, text, color=(0, 255, 0)):
		chargen_draw_str(self.surf, x, y, text, color=color)

	def render(self, cpu, frame_time_ms):
		lc = (0xff, 0xcc, 0x00)
		self.draw_text(0, 0 * 8, 'A  X  Y', color=lc)
		self.draw_text(0, 1 * 8, '%02X %02X %02X' % (cpu.a, cpu.x, cpu.y))

		self.draw_text(0, 2 * 8, 'PC:', color=lc)
		self.draw_text(8 * 8, 2 * 8, 'SP:', color=lc)
		self.draw_text(3 * 8, 2 * 8, '%04X' % cpu.pc)
		self.draw_text(11 * 8, 2 * 8, '%04X' % cpu.sp)

		self.draw_text(8 * 8, 0 * 8, "NVssDIZC", color=lc)
		self.draw_text(8 * 8, 1 * 8, "{0:b}".format(cpu.flags))
