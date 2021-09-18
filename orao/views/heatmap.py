import pygame
import numpy
from ..chargen import chargen_draw_str

MAX_LABELS = 33

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

	def __init__(self):
		# mem view surface
		self.surf = pygame.Surface(self.dims, depth=8)
		self.surf.set_palette(palette)

		# label surface
		self.surf_labels = pygame.Surface((2 * 8 + 1, MAX_LABELS * 8 * 2), depth=24)

		self.width = self.surf.get_width()
		self.width += self.surf_labels.get_width() + 1

		self.height = self.surf.get_height()
		self.surf.fill((0, 0, 0))
		self.surf_labels.fill((0, 0, 0))

		# build labels
		for i in range(0, MAX_LABELS):
			chargen_draw_str(self.surf_labels, 0, i * 8 * 3, '%02X' % i, color=(0xff, 0xcc, 0x00))
			self.surf_labels.set_at((16, i * 8 * 3), (0, 255, 0))

	def scale(self, f):
		return pygame.transform.scale(self.surf, (int(self.surf.get_width() * f), int(self.surf.get_height() * f)))

	def render(self, cpu):
		w, h = self.dims
		arr = numpy.reshape(cpu.memory[0:(w * h)], (h, w))
		pygame.surfarray.blit_array(self.surf, numpy.transpose(arr))
		pass

	def blit(self, screen, pos, scale=1):
		x, y = pos
		screen.blit(self.surf_labels, pos)
		screen.blit(self.scale(3), [x + self.surf_labels.get_width()+1, y])
		return [x + self.width, y + self.height]
