from magma.shield.LogicStart import *
from mantle.spartan3.slices import col
from mantle.spartan3.CLB import CARRY
from mantle.spartan3.RAM import RAM16


#
# type: [DI[n], A[4], WE, INCR] -> O[n]
#
# function computes
#
# combinational
#    returns ram16[A] + INCR
#
# sequential
#    if WE: ram16[A] = DI
#
def RAM(n, site=None):

    site = make_site(site)

    # RAM16 + CIN
    def ram16(x, y, s, e):
        ram = RAM16(0, o=False, site=s, elem=e)
        return CARRY(ram, 'CIN', 'COUT', 0, site=s, elem=e)

    #
    # Need to feed increment through COUT of the lower slice
    #
    # wire A into cy0
    # lut selects cy0
    #
    lut = LUT('A&~A', o=False, site=site, elem='Y')
    lut = CARRY(lut, None, 'COUT', 'A', o=False, site=site, elem='Y')

    c = Wire()
    lut(c)

    ram = forkjoin(col(ram16, n, site.delta(0, 1)), 'jff')
    ram.I = [ram.I + [c]]  # [DI, A, WE] + [INCR]

    wire(lut.COUT, ram.CIN)

    return ram

#
# Build an sequencer with an n-bit program counter
#
# returns [INCR, JUMP, ADDR[n], PUSH, POP] -> O[n]
#
#  combinational
#    newsp = SP+PUSH-POP
#    newpc = ADDR if JUMP else RAM[newsp]+INCR
#
#  sequential
#    RAM[newsp] = newpc
#    SP = newsp
#
#  O = newpc
#


def Sequencer(n, site=None):

    site = make_site(site)

    addr = Bus(n)
    incr = Wire()
    jump = Wire()
    push = Wire()
    pop = Wire()
    we = Wire()

    #
    # o=True makes the combinational output be the output of the counter
    # (rather than the register).
    #
    print 'building sp'
    newsp = UpDownCounter(4, o=True, site=site)(push, pop, ce=we)
    site = site.delta(0, 2)

    print 'building pc'
    PC = RAM(n, site=site)
    site = site.delta(0, 1 + n / 2)

    print 'building mux'
    newpc = Mux(2, n, site=site)([PC, addr], jump)

    print 'wiring pc'
    PC(newpc, newsp, we, incr)

    return Module([incr, jump, addr, push, pop], newpc, ce=we)
)
