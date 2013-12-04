from magma.shield.LogicStart import *
from mantle.util import debounce, falling
from logic import Logic

slow = Counter(16, cout=True, site=(30,10)) (1) [16]
select = debounce( JOYSTICK["select"], slow, site=(31,10) )
pulse = falling(select, site=(32,10))

alu = Logic( 2, site=(0,0) )

A = SWITCH[0:2]
B = SWITCH[2:4]
S = SWITCH[6:8]

res = alu( [A, B, S[0], S[1]] )

# switch(S)
#  case 00: B
#  case 01: A | B
#  case 10: A & B
#  case 11: A ^ B
wire( res, LED[0:2] )
