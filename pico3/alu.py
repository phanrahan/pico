from magma.shield.LogicStart import *

# 
# switch(S)  
#  case 00: B     -> 0xA
#  case 01: A | B -> 0xE
#  case 10: A & B -> 0x8
#  case 11: A ^ B -> 0x6
#
def Logic( n, site=None ):

    expr = 0x68EA
    def alu( x, y, s, e ):
        return LUT4( expr, site=s, elem=e )

    return flip( flat( coln( alu, n, site ) ) )


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

    # I[0] A
    # I[1] B
    # I[2] SUB
    #  out = A ^ ((~SUB & B) | (SUB & ~B))
    e1 = 'A ^ ((~C & B) | (C & ~B))'
    e2 = 'A'
    def alu( x, y, s, e ):
        ci = None
        if y % 2 == 0:
            ci = 'BX' if y == 0 else 'CIN'
        co = None
        if y % 2 == 1:
            co = 'YB' if y == n-1 else 'COUT'
        #print x, y, s, e, ci, co
        return CarryAdd(e1, e2, ci, co, True, site=s, elem=e)

    arith = flip( flat( CarryChain( coln( alu, n, site ) ) ) )


    # I[0] SEL
    # I[1] SUB
    # I[2] CIN
    #        SEL SUB C
    #  ADD    0   0  0
    #  ADDC   1   0  C
    #  SUB    0   1  1
    #  SUBC   1   1 ~C
    expr = '(~A & B) | (A & ((B & ~C) | (~B & C)))'
    carry = LUT3( expr, site=site.delta(0,n/2) )
    wire(carry.O, arith.CIN)

    carryI = carry.I[0]
    sel =  carryI[0]
    sub = [carryI[1], arith.I[2]]

    # A, B, CIN, SEL, SUB
    arith.I =[arith.I[0], arith.I[1], carryI[2], sel, sub]
    arith.O.append( arith.COUT )

    return arith

