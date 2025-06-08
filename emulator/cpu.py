from .registers     import *
from .flags         import *
from .alu           import ALU
from .core          import pack, unpack

class CPU:

    def __init__(self):

        # program counter
        self.pc = 0x0000

        # stack pointer
        self.sp = 0xBEEF

        # 8-bit registers
        self.acc = 0x00
        self.flags = 0x02
        
        # instruction register
        self.ir = 0x00

        # A - L
        self.regs = [0x00] * 8

        # ALU
        self.alu = ALU()

        # Set by HLT instruction, terminates exec loop
        self.halt = False

        # memory
        self.mem = [0x00] * 64 * (1 << 10)

        #self.__init_optable()

        # conditions
        self.conds = [None] * 8
        self.__init_conds()

        self.cycles = 0


    def dispatch(self):
        return self.optable[self.ir]

    def load(self, arr):
        for idx, data in enumerate(arr):
            self.mem[idx] = data

    
    def __get_register(self, r):
        if r == M:
            return self.M
        else:
            return self.regs[r]
        
    def __set_register(self, r, data):
        if r == M:
            self.set_M(data)

    @property
    def A(self):
        return self.regs[A]
    
    @A.setter
    def A(self, data):
        self.regs[A] = data
    
    @property
    def B(self):
        return self.regs[B]

    @B.setter
    def B(self, data):
        self.regs[B] = data
    
    @property
    def C(self):
        return self.regs[C]
    
    @C.setter
    def C(self, data):
        self.regs[C] = data
    
    @property
    def D(self):
        return self.regs[D]
    
    @D.setter
    def D(self, data):
        self.regs[D] = data
    
    @property
    def M(self):
        return self.read(self.HL)
    
    @M.setter
    def M(self, data):
        self.write(self.HL, data)
    
    @property
    def src(self):
        if self.__SRC() == M:
            return self.M
        else:
            return self.regs[self.__SRC()]
        
    @src.setter
    def src(self, data):
        self.__set_reg(self.__SRC(), data)
    
    @property
    def dst(self):
        return self.__get_register(self.__DST())
    
    @dst.setter
    def dst(self, data):
        self.__set_reg(self.__DST(), data)
    
    @property
    def BC(self):
        return pack(self.B, self.C)
    
    @BC.setter
    def BC(self, data_16):
        self.B, self.C = unpack(data_16)
    
    @property
    def DE(self):
        return pack(self.D, self.E)
    
    @DE.setter
    def DE(self, data_16):
        self.D, self.E = unpack(data_16)
    
    @property
    def HL(self):
        return pack(self.H, self.L)
    
    @HL.setter
    def HL(self, data_16):
        self.H, self.L = unpack(data_16)
    
    @property
    def PSW(self):
        return pack(self.A, self.flags)
    
    @PSW.setter
    def PSW(self, data_16):
        self.A, self.flags = unpack(data_16)
    
    @property
    def rp(self):
        if self.__RP() == 0:
            return self.BC()
        elif self.__RP() == 1:
            return self.DE()
    
    @rp.setter
    def rp(self):
        pass
    
    @property
    def rl(self):
        _, data = unpack(self.rp)
        return data
    
    @rl.setter
    def rl(self, data):
        self.rp = pack(self.rh, data)

    @property
    def rh(self):
        data, _ = unpack(self.rp)
        return data
    
    @rh.setter
    def rh(self, data):
        self.rp = pack(data, self.rl)

    @property
    def Z(self):
        return bool(self.flags & Z)
    
    @property
    def S(self):
        return bool(self.flags & S)
    
    @property
    def P(self):
        return bool(self.flags & P)
    
    @property
    def AC(self):
        return bool(self.flags & AC)
    
    @property
    def CY(self):
        return bool(self.flags & CY)
    
    @property
    def cond(self):
        return self.conds[self.__COND]

    def reset(self):
        self.alu.reset()
        self.pc = 0x0000
        self.sp = 0xBEEF
        self.halt = False
    
    def flag(self, flag):
        return bool(self.flags & flag)
    
    def reg(self, reg):
        if reg == M:
            pass
        else:
            return self.regs[reg]
    
    def __set_RP(self, data_16):
        self.set_pair(self.__RP(), data_16)

    def fetch(self):
        data = self.read(self.pc)
        self.pc += 1
        return data
    
    def read(self, addr):
        self.cycles += 1
        return self.mem[addr]
    
    def write(self, addr, data):
        self.cycles += 1
        self.mem[addr] = data
    
    def read_16(self, addr):
        self.cycles += 2
        return pack(self.read(addr), self.read(addr + 1))
    
    def write_16(self, addr, data_16):
        data_hi, data_lo = unpack(data_16)
        self.write(addr, data_lo)
        self.write(addr + 1, data_hi)

    # memory operation

    def fetch(self):
        data = self.read(self.pc)
        self.pc += 1
        return data
    
    def fetch_16(self):
        data = self.read_16(self.pc)
        self.pc += 2
        return data
    
    # stack operations
    
    def pop_16(self):
        data_16 = self.read_16(self.sp)
        self.sp += 2
        return data_16

    def push_16(self, data_16):
        self.sp -= 2
        self.write_16(self.sp, data_16)

    def __init_conds(self):
        self.conds[0] = lambda: self.Z  == 0
        self.conds[1] = lambda: self.Z  == 1
        self.conds[2] = lambda: self.CY == 0
        self.conds[3] = lambda: self.CY == 1
        self.conds[4] = lambda: self.P  == 0
        self.conds[5] = lambda: self.P  == 1
        self.conds[6] = lambda: self.S  == 0
        self.conds[7] = lambda: self.S  == 1
    
    def __SRC(self):
        """ decode source register index """
        return self.ir & 0x07

    def __DST(self):
        """ decode destination register index """
        return (self.ir & 0x38) >> 3
    
    def __RP(self):
        """ decode register pair index """
        return (self.ir & 0x03) >> 4
    
    def __ALU(self):
        """ decode alu opcode """
        return (self.ir & 0x38) >> 3

    def __CCC(self):
        """ decode condition code """
        return (self.ir & 0x38) >> 3
    
    def __NNN(self):
        """ decode n """
        return (self.ir & 0x38) >> 3
