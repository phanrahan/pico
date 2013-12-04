from pico import *
from mem import save

def prog():

    movi(r0,3)
    outi(r0,0)
    subi(r0,1)
    jc(1)
    jmp(0)


assemble(prog)

save(mem, 'a.mem')
