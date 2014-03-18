from magma.shield.LogicStart import *

# 
# switch(S)  
#  case 00: B     -> 0xA
#  case 01: A | B -> 0xE
#  case 10: A & B -> 0x8
#  case 11: A ^ B -> 0x6
#
def Logic( n, site=None ):

    site = make_site(site)

    def alu( x, y, s ):
        expr = 0x68EA
        return LUT4X2( expr, expr, site=s )

    f = flip( flat( col( alu, (n+1)/2, site ) ) )
    #print len(f.I), '4'
    #print len(f.I[0]), '8'
    return f


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
        e1 = 'A ^ ((~C & B) | (C & ~B))'
        e2 = 'A'
        return CarryAdd2(expr1=e1, expr2=e2, site=s)

    arith = flip( flat( CarryChain( col( alu, n, site ) ) ) )
    #print len(arith.I), '3'
    #print len(arith.I[0]), '8'


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
    arith.I =[arith.I[0], arith.I[1], carryI[2], sel, sub]
    arith.O.append( arith.COUT )

    #print len(arith.I), '5'
    #print len(arith.I[0]), '8'

    return arith

