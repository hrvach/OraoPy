import pygame

terminal = pygame.Surface((256, 256), pygame.SRCALPHA, depth=32)
terminal.fill((255, 255, 255))
alphaarray = pygame.surfarray.pixels_alpha(terminal)

def mem_listener(addr, val, cpu):
	if 0x6000 <= addr <= 0x7FFF:  # Video RAM
		y, x = divmod((addr - 0x6000) * 8, 256)
		for i in range(8):
			alphaarray[x + i, y] = 255 if (val >> i) & 1 else 40  # Transparency mask
