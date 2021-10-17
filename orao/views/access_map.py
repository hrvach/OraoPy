
import pygame
from .view import View

# mark accessed locations

class AccessMap(View):
	decay_locations = []

	def __init__(self, size=0x5F00, start_addr=0, disp_width=256, color=(255, 0, 0)):
		self.start_addr = start_addr
		self.size = size
		self.disp_width = disp_width

		dims = (disp_width, size / disp_width)
		self.init_surface(pygame.Surface(dims, pygame.SRCALPHA, depth=32))
		r,g,b = color
		self.surf.fill((r, g, b, 0))
		self.writes = []

	def render(self, cpu, frame_time_ms):
		# decay alfa
		decay = int(frame_time_ms*256/500)
		new_decay_locations = []
		alpha = pygame.surfarray.pixels_alpha(self.surf)

		for w in self.decay_locations:
			v = alpha[w]
			if v > 0:
				nv = max(v-decay,0)
				alpha[w] = nv
				if nv > 0:
					new_decay_locations.append(w)

		# mark new writes
		for w in self.writes:
			alpha[w] = 192
			new_decay_locations.append(w)

		alpha = None
		self.writes = []
		self.decay_locations = new_decay_locations

	def mem_listener(self, addr, val, cpu):
		if addr < self.start_addr:
			return

		addr -= self.start_addr
		if addr >= self.size:
			return

		y, x = divmod(addr, self.disp_width)
		self.writes.append((x, y))
