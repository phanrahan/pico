from pico import *
from mem import save

DELAY = -1 

def delay():
    movi(r1,DELAY)
    loop1 = getpc()
    movi(r2,DELAY)
    loop2 = getpc()
    movi(r3,DELAY)
    loop3 = getpc()
    subi(r3,1)
    jnz(loop3)
    subi(r2,1)
    jnz(loop2)
    subi(r1,1)
    jnz(loop1)

def prog():

    loop = getpc()

    mov(ord('h'), r0)
    delay()

    jmp(loop)


assemble(prog)

save(mem, 'a.mem')
