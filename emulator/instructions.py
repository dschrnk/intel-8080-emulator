from .flags import *

def MOV(cpu, alu):
    """
    Move Register

    (r1) <- (r2)

    The content of register r2 is moved to register r1. 

    """
    cpu.dst = cpu.src

def MVI(cpu, alu):
    """ Move immediate register """
    cpu.dst = cpu.fetch()

def LXI(cpu, alu):
    """ Load register pair immediate """
    cpu.rp = cpu.fetch_16()

def LDA(cpu, alu):
    """ Load accumulator direct """
    cpu.A = cpu.read(cpu.fetch_16())

def STA(cpu, alu):
    """ Store Accumulator direct """
    cpu.write(cpu.fetch_16(), cpu.A)

def LHLD(cpu, alu):
    """ Load L and H direct """
    cpu.HL = cpu.read_16(cpu.fetch_16())

def SHLD(cpu, alu):
    """ 
    Store H and L direct 
    """
    cpu.write_16(cpu.fetch_16(), cpu.HL)

def LDAX(cpu, alu):
    """
    Load accumulator indirect
    BC or DE
    """
    cpu.A = cpu.read(cpu.rp)

def STAX(cpu, alu):
    """ Store accumulator indirect """
    cpu.write(cpu.rp, cpu.A)

def XCHG(cpu, alu):
    """
    Exchange H and L with D and E

    The contents of registers H and L are exchanged with 
    the contents of registers D and E.

    """
    cpu.HL, cpu.DE = cpu.DE, cpu.HL

def ADD(cpu, alu):
    """ 
    Add register 

    (A) <- (A) + (r) 
    
    The content of register r is added to the content of the 
    accumulator. The result is placed in the accumulator.

    """
    cpu.A, cpu.flags = alu.add(cpu.A, cpu.src)

def ADI(cpu, alu):
    """ 
    Add immediate 
    
    (A) <- (A) + (byte 2) 

    The content of the second byte of the instruction is 
    added to the content of the accumulator. The result 
    is placed in the accumulator. 

    """
    cpu.A, cpu.flags = alu.add(cpu.A, cpu.fetch())

def ADC(cpu, alu):
    """
    Add register with carry

    (A) <- (A) + (r) + (CY) 

    The content of register r and the content of the carry 
    bit are added to the content of the accumulator. The 
    result is placed in the accumulator. 

    """
    cpu.A, cpu.flags = alu.adc(cpu.A, cpu.src, cpu.CY)

def ACI(cpu, alu):
    """ 
    Add immediate with carry 

    (A) <- (A) + (byte 2) + (CY) 
    
    The content of the second byte of the instruction and 
    the content of the CY flag are added to the contents 
    of the accumulator. The result is placed in the 
    accumulator. 
    
    """
    cpu.A, cpu.flags = alu.ADC(cpu.A, cpu.fetch(), cpu.CY)

def SUB(cpu, alu):
    """ 
    Subtract register 

    (A) <- (A) - (r) 
    
    The content of register r is subtracted from the con
    tent of the accumulator. The result is placed in the 
    accumulator. 
    
    """
    cpu.A, cpu.flags = alu.sub(cpu.A, cpu.src)

def SUI(cpu, alu):
    """ 
    Subtract immediate 
    
    (A) <- (A) - (byte 2) 
    
    The content of the second byte of the instruction is 
    subtracted from the content of the accumulator. The 
    result is placed in the accumulator. 
    
    """
    cpu.A, cpu.flags = alu.sub(cpu.A, cpu.fetch())

def SBB(cpu, alu):
    """ Subtract register with borrow """
    cpu.A, cpu.flags = alu.sbb(cpu.A, cpu.src, cpu.CY)

def SBI(cpu, alu):
    """ Subtract immediate with borrow """
    cpu.A, cpu.flags = alu.sbb(cpu.A, cpu.fetch(), cpu.CY)

def INR(cpu, alu):
    """ 
    Increment register 

    (r) <- (r) + 1
    
    The content of register r is incremented by one. 
    Note: All condition flags except CY are affected.
    
    """
    cpu.dst, flags = alu.add(cpu.dst, 1)
    cpu.flags = (flags & ~CY) | (cpu.flags & CY)    # preserve cy

def DCR(cpu, alu):
    """ 
    Decrement register 
    
    (r) <- (r) - 1

    The content of register r is decremented by one. 
    Note: All condition flags except CY are affected. 
    
    """
    cpu.dst, flags = alu.sub(cpu.dst, 1)
    cpu.flags = (flags & ~CY) | (cpu.flags & CY)    # preserve cy

