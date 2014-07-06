from magma.shield.LogicStart import *
from alu3 import Logic

alu = Logic(2, site=(0, 0))

A = SWITCH[0:2]
B = SWITCH[2:4]
S = SWITCH[6:8]

res = alu([A, B, S[0], S[1]])

# switch(S)
#  case 00: B
#  case 01: A | B
#  case 10: A & B
#  case 11: A ^ B
wire(res, LED[0:2])
