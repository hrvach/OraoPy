import pygame
import numpy

palette = []
# below chars
palette += [(i * 8, 0, 0) for i in range(32)]
# text chars
palette += [(i * 2, 255, 0) for i in range(128 - 32)]
# other
palette += [(i * 2, 0, 255) for i in range(128)]

micro_mem_view_dims = (32, 192)
micro_mem_view = pygame.Surface(micro_mem_view_dims, depth=8)
micro_mem_view.set_palette(palette)

def store_mem_view(memory):
	w, h = micro_mem_view_dims
	arr = numpy.reshape(memory[0:(w * h)], (h, w))
	pygame.surfarray.blit_array(micro_mem_view, numpy.transpose(arr))
