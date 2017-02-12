from magma import *
from mantle import *
from parts.lattice.ice40.primitives.RAMB import ROMB
from asm import read as readmem
from seq import Sequencer
from alu import Arith, Logic
from ram import DualRAM

__all__ = ['pico', 'ADDRN', 'INSTN', 'DATAN']

def instructiondecode(inst):
    insttype = inst[14:16]

    # alu instructions
    logicinst = ROM2((1 << 0))(insttype)
    arithinst = ROM2((1 << 1))(insttype)
    aluinst =  ROM2((1 << 0) | (1 << 1))(insttype)

    # ld and st (immediate)
    ldloinst = ROM4(1 << 8)(inst[12:16])
    ldinst = ROM4(1 << 10)(inst[12:16])
    stinst = ROM4(1 << 11)(inst[12:16])

    # control flow instructions
    jumpinst = ROM4(1 << 12)(inst[12:16])
    #callinst = ROM4(1 << 13)(inst[12:16])

    return logicinst, arithinst, aluinst, \
           ldloinst, ldinst, stinst, \
           jumpinst

ADDRN = 8
INSTN = 16
DATAN = 8
N = DATAN

def pico(mem):

    # program memory
    romb = ROMB(mem)
    wire( 1, romb.RCLKE )
    wire( 1, romb.RE    )
    inst = romb.RDATA

    # instruction decode
    addr = inst[0:ADDRN]
    imm = inst[0:N]
    rb = inst[4:8]
    ra = inst[8:12]
    cc = inst[8:12]
    op = inst[12:14]

    logicinst, arithinst, aluinst, ldloinst, ldinst, stinst, jumpinst =\
        instructiondecode(inst)

    # romb's output is registered
    # phase=0
    #   fetch()
    # phase=1
    #   execute()
    phase = TFF()(1)

    print 'Building z'
    z = DFF(ce=True)
    condz = Decode(0, 4)(cc)  #jz
    condnz = Decode(1, 4)(cc) #jnz
    jumpz = LUT3((I0&I2)|(I1&~I2))(condz, condnz, z)

    always = Decode(15, 4)(cc)

    # jump is jump always of jump cond 
    cond = Or2()(always, jumpz) 
    jump = And2()(jumpinst, cond)

    # register write
    regwr = LUT4((I0|I1|I2)&I3)(aluinst, ldloinst, ldinst, phase)


    # sequencer
    print 'Building sequencer'
    seq = Sequencer(ADDRN)  
    pc = seq(addr, jump, phase)
    wire(pc, romb.RADDR)

    print 'Building input'
    input = In(Array(8,Bit))()

    print 'Building input mux'
    regiomux = Mux(2, N)
    regiomux(imm, input, ldinst)

    print 'Building register input mux'
    regimux = Mux(2, N)

    print 'Building registers'
    raval, rbval = DualRAM(4, ra, rb, ra, regimux, regwr)

    # alu
    print 'Building logic unit'
    logicunit = Logic(N)
    print 'Building arith unit'
    arithunit = Arith(N)
    print 'Building alu mux'
    alumux = Mux(2, N)

    print 'Wiring logic unit'
    logicres = logicunit(raval, rbval, op[0], op[1])
    print 'Wiring arith unit'
    arithres = arithunit(raval, rbval, op[0], op[1])
    wire(0, arithunit.CIN)
    print 'Wiring alumux'
    res = alumux(logicres, arithres, arithinst)

    print 'Wiring register input mux'
    ld = Or2()(ldinst, ldloinst)
    regimux(res, regiomux, ld) 

    # z flag
    print 'Wiring z'
    zval = Decode(0, N)
    zwr =  And2()(aluinst, phase)
    z(zval(res), CE=zwr)

    print 'Wiring output'
    output = Register(N, ce=True)
    owr = And2()(stinst, phase)
    output(raval, CE=owr)

    return input, output

