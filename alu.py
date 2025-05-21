
def add(acc, tmp):
    return (acc + tmp) // 256, (acc + tmp) % 256

class ALU:

    def __init__(self):
        self.ACC    = 0x00
        self.ACT    = 0x00
        self.flags  = 0x02
        self.TMP    = 0x00

        # pseudo-register storing ALU result
        self.out    = 0x00
    
    def reset(self):
        pass
    
    def get_flag(self, f):
        pass
    
    def set_flag(self, f):
        pass
    
    def update_flag(self, f):
        pass
    
    def update_CY(self):
        cy = bool(
            (self.ACT + self.TMP) // 256
        )
    
    def update_AC(self):
        ac = bool(
            (self.ACT % 16 + self.TMP % 16 + self.get_CY()) // 16
        )
    
    def update_Z(self):
        z = not self.out
    
    def update_S(self):
        s = bool(
            self.out & 0x80
        )
    
    def update_flags(self):
        self.update_Z()
        self.update_S()
        self.update_P()
        #self.update_AC()
        #self.update_CY()
    
    def __ADD(self):
        self.out = (self.ACT + self.TMP) % 256

    def ADD(self):
        """ Add """
        self.ACT = self.ACC
        self.__ADD()
        self.update_flags()
        self.ACC = self.out
    
    def ADC(self):
        """ Add with carry """
        self.ADD()
        self.ACT = self.ACC
        self.TMP = self.get_CY()
        self.ADD()

    def SUB(self):
        """ Subtract """
        self.TMP = 256 - self.TMP
        self.ADD()
    
    def SBB(self):
        """ Subtract with borrow """
        pass
    
    def INR(self):
        """ Increment register """
        self.ACT = 1
        self.out = (self.TMP + 1) % 256
        self.__ADD()
    
    def DCR(self):
        """ Decrement register """
        self.ACT = 255
        self.__ADD()
        return self.out

    def ANA(self, data):
        """ Logical AND """
        self.ACC &= data
        self.out = self.ACC
        self.update_flags()

    def XRA(self, data):
        """ Logical exclusive OR """
        self.ACT = self.ACC
        self.out = (self.ACT ^ self.TMP)
        self.ACC = self.out
    
    def ORA(self, data):
        """ Logical OR """
        self.TMP = data
        self.ACT = self.ACC
        self.out = self.ACT | self.TMP
        self.ACC = self.out
    
    def RLC(self):
        pass
    
    def RRC(self):
        pass
    
    def RAL(self):
        pass
    
    def RAR(self):
        pass
    
    def CMA(self):
        pass
    
    def CMC(self):
        pass
    
    def STC(self):
        pass
    
    def DAD(self):
        self.__ADC()
        self.update_CY()
        return self.out
    
    def CMP(self, data):
        self.SUB(data)
        self.ACC = self.ACT
