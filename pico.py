from magma.shield.LogicStart import *
from mem import read as readmem
from mantle.util import debounce, falling
from seq import Sequencer
from logic import Logic
from arith import Arith

mem = readmem('a.mem')

#slow = Counter(16, carry=True, site=(30,10)) (1) [16]
#select = debounce( JOYSTICK["select"], slow, site=(31,10) )
#step = falling(select, site=(32,10))
step = 1

ADDRN = 10
DATAN = 18

N = 8

# program memory 
rom = ROMB( mem, DATAN, site=(0,0) )
inst = rom.O

# condition code registers
z = FF( site=(2,0) )
c = FF( site=(2,2) )

# instruction decode
addr = inst[0:ADDRN]
imm = inst[0:8]
rb = inst[4:8]
ra = inst[8:12]
zcflag = inst[10]
nflag = inst[11]
vflag = iflag = inst[12]
ccflag = wflag = inst[13]
op = inst[14:16]
kk = inst[16:18]

logicinst = LUT2( (1 << 0), site=(3,0) ) ( kk )
arithinst = LUT2( (1 << 1), site=(3,1) ) ( kk )
ioinst    = LUT2( (1 << 2), site=(3,2) ) ( kk ) # 4-bit instruction
jumpinst  = LUT2( (1 << 3), site=(3,3) ) ( kk )
aluinst   = LUT2( (1 << 0) | (1 << 1), site=(3,4) ) ( kk )

expr = '(~A & ~(B^C)) | (A & ~(B^D))'
cc = LUT( expr, site=(3,6) ) ( [zcflag, nflag, z.O, c.O] )
jump = LUT( 'A & (~B | (B & C))', site=(3,7) )( [jumpinst, ccflag, cc] ) 

regwr = LUT( 'A & ((B&C)|(~B&D))', site=(3,8) ) ( [step,wflag,aluinst,ioinst] ) 
zwr   = LUT( 'A & B', site=(3,9) ) ( [step, aluinst] )
cwr   = zwr

rd = LUT('A & ~B', site=(3,10)) ([ioinst, wflag])
wr = LUT('A &  B', site=(3,11)) ([ioinst, wflag])


# sequencer
seq = Sequencer( ADDRN, site=(0,0) ) # site must be even, ...
pc = seq( 1, addr, jump, ce=step )
inst = rom( pc, ce=step ) 

# input
imux = Mux( 4, N, site=(4,0) )
inval = imux.O

# reg and alu 
regimux = Mux( 2, N, site=(5,0) )
reg = DualPortRegister( N, site=(6,0) ) # site x must be even, dual-ported RAM
rmux = Mux( 2, N, site=(7,0) )

logicunit = Logic( N, site=(8,0) )
arithunit = Arith( N, site=(9,0) )
# shift (10,0)
regomux = Mux( 2, N, site=(11,0) )

raval, rbval = reg.O
rbval = rmux( [[imm, rbval], iflag] ) 
logicres = logicunit( rbval, raval, op[0], op[1] )
arithres = arithunit( raval, rbval, c.O, op[0], op[1] )
res = regomux( [logicres, arithres[0:N]], arithinst ) 
res = regimux( [res, inval], rd )
reg( res, ra, rb, regwr )

zval = Decode( 0, N, site=(2,1) )
z( zval( res ), ce=zwr ) 

cval = LUT2( 'A & B', site=(2,3) ) ( [arithres[N], arithinst] )
c( cval, ce=cwr )

# input and output
port = rbval
val = raval

joystick = [ JOYSTICK['select'], 
             JOYSTICK['up'], 
             JOYSTICK['down'], 
             JOYSTICK['left'], 
             JOYSTICK['right'], 
             0, 0, 0 ]
          
imux( [SWITCH, joystick, SWITCH, joystick], port[0:2] )

portena = Decode( 0, N, site=(12, 0) )( port )
portwr = LUT('A & B & C', site=(12, 1) )( [step, wr, portena] )
portreg = Register( N, site=(12, 2) )
wire( portreg( val, ce=portwr ), LED )

portena = Decode( 2, N, site=(14, 0) )( port )
portwr = LUT('A & B & C', site=(14, 1) )( [step, wr, portena] )
portreg = Register( 4, init=[1,1,1,1], site=(14, 2) )
wire( portreg( val[0:4], ce=portwr ), ANODE )

portena = Decode( 3, N, site=(15, 0) )( port )
portwr = LUT('A & B & C', site=(15, 1) )( [step, wr, portena] )
portreg = Register( N, site=(15, 2) )
wire( portreg( val, ce=portwr ), SEGMENT )

RX, TX = MegaWing.UART()
portena = Decode( 4, N, site=(16, 0) )( port )
portwr = LUT('A & B & C', site=(16, 1) )( [step, wr, portena] )
portreg = FF( site=(16, 2) )
wire( portreg( val[0], ce=portwr ), TX )


# debug
#wire( pc[0:8], LED )
#wire( res, LED )

#wire( kk + [jumpinst], LED[0:3] )
#wire( inst[12:18], LED )
#wire( [aluinst, ioinst, jumpinst, 0, 0, 0, c.O, z.O], LED )

#wire( ra, LED )
#wire( rb, LED )

