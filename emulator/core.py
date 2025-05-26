from .flags import *


def ADD(acc, tmp, flags):
    """ Add """
    return ADC(acc, tmp, 0)

def ADC(acc, tmp, flags):
    """ Add with carry """
    cy = __CY(acc, tmp, flags)
    ac = __AC(acc, tmp, flags)
    acc = (acc + tmp + (flags & 0x01)) % 256
    flags = __Z(acc) | __S(acc) | __P(acc) | cy | ac | 0x02
    return acc, flags
 
def SUB(acc, tmp, flags):
    """ Subtract """
    return ADD(acc, 256 - tmp, flags)

def SBB(acc, tmp, flags):
    """ Subtract with borrow """
    pass

def ANA(acc, tmp, flags):
    """ And """
    acc = (acc & tmp)
    flags = __Z(acc) | __S(acc) | __P(acc) | 0x02
    return acc, flags

def XRA(acc, tmp, flags):
    """ Exclusive or """
    acc = (acc ^ tmp)
    flags = __Z(acc) | __S(acc) | __P(acc) | 0x02
    return acc, flags

def ORA(acc, tmp, cy=0):
    """ Or """
    acc = (acc | tmp)
    flags = __Z(acc) | __S(acc) | __P(acc) | 0x02
    return acc, flags

def CMP(acc, tmp, flags):
    """ Compare """
    _, flags = SUB(acc, tmp, flags)
    return acc, flags

def INR(acc, tmp, flags):
    """ Increment register """
    cy = flags & CY
    acc, flags = ADD(tmp, 1, flags)
    return acc, (flags & ~CY) | cy

def DCR(acc, tmp, flags):
    """ Decrement register """
    cy = flags & cy
    acc, flags = SUB(tmp, 1, flags)
    return acc, (flags & ~CY) | cy

def RLC(acc, tmp, flags):
    """ Rotate left """
    cy = (acc << 1) // 256
    acc = (acc << 1) % 256 + cy
    flags = (flags & ~1) | cy
    return acc, flags

def RRC(acc, tmp, flags):
    """ Rotate right """
    pass

def RAL(acc, tmp, flags):
    """ Rotate left through carry """
    pass

def RAR(acc, tmp, flags):
    """ Rotate right through carry """
    pass

def __AC(op, acc, tmp, cy=0):
    """ Auxiliary carry flag """
    return bool(
        0
    ) << 4

def __CY(acc, tmp, flags):
    """ Carry flag """
    return bool(
        (acc + tmp + (flags & CY)) // 256
    ) << 0

def __Z(acc):
    """ Zero flag (Z) """ 
    return bool(
        not acc
    ) << 6

def __S(acc):
    """ Sign flag (S) """
    return bool(
        acc & 0x80
    ) << 7

def __P(acc):
    """ Parity flag """
    return bool(
        0
    ) << 2
