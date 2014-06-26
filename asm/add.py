from pico import *
from mem import save


def prog():
    movi(r1, 1)
    addi(r1, 2)
    subi(r1, 1)
    jmp(0)

assemble(prog)

save(mem, 'a.mem')
m')
