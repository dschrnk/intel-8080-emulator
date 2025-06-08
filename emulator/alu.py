from .flags import *
from .core import *

ADD = 0
ANA = 1
XRA = 2
ORA = 3


class ALU:

    def __init__(self):
        pass

    def ADD(self, act, tmp, _):
        return alu(ADD, act, tmp, 0)
    
    def ADC(self, act, tmp, cy):
        return alu(ADD, act, tmp, cy)
    
    def SUB(self, act, tmp, _):
        return alu(ADD, act, 256 - tmp, 0)
    
    def SBB(self, act, tmp, flags):
        return SBB(act, tmp, flags)
    
    def ANA(self, act, tmp, flags):
        return alu(2, act, tmp, flags)
    
    def XRA(self, act, tmp, flags):
        return alu(3, act, tmp, flags)
    
    def ORA(self, act, tmp, flags):
        return alu(4, act, tmp, flags)
    
    def CMP(self, act, tmp, flags):
        _, flags = self.SUB(act, tmp, flags)
        return act, flags

    def INR(self, act, tmp, flags_in):
        acc, flags = ADD(act, 1, flags_in)
        flags = (flags & ~CY) | (flags_in & CY)
        return acc, flags

    def DCR(self, act, tmp, flags_in):
        acc, flags = ADD(act, 256 - 1, flags_in)
        flags = (flags & ~CY) | (flags_in & CY)
        return acc, flags
    
    def RLC(self, act, _, flags_in):
        """ 
        Rotate left

        (An+1) <- (An); (A0) <- (A7); (CY) <- (A7)

        """
        cy = act // 128
        acc = (act << 1) % 256 + cy
        flags = cy | (flags_in & ~CY)
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

    
    def add(self):

        self.exec(lambda acc, tmp, flags: acc + tmp + (flags & CY))

    
def alu(sel, acc, tmp, cy):

    acc_lo, ac = alu_4(sel, act % 16, tmp % 16, cy)

    acc_hi, cy = alu_4(sel, act // 16, tmp // 16, ac)

    acc = (acc_hi << 8) | acc_lo

    z = bool(
        acc_hi == 0 and acc_lo == 0
    )

    s = bool(acc_hi & 0x08)

    p = 0

    flags = (
        cy  << 0 |
        1   << 1 |
        p   << 2 |
        ac  << 4 |
        z   << 6 |
        s   << 7
    )

    return acc, flags


def alu_4(sel, act, tmp, cy):

    match sel:

        case 0:
            return (
                (act + tmp) // 16
                (act + tmp) % 16,
            )
        
        case 1:
            return (
                (act + tmp + cy) // 16
                (act + tmp + cy) % 16,
            )
        
        case 2:
            return (
                0, 0
            )
        
        case 3:
            return (
                0, 0
            )
        
        case 4:
            return (
                0,
                act & tmp
            )
        
        case 5:
            return (
                0,
                act ^ tmp
            )
        
        case 6:
            return (
                0,
                act | tmp
            )


def alu_1(sel, act, tmp, cy):
    match sel:

        # ADD
        case 0 | 1 | 2 | 3 | 7:
            return (
                act & tmp & cy,     # OUT
                act ^ tmp ^ cy      # CY
            )
        
        # ANA
        case 4:
            return(
                act & tmp,
                False
            )
        
        # XRA
        case 5:
            return (
                act ^ tmp,
                False
            )
        
        # ORA
        case 6:
            return (
                act | tmp,
                False
            )
