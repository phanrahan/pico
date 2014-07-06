from pico import *


def prog():
    movi(r1, 1)
    movi(r2, 2)
    mov(r3, r1)
    mov(r4, r2)
    jmp(0)

mem = assemble(prog)

save(mem, 'a.mem')
