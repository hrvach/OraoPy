import pygame
import numpy
from ..chargen import chargen_draw_str

SURF_SCALE = 2

palette = []
# below chars
palette += [(i * 8, 0, 0) for i in range(32)]
# text chars
palette += [(i * 2, 255, 0) for i in range(128 - 32)]
# other
palette += [(i * 2, 0, 255) for i in range(128)]


class MemHeatmap:
	dims = (32, 192)
	surf = None
	tick_color = (0xff, 0xcc, 0x00)
	label_color = (0xff, 0xcc, 0x00)
	tick_size = 2
	start_addr = 0

	def __init__(self, size=16, start_addr=0):
		# mem view surface
		self.start_addr = start_addr
		self.dims = (32, size * 8)
		self.surf = pygame.Surface(self.dims, depth=8)
		self.surf.set_palette(palette)

		# label surface
		self.surf_labels = pygame.Surface((2 * 8 + self.tick_size, size * 8 * 2), depth=24)

		self.width = self.surf.get_width() * SURF_SCALE
		self.width += self.surf_labels.get_width()

		self.height = self.surf.get_height()
		self.surf.fill((0, 0, 0))
		self.surf_labels.fill((0, 0, 0))

		# build labels
		for i in range(0, size):
			y = i * 8 * SURF_SCALE
			chargen_draw_str(self.surf_labels, 0, y, '%02X' % i, color=self.label_color)
			# draw ticks
			for t in range(0, self.tick_size):
				self.surf_labels.set_at((16 + t, y), self.tick_color)

	def scale(self, f):
		return pygame.transform.scale(self.surf, (int(self.surf.get_width() * f), int(self.surf.get_height() * f)))

	def render(self, cpu):
		w, h = self.dims
		arr = numpy.reshape(cpu.memory[self.start_addr:(w * h)], (h, w))
		pygame.surfarray.blit_array(self.surf, numpy.transpose(arr))

	def blit(self, screen, pos, scale=1):
		x, y = pos
		screen.blit(self.surf_labels, pos)
		x += self.surf_labels.get_width()
		screen.blit(self.scale(SURF_SCALE), [x, y])
		return [x + self.width, y + self.height]