def INX(cpu, alu):
    """ 
    Increment register pair 

    (rh) (rl) <- (rh) (rl) + 1
    
    the content of the register pair rp is incremented by 
    one. Note: No condition ftags are affected.  
    
    """
    cpu.rl, flags = alu.add(cpu.rl, 1)
    cpu.rh, _     = alu.ADC(cpu.rh, 0, flags & CY)

def DCX(cpu, alu):
    """ Decrement register pair """
    cpu.rl, flags = alu.sub(cpu.rl, 1)
    cpu.rh, _     = alu.sbb(cpu.rh, 0, flags & CY)

def DAD(cpu, alu):
    cpu.L, flags = alu.add(cpu.L, cpu.rl)
    cpu.H, flags = alu.ADC(cpu.H, cpu.rh, flags & CY)

    cpu.flags = (flags & CY) | (cpu.flags & ~CY)

def DAA(cpu, alu):
    """ Decimal adjust accumulator """
    pass

def ANA(cpu, alu):
    cpu.A, cpu.flags = alu.ana(cpu.A, cpu.src)

def ANI(cpu, alu):
    """ And immediate """
    cpu.A, cpu.flags = alu.ana(cpu.A, cpu.fetch())

def XRA(cpu, alu):
    """ Exclusive OR register """
    cpu.A, cpu.flags = alu.xra(cpu.A, cpu.src)

def XRI(cpu, alu):
    """ Exclusive OR immediate """
    cpu.A, cpu.flags = alu.xra(cpu.A, cpu.fetch())

def ORA(cpu, alu):
    """ OR register """
    cpu.A, cpu.flags = alu.ora(cpu.A, cpu.src)

def ORI(cpu, alu):
    """ OR immediate """
    cpu.A, cpu.flags = alu.ora(cpu.A, cpu.fetch())

def CMP(cpu, alu):
    """ Compare register """
    _, cpu.flags = alu.sub(cpu.A, cpu.src)

def CPI(cpu, alu):
    """ Compare immediate """
    _, cpu.flags = alu.sub(cpu.A, cpu.fetch())

def RLC(cpu, alu):
    """ Rotate left """
    cpu.A, cpu.flags = alu.RRC(cpu.A, 0, cpu.CY)

def RRC(cpu, alu):
    """ Rotate right """
    cpu.A, cpu.flags = alu.RRC(cpu.A, 0, cpu.CY)

def RAL(cpu, alu):
    """ Rotate left through carry """
    cpu.A, cpu.flags = alu.RAL(cpu.A, 0, cpu.CY)

def RAR(cpu, alu):
    """ Rotate right through carry """
    cpu.A, cpu.flags = alu.RAR(cpu.A, 0, cpu.CY)

def CMA(cpu, alu):
    """ Complement accumulator """
    cpu.A = 255 - cpu.A

def CMC(cpu, alu):
    """ Complement carry """
    cpu.flags ^= CY

def STC(cpu, alu):
    """ Set carry """
    cpu.CY = 1

def JMP(cpu, alu):
    """ Jump """
    cpu.pc = cpu.fetch_16()

def CALL(cpu, alu):
    """ Unconditional call """
    cpu.push_16(cpu.pc)
    cpu.pc = cpu.fetch_16()

def JCC(cpu, alu):
    """ Conditional jump """
    if cpu.cond():
        print("Jump")
        JMP(cpu, alu)

def CCC(cpu, alu):
    """ Condition call """
    if cpu.cond():
        CALL(cpu, alu)

def RET(cpu, alu):
    """ Return """
    cpu.pc = cpu.pop_16()

def RCC(cpu, alu):
    """ Conditional return """
    if cpu.cond():
        RET(cpu, alu)

def RST(cpu, alu):
    """ Restart """
    cpu.push_16(cpu.pc)
    cpu.pc = 8 * cpu.__NNN()

def PCHL(cpu, alu):
    """ Jump H and L indirect """
    cpu.pc = cpu.HL

def PUSH(cpu, alu):
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

def POP(cpu, alu):
    """ Pop """
    if cpu.ir == 0xf1:          # POP PSW
        cpu.PSW = cpu.pop_16()
    else:
        cpu.rp = cpu.pop_16()

def XTHL(cpu, alu):
    """ Exchange stack top with H and L """
    data_16 = cpu.pop_16()
    cpu.push_16(cpu.HL)
    cpu.HL = data_16

