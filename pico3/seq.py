from magma.wiring import *
from mantle.spartan3 import *
from mantle.spartan3.slices import coln
from mantle.spartan3.CLB import CARRY
from magma.shield.LogicStart import *


#
# returns [DI[n], A[4], WE] -> O[n]
#
def RAM( n, site=None ):

    site = make_site(site)

    def ram16( x, y, s, e ):
        ram = RAM16( 0, o=False, site=s, elem=e )
        return CARRY( ram, 'CIN', 'COUT', 0, site=s, elem=e )


    lut = LUT('A&~A', o=False, site=site, elem='Y' )
    lut = CARRY( lut, None, 'COUT', 'A', False, site=site, elem='Y' )

    c = Wire()
    lut(c)

    ram = forkjoin( CarryChain( coln( ram16, n, site.delta(0,1) ) ), 'jff' )
    ram.I = [ram.I + [c]]

    wire( lut.COUT, ram.CIN )

    return ram

#
# 
def Sequencer( n, site=None ):

    site = make_site(site)

    addr = Bus(n)
    incr = Wire()
    jump = Wire()
    push = Wire()
    pop = Wire()
    we = Wire()

    print 'building sp'
    SP = UpDownCounter( 4, o=True, site=site )( push, pop, ce=we )
    site = site.delta(0,2)

    #wire( SP, LED[4:8] )
    print 'building pc'
    PC = RAM( n, site=site )
    site = site.delta(0,1+n/2)

    print 'building mux'
    newpc = Mux( 2, n, site=site )( [PC, addr], jump )

    print 'wiring pc'
    PC( newpc, SP, we, incr )

    return Module( [incr, jump, addr, push, pop], newpc, ce=we )


