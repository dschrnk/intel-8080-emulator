from .cpu import *

class VM:

    def __init__(self):
        self.cpu = CPU()
        
        self.optable = [self.NOP] * 256

        self.__init_optable()
    
    def run(self):
        while not self.cpu.halt:
            
            opc = self.cpu.fetch()

            self.cpu.ir = opc
            
            ins = self.optable[opc]
            
            ins(self.cpu)
    
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

        self.optable[0xc1] = self.RCC
        self.optable[0xc2] = self.POP
        self.optable[0xc3] = self.JMP
        self.optable[0xc4] = self.CCC
        self.optable[0xc5] = self.PUSH
        self.optable[0xc6] = self.ADI
        self.optable[0xc7] = self.RST
        self.optable[0xc8] = self.RCC
        
        self.optable[0xc9] = self.RET
        self.optable[0xca] = self.JCC
        self.optable[0xcb] = self.JMP
        self.optable[0xcc] = self.CCC


    def MOV(self, cpu):
        """
        Move Register

        (r1) <- (r2)

        The content of register r2 is moved to register r1. 

        """
        cpu.dst = cpu.src
    
    def MVI(self, cpu):
        """ Move immediate register """
        cpu.dst = cpu.fetch()
    
    def LXI(self, cpu):
        """ Load register pair immediate """
        cpu.rp = cpu.fetch_16()
    
    def LDA(self, cpu):
        """ Load accumulator direct """
        cpu.A = cpu.read(cpu.fetch_16())
    
    def STA(self, cpu):
        """ Store Accumulator direct """
        cpu.write(cpu.fetch_16(), cpu.A)
    
    def LHLD(self, cpu):
        """ Load L and H direct """
        cpu.HL = cpu.read_16(
            cpu.fetch_16()
        )
    
    def SHLD(self, cpu):
        """ 
        Store H and L direct 
        """
        cpu.write_16(cpu.fetch_16(), cpu.HL)
    
    def LDAX(self, cpu):
        """
        Load accumulator indirect
        BC or DE
        """
        cpu.A = cpu.read(cpu.rp)
    
    def STAX(self, cpu):
        """ Store accumulator indirect """
        cpu.write(cpu.rp, cpu.A)
    
    def XCHG(self, cpu):
        """
        Exchange H and L with D and E

        The contents of registers H and L are exchanged with 
        the contents of registers D and E.

        """
        cpu.HL, cpu.DE = cpu.DE, cpu.HL

    def ADD(self, cpu):
        """ 
        Add register 

        (A) <- (A) + (r) 
        
        The content of register r is added to the content of the 
        accumulator. The result is placed in the accumulator.

        """
        cpu.A, cpu.flags = cpu.alu.ADD(cpu.A, cpu.src, 0)
    
    def ADI(self, cpu):
        """ 
        Add immediate 
        
        (A) <- (A) + (byte 2) 

        The content of the second byte of the instruction is 
        added to the content of the accumulator. The result 
        is placed in the accumulator. 

        """
        cpu.A, cpu.flags = cpu.alu.ADD(cpu.A, cpu.fetch(), 0)
    
    def ADC(self, cpu):
        """
        Add register with carry

        (A) <- (A) + (r) + (CY) 

        The content of register r and the content of the carry 
        bit are added to the content of the accumulator. The 
        result is placed in the accumulator. 

        """
        cpu.A, cpu.flags = cpu.alu.ADC(cpu.A, cpu.src, cpu.CY)
    
    def ACI(self, cpu):
        """ 
        Add immediate with carry 

        (A) <- (A) + (byte 2) + (CY) 
        
        The content of the second byte of the instruction and 
        the content of the CY flag are added to the contents 
        of the accumulator. The result is placed in the 
        accumulator. 
        
        """
        cpu.A, cpu.flags = cpu.alu.ADC(cpu.A, cpu.fetch(), cpu.CY)

    def SUB(self, cpu):
        """ 
        Subtract register 

        (A) <- (A) - (r) 
        
        The content of register r is subtracted from the con
        tent of the accumulator. The result is placed in the 
        accumulator. 
        
        """
        cpu.A, cpu.flags = cpu.alu.SUB(cpu.A, cpu.src, 0)
    
    def SUI(self, cpu):
        """ 
        Subtract immediate 
        
        (A) <- (A) - (byte 2) 
        
        The content of the second byte of the instruction is 
        subtracted from the content of the accumulator. The 
        result is placed in the accumulator. 
        
        """
        cpu.A, cpu.flags = cpu.alu.SUB(cpu.A, cpu.fetch(), 0)

    def SBB(self, cpu):
        """ Subtract register with borrow """
        cpu.A, cpu.flags = cpu.alu.SBB(cpu.A, cpu.src, cpu.CY)

    def SBI(self, cpu):
        """ Subtract immediate with borrow """
        cpu.A, cpu.flags = cpu.alu.SBB(cpu.A, cpu.fetch(), cpu.CY)
    
    def INR(self, cpu):
        """ 
        Increment register 

        (r) <- (r) + 1
        
        The content of register r is incremented by one. 
        Note: All condition flags except CY are affected.
        
        """
        cpu.dst, cpu.flags = cpu.alu.INR(cpu.dst, 0)
    
    def DCR(self, cpu):
        """ 
        Decrement register 
        
        (r) <- (r) - 1

        The content of register r is decremented by one. 
        Note: All condition flags except CY are affected. 
        
        """
        cpu.dst, cpu.flags = cpu.alu.DCR(0, cpu.dst, cpu.flags)
    
    def INX(self, cpu, tmp_16):
        """ 
        Increment register pair 

        (rh) (rl) <- (rh) (rl) + 1
        
        the content of the register pair rp is incremented by 
        one. Note: No condition ftags are affected.  
        
        """
        cpu.rl, flags = cpu.alu.ADD(cpu.rl, 1, 0)
        cpu.rh, _     = cpu.alu.ADC(cpu.rh, 0, flags & CY)
    
    def DCX(self, cpu):
        """ Decrement register pair """
        tmp_lo, tmp_hi  = cpu.rp % 256, cpu.rp // 256

        acc_lo, flags   = cpu.alu.SUB(tmp_lo, 1, cpu.flags)
        acc_hi, flags   = cpu.alu.SBB(tmp_hi, 0, flags)
        
        cpu.__set_RP(256 * acc_hi + acc_lo)
    
    def DAD(self, cpu, tmp_16):
        cpu.L, flags = cpu.alu.ADD(cpu.L, cpu.rl, 0)
        cpu.H, flags = cpu.alu.ADC(cpu.H, cpu.rh, flags)

        cpu.flags = (flags & CY) | (cpu.flags & ~CY)
    
    def DAA(self, cpu):
        """ Decimal adjust accumulator """
        pass
    
    def ANA(self, cpu):
        cpu.A, cpu.flags = cpu.alu.ANA(cpu.A, cpu.src, 0)
    
    def ANI(self, cpu):
        """ And immediate """
        cpu.A, cpu.flags = cpu.alu.ANA(cpu.A, cpu.fetch(), 0)
    
    def XRA(self, cpu):
        """ Exclusive OR register """
        cpu.A, cpu.flags = cpu.alu.XRA(cpu.A, cpu.src, 0)

    def XRI(self, cpu):
        """ Exclusive OR immediate """
        cpu.A, cpu.flags = cpu.alu.XRA(cpu.A, cpu.fetch(), 0)
    
    def ORA(self, cpu):
        """ OR register """
        cpu.A, cpu.flags = cpu.alu.ORA(cpu.A, cpu.src, 0)
    
    def ORI(self, cpu):
        """ OR immediate """
        cpu.A, cpu.flags = cpu.alu.ORA(cpu.A, cpu.fetch(), 0)
    
    def CMP(self, cpu):
        """ Compare register """
        _, cpu.flags = cpu.alu.SUB(cpu.A, cpu.src, 0)
    
    def CPI(self, cpu):
        """ Compare immediate """
        _, cpu.flags = cpu.alu.SUB(cpu.A, cpu.fetch(), 0)
    
    def RLC(self, cpu):
        """ Rotate left """
        cpu.A, cpu.flags = cpu.alu.RRC(cpu.A, 0, cpu.CY)
    
    def RRC(self, cpu):
        """ Rotate right """
        cpu.A, cpu.flags = cpu.alu.RRC(cpu.A, 0, cpu.CY)
    
    def RAL(self, cpu):
        """ Rotate left through carry """
        cpu.A, cpu.flags = cpu.alu.RAL(cpu.A, 0, cpu.CY)
    
    def RAR(self, cpu):
        """ Rotate right through carry """
        cpu.A, cpu.flags = cpu.alu.RAR(cpu.A, 0, cpu.CY)
    
    def CMA(self, cpu):
        """ Complement accumulator """
        cpu.A = 255 - cpu.A
    
    def CMC(self, cpu):
        """ Complement carry """
        cpu.flags ^= CY
    
    def STC(self, cpu):
        """ Set carry """
        cpu.CY = 1
    
    def JMP(self, cpu):
        """ Jump """
        cpu.pc = cpu.fetch_16()

    def CALL(self, cpu):
        """ Unconditional call """
        cpu.push_16(cpu.pc)
        cpu.pc = cpu.fetch_16()
    
    def JCC(self, cpu):
        """ Conditional jump """
        if cpu.cond():
            cpu.JMP()
    
    def CCC(self, cpu):
        """ Condition call """
        if cpu.cond():
            cpu.CALL()
    
    def RET(self, cpu):
        """ Return """
        cpu.pc = cpu.pop_16()
    
    def RCC(self, cpu):
        """ Conditional return """
        if cpu.cond():
            self.RET()
    
    def RST(self, cpu):
        """ Restart """
        cpu.push_16(cpu.pc)
        cpu.pc = 8 * cpu.__NNN()
    
    def PCHL(self, cpu):
        """ Jump H and L indirect """
        cpu.pc = cpu.HL
    
    def PUSH(self, cpu):
        """ 
        Push 

        ((SP) - 1) <- rh
        ...
        
        The content of the high-order register of register pair 
        rp is moved to the memory location whose address is 
        one less than the content of register SP. The content 
        of the low-order register of register pair rp is moved 
        to the memory location whose address is two less 
        than the content of register SP. The content of reg
        ister SP is decremented by 2. Note: Register pair 
        rp = SP may not be specified. 
        
        """
        if cpu.ir == 0xf5:          # PUSH PSW
            cpu.push_16(cpu.PSW)
        else:
            cpu.push_16(cpu.rp)

    def POP(self, cpu):
        """ Pop """
        if cpu.ir == 0xf1:          # POP PSW
            cpu.PSW = data_16
        else:
            cpu.rp = data_16
    
    def XTHL(self, cpu):
        """ Exchange stack top with H and L """
        data_16 = cpu.pop_16()
        cpu.push_16(cpu.HL)
        cpu.HL = data_16
    
    def SPHL(self, cpu):
        """ Move HL to SP """
        cpu.sp = cpu.HL
    
    def IN(self, cpu):
        """ Input """
        pass
    
    def OUT(self, cpu):
        """ Output """
        pass
    
    def EI(self, cpu):
        """ Enable interrupts """
        pass
    
    def DI(self, cpu):
        """ Disable interrupts """
        pass
    
    def HLT(self, cpu):
        """ Halt """
        print("halt")
        cpu.halt = True
    
    def NOP(self, cpu):
        """ No op """
        print("nop")
        pass
