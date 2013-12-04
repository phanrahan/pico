from tiny import *

def movi ( a, i ):
    a = checku ( a , 4 )
    i = checks ( i , 8 )
    emit( 0x2000 | (a<<8) | (i<<0) )

def mov ( a, b ):
    a = checku ( a , 4 )
    b = checku ( b , 4 )
    emit( 0x3000 | (a<<8) | (b<<4) )

def ori ( a, i ):
    a = checku ( a , 4 )
    i = checks ( i , 8 )
    emit( 0x6000 | (a<<8) | (i<<0) )

def _or ( a, b ):
    a = checku ( a , 4 )
    b = checku ( b , 4 )
    emit( 0x7000 | (a<<8) | (b<<4) )

def andi ( a, i ):
    a = checku ( a , 4 )
    i = checks ( i , 8 )
    emit( 0xa000 | (a<<8) | (i<<0) )

def _and ( a, b ):
    a = checku ( a , 4 )
    b = checku ( b , 4 )
    emit( 0xb000 | (a<<8) | (b<<4) )

def xori ( a, i ):
    a = checku ( a , 4 )
    i = checks ( i , 8 )
    emit( 0xe000 | (a<<8) | (i<<0) )

def xor ( a, b ):
    a = checku ( a , 4 )
    b = checku ( b , 4 )
    emit( 0xf000 | (a<<8) | (b<<4) )

def tsti ( a, i ):
    a = checku ( a , 4 )
    i = checks ( i , 8 )
    emit( 0x8000 | (a<<8) | (i<<0) )

def tst ( a, b ):
    a = checku ( a , 4 )
    b = checku ( b , 4 )
    emit( 0x9000 | (a<<8) | (b<<4) )

def addi ( a, i ):
    a = checku ( a , 4 )
    i = checks ( i , 8 )
    emit( 0x12000 | (a<<8) | (i<<0) )

def add ( a, b ):
    a = checku ( a , 4 )
    b = checku ( b , 4 )
    emit( 0x13000 | (a<<8) | (b<<4) )

def adci ( a, i ):
    a = checku ( a , 4 )
    i = checks ( i , 8 )
    emit( 0x16000 | (a<<8) | (i<<0) )

def adc ( a, b ):
    a = checku ( a , 4 )
    b = checku ( b , 4 )
    emit( 0x17000 | (a<<8) | (b<<4) )

def subi ( a, i ):
    a = checku ( a , 4 )
    i = checks ( i , 8 )
    emit( 0x1a000 | (a<<8) | (i<<0) )

def sub ( a, b ):
    a = checku ( a , 4 )
    b = checku ( b , 4 )
    emit( 0x1b000 | (a<<8) | (b<<4) )

def sbci ( a, i ):
    a = checku ( a , 4 )
    i = checks ( i , 8 )
    emit( 0x1e000 | (a<<8) | (i<<0) )

def sbc ( a, b ):
    a = checku ( a , 4 )
    b = checku ( b , 4 )
    emit( 0x1f000 | (a<<8) | (b<<4) )

def cmpi ( a, i ):
    a = checku ( a , 4 )
    i = checks ( i , 8 )
    emit( 0x18000 | (a<<8) | (i<<0) )

def cmp ( a, b ):
    a = checku ( a , 4 )
    b = checku ( b , 4 )
    emit( 0x19000 | (a<<8) | (b<<4) )

def ini ( a, i ):
    a = checku ( a , 4 )
    i = checks ( i , 8 )
    emit( 0x20000 | (a<<8) | (i<<0) )

def _in ( a, b ):
    a = checku ( a , 4 )
    b = checku ( b , 4 )
    emit( 0x21000 | (a<<8) | (b<<4) )

def outi ( a, i ):
    a = checku ( a , 4 )
    i = checks ( i , 8 )
    emit( 0x22000 | (a<<8) | (i<<0) )

def out ( a, b ):
    a = checku ( a , 4 )
    b = checku ( b , 4 )
    emit( 0x23000 | (a<<8) | (b<<4) )

def jmp ( a ):
    a = checku ( a , 10 )
    emit( 0x30000 | (a<<0) )

def jnz ( a ):
    a = checku ( a , 10 )
    emit( 0x32000 | (a<<0) )

def jz ( a ):
    a = checku ( a , 10 )
    emit( 0x32400 | (a<<0) )

def jnc ( a ):
    a = checku ( a , 10 )
    emit( 0x32800 | (a<<0) )

def jc ( a ):
    a = checku ( a , 10 )
    emit( 0x32c00 | (a<<0) )

