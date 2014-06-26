from pico import *
from mem import save


def prog():

    ini(r0, 0)
    outi(r0, 0)

    jmp(0)


assemble(prog)

save(mem, 'a.mem')
