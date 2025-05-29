from .registers     import *
from .flags         import *
from .alu           import ALU

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

        self.pairs = [
            (B, C), # BC
            (D, E), # DE
            (H, L), # HL
            (6, 7)
        ]

        # ALU
        self.alu = ALU()

        # Set by HLT instruction, terminates exec loop
        self.halt = False

        # memory
        self.mem = [0x00] * 64 * (1 << 10)

        self.optable = [self.NOP] * 256
        self.__init_optable()

        # conditions
        self.conds = [None] * 8
        self.__init_conds()

        self.cycles = 0

    def __init_optable(self):
        self.optable[0x00] = self.NOP
        self.optable[0x01] = self.LXI
        self.optable[0x02] = self.STAX
        self.optable[0x03] = self.INX
        self.optable[0x04] = self.INR
        self.optable[0x05] = self.DCR
        self.optable[0x06] = self.MVI
        self.optable[0x07] = self.RLC
        
        self.optable[0x09] = self.DAD
        self.optable[0x0a] = self.LDAX
        self.optable[0x0b] = self.DCX
        self.optable[0x0c] = self.INR
        self.optable[0x0d] = self.DCR
        self.optable[0x0e] = self.MVI
        self.optable[0x0f] = self.RRC

        self.optable[0x11] = self.LXI
        self.optable[0x12] = self.STAX
        self.optable[0x13] = self.INX
        self.optable[0x14] = self.INR
        self.optable[0x15] = self.DCR
        self.optable[0x16] = self.MVI
        self.optable[0x17] = self.RAL
        
        self.optable[0x19] = self.DAD
        self.optable[0x1a] = self.LDAX
        self.optable[0x1b] = self.DCX
        self.optable[0x1c] = self.INR
        self.optable[0x1d] = self.DCR
        self.optable[0x1e] = self.MVI
        self.optable[0x1f] = self.RAR

        self.optable[0x21] = self.LXI
        self.optable[0x22] = self.SHLD
        self.optable[0x23] = self.INX
        self.optable[0x24] = self.INR
        self.optable[0x25] = self.DCR
        self.optable[0x26] = self.MVI
        self.optable[0x27] = self.DAA

        self.optable[0x29] = self.DAD
        self.optable[0x2a] = self.LHLD
        self.optable[0x2b] = self.DCX
        self.optable[0x2c] = self.INR
        self.optable[0x2d] = self.DCR
        self.optable[0x2e] = self.MVI
        self.optable[0x2f] = self.CMA

        self.optable[0x31] = self.LXI
        self.optable[0x32] = self.STA
        self.optable[0x33] = self.INX
        self.optable[0x34] = self.INR
        self.optable[0x35] = self.DCR
        self.optable[0x36] = self.MVI
        self.optable[0x37] = self.STC

        self.optable[0x39] = self.DAD
        self.optable[0x3a] = self.LDA
        self.optable[0x3b] = self.DCX
        self.optable[0x3c] = self.INR
        self.optable[0x3d] = self.DCR
        self.optable[0x3e] = self.MVI
        self.optable[0x3f] = self.CMC
        self.optable[0x40] = self.MOV
        self.optable[0x41] = self.MOV
        self.optable[0x42] = self.MOV
        self.optable[0x43] = self.MOV
        self.optable[0x44] = self.MOV
        self.optable[0x45] = self.MOV
        self.optable[0x46] = self.MOV
        self.optable[0x47] = self.MOV
        self.optable[0x48] = self.MOV
        self.optable[0x49] = self.MOV
        self.optable[0x4a] = self.MOV

        self.optable[0x50] = self.MOV
        self.optable[0x51] = self.MOV
        self.optable[0x52] = self.MOV
        self.optable[0x53] = self.MOV
        self.optable[0x54] = self.MOV
        self.optable[0x55] = self.MOV
        self.optable[0x56] = self.MOV
        self.optable[0x57] = self.MOV

        self.optable[0x58] = self.MOV
        self.optable[0x59] = self.MOV
        self.optable[0x5a] = self.MOV
        self.optable[0x5b] = self.MOV
        self.optable[0x5c] = self.MOV
        self.optable[0x5d] = self.MOV
        self.optable[0x5e] = self.MOV
        self.optable[0x5f] = self.MOV

        self.optable[0x60] = self.MOV
        self.optable[0x61] = self.MOV
        self.optable[0x62] = self.MOV
        self.optable[0x63] = self.MOV
        self.optable[0x64] = self.MOV
        self.optable[0x65] = self.MOV
        self.optable[0x66] = self.MOV
        self.optable[0x67] = self.MOV

        self.optable[0x68] = self.MOV
        self.optable[0x69] = self.MOV
        self.optable[0x6a] = self.MOV
        self.optable[0x6b] = self.MOV
        self.optable[0x6c] = self.MOV
        self.optable[0x6d] = self.MOV
        self.optable[0x6e] = self.MOV
        self.optable[0x6f] = self.MOV

        self.optable[0x70] = self.MOV
        self.optable[0x71] = self.MOV
        self.optable[0x72] = self.MOV
        self.optable[0x73] = self.MOV
        self.optable[0x74] = self.MOV
        self.optable[0x75] = self.MOV
        self.optable[0x76] = self.HLT
        self.optable[0x77] = self.MOV

        self.optable[0x78] = self.MOV
        self.optable[0x79] = self.MOV
        self.optable[0x7a] = self.MOV
        self.optable[0x7b] = self.MOV
        self.optable[0x7c] = self.MOV
        self.optable[0x7d] = self.MOV
        self.optable[0x7e] = self.MOV
        self.optable[0x7f] = self.MOV

        self.optable[0x80] = self.ADD
        self.optable[0x81] = self.ADD
        self.optable[0x82] = self.ADD
        self.optable[0x83] = self.ADD
        self.optable[0x84] = self.ADD
        self.optable[0x85] = self.ADD
        self.optable[0x86] = self.ADD
        self.optable[0x87] = self.ADD

        self.optable[0x88] = self.ADC
        self.optable[0x89] = self.ADC
        self.optable[0x8a] = self.ADC
        self.optable[0x8b] = self.ADC
        self.optable[0x8c] = self.ADC
        self.optable[0x8d] = self.ADC
        self.optable[0x8e] = self.ADC
        self.optable[0x8f] = self.ADC

        self.optable[0x90] = self.SUB
        self.optable[0x91] = self.SUB
        self.optable[0x92] = self.SUB
        self.optable[0x93] = self.SUB
        self.optable[0x94] = self.SUB
        self.optable[0x95] = self.SUB
        self.optable[0x96] = self.SUB
        self.optable[0x97] = self.SUB

        self.optable[0x98] = self.SBB
        self.optable[0x99] = self.SBB
        self.optable[0x9a] = self.SBB
        self.optable[0x9b] = self.SBB
        self.optable[0x9c] = self.SBB
        self.optable[0x9d] = self.SBB
        self.optable[0x9e] = self.SBB
        self.optable[0x9f] = self.SBB

        self.optable[0xa0] = self.ANA
        self.optable[0xa1] = self.ANA
        self.optable[0xa2] = self.ANA
        self.optable[0xa3] = self.ANA
        self.optable[0xa4] = self.ANA
        self.optable[0xa5] = self.ANA
        self.optable[0xa6] = self.ANA
        self.optable[0xa7] = self.ANA

        self.optable[0xa8] = self.XRA
        self.optable[0xa9] = self.XRA
        self.optable[0xaa] = self.XRA
        self.optable[0xab] = self.XRA
        self.optable[0xac] = self.XRA
        self.optable[0xad] = self.XRA
        self.optable[0xae] = self.XRA
        self.optable[0xaf] = self.XRA

        self.optable[0xb0] = self.ORA
        self.optable[0xb1] = self.ORA
        self.optable[0xb2] = self.ORA
        self.optable[0xb3] = self.ORA
        self.optable[0xb4] = self.ORA
        self.optable[0xb5] = self.ORA
        self.optable[0xb6] = self.ORA
        self.optable[0xb7] = self.ORA

        self.optable[0xb8] = self.CMP
        self.optable[0xb9] = self.CMP
        self.optable[0xba] = self.CMP
        self.optable[0xbb] = self.CMP
        self.optable[0xbc] = self.CMP
        self.optable[0xbd] = self.CMP
        self.optable[0xbe] = self.CMP
        self.optable[0xbf] = self.CMP



        self.optable[0xc3] = self.JMP

    def dispatch(self):
        return self.optable[self.ir]

    def load(self, arr):
        for idx, data in enumerate(arr):
            self.mem[idx] = data
    
    def exec(self):
        while not self.halt:
            
            self.ir = self.fetch()
            
            instruction = self.dispatch()
            
            instruction()
    
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
    
    def pair(self, rh, rl):
        return self.reg(rh), self.reg(rl)
    
    def set_pair(self, rh, rl, dh, dl):
        self.regs[rh] = dh
        self.regs[rl] = rl
        self.regs[rp + 1] = data_16 % 256
    
    def __get_RP(self):
        return self.get_pair(self.__RP())
    
    def __set_RP(self, data_16):
        self.set_pair(self.__RP(), data_16)
    
    def set_BC(self, data_16):
        """ Set register pair BC """
        self.set_pair(B, data_16)
    
    def set_DE(self, data_16):
        """ Set register pair DE """
        self.regs[D] = data_16 // 256
        self.regs[E] = data_16 % 256
    
    def set_HL(self, data_16):
        """ Set register pair HL """
        self.regs[H] = data_16 // 256
        self.regs[L] = data_16 % 256
    
    def PSW(self):
        return (self.regs[A] << 8) | self.flags

    def set_PSW(self, data_16):
        pass

    def fetch(self):
        data = self.read(self.pc)
        self.pc += 1
        return data
    
    def read(self, addr):
        self.cycles += 1
        return self.mem[addr]
    
    def store(self, addr, data):
        self.cycles += 1
        self.mem[addr] = data
    
    def read_16(self, addr):
        self.cycles += 2
        return self.read(addr) + 256 * self.read(addr + 1)
    
    def store_16(self, addr, data_16):
        self.store(addr, data_16 % 256)
        self.store(addr + 1, data_16 // 256)

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
        self.store_16(self.sp, data_16)

    def read_M(self):
        return self.read(self.get_HL())

    def __init_conds(self):
        self.conds[0] = lambda: self.flag(Z)  == 0
        self.conds[1] = lambda: self.flag(Z)  == 1
        self.conds[2] = lambda: self.flag(CY) == 0
        self.conds[3] = lambda: self.flag(CY) == 1
        self.conds[4] = lambda: self.flag(P)  == 0
        self.conds[5] = lambda: self.flag(P)  == 1
        self.conds[6] = lambda: self.flag(S)  == 0
        self.conds[7] = lambda: self.flag(S)  == 1
    
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
    
    def __get_SRC(self):
        if self.__SRC() == M:
            return self.read_M()
        else:
            return self.regs[self.__SRC()]
    
    def __get_DST(self):
        if self.__DST() == M:
            return self.read_M()
        else:
            return self.regs[self.__DST()]
    
    def __set_DST(self, data):
        if self.__DST() == M:
            self.store_M(data)
        else:
            self.regs[self.__DST()] = data

    def __CCC(self):
        """ decode condition code """
        return (self.ir & 0x38) >> 3
    
    def __NNN(self):
        """ decode n """
        return (self.ir & 0x38) >> 3
    

    def MOV(self):
        self.__set_DST(self.__get_SRC())
    
    def MVI(self):
        """ Move immediate register """
        self.__set_DST(self.fetch())
    
    def LXI(self):
        """ Load register pair immediate """
        self.__set_RP(self.fetch_16())
    
    def LDA(self):
        """ Load accumulator direct """
        self.regs[A] = self.read(self.fetch_16())
    
    def STA(self):
        """ Store Accumulator direct """
        self.store(self.fetch_16(), self.regs[A])
    
    def LHLD(self):
        """ Load L and H direct """
        self.set_HL(self.read_16(
            self.fetch_16()
        ))
    
    def SHLD(self):
        """ 
        Store H and L direct 
        """
        self.store_16(self.fetch_16(), self.get_HL())
    
    def LDAX(self):
        """
        Load accumulator indirect
        BC or DE
        """
        self.regs[A] = self.read(self.__get_RP())
    
    def STAX(self):
        """ Store accumulator indirect """
        self.store(self.__get_RP(), self.regs[A])
    
    def XCHG(self):
        self.regs[H], self.regs[D] = self.regs[D], self.regs[H]
        self.regs[L], self.regs[E] = self.regs[E], self.regs[L]

    def __ALR(self):
        """ ALU operation on register """
        func = self.alu.dispatch(self.__ALU())
        self.regs[A], self.flags = func(
            self.regs[A], self.regs[self.__SRC()], self.flags
        )
    
    def __ALI(self):
        """ ALU operation on immediate """
        func = self.alu.dispatch(self.__ALU())
        
        self.regs[A], self.flags = func(
            self.regs[A], self.fetch(), self.flags
        )

    def ADD(self):
        """ 
        Add register 

        (A) <- (A) + (r) 
        
        The content of register r is added to the content of the 
        accumulator. The result is placed in the accumulator.

        """
        self.__ALR()
    
    def ADI(self):
        """ 
        Add immediate 
        
        (A) <- (A) + (byte 2) 

        The content of the second byte of the instruction is 
        added to the content of the accumulator. The result 
        is placed in the accumulator. 

        """
        self.__ALI()
    
    def ADC(self):
        """
        Add register with carry

         (A) <- (A) + (r) + (CY) 

        The content of register r and the content of the carry 
        bit are added to the content of the accumulator. The 
        result is placed in the accumulator. 

        """
        self.__ALR()
    
    def __ACI(self):
        """ 
        Add immediate with carry 

        (A) <- (A) + (byte 2) + (CY) 
        
        The content of the second byte of the instruction and 
        the content of the CY flag are added to the contents 
        of the accumulator. The result is placed in the 
        accumulator. 
        
        """
        self.regs[A], self.flags = self.alu.ADC(
            self.regs[A],
            self.fetch(),
            self.flags
        )

    def SUB(self):
        """ 
        Subtract register 

        (A) <- (A) - (r) 
        
        The content of register r is subtracted from the con
        tent of the accumulator. The result is placed in the 
        accumulator. 
        
        """
        self.__ALR()
    
    def __SUI(self):
        """ 
        Subtract immediate 
        
        (A) <- (A) - (byte 2) 
        
        The content of the second byte of the instruction is 
        subtracted from the content of the accumulator. The 
        result is placed in the accumulator. 
        
        """
        self.__ALI()

    def SBB(self):
        """ Subtract register with borrow """
        self.SBB(self.regs[self.__SRC])

    def __SBI(self):
        """ Subtract immediate with borrow """
        self.alu.SBB(self.fetch())
    
    def INR(self):
        """ 
        Increment register 

        (r) <- (r) + 1
        
        The content of register r is incremented by one. 
        Note: All condition flags except CY are affected.
        
        """
        acc, self.flags = self.alu.INR(0, self.__get_DST(), self.flags)
        self.__set_DST(acc)
    
    def DCR(self):
        """ 
        Decrement register 
        
        (r) <- (r) - 1

        The content of register r is decremented by one. 
        Note: All condition flags except CY are affected. 
        
        """
        acc, self.flags = self.alu.DCR(0, self.__get_DST(), self.flags)
        self.__set_DST(acc)
    
    def INX(self, tmp_16):
        """ 
        Increment register pair 

        (rh) (rl) <- (rh) (rl) + 1
        
        the content of the register pair rp is incremented by 
        one. Note: No condition ftags are affected.  
        
        """
        tmp_16 = self.__get_RP()

        if self.__RP() == 4:
            tmp_16 = self.pc

        acc_lo, flags = self.alu.ADD(tmp_16 % 256, 1, self.flags)
        acc_hi, flags = self.alu.ADC(tmp_16 // 256, 0, flags)

        self.__set_RP(256 * acc_hi + acc_lo)
    
    def DCX(self):
        """ Decrement register pair """
        tmp_lo, tmp_hi  = self.__get_RP() % 256, self.__get_RP() // 256

        acc_lo, flags   = SUB(tmp_lo, 1, self.flags)
        acc_hi, _       = SBB(tmp_hi, 0, flags)
        
        self.__set_RP(256 * acc_hi + acc_lo)
    
    def DAD(self, tmp_16):
        tmp_lo, tmp_hi = self.__get_RP() % 256, self.__get_RP() // 256

        self.regs[L], flags = self.alu.ADD(self.regs[L], tmp_lo, self.flags)
        self.regs[H], flags = self.alu.ADC(self.regs[H], tmp_hi, flags)

        self.flags = (flags & CY) | (self.flags & ~CY)
    
    def DAA(self):
        """ Decimal adjust accumulator """
        pass
    
    def ANA(self):
        self.alu.ANA(self.regs[A], 123, self.flags)
        self.flags, self.acc = alu(ANA, self.acc, tmp)
    
    def ANI(self):
        """ And immediate """
        self.alu.ANA(self.fetch())
    
    def XRA(self):
        """ Exclusive OR register """
        self.alu.XRA(self.regs[self.__SRC])

    def XRI(self):
        """ Exclusive OR immediate """
        self.__alu_xra(self.fetch())
    
    def ORA(self):
        """ OR register """
        self.alu.ORA(self.regs[self.__SRC])
    
    def ORI(self):
        """ OR immediate """
        self.__alu_or(self.fetch())
    
    def CMP(self):
        """ Compare register """
        _, self.flags = self.alu.CMP(
            self.regs[A], self.__get_SRC(), self.flags
        )
    
    def CPI(self):
        """ Compare immediate """
        _, self.flags = self.alu.CMP(
            self.regs[A], self.fetch(), self.flags
        )
    
    def RLC(self):
        """ Rotate left """
        self.regs[A], self.flags = self.alu.RRC(
            self.regs[A], 0, self.flags
        )
    
    def RRC(self):
        """ Rotate right """
        self.alu.RRC()
    
    def RAL(self):
        """ Rotate left through carry """
        self.alu.RAL()
    
    def RAR(self):
        """ Rotate right through carry """
        self.alu.RAR()
    
    def CMA(self):
        """ Complement accumulator """
        self.regs[A] = 255 - self.regs[A]
    
    def CMC(self):
        """ Complement carry """
        self.flags ^= CY
    
    def STC(self):
        """ Set carry """
        self.flags |= CY
    
    def JMP(self):
        """ Jump """
        self.pc = self.fetch_16()

    def CALL(self):
        """ Unconditional call """
        self.push_16(self.pc)
        self.pc = self.fetch_16()
    
    def JCC(self):
        """ Conditional jump """
        if self.conds[self.__CCC()]:
            self.JMP()
    
    def CCC(self):
        """ Condition call """
        if self.conds[self.__CCC()]:
            self.CALL()
    
    def RET(self):
        """ Return """
        self.pc = self.pop_16()
    
    def RCC(self):
        """ Conditional return """
        if self.conds[self.__CCC()]:
            self.RET()
    
    def RST(self):
        """ Restart """
        self.push_16(self.pc)
        self.pc = 8 * self.__NNN()
    
    def PCHL(self):
        """ Jump H and L indirect """
        self.pc = self.get_HL()
    
    def PUSH(self):
        """ Push """
        self.push_16(
            self.__get_RP()
        )

    def POP(self):
        """ Pop """
        data_16 = self.pop_16()
        if self.__DST() == SP:
            # TODO: set PSW
            pass
        else:
            self.__set_RP(data_16)
    
    def XTHL(self):
        """ Exchange stack top with H and L """
        data_16 = self.pop_16()
        self.push_16(self.get_HL())
        self.set_HL(data_16)
    
    def SPHL(self):
        """ Move HL to SP """
        self.sp = self.get_pair(HL)
    
    def IN(self):
        """ Input """
        pass
    
    def OUT(self):
        """ Output """
        pass
    
    def EI(self):
        """ Enable interrupts """
        pass
    
    def DI(self):
        """ Disable interrupts """
        pass
    
    def HLT(self):
        """ Halt """
        print("halt")
        self.halt = True
    
    def NOP(self):
        """ No op """
        print("nop")
        pass
