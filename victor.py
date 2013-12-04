from magma.shield.LogicStart import *

def Sequencer( n, site=None ):

    site = make_site(site)

    n = (n+1)/2

    expr = '(C & B) | (~C & A)'

    def counter(x, y, site):
        # [VEC, LOAD] -> inc.O
        return Counter2(expr=expr, full=False, cout=(y!=n-1), x=True, 
            site=site)

    c = flip( FoldCarry( col( counter, n, site ) ) )

    # A = /LOAD
    # B = INCR
    inc = LUT2('(~A) & B', site=site.delta(0,n) )
    wire(inc.O, c.CIN)
    #wire(inc, c.CIN)

    # U, I, L
    I = [inc.I[1], c.I[0], [inc.I[0], c.I[1]]]

    return Module( I, c.O, ce=c.CE )

