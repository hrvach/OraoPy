
from .heatmap import MemHeatmap
from .access_map import AccessMap
from .text_label import TextLabel

class MicroMemView:
	mem_map = None
	read_map = None
	write_map = None

	def __init__(self, size=0x1000, start_addr=0, caption='Unnamed', disp_width=256):
		self.mem_map = MemHeatmap(start_addr=start_addr, size=size, disp_width=disp_width)
		self.mem_map.surf.set_alpha(128)
		self.caption = TextLabel("%04X-%04X: %s (%d bpl)" % (start_addr, start_addr+size-1, caption, disp_width))

		self.read_map = AccessMap(start_addr=start_addr, size=size, disp_width=disp_width, color=(0,128+64,255))
		self.write_map = AccessMap(start_addr=start_addr, size=size, disp_width=disp_width)
		self.width = self.mem_map.width
		self.height = self.mem_map.height

	def render(self, cpu, frame_time_ms):
		self.mem_map.render(cpu, frame_time_ms)
		self.read_map.render(cpu, frame_time_ms)
		self.write_map.render(cpu, frame_time_ms)

	def blit(self, screen, pos, scale=1):
		x,y = pos
		_,y = self.caption.blit(screen, pos)
		self.mem_map.blit(screen, (x,y), scale=scale)
		self.read_map.blit(screen, (x,y), scale=scale)
		x, y = self.write_map.blit(screen, (x,y), scale=scale)
		return [x, y]

	def listen(self, cpu):
		cpu.store_mem_listeners.append(self.write_map.mem_listener)
		cpu.read_mem_listeners.append(self.read_map.mem_listener)
