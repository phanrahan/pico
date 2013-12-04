from magma.shield.LogicStart import *

# 
# switch(S)  
#  case 00: B     -> 0xA
#  case 01: A | B -> 0xE
#  case 10: A & B -> 0x8
#  case 11: A ^ B -> 0x6
#
def Logic( n, site=None ):

    def alu( x, y, s ):
        expr = 0x68EA
        return LUT4X2( expr, expr, site=s )

    return fork( col( alu, (n+1)/2, site ), flat=True )


