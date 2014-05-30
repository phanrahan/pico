from mem import save

def checku( u, len ):
    max = 1 << len
    assert( u < max )
    mask = max - 1
    return u & mask

def checks( i, len ):
    max = 1 << (len-1)
    mask = (1 << len) - 1
    assert( i >= -max )
    assert( i < max )
    return i & mask

DATAW = 16
INSTW = 18
ADDRH = 10
ADDRMAX = 1 << ADDRH
mem = ADDRMAX * [0]

pc = 0

pass_ = 0
labels = {}

def assemble(prog):
    global pc, pass_

    pass_ = 0
    pc = 0
    prog()

    pass_ = 1
    pc = 0
    prog()

def emit(x):
    global mem, pc
    if pc >= 0 and pc < ADDRMAX :
        mem[pc] = x
    pc += 1

def org(value):
    global pc
    pc = value

def equ(name, value):
    global labels
    labels[name] = value

def label(name=None):
    global labels
    if name:
        if pass_ == 0:
            labels[name] = pc
        if pass_ == 1:
            return labels[name]
        return 0
    return pc

def word(value):
    emit(value)

# registers
r0  = 0
r1  = 1
r2  = 2 
r3  = 3 
r4  = 4
r5  = 5
r6  = 6
r7  = 7
r8  = 8
r9  = 9
r10 = 10
r11 = 11
r12 = 12
r13 = 13 
r14 = 14
r15 = 15