def SPHL(cpu, alu):
    """ Move HL to SP """
    cpu.sp = cpu.HL

def IN(cpu, alu):
    """ Input """
    pass

def OUT(cpu, alu):
    """ Output """
    pass

def EI(cpu, alu):
    """ Enable interrupts """
    cpu.ints = 1

def DI(cpu, alu):
    """ Disable interrupts """
    cpu.ints = 0

def HLT(cpu, alu):
    """ Halt """
    print("halt")
    cpu.halt = True

def NOP(cpu, alu):
    """ No op """
    pass

dispatch = [
    NOP,   LXI,   STAX,  INX,   INR,   DCR,   MVI,   RLC,   # 0x00–0x07
    NOP,   DAD,   LDAX,  DCX,   INR,   DCR,   MVI,   RRC,   # 0x08–0x0F
    NOP,   LXI,   STAX,  INX,   INR,   DCR,   MVI,   RAL,   # 0x10–0x17
    NOP,   DAD,   LDAX,  DCX,   INR,   DCR,   MVI,   RAR,   # 0x18–0x1F
    NOP,   LXI,   SHLD,  INX,   INR,   DCR,   MVI,   DAA,   # 0x20–0x27
    NOP,   DAD,   LHLD,  DCX,   INR,   DCR,   MVI,   CMA,   # 0x28–0x2F
    NOP,   LXI,   STA,   INX,   INR,   DCR,   MVI,   STC,   # 0x30–0x37
    NOP,   DAD,   LDA,   DCX,   INR,   DCR,   MVI,   CMC,   # 0x38–0x3F
    MOV,   MOV,   MOV,   MOV,   MOV,   MOV,   MOV,   MOV,   # 0x40–0x47
    MOV,   MOV,   MOV,   MOV,   MOV,   MOV,   MOV,   MOV,   # 0x48–0x4F
    MOV,   MOV,   MOV,   MOV,   MOV,   MOV,   MOV,   HLT,   # 0x50–0x57
    MOV,   MOV,   MOV,   MOV,   MOV,   MOV,   MOV,   MOV,   # 0x58–0x5F
    MOV,   MOV,   MOV,   MOV,   MOV,   MOV,   MOV,   MOV,   # 0x60–0x67
    MOV,   MOV,   MOV,   MOV,   MOV,   MOV,   MOV,   MOV,   # 0x68–0x6F
    MOV,   MOV,   MOV,   MOV,   MOV,   MOV,   HLT,   MOV,   # 0x70–0x77
    MOV,   MOV,   MOV,   MOV,   MOV,   MOV,   MOV,   MOV,   # 0x78–0x7F
    ADD,   ADD,   ADD,   ADD,   ADD,   ADD,   ADD,   ADD,   # 0x80–0x87
    ADC,   ADC,   ADC,   ADC,   ADC,   ADC,   ADC,   ADC,   # 0x88–0x8F
    SUB,   SUB,   SUB,   SUB,   SUB,   SUB,   SUB,   SUB,   # 0x90–0x97
    SBB,   SBB,   SBB,   SBB,   SBB,   SBB,   SBB,   SBB,   # 0x98–0x9F
    ANA,   ANA,   ANA,   ANA,   ANA,   ANA,   ANA,   ANA,   # 0xA0–0xA7
    XRA,   XRA,   XRA,   XRA,   XRA,   XRA,   XRA,   XRA,   # 0xA8–0xAF
    ORA,   ORA,   ORA,   ORA,   ORA,   ORA,   ORA,   ORA,   # 0xB0–0xB7
    CMP,   CMP,   CMP,   CMP,   CMP,   CMP,   CMP,   CMP,   # 0xB8–0xBF
    RCC,   POP,   JCC,   JMP,   CCC,   PUSH,  ADI,   RST,   # 0xC0–0xC7
    RCC,   RET,   JCC,   JMP,   CCC,   CALL,  ACI,   RST,   # 0xC8–0xCF
    RCC,   POP,   JCC,   OUT,   CCC,   PUSH,  SUI,   RST,   # 0xD0-0xD7
    RCC,   RET,   JCC,   IN,    CCC,   CALL,  SBI,   RST,   # 0xD8-0xDF
    RCC,   POP,   JCC,   XTHL,  CCC,   PUSH,  ANI,   RST,   # 0xE0-0xE7
    RCC,   PCHL,  JCC,   XCHG,  CCC,   CALL,  XRI,   RST,   # 0xE8-0xEF
    RCC,   POP,   JCC,   DI,    CCC,   PUSH,  ORI,   RST,   # 0xF0-0xF7
    RCC,   SPHL,  JCC,   EI,    CCC,   CALL,  CPI,   RST    # 0xF8-0xFF                                                 
]

