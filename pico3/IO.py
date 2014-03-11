from magma.shield.LogicStart import *
from magma.design import composei

#
# port = 0 SWITCH
# port = 1 JOYSTICK
#
def Input( N, site=None ):

    joystick = [ JOYSTICK['select'], 
                 JOYSTICK['up'], 
                 JOYSTICK['down'], 
                 JOYSTICK['left'], 
                 JOYSTICK['right'], 
                 0, 0, 0 ]

    inputs = [SWITCH, joystick, SWITCH, joystick]

    imux = Mux( 4, N, site=(4,0) )
          
    return composei( imux, inputs, 0 )

#
# port = 0 LED
# port = 2 ANODE
# port = 3 SEGMENT
# port = 4 TX
def Output( port, val, en, wr, N, site=None ):

    # LED
    ena  = Decode( 0, N, site=(12, 0) )( port )
    ce = LUT('A & B & C', site=(12, 1) )( [en, wr, ena] )
    led = Register( N, site=(12, 2) )
    wire( led( val, ce=ce ), LED )

    # ANODE and SEGMENT
    ena = Decode( 2, N, site=(14, 0) )( port )
    ce = LUT('A & B & C', site=(14, 1) )( [en, wr, ena] )
    anode = Register( 4, init=[1,1,1,1], site=(14, 2) )
    wire( anode( val[0:4], ce=ce ), ANODE )

    ena = Decode( 3, N, site=(15, 0) )( port )
    ce = LUT('A & B & C', site=(15, 1) )( [en, wr, ena] )
    segment = Register( N, site=(15, 2) )
    wire( segment( val, ce=ce ), SEGMENT )

    # UART 
    #RX, TX = MegaWing.UART()
    #en = Decode( 4, N, site=(16, 0) )( port )
    #ff = FF( site=(16, 2) )
    #wire( ff( val[0], ce=ce ), TX )


