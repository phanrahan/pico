import sys
from magma import *
from mantle import *
from parts.lattice.ice40.primitives.RAMB import ROMB
from mem import read as readmem
from seq import Sequencer
from alu import Arith, Logic
from ram import DualRAM
#from io import Input, Output

from boards.icestick import IceStick

icestick = IceStick()

icestick.Clock.on()
for i in range(8):
    icestick.J1[i].input().on()
for i in range(8):
    icestick.J3[i].output().on()

main = icestick.main()

# romb's output is registered
# phase=0
#   fetch()
# phase=1
#   execute()
phase = TFF()(1)

mem = readmem('a.mem', 256)

ADDRN = 8
INSTN = 16

N = 8

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
insttype = inst[14:16]

# alu instructions
logicinst = ROM2((1 << 0))(insttype)
arithinst = ROM2((1 << 1))(insttype)
aluinst = ROM2((1 << 0) | (1 << 1))(insttype)

# ld and st (immediate)
ldloinst = ROM4(1 << 8)(inst[12:16])
ldinst = ROM4(1 << 10)(inst[12:16])
stinst = ROM4(1 << 11)(inst[12:16])
ld = Or2()(ldinst, ldloinst)

# register write
regwr = Or3()(aluinst, ld, phase)


# control flow instructions
jumpinst = ROM4(1 << 12)(inst[12:16])
#callinst = ROM4(1 << 13)(inst[12:16])
#retinst  = ROM4(1 << 14)(inst[12:16])

# condition code registers
z = DFF(ce=True)
c = DFF(ce=True)

# z condition code
print 'z'
condz = Decode(0, 4)(cc)
condnz = Decode(1, 4)(cc)
jumpz = LUT3((I0&I2)|(I1&~I2))(condz, condnz, z)
# c condition code
print 'c'
condc = Decode(2, 4)(cc)
condnc = Decode(3, 4)(cc)
jumpc = LUT3((I0&I2)|(I1&~I2))(condc, condnc, c)
# always
always = Decode(15, 4)(cc)
cond = Or3()(always, jumpz, jumpc)
#cond=1

jump = And2()(jumpinst, cond)

# sequencer
print 'Building sequencer'
seq = Sequencer(ADDRN)  
pc = seq(addr, jump, phase)

print 'Wiring romb'
wire(pc, romb.RADDR)

print 'Building input'
input = main.J1

print 'Building regiomux'
regiomux = Mux(2, N)
regiomux(imm, input, ldinst)

print 'Building regimux'
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

#
print 'Wiring logic unit'
logicres = logicunit(raval, rbval, op[0], op[1])
print 'Wiring arith unit'
arithres = arithunit(raval, rbval, op[0], op[1])
cout = arithunit.COUT
wire(c, arithunit.CIN)
print 'Wiring alumux'
res = alumux(logicres, arithres, arithinst)

# print 'Wiring register imux'
#regimux( rbval, imm, ldloinst ) # debug ldlo
#regimux( logicres, imm, ldloinst ) # debug logicres
#regimux( arithres, imm, ldloinst ) # debug logicres
#regimux( res, imm, ldloinst ) # debug alu
regimux(res, regiomux, ld) # full io

# z flag
print 'Wiring z'
zval = Decode(0, N)
zwr =  And2()(aluinst, phase)
z(zval(res), CE=zwr)

# c flag
print 'Wiring c'
cwr =  And2()(arithinst, phase)
c(cout, CE=cwr)

print 'Wiring output'
output = Register(N, ce=True)
output(raval, CE=stinst)

wire(output, main.J3)

# Debug pc and inst
#debugmux = Mux(2,8)
#debugmux( pc, inst[8:16], phase )
#wire( debugmux, main.J3 )

# Debug pc and regimux
#debugmux = Mux(2,8)
#debugmux( pc, regimux, phase )
#wire( debugmux, main.J3 )

# Debug pc and imm
#debugmux = Mux(2,8)
#debugmux( pc, imm, phase )
#wire( debugmux, main.J3 )

compile(sys.argv[1], main)
