import pygame
import numpy
from .view import View

palette = []
# below chars
palette += [(i * 8, 0, 0) for i in range(32)]
# text chars
palette += [(i * 2, 255, 0) for i in range(128 - 32)]
# other
palette += [(i * 2, 0, 255) for i in range(128)]

# displays memory locations as colors of palette based on value

class MemHeatmap(View):
	surf = None
	start_addr = 0
	size = 0

	def __init__(self, size=0x1000, start_addr=0, disp_width=256):
		self.start_addr = start_addr
		self.size = size

		dims = (disp_width, size / disp_width)
		self.init_surface(pygame.Surface(dims, depth=8))
		self.surf.set_palette(palette)

	def render(self, cpu, frame_time_ms):
		w, h = self.dims()
		mem = cpu.memory[self.start_addr:self.start_addr + (w * h)]
		arr = numpy.reshape(mem, (h, w))
		pygame.surfarray.blit_array(self.surf, numpy.transpose(arr))

