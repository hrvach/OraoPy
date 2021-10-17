import pygame

class View:
	surf = None
	scale_method = pygame.transform.scale

	def init_surface(self, surf):
		self.surf = surf
		self.width = self.surf.get_width()
		self.height = self.surf.get_height()

	def set_smooth_scale(self):
		self.scale_method = pygame.transform.smoothscale

	def scaled_surf(self, f):
		return self.scale_method(self.surf, (int(self.width * f), int(self.surf.get_height() * f)))

	def dims(self):
		return self.width, self.height

	def blit(self, screen, pos, scale=1):
		if self.surf is None:
			return pos

		# if scale == 1:
		# 	screen.blit(self.surf, pos)
		# else:
		screen.blit(self.scaled_surf(scale), pos)

		x, y = pos
		return [int(x + self.width * scale), int(y + self.height * scale)]
