from pico import *
from mem import save

DELAY = -1 

def delay():
    movi(r1,DELAY)
    loop1 = label()
    movi(r2,DELAY)
    loop2 = label()
    movi(r3,DELAY)
    loop3 = label()
    subi(r3,1)
    jnz(loop3)
    subi(r2,1)
    jnz(loop2)
    subi(r1,1)
    jnz(loop1)

def prog():

    loop = label()

    mov(ord('h'), r0)
    delay()

    jmp(loop)


assemble(prog)

save(mem, 'a.mem')
