from magma.shield.LogicStart import *
from mantle.util import debounce, falling
from mem import read as readmem
from seq import Sequencer
from alu import Arith, Logic
from IO import Input, Output

mem = readmem('a.mem')

#slow = Counter(16, cout=True, site=(30,10)) (1) [16]
#select = debounce( JOYSTICK["select"], slow, site=(31,10) )
#step = falling(select, site=(32,10))
step = 1

ADDRN = 10
DATAN = 18

N = 8

# program memory 
rom = ROMB( mem, DATAN, site=(0,0) )

# condition code registers
z = FF( site=(2,0) )
c = FF( site=(2,2) )

# instruction decode
inst = rom
addr = inst[0:ADDRN]
imm = inst[0:8]
rb = inst[4:8]
ra = inst[8:12]
zcflag = inst[10]
nflag = inst[11]
vflag = iflag = inst[12]
ccflag = wflag = inst[13]
op = inst[14:16]
insttype = inst[16:18]

# type of instruction
logicinst = LUT2( (1 << 0), site=(3,0) ) ( insttype )
arithinst = LUT2( (1 << 1), site=(3,1) ) ( insttype )
aluinst   = LUT2( (1 << 0) | (1 << 1), site=(3,2) ) ( insttype )
ioinst    = LUT2( (1 << 2), site=(3,3) ) ( insttype ) 

jumpinst = LUT2( 'A & B & ~C &  D', site=(3,4) ) (insttype[0], insttype[1], op[0], op[1])
callinst = LUT2( 'A & B &  C &  D', site=(3,5) ) (insttype[0], insttype[1], op[0], op[1])
retinst =  LUT2( 'A & B &  C & ~D', site=(3,6) ) (insttype[0], insttype[1], op[0], op[1])

# condition codes
expr = '(~A & ~(B^C)) | (A & ~(B^D))'
cc = LUT( expr, site=(3,7) ) ( zcflag, nflag, z, c )

expr = '(A | B) & (~C | (C & D))'
jump = LUT(  expr, site=(3,8) )( callinst, jumpinst, ccflag, cc ) 
push = LUT( 'A & (~B | (B & C))', site=(3,9)  )( callinst, ccflag, cc ) 
pop =  LUT( 'A & (~B | (B & C))', site=(3,10) )( retinst, ccflag, cc ) 

# register write, z and c write
regwr = LUT( 'A & ((B&C)|(~B&D))', site=(3,11) ) ( step,wflag,aluinst,ioinst ) 
zwr   = LUT( 'A & B', site=(3,12) ) ( step, aluinst )
cwr   = zwr

# io rd or wr
iord = LUT('A & ~B', site=(3,13)) (ioinst, wflag)
iowr = LUT('A &  B', site=(3,14)) (ioinst, wflag)


# sequencer
print 'Building sequencer'
seq = Sequencer( ADDRN, site=(0,0) ) # site must be even, ...
pc = seq( 1, jump, addr, push, pop, ce=step )
inst = rom( pc, ce=step ) 

# input
print 'Building input'
input = Input( N, site=(4,0) )

# create reg, input mux, output mux
print 'Building registers'
regimux = Mux( 2, N, site=(5,0) )
reg = DualPortRegister( N, site=(6,0) ) # site x must be even
regomux = Mux( 2, N, site=(7,0) )

# register values
raval, rbval = reg[0], reg[1]
rbval = regomux( [imm, rbval], iflag ) 

# alu
print 'Building logic unit'
logicunit = Logic( N, site=(8,0) )

print 'Building arith unit'
arithunit = Arith( N, site=(9,0) )
alumux = Mux( 2, N, site=(11,0) )

print 'Wiring logic unit'
logicres = logicunit( raval, rbval, op[0], op[1] )
print 'Wiring arith unit'
arithres = arithunit( raval, rbval, c, op[0], op[1] )
print 'Wiring alumux'
res = alumux( [logicres, arithres[0:N]], arithinst ) 

# choose between res and input
print 'Wiring register imux'
res = regimux( [res, input], iord )
print 'Wiring register'
reg( res, ra, rb, regwr )

# z flag
zval = Decode( 0, N, site=(2,1) )
z( zval( res ), ce=zwr ) 

# c flag
cval = LUT2( 'A & B', site=(2,3) )
c( cval( [arithres[N], arithinst] ), ce=cwr )

# IO
print 'Wiring input'
input( rbval[0:2] )
print 'Wiring output'
Output( rbval, raval, step, iowr, N, site=(12,0) )












# debug
#wire( pc[0:8], LED )
#wire( [jump, push, pop], LED[0:3] )

#wire( inst[12:18], LED )
#wire( [aluinst, ioinst, jumpinst, 0, 0, 0, c, z], LED )

#wire( ra, LED )
#wire( rb, LED )

#wire( raval, LED )
#wire( rbval, LED )

#wire( res, LED )

