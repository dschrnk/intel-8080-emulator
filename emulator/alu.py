from .flags import *
from .core import *


class ALU:

    def __init__(self):
        self.optable = [None] * 8
        self.__init_optable()
    
    def __init_optable(self):
        self.optable[0] = self.ADD
        self.optable[1] = self.ADC
        self.optable[2] = self.SUB
        self.optable[3] = self.SBB
        self.optable[4] = self.ANA
        self.optable[5] = self.XRA
        self.optable[6] = self.ORA
        self.optable[7] = self.CMP
    
    def dispatch(self, opc):
        return self.optable[opc]

    def ADD(self, act, tmp, flags):
        return self.ADC(act, tmp, flags & ~CY)
    
    def ADC(self, act, tmp, flags):
        return ADC(act, tmp, flags)
    
    def SUB(self, act, tmp, flags):
        return self.ADD(act, 256 - tmp, flags)
    
    def SBB(self, act, tmp, flags):
        return SBB(act, tmp, flags)
    
    def ANA(self, act, tmp, flags):
        return ANA(act, tmp, flags)
    
    def XRA(self, act, tmp, flags):
        return XRA(act, tmp, flags)
    
    def ORA(self, act, tmp, flags):
        return 0x00, 0x00
    
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
    
    def RLC(self, act, tmp, flags_in):
        """ 
        Rotate left

        (An+1) <- (An); (A0) <- (A7); (CY) <- (A7)

        """
        cy = act // 256
        acc = (act << 1) % 256 + cy
        flags = cy | (flags_in & ~CY)
        return acc, flags

    def RRC(self, act, tmp, flags):
        return 0x00, 0x00

    def RAL(self, act, tmp, flags):
        return 0x00, 0x00

    def RAR(self, act, tmp, flags):
        return 0x00, 0x00
