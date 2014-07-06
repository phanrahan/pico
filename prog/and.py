from pico import *


def prog():
    movi(r1, 3)
    andi(r1, 2)
    movi(r2, 1)
    ori(r2, 3)
    jmp(0)

mem = assemble(prog)

save(mem, 'a.mem')
