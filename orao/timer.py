
timer = {}

def mem_listener(addr, val, cpu):
	if addr >= 0xa000 and addr <= 0xa0ff:
		timer_ix = addr & 0xff
		if timer_ix in timer:
			print('timer(%s):duration %d cy' % (timer_ix, cpu.cycles - timer[timer_ix] - 4))
			del timer[timer_ix]
		else:
			timer[timer_ix] = cpu.cycles
