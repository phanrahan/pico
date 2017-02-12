import sys
from magma import *
from pico import *
from setup import makepico

MAXINSTS = 1 << ADDRN

def prog():
    ldlo(r0, 0x55)
    st(r0, 0)
    jmp(0)

main = makepico(prog)

compile(sys.argv[1], main)
