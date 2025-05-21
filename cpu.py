from alu import *

# Register pairs
BC =    0x0
DE =    0x1
HL =    0x2
SP =    0x3

KB = 1 << 10

# Flags
Z =     0x80
S =     0x40
AC =    0x10
P =     0x04
CY =    0x01

# Registers
B = 0
C = 1
D = 2
E = 3
H = 4
L = 5
W = 6
Z = 7

class CPU:

    def __init__(self):

        # program counter
        self.pc = 0x0000

        # stack pointer
        self.sp = 0x8000

        # 8-bit registers
        
        # instruction register
        self.ir = 0x00

        # A - L
        self.regs = [0x00] * 8

        self.alu = ALU()

        # flags register
        self.flags = [False] * 8
        self.flags[2] = True

        # Set by HLT instruction, terminates exec loop
        self.halt = False

        # memory
        self.mem = [0x00] * 64 * KB

        self.optable = [self.NOP] * 256
        self.__init_optable()

        self.cycles = 0

        self.__RS = 0
        self.__RD = 0
        self.__CC = 0
        self.__NN = 0

    def load(self, addr, arr):
        self.mem.load(addr, arr)
    
    def exec(self):
        while not self.halt:
            self.ir = self.fetch()
            self.__decode()
            #self.__conds.update()
            self.__exec()
    
    def __exec(self):
        self.optable[self.ir]()
    
    def reset(self):
        self.alu.reset()
        self.pc = 0x0000
        self.sp = 0x8000
        self.halt = False
    
    def get_BC(self):
        """ Get register pair BC """
        return 256 * self.regs[B] + self.regs[C]
    
    def get_DE(self):
        """ Get register pair DE """
        return 256 * self.regs[D] + self.regs[E]
    
    def get_HL(self):
        """ Get register pair HL """
        return 256 * self.regs[H] + self.regs[L]
    
    def set_BC(self, data_16):
        """ Set register pair BC """
        self.regs[B] = data_16 // 256
        self.regs[C] = data_16 % 256
    
    def set_DE(self, data_16):
        """ Set register pair DE """
        self.regs[D] = data_16 // 256
        self.regs[E] = data_16 % 256
    
    def set_HL(self, data_16):
        """ Set register pair HL """
        self.regs[H] = data_16 // 256
        self.regs[L] = data_16 % 256

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
    
    def __get_psw(self):
        return 256 * self.__get_a() + self.flags.get(ALL)
    
    def __set_psw(self, data):
        self.regs[A] = data // 256
        self.flags.reset()
        self.flags.set(data % 256)

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

    # ALU

    def __ADD(self, data):
        """ ALU add """
        cy, ac, res = alu.ADD(self.regs[A], data)
        self.regs[A] = res
        self.flags[CY] = cy
        self.flags[AC] = ac
        self.flags.update(cy, ac, res)
    
    def __ADC(self, data):
        """ ALU add with carry """
        self.__ADD(data + self.flags.get_CY())

    def __SUB(self, data):
        """ ALU subtract """
        self.__ADD(256 - data)
    
    def __SBB(self, data):
        """ ALU subtract with borrow """
        self.__SUB(data + self.flags.get_CY)
    
    def __AND(self, data):
        flags, res = alu.AND(self.regs[A], data)
        self.regs[A] = res
    
    def __XRA(self, data):
        """ ALU exclusive or """
        cy, ac, res = alu.XRA(self.regs[A], data)
        self.regs[A] = res
        self.flags.update(cy, ac, res)
    
    def __ORA(self, data):
        """ ALU or """
        cy, ac, res = alu.OR(self.regs[A], data)
        self.flags.update(cy, ac, res)
        self.regs[A] = res
    
    def __CMP(self, data):
        """ ALU compare """
        cy, ac, res = alu.SUB(self.regs[A], data)
        self.flags.update(cy, ac, res)
    
    def __INR(self):
        _, ac, res = alu.INR(self.__get_RD())
        self.regs[self.__SD] = res
    
    def __DCR(self, data):
        _, ac, res = alu.DCR(self.__get_RD())
        self.__set_RD(res)

    def read_M(self):
        return self.read(self.get_HL())
    
    def store_M(self, data):
        self.store(self.get_HL(), data)

    def __init_optable(self):
        self.optable[0x00] = self.NOP
        self.optable[0x01] = self.LXI_BC
        self.optable[0x02] = self.STAX_BC
        self.optable[0x03] = self.INX_BC
        self.optable[0x04] = self.INR_B
        self.optable[0x05] = self.DCR_B
        self.optable[0x06] = self.MVI_B
        self.optable[0x07] = self.RLC
        
        self.optable[0x09] = self.DAD_BC
        self.optable[0x0a] = self.LDAX_BC
        self.optable[0x0b] = self.DCX_BC
        self.optable[0x0c] = self.INR_C
        self.optable[0x0d] = self.DCR_C
        self.optable[0x0e] = self.MVI_C
        self.optable[0x0f] = self.RRC

        self.optable[0x11] = self.LXI_DE
        self.optable[0x12] = self.STAX_DE
        self.optable[0x13] = self.INX_DE
        self.optable[0x14] = self.INR_D
        self.optable[0x15] = self.DCR_D
        self.optable[0x16] = self.MVI_D
        self.optable[0x17] = self.RAL
        
        self.optable[0x19] = self.DAD_DE
        self.optable[0x1a] = self.LDAX_DE
        self.optable[0x1b] = self.DCX_DE
        self.optable[0x1c] = self.INR_E
        self.optable[0x1d] = self.DCR_E
        self.optable[0x1e] = self.MVI_E
        self.optable[0x1f] = self.RAR

        self.optable[0x21] = self.LXI_HL
        self.optable[0x22] = self.SHLD
        self.optable[0x23] = self.INX_HL
        self.optable[0x24] = self.INR_H
        self.optable[0x25] = self.DCR_H
        self.optable[0x26] = self.MVI_H
        self.optable[0x27] = self.DAA

        self.optable[0x29] = self.DAD_HL
        self.optable[0x2a] = self.LHLD
        self.optable[0x2b] = self.DCX_HL
        self.optable[0x2c] = self.INR_L
        self.optable[0x2d] = self.DCR_L
        self.optable[0x2e] = self.MVI_L
        self.optable[0x2f] = self.CMA

        self.optable[0x31] = self.LXI_SP
        self.optable[0x32] = self.STA
        self.optable[0x33] = self.INX_SP
        self.optable[0x34] = self.INR_M
        self.optable[0x35] = self.DCR_M
        self.optable[0x36] = self.MVI_M
        self.optable[0x37] = self.STC

        self.optable[0x39] = self.DAD_SP
        self.optable[0x3a] = self.LDA
        self.optable[0x3b] = self.DCX_SP
        self.optable[0x3c] = self.INR_A
        self.optable[0x3d] = self.DCR_A
        self.optable[0x3e] = self.MVI_A
        self.optable[0x3f] = self.CMC
        self.optable[0x40] = self.MOV_B_B
        self.optable[0x41] = self.MOV_B_C
        self.optable[0x42] = self.MOV_B_D
        self.optable[0x43] = self.MOV_B_E
        self.optable[0x44] = self.MOV_B_H
        self.optable[0x45] = self.MOV_B_L
        self.optable[0x46] = self.MOV_B_M
        self.optable[0x47] = self.MOV_B_A
        self.optable[0x48] = self.MOV_C_B
        self.optable[0x49] = self.MOV_C_C
        self.optable[0x4a] = self.MOV_C_D

        self.optable[0x50] = self.MOV_D_B
        self.optable[0x51] = self.MOV_D_C
        self.optable[0x52] = self.MOV_D_D
        self.optable[0x53] = self.MOV_D_E
        self.optable[0x54] = self.MOV_D_H
        self.optable[0x55] = self.MOV_D_L
        self.optable[0x56] = self.MOV_D_M
        self.optable[0x57] = self.MOV_D_A

        self.optable[0x58] = self.MOV_E_B
        self.optable[0x59] = self.MOV_E_C
        self.optable[0x5a] = self.MOV_E_D
        self.optable[0x5b] = self.MOV_E_E
        self.optable[0x5c] = self.MOV_E_H
        self.optable[0x5d] = self.MOV_E_L
        self.optable[0x5e] = self.MOV_E_M
        self.optable[0x5f] = self.MOV_E_A

        self.optable[0x60] = self.MOV_H_B
        self.optable[0x61] = self.MOV_H_C
        self.optable[0x62] = self.MOV_H_D
        self.optable[0x63] = self.MOV_H_E
        self.optable[0x64] = self.MOV_H_H
        self.optable[0x65] = self.MOV_H_L
        self.optable[0x66] = self.MOV_H_M
        self.optable[0x67] = self.MOV_H_A

        self.optable[0x68] = self.MOV_L_B
        self.optable[0x69] = self.MOV_L_C
        self.optable[0x6a] = self.MOV_L_D
        self.optable[0x6b] = self.MOV_L_E
        self.optable[0x6c] = self.MOV_L_H
        self.optable[0x6d] = self.MOV_L_L
        self.optable[0x6e] = self.MOV_L_M
        self.optable[0x6f] = self.MOV_L_A

        self.optable[0x70] = self.MOV_M_B
        self.optable[0x71] = self.MOV_M_C
        self.optable[0x72] = self.MOV_M_D
        self.optable[0x73] = self.MOV_M_E
        self.optable[0x74] = self.MOV_M_H
        self.optable[0x75] = self.MOV_M_L
        self.optable[0x76] = self.HLT
        self.optable[0x77] = self.MOV_M_A

        self.optable[0x78] = self.MOV_A_B
        self.optable[0x79] = self.MOV_A_C
        self.optable[0x7a] = self.MOV_A_D
        self.optable[0x7b] = self.MOV_A_E
        self.optable[0x7c] = self.MOV_A_H
        self.optable[0x7d] = self.MOV_A_L
        self.optable[0x7e] = self.MOV_A_M
        self.optable[0x7f] = self.MOV_A_A

        self.optable[0x80] = self.ADD_B
        self.optable[0x81] = self.ADD_C
        self.optable[0x82] = self.ADD_D
        self.optable[0x83] = self.ADD_E
        self.optable[0x84] = self.ADD_H
        self.optable[0x85] = self.ADD_L
        self.optable[0x86] = self.ADD_M
        self.optable[0x87] = self.ADD_A

        self.optable[0x88] = self.ADC_B
        self.optable[0x89] = self.ADC_C
        self.optable[0x8a] = self.ADC_D
        self.optable[0x8b] = self.ADC_E
        self.optable[0x8c] = self.ADC_H
        self.optable[0x8d] = self.ADC_L
        self.optable[0x8e] = self.ADC_M
        self.optable[0x8f] = self.ADC_A

        self.optable[0x90] = self.SUB_B
        self.optable[0x91] = self.SUB_C
        self.optable[0x92] = self.SUB_D
        self.optable[0x93] = self.SUB_E
        self.optable[0x94] = self.SUB_H
        self.optable[0x95] = self.SUB_L
        self.optable[0x96] = self.SUB_M
        self.optable[0x97] = self.SUB_A

        self.optable[0x98] = self.SBB_B
        self.optable[0x99] = self.SBB_C
        self.optable[0x9a] = self.SBB_D
        self.optable[0x9b] = self.SBB_E
        self.optable[0x9c] = self.SBB_H
        self.optable[0x9d] = self.SBB_L
        self.optable[0x9e] = self.SBB_M
        self.optable[0x9f] = self.SBB_A

        self.optable[0xa0] = self.ANA_B
        self.optable[0xa1] = self.ANA_C

    def __decode(self):
        self.__decode_RS()
        self.__decode_RD()
        self.__decode_CC()
        self.__decode_NN()
    
    def __decode_RS(self):
        """ decode source register index """
        self.__RS = self.ir & 0x07

    def __decode_RD(self):
        """ decode destination register index """
        self.__RD = (self.ir & 0x38) >> 3
    
    def __decode_CC(self):
        """ decode condition code """
        self.__CC = (self.ir & 0x38) >> 3
    
    def __decode_NN(self):
        """ decode n """
        self.__NN = (self.ir & 0x38) >> 3

    def __MOV_r1_r2(self):
        """ Move register """
        self.regs[self.__RD] = self.regs[self.__RS]
    
    def MOV_B_B(self):
        """ Move register B to B """
        self.__MOV_r1_r2()

    def MOV_B_C(self):
        """ Move register B to C """
        self.__MOV_r1_r2()

    def MOV_B_D(self):
        """ Move register B to D """
        self.__MOV_r1_r2()

    def MOV_B_E(self):
        """ Move register B to E """
        self.__MOV_r1_r2()

    def MOV_B_H(self):
        """ Move register B to H """
        self.__MOV_r1_r2()

    def MOV_B_L(self):
        """ Move register B to L """
        self.__MOV_r1_r2()

    def MOV_B_M(self):
        """ Move memory (at HL) to B """
        pass

    def MOV_B_A(self):
        """ Move register A to B """
        self.__MOV_r1_r2()

    def MOV_C_B(self):
        """ Move register B to C """
        self.__MOV_r1_r2()

    def MOV_C_C(self):
        """ Move register C to C """
        self.__MOV_r1_r2()

    def MOV_C_D(self):
        """ Move register D to C """
        self.__MOV_r1_r2()

    def MOV_C_E(self):
        """ Move register E to C """
        self.__MOV_r1_r2()

    def MOV_C_H(self):
        """ Move register H to C """
        self.__MOV_r1_r2()

    def MOV_C_L(self):
        """ Move register L to C """
        self.__MOV_r1_r2()

    def MOV_C_M(self):
        """ Move memory (at HL) to C """
        pass

    def MOV_C_A(self):
        """ Move register A to C """
        self.__MOV_r1_r2()

    def MOV_D_B(self):
        """ Move register B to D """
        self.__MOV_r1_r2()

    def MOV_D_C(self):
        """ Move register C to D """
        self.__MOV_r1_r2()

    def MOV_D_D(self):
        """ Move register D to D """
        self.__MOV_r1_r2()

    def MOV_D_E(self):
        """ Move register E to D """
        self.__MOV_r1_r2()

    def MOV_D_H(self):
        """ Move register H to D """
        self.__MOV_r1_r2()

    def MOV_D_L(self):
        """ Move register L to D """
        self.__MOV_r1_r2()

    def MOV_D_M(self):
        """ Move memory (at HL) to D """
        pass

    def MOV_D_A(self):
        """ Move register A to D """
        pass

    def MOV_E_B(self):
        """ Move register B to E """
        pass

    def MOV_E_C(self):
        """ Move register C to E """
        pass

    def MOV_E_D(self):
        """ Move register D to E """
        pass

    def MOV_E_E(self):
        """ Move register E to E """
        pass

    def MOV_E_H(self):
        """ Move register H to E """
        pass

    def MOV_E_L(self):
        """ Move register L to E """
        pass

    def MOV_E_M(self):
        """ Move memory (at HL) to E """
        pass

    def MOV_E_A(self):
        """ Move register A to E """
        pass

    def MOV_H_B(self):
        """ Move register B to H """
        pass

    def MOV_H_C(self):
        """ Move register C to H """
        pass

    def MOV_H_D(self):
        """ Move register D to H """
        pass

    def MOV_H_E(self):
        """ Move register E to H """
        pass

    def MOV_H_H(self):
        """ Move register H to H """
        pass

    def MOV_H_L(self):
        """ Move register L to H """
        pass

    def MOV_H_A(self):
        """ Move register A to H """
        pass

    def MOV_L_B(self):
        """ Move register B to L """
        pass

    def MOV_L_C(self):
        """ Move register C to L """
        self.regs[L] = self.regs[C]

    def MOV_L_D(self):
        """ Move register D to L """
        pass

    def MOV_L_E(self):
        """ Move register E to L """
        pass

    def MOV_L_H(self):
        """ Move register H to L """
        pass

    def MOV_L_L(self):
        """ Move register L to L """
        pass

    def MOV_L_A(self):
        """ Move register A to L """
        pass
    
    def MOV_A_r(self):
        """ Move register r to A """
        self.alu.ACC = self.regs[self.__RS]

    def MOV_A_B(self):
        """ Move register B to A """
        self.alu.ACC = self.regs[B]

    def MOV_A_C(self):
        """ Move register C to A """
        self.MOV_A_r()

    def MOV_A_D(self):
        """ Move register D to A """
        self.MOV_A_r()

    def MOV_A_E(self):
        """ Move register E to A """
        pass

    def MOV_A_H(self):
        """ Move register H to A """
        pass

    def MOV_A_L(self):
        """ Move register L to A """
        pass

    def MOV_A_A(self):
        """ Move register A to A """
        pass
    
    def __MOV_r_M(self):
        """ Move memory """
        self.regs[self.__RD] = self.read_M()
    
    def MOV_B_M(self):
        """ Move memory B """
        pass
    
    def MOV_C_M(self):
        """ Move memory C """
        pass
    
    def MOV_D_M(self):
        """ Move memory D """
        pass
    
    def MOV_E_M(self):
        """ Move memory E """
        pass
    
    def MOV_H_M(self):
        """ Move memory H """
        pass
    
    def MOV_L_M(self):
        """ Move memory L """
        pass
    
    def MOV_A_M(self):
        """ Move memory A """
        pass
    
    def __MOV_M_r(self):
        """ Move register to memory """
        self.store_M(self.regs[self.__RS])
    
    def MOV_M_B(self):
        """ Move register B to memory """
        self.__MOV_M_r()
    
    def MOV_M_C(self):
        """ Move register C to memory """
        pass
    
    def MOV_M_D(self):
        """ Move register D to memory """
        pass
    
    def MOV_M_E(self):
        """ Move register E to memory """
        pass
    
    def MOV_M_H(self):
        """ Move register H to memory """
        pass
    
    def MOV_M_L(self):
        """ Move register L to memory """
        pass
    
    def MOV_M_A(self):
        """ Move register A to memory """
        pass
    
    def __MVI_r(self):
        """ Move immediate register """
        self.regs[self.__RD] = self.fetch()

    def MVI_B(self):
        """ Move immediate register B """
        self.__MVI_r()
    
    def MVI_C(self):
        """ Move immediate register C """
        self.__MVI_r()
    
    def MVI_D(self):
        """ Move immediate register D """
        self.__MVI_r()
    
    def MVI_E(self):
        """ Move immediate register E """
        self.__MVI_r()
    
    def MVI_H(self):
        """ Move immediate register H """
        self.__MVI_r()
    
    def MVI_L(self):
        """ Move immediate register L """
        self.__MVI_r()

    def MVI_A(self):
        """ Move immediate register A """
        self.__MVI_r()

    def MVI_M(self):
        """ Move immediate memory """
        self.store_M(self.fetch())
    
    def LXI_rp_data_16(self):
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
        """ Store H and L direct """
        self.store_16(self.fetch_16(), self.get_HL())
    
    def __LDAX_rp(self):
        """ Load accumulator indirect """
        pass
    
    def LDAX_BC(self):
        """ Load accumulator indirect BC """
        self.regs[A] = self.read(self.get_BC())
    
    def LDAX_DE(self):
        """ Load accumulator indirect DE """
        self.regs[A] = self.read(self.get_DE())
    
    def __STAX_rp(self):
        """ Store accumulator indirect """
        pass
    
    def STAX_BC(self):
        """ Store accumulator indirect BC """
        self.store(self.get_BC(), self.regs[A])
    
    def STAX_DE(self):
        """ Store accumulator indirect DE """
        self.store(self.get_DE(), self.regs[A])
    
    def XCHG(self):
        pass

    def __ADD_r(self):
        """ Add register """
        self.alu.TMP = self.regs[self.__RS]
        self.alu.ADD()
    
    def ADD_B(self):
        """ Add register B """
        self.alu.ADD(self.regs[B])
    
    def ADD_C(self):
        """ Add register C """
        self.alu.TMP = self.regs[B]
        self.alu.ADD()

    def ADD_D(self):
        """ Add register D """
        self.__ADD_r()
    
    def ADD_E(self):
        """ Add register E """
        pass
    
    def ADD_H(self):
        """ Add register H """
        pass
    
    def ADD_L(self):
        """ Add register L """
        pass
    
    def ADD_M(self):
        """ Add memory """
        self.alu.TMP = self.read_M()
        self.alu.ADD()
    
    def ADD_A(self):
        """ Add register A """
        pass
    
    def ADI(self):
        """ Add immediate """
        self.alu.TMP = self.fetch()
        self.alu.ADD()
    
    def __ADC_r(self):
        """ Add register with carry """
        self.alu.TMP = self.regs[self.__RS]
        self.alu.ADC()
    
    def ADC_B(self):
        """ Add register B with carry """
        self.alu.ADC(self.regs[B])
    
    def ADC_C(self):
        """ Add register C with carry """
        self.__ADC_r()
    
    def ADC_D(self):
        """ Add register D with carry """
        self.__ADC_r()
    
    def ADC_E(self):
        """ Add register E with carry """
        self.__ADC_r()
    
    def ADC_H(self):
        """ Add register H with carry """
        self.__ADC_r()
    
    def ADC_L(self):
        """ Add register L with carry """
        pass
    
    def ADC_A(self):
        """ Add register A with carry """
        self.__ADC(self.regs[A])
    
    def ADC_M(self):
        """ Add memory with carry """
        self.__ADC(self.read_M())
    
    def ACI_data(self):
        """ Add immediate with carry """
        self.__ADD(self.fetch() + self.__conds[3])
    
    def __SUB(self, data):
        self.__ADD(256 - data)

    def __SUB_r(self):
        """ Subtract register """
        self.__SUB(self.regs[self.__RS])
    
    def SUB_B(self):
        """ Subtract register B """
        self.__SUB_r()
    
    def SUB_C(self):
        """ Subtract register C """
        self.__SUB_r()
    
    def SUB_D(self):
        pass
    
    def SUB_E(self):
        pass
    
    def SUB_H(self):
        pass
    
    def SUB_L(self):
        pass
    
    def SUB_M(self):
        """ Subtract memory """
        self.__SUB(self.read_M())
    
    def SUB_A(self):
        pass
    
    def SUI_data(self):
        """ Subtract immediate """
        self.__SUB(self.fetch())
    
    def __SBB(self, data):
        self.__SUB(data + self.__conds.get(3))

    def __SBB_r(self):
        """ Subtract register with borrow """
        self.__SBB(self.regs[self.__RS])
    
    def SBB_B(self):
        pass
    
    def SBB_C(self):
        pass
    
    def SBB_D(self):
        pass

    def SBB_E(self):
        pass
    
    def SBB_H(self):
        pass
    
    def SBB_L(self):
        pass
    
    def SBB_M(self):
        """ Subtract memory with borrow """
        self.__SBB(self.read_M())
    
    def SBB_A(self):
        pass

    def SBI_data(self):
        """ Subtract immediate with borrow """
        self.__SBB(self.fetch())
    
    def __INR_r(self):
        """ Increment register """
        self.alu.TMP = self.regs[self.__RD]
        self.alu.INR()
        self.regs[self.__RD] = self.alu.data
    
    def INR_B(self):
        """ Increment register B """
        self.__INR_r()
    
    def INR_C(self):
        """ Increment register C """
        self.__INR_r()
    
    def INR_D(self):
        """ Increment register D """
        pass
    
    def INR_E(self):
        """ Increment register E """
        self.__INR_r()
    
    def INR_H(self):
        """ Increment register H """
        self.__INR_r()
    
    def INR_L(self):
        self.__INR_r()
    
    def INR_M(self):
        """ Increment memory """
        self.alu.TMP = self.read_M()
        self.store_M(self.alu.INR())
    
    def INR_A(self):
        """ Increment register A """
        self.alu.TMP = self.alu.ACC
        self.alu.ACC = self.alu.INR()
    
    def __DCR_r(self):
        """ Decrement register """
        self.alu.TMP = self.regs[self.__RD]
        self.regs[self.__RD] = self.alu.DCR()
    
    def DCR_B(self):
        """ Decrement register B """
        pass
    
    def DCR_C(self):
        """ Decrement register C """
        pass
    
    def DCR_D(self):
        """ Decrement register D """
        pass
    
    def DCR_E(self):
        """ Decrement register E """
        self.__DCR_r()
    
    def DCR_H(self):
        """ Decrement register H """
        self.__DCR_r()
    
    def DCR_L(self):
        """ Decrement register L """
        self.__DCR_r()

    def DCR_M(self):
        """ Decrement memory """
        pass
    
    def DCR_A(self):
        """ Decrement register A """
        self.__DCR_r()
    
    def __INX_rp(self):
        """ Increment register pair """
        pass
    
    def INX_BC(self):
        """ Increment register pair BC """
        self.set_BC(
            (self.get_BC() + 1) % 65536
        )
    
    def INX_DE(self):
        """ Increment register pair DE """
        self.set_DE(
            (self.get_DE() + 1) % 65536
        )
    
    def INX_HL(self):
        """ Increment register pair HL """
        self.set_HL(
            (self.get_HL() + 1) % 65536
        )
    
    def INX_SP(self):
        """ Increment stack pointer """
        _, _, res_16 = alu.INX_16(self.sp)
        self.sp = res_16
        self.flags.update(res)
    
    def __DCX_rp(self):
        """ Decrement register pair """
        pass
    
    def DCX_BC(self):
        """ Decrement register pair BC """
        _, _, res_16 = alu.DCX_16(self.get_BC())
        self.set_BC(res_16)
    
    def DCX_DE(self):
        """ Decrement register pair DE """
        _, _, res_16 = alu.DCX_16(self.get_DE())
        self.set_DE(res_16)
    
    def DCX_HL(self):
        """ Decrement register pair HL """
        _, _, res_16 = alu.DCX_16(self.get_HL())
        self.set_HL(res_16)
    
    def DCX_SP(self):
        """ Decrement SP """
        _, _, res_16 = alu.DCX_16(self.sp)
        self.sp = res_16
    
    def __DAD_rp(self, data_16):
        cy, _, res_16 = alu.ADD_16(self.get_HL(), data_16)
        self.set_HL(res_16)

    def DAD_BC(self):
        """ Add register pair BC to HL """
        self.alu.set_CY(False)
        self.alu.ACT = self.regs[C]
        self.alu.TMP = self.regs[L]
        self.regs[L] = self.alu.DAD()
        self.alu.ACT = self.regs[B]
        self.alu.TMP = self.regs[H]
        self.regs[H] = self.alu.DAD()
    
    def DAD_DE(self):
        """ Add register pair DE to HL """
        self.__DAD_rp(self.get_DE())
    
    def DAD_HL(self):
        """ Add register pair HL to HL """
        self.__DAD_rp(self.get_HL())
    
    def DAD_SP(self):
        """ Add SP to HL """
        self.__DAD_rp(self.sp)
    
    def DAA(self):
        """ Decimal adjust accumulator """
        pass

    def __ANA_r(self):
        """ And register """
        self.alu.TMP = self.regs[self.__RS]
        self.alu.ANA()
    
    def ANA_B(self):
        """ And register B """
        self.__ANA_r()
    
    def ANA_C(self):
        """ And register C """
        self.__ANA_r()
    
    def ANA_D(self):
        """ And register D """
        pass
    
    def ANA_E(self):
        """ And register E """
        pass
    
    def ANA_H(self):
        """ And register H """
        pass
    
    def ANA_L(self):
        """ And register L """
        pass
    
    def ANA_A(self):
        """ And register A """
        pass

    def ANA_M(self):
        """ And memory """
        self.alu.ANA(self.read_M())
    
    def ANI_data(self):
        """ And immediate """
        self.__alu_and(self.fetch())
    
    def __XRA_r(self):
        """ Exclusive OR register """
        self.alu.XRA(self.regs[self.__RS])
    
    def XRA_B(self):
        """ Exclusive or register B """
        self.__XRA_r()
    
    def XRA_C(self):
        """ Exclusive or register C """
        pass
    
    def XRA_D(self):
        """ Exclusive or register D """
        pass

    def XRA_E(self):
        """ Exclusive or register E """
        pass
    
    def XRA_H(self):
        """ Exclusive or register H """
        pass
    
    def XRA_L(self):
        """ Exclusive or register L """
        pass
    
    def XRA_M(self):
        """ Exclusive OR memory """
        self.__alu_xra(self.read_M())
    
    def XRA_A(self):
        """ Exclusive or register A """
        pass

    def XRI_data(self):
        """ Exclusive OR immediate """
        self.__alu_xra(self.fetch())
    
    def __ORA_r(self):
        """ OR register """
        self.alu.ORA(self.regs[self.__RS])
    
    def ORA_B(self):
        """ Or register B """
        self.alu.ORA(self.regs[B])
    
    def ORA_M(self):
        """ OR memory """
        self.alu.ORA(self.read_M())
    
    def ORI_data(self):
        """ OR immediate """
        self.__alu_or(self.fetch())
    
    def __CMP_r(self):
        """ Compare register """
        self.alu.TMP = self.regs[self.__RS]
        self.alu.CMP()
    
    def CMP_B(self):
        """ Compare register B """
        self.__CMP_r()
    
    def CMP_C(self):
        """ Compare register C """
        self.__CMP_r()
    
    def CMP_D(self):
        """ Compare register D """
        self.__CMP_r()
    
    def CMP_E(self):
        """ Compare register E """
        pass
    
    def CMP_H(self):
        """ Compare register H """
        pass
    
    def CMP_L(self):
        """ Compare register L """
        pass
    
    def CMP_A(self):
        """ Compare register A """
        self.alu.TMP = self.alu.ACC
        self.alu.CMP()
    
    def CMP_M(self):
        """ Compare memory """
        self.alu.TMP = self.read_M()
        self.alu.CMP()
    
    def CPI(self):
        """ Compare immediate """
        self.alu.TMP = self.fetch()
        self.alu.CMP()
    
    def RLC(self):
        """ Rotate left """
        self.__set_a(
            (2 * self.__get(a)) % 256 + self.__get_a() // 256
        )
        self.__carry = (self.__get_a() << 7) % 256
    
    def RRC(self):
        """ Rotate right """
        pass
    
    def RAL(self):
        """ Rotate left through carry """
        pass
    
    def RAR(self):
        """ Rotate right through carry """
        pass
    
    def CMA(self):
        """ Complement accumulator """
        self.regs[A] = 255 - self.regs[A]
    
    def CMC(self):
        """ Complement carry """
        pass
    
    def STC(self):
        """ Set carry """
        self.flags.set_CY()
    
    def JMP(self):
        """ Jump """
        self.pc = self.fetch_16()

    def CALL(self):
        """ Unconditional call """
        self.push_16(self.pc)
        self.pc = self.fetch_16()
    
    def __Jcondition(self):
        """ Conditional jump """
        if self.__conds.get(self.__CC):
            self.JMP()
    
    def JC(self):
        """ Jump on carry """
        self.__Jcondition()
    
    def JNC(self):
        """ Jump on no carry """
        self.__Jcondition()
    
    def JZ(self):
        """ Jump on zero """
        self.__Jcondition()
    
    def JNZ(self):
        """ Jump on no zero """
        self.__Jcondition()
    
    def JP(self):
        """ Jump on positive """
        self.__Jcondition()
    
    def JM(self):
        """ Jump on minus """
        self.__Jcondition()
    
    def JPE(self):
        """ Jump on parity even """
        self.__Jcondition()
    
    def JPO(self):
        """ Jump on parity odd """
        self.__Jcondition()
    
    def __Ccondition(self):
        """ Condition call """
        if self.__conds.get(self.__CC):
            self.CALL()
    
    def CC(self):
        """ Call on carry """
        self.__Ccondition()
    
    def CNC(self):
        """ Call on no carry """
        self.__Ccondition()
    
    def CZ(self):
        """ Call on zero """
        self.__Ccondition()
    
    def CNZ(self):
        """ Call on no zero """
        self.__Ccondition()
    
    def CP(self):
        """ Call on positive """
        self.__Ccondition()
    
    def CM(self):
        """ Call on minus """
        self.__Ccondition()
    
    def CPE(self):
        """ Call on parity even """
        self.__Ccondition()
    
    def CPO(self):
        """ Call on parity odd """
        self.__Ccondition()
    
    def RET(self):
        """ Return """
        self.pc = self.pop_16()
    
    def __Rcondition(self):
        """ Conditional return """
        if self.__conds.get(self.__CC):
            self.RET()
    
    def RC(self):
        """ Return on carry """
        self.__Rcondition()
    
    def RNC(self):
        """ Return on no carry """
        self.__Rcondition()
    
    def RZ(self):
        """ Return on zero """
        self.__Rcondition()
    
    def RNZ(self):
        """ Return on no zero """
        self.__Rcondition()
    
    def RP(self):
        """ Return on positive """
        self.__Rcondition()
    
    def RM(self):
        """ Return on minus """
        self.__Rcondition()
    
    def RPE(self):
        """ Return on parity even """
        self.__Rcondition()
    
    def RPO(self):
        """ Return on parity odd """
        self.__Rcondition()
    
    def __RST_n(self):
        """ Restart """
        self.push_16(self.pc)
        self.pc = 8 * self.__NN
    
    def RST_0(self):
        """ Restart 0 """
        self.__RST_n()
    
    def RST_1(self):
        """ Restart 1 """
        self.__RST_n()
    
    def RST_2(self):
        """ Restart 2 """
        self.__RST_n()
    
    def RST_3(self):
        """ Restart 3 """
        self.__RST_n()
    
    def RST_4(self):
        """ Restart 4 """
        self.__RST_n()
    
    def RST_5(self):
        """ Restart 5 """
        self.__RST_n()
    
    def RST_6(self):
        """ Restart 6 """
        self.__RST_n()
    
    def RST_7(self):
        """ Restart 7 """
        self.__RST_n()
    
    def PCHL(self):
        """ Jump H and L indirect """
        self.pc = self.get_HL()
    
    def __PUSH_rp(self):
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
            self.get_psw()
        )

    def __POP_rp(self):
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
        pass
    
    def SPHL(self):
        """ Move HL to SP """
        pass
    
    def IN_port(self):
        """ Input """
        pass
    
    def OUT_port(self):
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
