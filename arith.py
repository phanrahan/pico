from magma.shield.LogicStart import *

# switch(S)  
#  case 00: A+B
#  case 01: A+B+Cin
#  case 10: A-B
#  case 11: A-B+Cin
#
#  [A, B, CIN, SUB, SEL] -> O
#
def Arith( n, site=None ):

    site = make_site(site)

    n = (n+1)/2

    # I[0] A
    # I[1] B
    # I[2] SUB
    #  out = A ^ ((~SUB & B) | (SUB & ~B))
    def alu(i, j, s):
        expr = 'A ^ ((~C & B) | (C & ~B))'
        return Add2(expr=expr, x=True, site=s)

    arith = flip( flat( CarryChain( col( alu, n, site ) ) ) )


    # I[0] SEL
    # I[1] SUB
    # I[2] CIN
    #        SEL SUB C
    #  ADD    0   0  0
    #  ADDC   1   0  C
    #  SUB    0   1  1
    #  SUBC   1   1 ~C
    expr = '(~A & B) | (A & ((B & ~C) | (~B & C)))'
    carry = LUT3( expr, site=site.delta(0,n) )
    wire(carry.O, arith.CIN)

    carryI = carry.I[0]
    sel =  carryI[0]
    sub = [carryI[1], arith.I[2]]

    # A, B, CIN, SEL, SUB
    arith.I = [arith.I[0], arith.I[1], carryI[2], sel, sub]
    arith.O.append( arith.COUT )

    return arith

