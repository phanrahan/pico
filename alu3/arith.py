from magma.shield.LogicStart import *
from alu3 import Arith

alu = Arith(2, site=(0, 0))

res = alu([SWITCH[0:2], SWITCH[2:4], SWITCH[4], SWITCH[6], SWITCH[7]])

wire(res, LED[0:3])
