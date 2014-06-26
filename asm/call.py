from pico import *
from mem import save


def prog():

    jmp(2)
    jmp(0)
    call(4)
    jmp(0)
    ret()


assemble(prog)

save(mem, 'a.mem')
