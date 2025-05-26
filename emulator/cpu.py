from .alu import *

class CPU:

    # Registers
    B   = 0
    C   = 1
    D   = 2
    E   = 3
    H   = 4
    L   = 5
    M   = 6
    A   = 7

    # Flags
    CY  = 0x01
    P   = 0x04
    AC  = 0x10
    Z   = 0x40
    S   = 0x80

    IR  = 0x00

    PC  = 0x0000
    SP  = 0x0800

    def __init__(self):

        # program counter
        self.pc = 0x0000

        # stack pointer
        self.sp = 0x8000

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

        self.dispatch = [self.NOP] * 256
        self.__init_dispatch()

        # conditions
        self.conds = [False] * 8

        self.cycles = 0

    def __init_dispatch(self):
        self.dispatch[0x00] = self.NOP
        self.dispatch[0x01] = self.LXI_BC
        self.dispatch[0x02] = self.STAX_BC
        self.dispatch[0x03] = self.INX
        self.dispatch[0x04] = self.INR
        self.dispatch[0x05] = self.DCR
        self.dispatch[0x06] = self.MVI
        self.dispatch[0x07] = self.RLC
        
        self.dispatch[0x09] = self.DAD
        self.dispatch[0x0a] = self.LDAX
        self.dispatch[0x0b] = self.DCX
        self.dispatch[0x0c] = self.INR
        self.dispatch[0x0d] = self.DCR
        self.dispatch[0x0e] = self.MVI
        self.dispatch[0x0f] = self.RRC

        self.dispatch[0x11] = self.LXI_DE
        self.dispatch[0x12] = self.STAX_DE
        self.dispatch[0x13] = self.INX
        self.dispatch[0x14] = self.INR
        self.dispatch[0x15] = self.DCR
        self.dispatch[0x16] = self.MVI
        self.dispatch[0x17] = self.RAL
        
        self.dispatch[0x19] = self.DAD
        self.dispatch[0x1a] = self.LDAX
        self.dispatch[0x1b] = self.DCX
        self.dispatch[0x1c] = self.INR
        self.dispatch[0x1d] = self.DCR
        self.dispatch[0x1e] = self.MVI
        self.dispatch[0x1f] = self.RAR

        self.dispatch[0x21] = self.LXI_HL
        self.dispatch[0x22] = self.SHLD
        self.dispatch[0x23] = self.INX
        self.dispatch[0x24] = self.INR
        self.dispatch[0x25] = self.DCR
        self.dispatch[0x26] = self.MVI
        self.dispatch[0x27] = self.DAA

        self.dispatch[0x29] = self.DAD
        self.dispatch[0x2a] = self.LHLD
        self.dispatch[0x2b] = self.DCX
        self.dispatch[0x2c] = self.INR
        self.dispatch[0x2d] = self.DCR
        self.dispatch[0x2e] = self.MVI
        self.dispatch[0x2f] = self.CMA

        self.dispatch[0x31] = self.LXI_SP
        self.dispatch[0x32] = self.STA
        self.dispatch[0x33] = self.INX
        self.dispatch[0x34] = self.INR
        self.dispatch[0x35] = self.DCR
        self.dispatch[0x36] = self.MVI
        self.dispatch[0x37] = self.STC

        self.dispatch[0x39] = self.DAD
        self.dispatch[0x3a] = self.LDA
        self.dispatch[0x3b] = self.DCX
        self.dispatch[0x3c] = self.INR
        self.dispatch[0x3d] = self.DCR
        self.dispatch[0x3e] = self.MVI
        self.dispatch[0x3f] = self.CMC
        self.dispatch[0x40] = self.MOV
        self.dispatch[0x41] = self.MOV
        self.dispatch[0x42] = self.MOV
        self.dispatch[0x43] = self.MOV
        self.dispatch[0x44] = self.MOV
        self.dispatch[0x45] = self.MOV
        self.dispatch[0x46] = self.MOV
        self.dispatch[0x47] = self.MOV
        self.dispatch[0x48] = self.MOV
        self.dispatch[0x49] = self.MOV
        self.dispatch[0x4a] = self.MOV

        self.dispatch[0x50] = self.MOV
        self.dispatch[0x51] = self.MOV
        self.dispatch[0x52] = self.MOV
        self.dispatch[0x53] = self.MOV
        self.dispatch[0x54] = self.MOV
        self.dispatch[0x55] = self.MOV
        self.dispatch[0x56] = self.MOV
        self.dispatch[0x57] = self.MOV

        self.dispatch[0x58] = self.MOV
        self.dispatch[0x59] = self.MOV
        self.dispatch[0x5a] = self.MOV
        self.dispatch[0x5b] = self.MOV
        self.dispatch[0x5c] = self.MOV
        self.dispatch[0x5d] = self.MOV
        self.dispatch[0x5e] = self.MOV
        self.dispatch[0x5f] = self.MOV

        self.dispatch[0x60] = self.MOV
        self.dispatch[0x61] = self.MOV
        self.dispatch[0x62] = self.MOV
        self.dispatch[0x63] = self.MOV
        self.dispatch[0x64] = self.MOV
        self.dispatch[0x65] = self.MOV
        self.dispatch[0x66] = self.MOV
        self.dispatch[0x67] = self.MOV

        self.dispatch[0x68] = self.MOV
        self.dispatch[0x69] = self.MOV
        self.dispatch[0x6a] = self.MOV
        self.dispatch[0x6b] = self.MOV
        self.dispatch[0x6c] = self.MOV
        self.dispatch[0x6d] = self.MOV
        self.dispatch[0x6e] = self.MOV
        self.dispatch[0x6f] = self.MOV

        self.dispatch[0x70] = self.MOV
        self.dispatch[0x71] = self.MOV
        self.dispatch[0x72] = self.MOV
        self.dispatch[0x73] = self.MOV
        self.dispatch[0x74] = self.MOV
        self.dispatch[0x75] = self.MOV
        self.dispatch[0x76] = self.HLT
        self.dispatch[0x77] = self.MOV

        self.dispatch[0x78] = self.MOV
        self.dispatch[0x79] = self.MOV
        self.dispatch[0x7a] = self.MOV
        self.dispatch[0x7b] = self.MOV
        self.dispatch[0x7c] = self.MOV
        self.dispatch[0x7d] = self.MOV
        self.dispatch[0x7e] = self.MOV
        self.dispatch[0x7f] = self.MOV

        self.dispatch[0x80] = self.ADD
        self.dispatch[0x81] = self.ADD
        self.dispatch[0x82] = self.ADD
        self.dispatch[0x83] = self.ADD
        self.dispatch[0x84] = self.ADD
        self.dispatch[0x85] = self.ADD
        self.dispatch[0x86] = self.ADD
        self.dispatch[0x87] = self.ADD

        self.dispatch[0x88] = self.ADC
        self.dispatch[0x89] = self.ADC
        self.dispatch[0x8a] = self.ADC
        self.dispatch[0x8b] = self.ADC
        self.dispatch[0x8c] = self.ADC
        self.dispatch[0x8d] = self.ADC
        self.dispatch[0x8e] = self.ADC
        self.dispatch[0x8f] = self.ADC

        self.dispatch[0x90] = self.SUB
        self.dispatch[0x91] = self.SUB
        self.dispatch[0x92] = self.SUB
        self.dispatch[0x93] = self.SUB
        self.dispatch[0x94] = self.SUB
        self.dispatch[0x95] = self.SUB
        self.dispatch[0x96] = self.SUB
        self.dispatch[0x97] = self.SUB

        self.dispatch[0x98] = self.SBB
        self.dispatch[0x99] = self.SBB
        self.dispatch[0x9a] = self.SBB
        self.dispatch[0x9b] = self.SBB
        self.dispatch[0x9c] = self.SBB
        self.dispatch[0x9d] = self.SBB
        self.dispatch[0x9e] = self.SBB
        self.dispatch[0x9f] = self.SBB

        self.dispatch[0xa0] = self.ANA
        self.dispatch[0xa1] = self.ANA
        self.dispatch[0xa2] = self.ANA
        self.dispatch[0xa3] = self.ANA
        self.dispatch[0xa4] = self.ANA
        self.dispatch[0xa5] = self.ANA

    def load(self, addr, arr):
        for idx, data in enumerate(arr):
            self.mem[addr + idx] = data
    
    def exec(self):
        while not self.halt:
            self.ir = self.fetch()
            #self.__conds.update()
            self.dispatch[self.ir]()
    
    def reset(self):
        self.alu.reset()
        self.pc = 0x0000
        self.sp = 0x8000
        self.halt = False
    
    def get_flag(self, flag):
        return bool(self.flags & flag)

    # register pairs
    def get_BC(self):
        """ Get register pair BC """
        return 256 * self.regs[CPU.B] + self.regs[CPU.C]
    
    def get_DE(self):
        """ Get register pair DE """
        return 256 * self.regs[CPU.D] + self.regs[CPU.E]
    
    def get_HL(self):
        """ Get register pair HL """
        return 256 * self.regs[CPU.H] + self.regs[CPU.L]
    
    def get_pair(self, rp):
        return 256 * self.regs[rp] + self.regs[rp + 1]
    
    def set_pair(self, rp, data_16):
        self.regs[rp] = data_16 // 256
        self.regs[rp + 1] = data_16 % 256
    
    def __get_rp(self):
        return self.get_pair(self.__rp())
    
    def __set_rp(self, data_16):
        self.set_pair(self.__rp(), data_16)
    
    def set_BC(self, data_16):
        """ Set register pair BC """
        self.set_pair(CPU.B, data_16)
    
    def set_DE(self, data_16):
        """ Set register pair DE """
        self.regs[CPU.D] = data_16 // 256
        self.regs[CPU.E] = data_16 % 256
    
    def set_HL(self, data_16):
        """ Set register pair HL """
        self.regs[CPU.H] = data_16 // 256
        self.regs[CPU.L] = data_16 % 256

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
    
    def store_M(self, data):
        self.store(self.get_HL(), data)

    def __update_conds(self):
        self.conds[0] =  not self.get_flag(CPU.CY)
        self.conds[1] =      self.get_flag(CPU.CY)
        self.conds[2] =  not self.get_flag(CPU.Z)
        self.conds[3] =      self.get_flag(CPU.Z)
        self.conds[4] =  not self.get_flag(CPU.S)
        self.conds[5] =      self.get_flag(CPU.S)
        self.conds[6] =  not self.get_flag(CPU.P)
        self.conds[7] =      self.get_flag(CPU.P)
    
    def __rs(self):
        """ decode source register index """
        return self.ir & 0x07

    def __rd(self):
        """ decode destination register index """
        return (self.ir & 0x38) >> 3
    
    def __rp(self):
        return (self.ir & 0x03) >> 4
    
    def __get_rs(self):
        if self.__rs() == CPU.M:
            return self.read_M()
        else:
            return self.regs[self.__rs()]
    
    def __get_rd(self):
        if self.__rd() == CPU.M:
            return self.read_M()
        else:
            return self.regs[self.__rd()]
    
    def __set_rd(self, data):
        if self.__rd() == CPU.M:
            self.store_M(data)
        else:
            self.regs[self.__rd()] = data

    def __cc(self):
        """ decode condition code """
        return (self.ir & 0x38) >> 3
    
    def __nn(self):
        """ decode n """
        return (self.ir & 0x38) >> 3
    
    def MOV(self):
        self.__set_rd(self.__get_rs())
    
    def MVI(self):
        """ Move immediate register """
        self.__set_rd(self.fetch())
    
    def LXI(self):
        """ Load register pair immediate """
        pass

    def LXI_BC(self):
        """ Load register pair BC immediate """
        self.set_BC(self.fetch_16())
    
    def LXI_DE(self):
        """ Load register pair DE immediate """
        self.set_DE(self.fetch_16())
    
    def LXI_HL(self):
        """ Load register pair HL immediate """
        self.__set_HL(self.fetch_16())
    
    def LXI_SP(self):
        """ Load stack pointer immediate """
        self.sp = self.fetch_16()
    
    def LDA(self):
        """ Load accumulator direct """
        self.alu.ACC = self.read(self.fetch_16())
    
    def STA(self):
        """ Store Accumulator direct """
        self.store(self.fetch_16(), self.regs[A])
    
    def LHLD(self):
        """ Load L and H direct """
        self.set_HL(self.read_16(
            self.fetch_16()
        ))
    
    def SHLD(self):
        """ Store H and L direct """
        self.store_16(self.fetch_16(), self.get_HL())
    
    def LDAX(self):
        """
        Load accumulator indirect
        BC or DE
        """
        self.regs[CPU.A] = self.read(self.__get_rp())
    
    def STAX(self):
        """ Store accumulator indirect """
        pass
    
    def STAX_BC(self):
        """ Store accumulator indirect BC """
        self.store(self.get_BC(), self.regs[A])
    
    def STAX_DE(self):
        """ Store accumulator indirect DE """
        self.store(self.get_DE(), self.regs[A])
    
    def XCHG(self):
        self.regs[H], self.regs[D] = self.regs[D], self.regs[H]
        self.regs[L], self.regs[E] = self.regs[E], self.regs[L]

    def __ADD(self, tmp):
        acc, flags = ADD(self.regs[CPU.A], tmp, 0)
        self.regs[CPU.A] = acc
        self.flags = flags

    def ADD(self):
        """ Add register """
        self.ALU(ADD, self.__get_rs())
    
    def ADI(self):
        """ Add immediate """
        self.__ADD(self.fetch())
    
    def ADC(self):
        acc, flags = ADC(self.acc, self.__get_rs(), self.flags)
        self.regs[CPU.A] = acc
        self.flags = flags
    
    def ACI(self):
        """ Add immediate with carry """
        self.alu.ADC(self.fetch())

    def __SUB(self, tmp):
        self.flags, self.acc = alu(
            SUB, self.acc, tmp
        )

    def SUB(self):
        """ Subtract register """
        self.__SUB(self.regs[self.__rs])
    
    def SUI(self):
        """ Subtract immediate """
        self.__SUB(self.fetch())
    
    def __SBB(self, tmp):
        self.flags, self.acc = alu(
            SBB, self.acc, tmp, self.cy()
        )

    def SBB(self):
        """ Subtract register with borrow """
        self.SBB(self.regs[self.__rs])

    def SBI(self):
        """ Subtract immediate with borrow """
        self.alu.SBB(self.fetch())
    
    def INR(self, tmp):
        acc, flags = INR(0, self.__get_rs(), self.flags)
        self.regs[CPU.A] = acc
        self.flags = flags
    
    def DCR(self):
        """ Decrement register """
        self.__set_rd((self.__get_rd() + 255) % 256)
    
    def INX(self, tmp_16):
        """ Increment register pair """
        tmp_16 = self.__get_rp()

        if self.__rp() == 4:
            tmp_16 = self.pc

        # ALU additions
        acc_lo, flags = ADD(tmp_16 % 256, 1, self.flags)
        acc_hi, flags = ADC(tmp_16 // 256, 0, flags)

        # update state
        self.flags = (flags & ALU.CY) | (self.flags & ~ALU.CY)
        self.__set_rp(256 * acc_hi + acc_lo)
    
    def DCX(self):
        """ Decrement register pair """
        tmp_lo, tmp_hi  = self.__get_rp() % 256, self.__get_rp() // 256

        acc_lo, flags   = SUB(tmp_lo, 1, self.flags)
        acc_hi, _       = SBB(tmp_hi, 0, flags)
        
        self.__set_rp(256 * acc_hi + acc_lo)
    
    def DAD(self, tmp_16):
        tmp_lo, tmp_hi          = self.__get_rp() % 256, self.__get_rp() // 256

        self.regs[CPU.L], flags = ADD(self.regs[CPU.L], tmp_lo, self.flags)
        self.regs[CPU.H], flags = ADC(self.regs[CPU.H], tmp_hi, flags)

        self.flags = (flags & CPU.CY) | (self.flags & ~CPU.CY)
    
    def DAA(self):
        """ Decimal adjust accumulator """
        pass
    
    def ANA(self):
        self.flags, self.acc = alu(ANA, self.acc, tmp)
    
    def ANI(self):
        """ And immediate """
        self.alu.ANA(self.fetch())
    
    def XRA(self):
        """ Exclusive OR register """
        self.alu.XRA(self.regs[self.__rs])

    def XRI(self):
        """ Exclusive OR immediate """
        self.__alu_xra(self.fetch())
    
    def ORA(self):
        """ OR register """
        self.alu.ORA(self.regs[self.__rs])
    
    def ORI(self):
        """ OR immediate """
        self.__alu_or(self.fetch())
    
    def __CMP(self, tmp):
        self.flags, _ = alu(SUB, self.acc, tmp)
    
    def CMP(self, r):
        """ Compare register """
        self.CMP(self.regs[r])
    
    def CPI(self):
        """ Compare immediate """
        self.alu.CMP(self.fetch())
    
    def RLC(self):
        """ Rotate left """
        self.rega[A]
        self.alu.RLC()
    
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
        self.regs[CPU.A] = 255 - self.regs[CPU.A]
    
    def CMC(self):
        """ Complement carry """
        self.flags ^= CPU.CY
    
    def STC(self):
        """ Set carry """
        self.flags |= CPU.CY
    
    def JMP(self):
        """ Jump """
        self.pc = self.fetch_16()

    def CALL(self):
        """ Unconditional call """
        self.push_16(self.pc)
        self.pc = self.fetch_16()
    
    def JCC(self):
        """ Conditional jump """
        if self.conds[self.__cc()]:
            self.JMP()
    
    def CCC(self):
        """ Condition call """
        if self.conds[self.__cc()]:
            self.CALL()
    
    def RET(self):
        """ Return """
        self.pc = self.pop_16()
    
    def RCC(self):
        """ Conditional return """
        if self.conds[self.__cc()]:
            self.RET()
    
    def RST(self):
        """ Restart """
        self.push_16(self.pc)
        self.pc = 8 * self.__NN
    
    def PCHL(self):
        """ Jump H and L indirect """
        self.pc = self.get_HL()
    
    def PUSH(self):
        """ Push """
        self.push_16(
            self.__get_rp()
        )
    
    def PUSH_BC(self):
        """ Push register pair BC """
        self.push_16(self.get_BC())
    
    def PUSH_DE(self):
        """ Push register pair DE """
        self.push_16(self.get_DE())
    
    def PUSH_HL(self):
        """ Push register pair HL """
        self.push_16(self.get_HL())
    
    def PUSH_PSW(self):
        """ Push processor status word """
        self.push_16(
            self.alu.PSW()
        )

    def POP(self):
        """ Pop """
        pass
    
    def POP_BC(self):
        """ Pop register pair BC """
        self.set_BC(self.pop_16())
    
    def POP_DE(self):
        """ Pop register pair DE """
        self.set_DE(self.pop_16())
    
    def POP_HL(self):
        """ Pop register pair HL """
        pass
    
    def POP_PSW(self):
        """ Pop processor status word """
        self.set_psw(
            self.pop_16()
        )
    
    def XTHL(self):
        """ Exchange stack top with H and L """
        data_16 = self.pop_16()
        self.push_16(self.get_HL())
        self.set_HL(data_16)
    
    def SPHL(self):
        """ Move HL to SP """
        pass
    
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
