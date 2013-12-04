from pico import *
from mem import save

def prog():

    ini( r0, 1) # from joystick
    outi(r0, 0) # to leds

    jmp(0)


assemble(prog)

save(mem, 'a.mem')
