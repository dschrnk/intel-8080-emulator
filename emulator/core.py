
# ALU
def ADD(acc, tmp, flags):
    """ Add """
    return ADC(acc, tmp, 0)

def ADC(acc, tmp, flags):
    """ Add with carry """
    cy = __CY(acc, tmp, flags)
    ac = __AC(acc, tmp, flags)
    acc = (acc + tmp + (flags & 0x01)) % 256
    flags = __Z(acc) | __S(acc) | __P(acc) | cy | ac
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
    _, flags = SUB(acc, tmp, flags)
    return acc, flags

def INR(acc, tmp, flags):
    """ Increment register """
    acc, _flags = ADD(tmp, 1, flags)
    return acc, (_flags & ~0x01) | (flags & 0x01)

def DCR(acc, tmp, flags):
    acc, _flags = SUB(tmp, 1, flags)
    return acc, (_flags & ~0x01) | (flags & 0x01)

def RLC(acc, tmp, flags):
    cy = (acc << 1) // 256
    acc = (acc << 1) % 256 + cy
    flags = (flags & ~1) | cy
    return acc, flags

def __AC(op, acc, tmp, cy=0):
    """ Auxiliary carry flag """
    return bool(
        op(acc & 0x0f, tmp & 0x0f, cy) // 16
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
