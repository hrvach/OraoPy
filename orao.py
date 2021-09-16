#!/usr/bin/python2
# -*- coding: utf8 -*-

import pygame, numpy, sys, datetime, wave, time
from orao.cpu import CPU
from orao.keyboard import listener as orao_kbd_listener
from orao.video import mem_listener as video_mem_listener, terminal
from orao.timer import mem_listener as timer_mem_listener
from orao.chargen import chargen_init, chargen_draw_str

MEM_LOAD_PRG = None

if len(sys.argv) == 2:
    MEM_LOAD_PRG = sys.argv[1]


# pygame init
ratio, running = 0, True

pygame.mixer.pre_init(44100, 8, 1, buffer=2048)
pygame.init()
pygame.time.set_timer(pygame.USEREVENT + 1, 40)

# setup surfaces
screen = pygame.display.set_mode((512+1+8+8+1+1+32*3, 512+ 3*8 + 2))
pygame.display.set_caption('Orao Emulator v0.1')
from orao.micro_mem_view import micro_mem_view, store_mem_view, micro_mem_view_dims

# create CPU
cpu = CPU(bytearray([0xFF]*0xC000) + bytearray(open('ORAO13.ROM', 'rb').read()))
cpu.channel = pygame.mixer.Channel(0)
cpu.store_mem_listeners.append(video_mem_listener)
cpu.store_mem_listeners.append(timer_mem_listener)

chargen_init(cpu.memory[0xE000:])

# status lines
status_line = pygame.Surface((64 * 8, 3*8), depth=24)
status_line.fill((0, 0, 0))
chargen_draw_str(status_line, 0, 0, 'Orao Emulator v0.1')
if MEM_LOAD_PRG is not None:
    chargen_draw_str(status_line, 0, 16, 'F8:', color=(0, 0, 0), bg=(0, 255, 0))
    chargen_draw_str(status_line, 24, 16, ' %s' % MEM_LOAD_PRG)

# memory view labels
MAX_LABELS = 33
mem_map_labels = pygame.Surface((2*8+1, MAX_LABELS*8*2), depth=24)
mem_map_labels.fill((0, 0, 0))
for i in range(0, MAX_LABELS):
    chargen_draw_str(mem_map_labels, 0, i*8*3, '%02x' % i, color=(0xff, 0xcc, 0x00))
    mem_map_labels.set_at((16, i*8*3), (0, 255, 0))

def render_frame():
    store_mem_view(cpu.memory)

    screen.fill((0, 0, 0))
    screen.blit(pygame.transform.smoothscale(terminal, (512, 512)), [0, 0])
    chargen_draw_str(status_line, 0, 8, 'Speed: {0:.2f} MHz'.format(ratio))
    screen.blit(status_line, [0, 512+1])
    w, h = micro_mem_view_dims
    screen.blit(mem_map_labels, [512+1, 0])
    screen.blit(pygame.transform.scale(micro_mem_view, (w * 3, h * 3)), [512 + 1 + 8 + 8 + 1 + 1, 0])
    pygame.display.flip()

while running:
    before, previous_loop_cycles = datetime.datetime.now(), cpu.cycles
    time_elapsed = lambda: (datetime.datetime.now()-before).microseconds + 1

    for i in range(5000):
        cpu.step()

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

        if event.type == pygame.USEREVENT + 1:
            render_frame()

            cpu.tape_out = None if cpu.cycles - cpu.last_sound_cycles > 20000 else cpu.tape_out

            if len(cpu.sndbuf) > 4096 or cpu.sndbuf and cpu.cycles - cpu.last_sound_cycles > 20000:
                while cpu.channel.get_queue():
                    if time_elapsed() > 10000: break

                cpu.channel.queue(pygame.sndarray.make_sound(numpy.uint8(cpu.sndbuf)))
                cpu.sndbuf = []

    overshoot = cpu.cycles - previous_loop_cycles - time_elapsed()
    pygame.time.wait((overshoot > 0) * overshoot // 1000)      # Pričekaj da budemo cycle exact

    ratio = 1.0 * (cpu.cycles - previous_loop_cycles) / time_elapsed()

pygame.quit()
