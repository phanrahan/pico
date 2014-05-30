from magma.shield.LogicStart import *
from mantle.util import debounce, falling
from seq import Sequencer

slow = Counter(16, cout=True, site=(30,10)) (1) [16]
select = debounce( JOYSTICK["select"], slow, site=(31,10) )
pulse = falling(select, site=(32,10))

seq = Sequencer( 2, site=(0,0) )

incr = SWITCH[0]
jump = SWITCH[1]
push = SWITCH[2]
pop  = SWITCH[3]
addr = SWITCH[4:6]

pc = seq( incr, jump, addr, push, pop, ce=pulse )

wire( pc, LED[0:2] )

