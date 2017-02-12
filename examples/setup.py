from magma import *
from mantle import *
from pico import *
from boards.icestick import IceStick

def makepico(prog):
    icestick = IceStick()
    icestick.Clock.on()
    for i in range(8):
        icestick.J1[i].input().on()
    for i in range(8):
        icestick.J3[i].output().on()

    main = icestick.main()

    mem = assemble(prog, 1 << ADDRN)

    input, output = pico(mem)

    wire(main.J1, input)
    wire(output, main.J3)

    return main
