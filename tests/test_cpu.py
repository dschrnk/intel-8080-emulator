import unittest

from emulator import CPU
from emulator.assembler import *
from emulator.registers import *
from emulator.flags import *

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
        cpu.regs[B],
        cpu.regs[C],
        cpu.alu.ACC
    ) == (
        0x12,
        0x12,
        0x00
    )

def test_ADD():
    rom = [
        MVI_B, 0x01,
        ADD_B,
        HLT
    ]
    cpu = CPU()
    cpu.load(0x0000, rom)
    cpu.exec()

    print(cpu.flags)

    assert(
        cpu.regs[A],
        cpu.flags
    ) == (0x01, 0x02)

def test_ADD_2():
    cpu = CPU()
    cpu.load(0x0000, [
        MVI_B, 0x80,
        ADD_B,
        ADD_B,
        HLT
    ])
    cpu.exec()

    assert(
        cpu.regs[A],
        cpu.regs[B],
        cpu.flag(CY)
    ) == (0x00, 0x80, True)

def test_JMP():
    cpu = CPU()

    cpu.load(0x0000, [
        NOP,
        JMP, 0x00, 0x10,
        NOP
    ])

    cpu.load(0x1000, [
        MVI_B, 0x01,
        HLT
    ])

    cpu.exec()

    assert(
        cpu.pc,
        cpu.regs[B]
    ) == (0x1003, 0x01)
