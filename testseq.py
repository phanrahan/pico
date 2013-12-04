from magma.shield.LogicStart import *
from mantle.util import debounce, falling
from seq import Sequencer

slow = Counter(16, cout=True, site=(30,10)) (1) [16]
select = debounce( JOYSTICK["select"], slow, site=(31,10) )
pulse = falling(select, site=(32,10))

seq = Sequencer( 6, site=(0,0) )

# seq( [incr, addr, load], ce= )
count = seq( [1, SWITCH[0:6], SWITCH[7]], ce=pulse )

wire( count, LED[0:6] )