class Instructions:

    def __init__(self):
        self.dispatch = self.__init_dispatch()


    def __init_dispatch(self):
        return [
            NOP,   LXI,   STAX,  INX,   INR,   DCR,   MVI,   RLC,   # 0x00–0x07
            NOP,   DAD,   LDAX,  DCX,   INR,   DCR,   MVI,   RRC,   # 0x08–0x0F
            NOP,   LXI,   STAX,  INX,   INR,   DCR,   MVI,   RAL,   # 0x10–0x17
            NOP,   DAD,   LDAX,  DCX,   INR,   DCR,   MVI,   RAR,   # 0x18–0x1F
            NOP,   LXI,   SHLD,  INX,   INR,   DCR,   MVI,   DAA,   # 0x20–0x27
            NOP,   DAD,   LHLD,  DCX,   INR,   DCR,   MVI,   CMA,   # 0x28–0x2F
            NOP,   LXI,   STA,   INX,   INR,   DCR,   MVI,   STC,   # 0x30–0x37
            NOP,   DAD,   LDA,   DCX,   INR,   DCR,   MVI,   CMC,   # 0x38–0x3F
            MOV,   MOV,   MOV,   MOV,   MOV,   MOV,   MOV,   MOV,   # 0x40–0x47
            MOV,   MOV,   MOV,   MOV,   MOV,   MOV,   MOV,   MOV,   # 0x48–0x4F
            MOV,   MOV,   MOV,   MOV,   MOV,   MOV,   MOV,   HLT,   # 0x50–0x57
            MOV,   MOV,   MOV,   MOV,   MOV,   MOV,   MOV,   MOV,   # 0x58–0x5F
            MOV,   MOV,   MOV,   MOV,   MOV,   MOV,   MOV,   MOV,   # 0x60–0x67
            MOV,   MOV,   MOV,   MOV,   MOV,   MOV,   MOV,   MOV,   # 0x68–0x6F
            MOV,   MOV,   MOV,   MOV,   MOV,   MOV,   HLT,   MOV,   # 0x70–0x77
            MOV,   MOV,   MOV,   MOV,   MOV,   MOV,   MOV,   MOV,   # 0x78–0x7F
            ADD,   ADD,   ADD,   ADD,   ADD,   ADD,   ADD,   ADD,   # 0x80–0x87
            ADC,   ADC,   ADC,   ADC,   ADC,   ADC,   ADC,   ADC,   # 0x88–0x8F
            SUB,   SUB,   SUB,   SUB,   SUB,   SUB,   SUB,   SUB,   # 0x90–0x97
            SBB,   SBB,   SBB,   SBB,   SBB,   SBB,   SBB,   SBB,   # 0x98–0x9F
            ANA,   ANA,   ANA,   ANA,   ANA,   ANA,   ANA,   ANA,   # 0xA0–0xA7
            XRA,   XRA,   XRA,   XRA,   XRA,   XRA,   XRA,   XRA,   # 0xA8–0xAF
            ORA,   ORA,   ORA,   ORA,   ORA,   ORA,   ORA,   ORA,   # 0xB0–0xB7
            CMP,   CMP,   CMP,   CMP,   CMP,   CMP,   CMP,   CMP,   # 0xB8–0xBF
            RCC,   POP,   JCC,   JMP,   CCC,   PUSH,  ADI,   RST,   # 0xC0–0xC7
            RCC,   RET,   JCC,   JMP,   CCC,   CALL,  ACI,   RST,   # 0xC8–0xCF
            RCC,   POP,   JCC,   OUT,   CCC,   PUSH,  SUI,   RST,   # 0xD0-0xD7
            RCC,   RET,   JCC,   IN,    CCC,   CALL,  SBI,   RST,   # 0xD8-0xDF
            RCC,   POP,   JCC,   XTHL,  CCC,   PUSH,  ANI,   RST,   # 0xE0-0xE7
            RCC,   PCHL,  JCC,   XCHG,  CCC,   CALL,  XRI,   RST,   # 0xE8-0xEF
            RCC,   POP,   JCC,   DI,    CCC,   PUSH,  ORI,   RST,   # 0xF0-0xF7
            RCC,   SPHL,  JCC,   EI,    CCC,   CALL,  CPI,   RST    # 0xF8-0xFF                                                 
        ]
