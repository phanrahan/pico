from pico import *
from mem import save


def prog():

    jmp(2)
    jmp(0)
    jmp(4)
    jmp(0)
    jmp(0)


assemble(prog)

save(mem, 'a.mem')
