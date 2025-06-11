import unittest

from emulator import CPU
from emulator.assembler import *

def test_cpu():
    cpu = CPU()
    cpu.load([
        NOP,
        MVI_B, 0x12,
        MOV_C_B,
        HLT
    ])

    cpu.run()
    assert(
        cpu.B, cpu.C, cpu.A
    ) == (
        0x12, 0x12, 0x00
    )

def test_ADD():
    rom = [
        MVI_B, 0x01,
        ADD_B,
        HLT
    ]
    cpu = CPU()
    cpu.load(rom)
    cpu.run()

    print(cpu.flags)

    assert(
        cpu.A,
        cpu.flags
    ) == (0x01, 0x02)

def test_ADD_2():
    cpu = CPU()
    cpu.load([
        MVI_B, 0x80,
        ADD_B,
        ADD_B,
        HLT
    ])
    cpu.run()

    assert(
        cpu.A,
        cpu.B,
        cpu.CY
    ) == (0x00, 0x80, 1)

def test_JMP():
    cpu = CPU()

    cpu.load([
        NOP,
        JMP, 0x08, 0x00,
        HLT,
        NOP,
        NOP,
        NOP,
        NOP,
        NOP,
        MVI_B, 0x01,
        HLT
    ])

    cpu.run()

    assert(
        cpu.pc,
        cpu.B
    ) == (0x000d, 0x01)
