from .core import *

class ALU:

    CY      = 0x01
    P       = 0x04
    AC      = 0x10
    Z       = 0x40
    S       = 0x80

    FLAGS   = 0x02

    def __init__(self):
        self.ACC    = 0x00
        self.flags  = 0x02

    def reset(self):
        self.ACC = 0x00
        self.flags = FLAGS
    
    def get(self, f):
        return bool(
            self.flags & f
        )
    
    def z(self):
        """ Get Z flag """
        return self.get(ALU.Z)
    
    def s(self):
        """ Get S flag """
        return self.get(ALU.S)
        
    def p(self):
        """ Get P flag """
        return self.get(ALU.P)
    
    def ac(self):
        """ Get AC flag """
        return self.get(ALU.AC)
    
    def cy(self):
        """ Get CY flag """
        return self.get(ALU.CY)
    
    def PSW(self):
        return self.flags << 8 | self.ACC
    
    def set_PSW(self, tmp_16):
        self.flags = tmp_16 >> 8
        self.ACC = tmp_16 & 0x0f

    def ADD(self, tmp, cy=0):
        """ Add """
        self.flags, self.ACC = exec(ADD, self.ACC, tmp)
    
    def ADC(self, tmp):
        """ Add with carry """
        self.flags, self.ACC = exec(ADD, self.ACC, tmp, self.cy())

    def SUB(self, tmp):
        """ Subtract """
        self.flags, self.ACC = exec(SUB, self.ACC, tmp)
    
    def SBB(self, tmp):
        """ Subtract with borrow """
        self.flags, self.ACC = exec(SBB, self.ACC, tmp, self.cy())
    
    def INR(self, tmp):
        """ Increment register """
        flags, acc = exec(ADD, 1, tmp)
        self.flags = (flags & ~ALU.CY) | (self.flags & ALU.CY) # preserve CY
        return acc
    
    def DCR(self):
        """ Decrement register """
        flags, acc = exec(SUB, 1, tmp)
        self.flags = (flags & ~ALU.CY) | (self.flags & ALU.CY) # preserve CY
        return acc

    def ANA(self, tmp):
        self.flags, self.ACC = exec(ANA, self.ACC, tmp)

    def XRA(self, tmp):
        """ Logical exclusive OR """
        self.flags, self.ACC = exec(XRA, self.ACC, tmp)
    
    def ORA(self, tmp):
        """ Logical OR """
        self.flags, self.ACC = exec(ORA, self.ACC, tmp)
    
    def RLC(self):
        self.ACC = (self.ACC << 1) // 256 \
         + (self.ACC << 1) % 256
    
    def RRC(self):
        self.ACC = (self.ACC & 0x01) << 7 \
        + (self.ACC >> 1)
    
    def RAL(self):
        self.ACT = self.ACC
        self.ACC = (2 * self.ACT + self.get_CY()) % 256
        self.set_CY(self.ACT // 128)
    
    def RAR(self):
        pass
    
    def CMA(self):
        """ Complement ACCumulator """
        self.ACC = 255 - self.ACC
    
    def CMC(self):
        """ Complement carry """
        self.flags ^= ALU.CY
    
    def STC(self):
        """ Set carry """
        self.flags |= ALU.CY
    
    def DAD(self, tmp16):
        self.__ADC()
        self.update_CY()
        return self.out
    
    def CMP(self, tmp):
        # subtract without updating ACC
        self.flags, _ = exec(sub, self.ACC, tmp)
