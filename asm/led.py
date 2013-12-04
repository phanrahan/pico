from pico import *
from mem import save

def prog():
    movi(r1, 1)
    outi(r1, 0)
    movi(r1, 2)
    outi(r1, 0)
    movi(r1, 3)
    outi(r1, 0)

    jmp(0)


assemble(prog)

save(mem, 'a.mem')
