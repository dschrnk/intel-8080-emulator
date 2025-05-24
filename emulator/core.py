
def ADD(acc, tmp, cy=0):
    """ Add """
    return (acc + tmp + cy)

def ADC(acc, tmp, cy=0):
    """ Add with carry """
    return ADD(acc, tmp, cy)

def SUB(acc, tmp, cy=0):
    """ Subtract """
    return ADD(acc, 256 - tmp, 256 - cy)

def SBB(acc, tmp, cy=0):
    """ Subtract with borrow """
    return sub(acc, tmp, cy)

def ANA(acc, tmp, cy=0):
    """ And """
    return (acc & tmp)

def XRA(acc, tmp, cy=0):
    """ Exclusive or """
    return (acc ^ tmp)

def ORA(acc, tmp, cy=0):
    """ Or """
    return (acc | tmp)

def CMP(acc, tmp, cy=0):
    """ Compare """
    return SUB(acc, tmp, cy)

def ac(op, acc, tmp, cy=0):
    """ Auxiliary carry flag """
    return bool(
        op(acc & 0x0f, tmp & 0x0f, cy) // 16
    ) << 4

def c(op, acc, tmp, cy=0):
    """ Carry flag """
    return bool(
        op(acc, tmp, cy) // 256
    ) << 0

def z(op, acc, tmp, cy=0):
    """ Zero flag """ 
    return bool(
        not op(acc, tmp, cy) % 256
    ) << 6

def s(op, acc, tmp, cy=0):
    """ Sign flag """
    return bool(
        op(acc, tmp, cy) & 0x80
    ) << 7

def p(op, acc, tmp, cy=0):
    """ Parity flag """
    return bool(
        0
    ) << 2

def flags(op, acc, tmp, cy=0):
    return (
        1 << 1 |
        s(op, acc, tmp, cy) |
        z(op, acc, tmp, cy) |
        p(op, acc, tmp, cy) |
        ac(op, acc, tmp, cy) |
        c(op, acc, tmp, cy)
    )

def alu(op, acc, tmp, cy=0):
    return(
        flags(op, acc, tmp, cy),
        op(acc, tmp, cy) % 256
    )

def exec(op, acc, tmp, cy=0):
    return ALU(op, acc, tmp, cy)

def DAD(acc_16, tmp_16):
    flags, acc_lo = ADD(acc_16 % 256, tmp_16 % 256)
    flags, acc_hi = ADC(acc_16 // 256, tmp_16 // 256, flags & 0x01)
    return flags, 256 * acc_hi + acc_lo

def INX(tmp_16):
    return DAD(tmp_16, 1)

def DCX(tmp_16):
    return DAD(tmp_16, 255)
