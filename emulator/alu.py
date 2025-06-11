from .flags import encode, decode, s, z, p
from .core import *


def __add_4(act_4, tmp_4, cy):
    return (
        (act_4 + tmp_4 + cy) // 16,
        (act_4 + tmp_4 + cy) % 16
    )

def __add(act, tmp, cy):
    ac, acc_l = __add_4(act % 16, tmp % 16, cy)
    cy, acc_h = __add_4(act // 16, tmp // 16, ac)
    acc = (acc_h << 4) | acc_l
    return acc, ac, cy

def adc(act, tmp, cy=0):
    acc, ac, cy = __add(act, tmp, cy)
    _s, _z, _p = s(acc), z(acc), p(acc)
    flags = encode(_s, _z, ac, _p, cy)
    return acc, flags

def sub(act, tmp):
    return add(act, 256 - tmp)

def ana(act, tmp):
    acc = act & tmp
    s, z, p = s(acc), z(acc), p(acc)
    flags = encode(s, z, 0, p, 0)
    return acc, flags

def xra(act, tmp):
    acc = act ^ tmp
    s, z, p = s(acc), z(acc), p(acc)
    flags = encode(s, z, 0, p, 0)
    return acc, flags

def ora(act, tmp):
    acc = act | tmp
    s, z, p = s(acc), z(acc), p(acc)
    flags = encode(s, z, 0, p, 0)
    return acc, flags

class ALU:

    def add(self, act, tmp):
        return adc(act, tmp, 0)
    
    def adc(self, act, tmp, cy=0):
        return adc(act, tmp, cy)
    
    def sub(self, act, tmp):
        return sub(act, tmp)
    
    def SBB(self, act, tmp, cy=0):
        return self.SBB(act, tmp, flags)
    
    def ana(self, act, tmp):
        return ana(act, tmp)
    
    def xra(self, act, tmp):
        return xra(act, tmp)
    
    def ORA(self, act, tmp):
        return ora(act, tmp)
    
    def CMP(self, act, tmp, _):
        _, flags = sub(act, tmp)
        return act, flags

    def INR(self, tmp):
        acc, flags = add(act, 1)
        s, z, ac, p, _ = decode(flags)
        flags = encode(s, z, ac, p, 0)
        return acc, flags

    def DCR(self, tmp):
        acc, flags = SUB(tmp, 1)
        s, z, ac, p, _ = decode(flags)
        flags = encode(s, z, ac, p, 0)
        return acc, flags
    
    def RLC(self, act):
        """ 
        Rotate left

        (An+1) <- (An); (A0) <- (A7); (CY) <- (A7)

        """
        cy = act // 128
        acc = (act << 1) % 256 + cy
        flags = encode(c=cy)
        return acc, flags

    def RRC(self, act, _, flags_in):
        """
        Rotate right

        (An) <- (An-1); (A7) <- (A0); (CY) <- (A0)

        """
        cy = act & 0x01
        acc = (cy << 7) | (act >> 1)
        flags = cy | (flags_in & ~CY)
        return acc, flags

    def RAL(self, act, _, flags):
        """
        Rotate left through carry

        (An+1) <- (An); (CY) <- (A7); (A0) <- (CY)

        """
        acc = (acc << 1) | (flags & CY)
        flags = (acc // 256) | (flags & ~CY)
        return acc % 256, flags

    def RAR(self, act, tmp, flags):
        """
        Rotate right through carry

        (An) <- (An+1); (CY) <- (A0); (A7) <- (CY)

        """
        cy = flags & CY
        

        return 0x00, 0x00
