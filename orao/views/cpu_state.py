import pygame
from ..chargen import chargen_draw_str

class CPUState:
	surf = None

	def __init__(self):
		self.surf = pygame.Surface((8 * 8, 6 * 8), depth=24)
		self.width = self.surf.get_width()
		self.height = self.surf.get_height()
		self.surf.fill((0, 0, 0))

	def scale(self, f):
		return pygame.transform.smoothscale(self.surf, (int(self.width * f), int(self.height * f)))

	def render(self, cpu):
		lc = (0xff, 0xcc, 0x00)
		chargen_draw_str(self.surf, 0, 0*8, 'A  X  Y', color=lc)
		chargen_draw_str(self.surf, 0, 1*8, '%02X %02X %02X' % (cpu.a, cpu.x, cpu.y))

		chargen_draw_str(self.surf, 0, 2*8, 'PC:', color=lc)
		chargen_draw_str(self.surf, 0, 3*8, 'SP:', color=lc)
		chargen_draw_str(self.surf, 4*8, 2*8, '%04X' % cpu.pc)
		chargen_draw_str(self.surf, 4*8, 3*8, '%04X' % cpu.sp)

		chargen_draw_str(self.surf, 0, 4*8, "NVssDIZC", color=lc)
		chargen_draw_str(self.surf, 0, 5*8, "{0:b}".format(cpu.flags))

	def blit(self, screen, pos, scale=1):
		if scale == 1:
			screen.blit(self.surf, pos)
			return (pos[0], pos[1] + self.height)
		else:
			screen.blit(self.scale(scale), pos)
			return (pos[0], pos[1] + int(self.height*scale))
