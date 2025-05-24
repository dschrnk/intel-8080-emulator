import unittest

from emulator import CPU
from emulator.assembler import *

def test_cpu():
    cpu = CPU()
    cpu.load(0x0000, [
        NOP,
        MVI_B, 0x12,
        MOV_C_B,
        HLT
    ])

    cpu.exec()
    assert(
        cpu.get_B(),
        cpu.regs[CPU.C],
        cpu.alu.ACC
    ) == (
        0x12,
        0x12,
        0x00
    )
