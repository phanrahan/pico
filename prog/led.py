from pico import *


def prog():
    movi(r1, 1)
    outi(r1, 0)
    movi(r1, 2)
    outi(r1, 0)
    movi(r1, 3)
    outi(r1, 0)

    jmp(0)


mem = assemble(prog)

save(mem, 'a.mem')
