import sys
from magma import *
from pico import *
from setup import makepico

MAXINSTS = 1 << ADDRN

def prog():
    ldlo(r0,0)
    ldlo(r1,1)
    loop = label()
    add(r0,r1)
    st(r0, 0)
    jmp(loop)

main = makepico(prog)

compile(sys.argv[1], main)
