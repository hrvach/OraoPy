#!/usr/bin/python3
# -*- coding: utf8 -*-

import pygame, numpy, sys, datetime
from orao.cpu import CPU
from orao.keyboard import listener as orao_kbd_listener
from orao.video import mem_listener as video_mem_listener, terminal
from orao.timer import mem_listener as timer_mem_listener
from orao.chargen import chargen_init, chargen_draw_str

# views
from orao.views.cpu_state import CPUState
from orao.views.micro_mem_view import MicroMemView

MEM_LOAD_PRG = None

if len(sys.argv) == 2:
    MEM_LOAD_PRG = sys.argv[1]


# pygame init
ratio, running = 0, True

# mixer setup
pygame.mixer.pre_init(44100, 8, 1, buffer=2048)
pygame.init()
pygame.time.set_timer(pygame.USEREVENT + 1, 40)

# create CPU
cpu = CPU(bytearray([0xFF]*0xC000) + bytearray(open('ORAO13.ROM', 'rb').read()))
cpu.channel = pygame.mixer.Channel(0)
cpu.store_mem_listeners.append(video_mem_listener)
cpu.store_mem_listeners.append(timer_mem_listener)

chargen_init(cpu.memory[0xE000:])

# views
view_cpu_state = CPUState()

# ram zero page & stack
view_zp = MicroMemView(start_addr=0x0000, size=0x0200, caption='ZP & stack', disp_width=64)
view_zp.listen(cpu)

# user ram view
view_ram = MicroMemView(start_addr=0x0200, size=0x5E00, caption='RAM', disp_width=128)
view_ram.listen(cpu)

# rom access view
view_rom = MicroMemView(start_addr=0xC000, size=0x4000, caption='ROM', disp_width=256)
view_rom.listen(cpu)

view_screen = MicroMemView(start_addr=0x6000, size=0x2000, disp_width=32)
view_screen.listen(cpu)

# status lines
status_line = pygame.Surface((64 * 8, 4*8), depth=24)
status_line.fill((0, 0, 0))
chargen_draw_str(status_line, 0, 0, 'Orao Emulator v0.1')

# setup screen
screen = pygame.display.set_mode((
    terminal.get_width() * 2 + 2 + int(max(view_rom.width, view_cpu_state.width * 2)),
    terminal.get_height() * 2 + 3*8 + 2 + 30
))
pygame.display.set_caption('Orao Emulator v0.1')

lc = (0xff, 0xcc, 0x00)
chargen_draw_str(status_line, 0, 16, 'F12:', color=lc)
chargen_draw_str(status_line, 24+8, 16, ' SCREENSHOT')

if MEM_LOAD_PRG is not None:
    chargen_draw_str(status_line, 0, 24, 'F8:', color=lc)
    chargen_draw_str(status_line, 24, 24, ' %s' % MEM_LOAD_PRG)

def render_frame(frame_time_ms):
    view_cpu_state.render(cpu, frame_time_ms)
    view_zp.render(cpu, frame_time_ms)
    view_ram.render(cpu, frame_time_ms)
    view_rom.render(cpu, frame_time_ms)
    view_screen.render(cpu, frame_time_ms)

    # blit
    screen.fill((0, 0, 0))
    screen.blit(pygame.transform.scale(terminal, (512, 512)), [0, 0])
    chargen_draw_str(status_line, 0, 8, 'Speed: {0:.2f} MHz'.format(ratio))
    screen.blit(status_line, [0, 512+1])
    x = 512 + 1
    y = 0
    cx, y = view_cpu_state.blit(screen, [x, y], scale=2)

    y += 5
    x2, y2 = view_zp.blit(screen, [x, y], scale=4)
    y2 += 5
    _, y2 = view_ram.blit(screen, [x, y2], scale=2)
    y2 += 5
    _, _ = view_rom.blit(screen, [x, y2], scale=1)

    screen.blit(pygame.transform.scale(view_screen.read_map.surf, (512,512)), [0,0])
    screen.blit(pygame.transform.scale(view_screen.write_map.surf, (512,512)), [0,0])

    # finish rendering
    pygame.display.flip()

clock = pygame.time.Clock()

while running:
    before, previous_loop_cycles = datetime.datetime.now(), cpu.cycles

    for i in range(5000):
        cpu.step()

    time_elapsed = (datetime.datetime.now()-before).microseconds + 1
    clock.tick()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            if 650 < x < 700 and 720 < y < 790:             # Reset button
                cpu.__init__(cpu.memory[:])                 # Warm reset

        orao_kbd_listener(event, cpu)

        if event.type in [pygame.KEYDOWN, pygame.KEYUP]:
            pkeys = pygame.key.get_pressed()
            if pkeys[pygame.K_ESCAPE]:
                running = False

            if pkeys[pygame.K_F8]:
                if MEM_LOAD_PRG is None:
                    break
                print("LOADING: %s" % MEM_LOAD_PRG)
                ba = bytearray(open(MEM_LOAD_PRG, "rb").read())

                # read load address
                addr = ba[1] * 256 + ba[0]
                ba = ba[2:]
                print('Loadaddr: %04x' % addr)

                # load file to memory
                for i in range(0, len(ba)):
                    cpu.memory[addr + i] = ba[i]

                # run
                cpu.pc = addr
                # HACK: reset stack pointer
                cpu.sp = 241

            if pkeys[pygame.K_F12]:
                now = datetime.datetime.now()  # current date and time
                pygame.image.save(screen, "assets/screenshot-%s.png" % now.strftime("%Y%m%d-%H%M%S"))

        if event.type == pygame.USEREVENT + 1:
            render_frame(clock.get_time())

            cpu.tape_out = None if cpu.cycles - cpu.last_sound_cycles > 20000 else cpu.tape_out

            if len(cpu.sndbuf) > 4096 or cpu.sndbuf and cpu.cycles - cpu.last_sound_cycles > 20000:
                while cpu.channel.get_queue():
                    if time_elapsed > 10000: break

                cpu.channel.queue(pygame.sndarray.make_sound(numpy.uint8(cpu.sndbuf)))
                cpu.sndbuf = []

    overshoot = cpu.cycles - previous_loop_cycles - time_elapsed
    pygame.time.wait((overshoot > 0) * overshoot // 1000)      # Pričekaj da budemo cycle exact

    ratio = 1.0 * (cpu.cycles - previous_loop_cycles) / time_elapsed

pygame.quit()
