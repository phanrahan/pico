from pico import *


def prog():
    jmp(2)
    jmp(0)
    jmp(4)
    jmp(0)
    jmp(0)


mem = assemble(prog)

save(mem, 'a.mem')
