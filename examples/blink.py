import sys
from magma import *
from pico import *
from setup import makepico

MAXINSTS = 1 << ADDRN

def prog():
    ldlo(r0,0)
    ldlo(r1,1)
    loop0 = label()
    sub(r0,r1)
    jnz(loop0)
    st(r0, 0)
    loop1 = label()
    sub(r0,r1)
    jnz(loop1)
    st(r1, 0)
    jmp(loop0)

main = makepico(prog)

compile(sys.argv[1], main)
