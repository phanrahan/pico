import sys
from magma import *
from pico import *
from setup import makepico

MAXINSTS = 1 << ADDRN

def prog():
    ldlo(r0, 2)
    ldlo(r1, 2)
    add(r1,r0)
    st(r1, 0)
    jmp(0)

main = makepico(prog)

compile(sys.argv[1], main)
