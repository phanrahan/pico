from magma.wiring import *
from mantle.spartan3 import *
from mantle.spartan3.slices import col

def Sequencer( n, site=None ):

    site = make_site(site)

    n = (n+1)/2

    expr = '(C & B) | (~C & A)'

    def counter(x, y, s):
        # [VEC, LOAD] -> inc.O
        co = False if y == n-1 else 'COUT'
        return Counter2(expr1=expr, cout=co, o=True, site=s)

    c = flip( flat( CarryChain( col( counter, n, site ) ) ) )

    assert( len(c.I) == 2 )

    # A = /LOAD
    # B = INCR
    inc = LUT2('(~A) & B', site=site.delta(0,n) )
    wire(inc, c.CIN)

    # U, I, L
    incI = inc.I[0]
    I = [incI[1], c.I[0], [incI[0], c.I[1]]]

    return Module( I, c.O, ce=c.CE )

