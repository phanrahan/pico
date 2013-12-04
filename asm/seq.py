from pico import *
from mem import save

def prog():
    nop()
    nop()
    nop()
    nop()
    jmp(0)

assemble(prog)

save(mem, 'a.mem')
