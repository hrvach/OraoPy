Orao Emulator
============

![Screenshot](assets/screenshot.png?raw=true)

[Orao](https://en.wikipedia.org/wiki/Orao_%28computer%29) is a Croatian 8-bit
computer used primarily in elementary schools, as part of a computer literacy
initiative.

This is an attempt of an emulator written in Python 2, licensed under the terms
of the GNU General Public License, version 2 or later (GPLv2+). 

It implements the 6502 CPU and all peripherals without external dependencies,
and it's meant to be as short as possible (267 SLOC). Sometimes it cuts
corners with readability and it's not PEP-8 compliant, but it wouldn't be
fun to have an emulator 2000 lines of boring, by the book code. Would it? :-)


Additional Requirements
------------------------------
    
1. Pygame
2. Numpy
       
Instructions
-------------

Run with python orao.py, enter BASIC using "BC". When asked about the memory
size, press ENTER unless you don't want BASIC to use the entire available
memory. 

WAV files containing programs / games should be located in the wav folder.

To save a BASIC program, use SAVE "filename" - a corresponding FILENAME.WAV
will be created.  Load it back using LOAD "filename".

DMEM "filename", ADDR, LENGTH can also be used to save a fragment of memory,
beginning at address ADDR and of length LENGTH (in decimal). LMEM "filename"
loads it back.
      
Clicking the POWER button does a warm reboot. You can then go back to BASIC
with BW to keep the memory intact, or re-initialize with BC. The enclosed PDF
describes the monitor mode and commands, but it is in Croatian only (Google
Translate can help).

Try LMEM "TETRIS" and run it using LNK4096. You can get double quotes by
pressing shift + 2. Erase by using the left arrow.

It *should* be cross-platform.

Loading `.prg` files
--------------------

Run emulator with:

```sh
./orao.py [path/to/file.prg]
```
Then press F8 to load and start program.


Known bugs
----------

- Pygame and Pulseaudio crash occasionally. - it seems that this 
  fork is less prone to lock-ups and **pygame*** crashes.
  Please report any issues you have.
- no error checking for input `.prg` file
