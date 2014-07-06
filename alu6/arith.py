from magma.shield.LogicStart import *
from alu6 import Arith

alu = Arith(2, site=(0, 2))

res = alu([SWITCH[0:2], SWITCH[2:4], SWITCH[4], SWITCH[6], SWITCH[7]])

# switch(SWITCH[6], SWITCH[7])
#  case 00: A+B
#  case 01: A+B+Cin
#  case 10: A-B
#  case 11: A-B+Cin
wire(res, LED[0:3])
