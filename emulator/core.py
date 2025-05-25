
# ALU
def ADD(acc, tmp, flags):
    """ Add """
    return ADC(acc, tmp, 0)

def ADC(acc, tmp, flags):
    """ Add with carry """
    cy = (acc + tmp + (flags & 0x01)) // 256
    ac = (acc % 16 + tmp % 16 + (flags & 0x01)) // 16
    acc = (acc + tmp + flags & 0x01) % 256
    flags = Z(acc) | S(acc) | P(acc) | cy 
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
    flags = Z(acc) | S(acc) | P(acc)
    return acc, flags

def XRA(acc, tmp, flags):
    """ Exclusive or """
    acc = (acc ^ tmp)
    flags = Z(acc) | S(acc) | P(acc)
    return acc, flags

def ORA(acc, tmp, cy=0):
    """ Or """
    acc = (acc | tmp)
    flags = Z(acc) | S(acc) | P(acc)
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

def ac(op, acc, tmp, cy=0):
    """ Auxiliary carry flag """
    return bool(
        op(acc & 0x0f, tmp & 0x0f, cy) // 16
    ) << 4

def cy(op, acc, tmp, cy=0):
    """ Carry flag """
    return bool(
        op(acc, tmp, cy) // 256
    ) << 0 | 0x02

def Z(acc):
    """ 
    Zero flag (Z)
    """ 
    return bool(
        not op(acc, tmp, cy) % 256
    ) << 6 | 0x02

def S(acc):
    """ 
    Sign flag (S)
    """
    return bool(
        op(acc, tmp, cy) & 0x80
    ) << 7 | 0x02

def P(acc):
    """ Parity flag """
    return bool(
        0
    ) << 2

def DAD(acc_16, tmp_16):
    flags, acc_lo = ADD(acc_16 % 256, tmp_16 % 256)
    flags, acc_hi = ADC(acc_16 // 256, tmp_16 // 256, flags & 0x01)
    return flags, 256 * acc_hi + acc_lo

def INX(tmp_16):
    return DAD(tmp_16, 1)

def DCX(tmp_16):
    return DAD(tmp_16, 255)
