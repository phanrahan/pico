from magma.shield.LogicStart import *
from mantle.util import debounce, falling
from arith import Arith

slow = Counter(16, cout=True, site=(30, 10))(1)[16]
select = debounce(JOYSTICK["select"], slow, site=(31, 10))
step = falling(select, site=(32, 10))

c = FF(site=(1, 0))

alu = Arith(2, site=(0, 0))

res = alu([SWITCH[0:2], SWITCH[2:4], c.O, SWITCH[6], SWITCH[7]])

creg = c(res[2], ce=step)

wire(res + [0, 0, 0, 0, creg], LED)
