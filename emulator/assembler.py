NOP	        = 0x00
LXI_BC		= 0x01
STAX_BC		= 0x02
INX_BC		= 0x03
INR_B		= 0x04
DCR_B		= 0x05
MVI_B		= 0x06
RLC	        = 0x07

DAD_BC		= 0x09

LDAX_BC		= 0x0a
DCX_BC		= 0x0b
INR_C		= 0x0c
DCR_C		= 0x0d
MVI_C		= 0x0e
RRC	        = 0x0f

LXI_DE		= 0x11
STAX_DE		= 0x12
INX_DE		= 0x13
INR_D		= 0x14
DCR_D		= 0x15
MVI_D		= 0x16
RAL	        = 0x17
DAD_DE		= 0x19
LDAX_DE		= 0x1a
DCX_DE		= 0x1b
INR_E		= 0x1c
DCR_E		= 0x1d
MVI_E		= 0x1e
RAR	        = 0x1f

LXI_HL		= 0x21
SHLD		= 0x22
INX_HL		= 0x23
INR_H		= 0x24
DCR_H		= 0x25
MVI_H		= 0x26
DAA	        = 0x27
DAD_HL		= 0x29
LHLD		= 0x2a
DCX_HL		= 0x2b
INR_L		= 0x2c
DCR_L		= 0x2d
MVI_L		= 0x2e
CMA	        = 0x2f

LXI_SP		= 0x31
STA	        = 0x32
INX_SP		= 0x33
INR_M		= 0x34
DCR_M		= 0x35
MVI_M		= 0x36
STC	        = 0x37
DAD_SP		= 0x39
LDA	        = 0x3a
DCX_SP		= 0x3b
INR_A		= 0x3c
DCR_A		= 0x3d
MVI_A		= 0x3e
CMC	        = 0x3f

MOV_B_B		= 0x40
MOV_B_C		= 0x41
MOV_B_D		= 0x42
MOV_B_E		= 0x43
MOV_B_H		= 0x44
MOV_B_L		= 0x45
MOV_B_M		= 0x46
MOV_B_A		= 0x47
MOV_C_B		= 0x48
MOV_C_C		= 0x49
MOV_C_D		= 0x4a
MOV_D_B		= 0x50
MOV_D_C		= 0x51
MOV_D_D		= 0x52
MOV_D_E		= 0x53
MOV_D_H		= 0x54
MOV_D_L		= 0x55
MOV_D_M		= 0x56
MOV_D_A		= 0x57
MOV_E_B		= 0x58
MOV_E_C		= 0x59
MOV_E_D		= 0x5a
MOV_E_E		= 0x5b
MOV_E_H		= 0x5c
MOV_E_L		= 0x5d
MOV_E_M		= 0x5e
MOV_E_A		= 0x5f
MOV_H_B		= 0x60
MOV_H_C		= 0x61
MOV_H_D		= 0x62
MOV_H_E		= 0x63
MOV_H_H		= 0x64
MOV_H_L		= 0x65
MOV_H_M		= 0x66
MOV_H_A		= 0x67
MOV_L_B		= 0x68
MOV_L_C		= 0x69
MOV_L_D		= 0x6a
MOV_L_E		= 0x6b
MOV_L_H		= 0x6c
MOV_L_L		= 0x6d
MOV_L_M		= 0x6e
MOV_L_A		= 0x6f
MOV_M_B		= 0x70
MOV_M_C		= 0x71
MOV_M_D		= 0x72
MOV_M_E		= 0x73
MOV_M_H		= 0x74
MOV_M_L		= 0x75
HLT	        = 0x76
MOV_M_A		= 0x77
MOV_A_B		= 0x78
MOV_A_C		= 0x79
MOV_A_D		= 0x7a
MOV_A_E		= 0x7b
MOV_A_H		= 0x7c
MOV_A_L		= 0x7d
MOV_A_M		= 0x7e
MOV_A_A		= 0x7f
ADD_B		= 0x80
ADD_C		= 0x81
ADD_D		= 0x82
ADD_E		= 0x83
ADD_H		= 0x84
ADD_L		= 0x85
ADD_M		= 0x86
ADD_A		= 0x87
ADC_B		= 0x88
ADC_C		= 0x89
ADC_D		= 0x8a
ADC_E		= 0x8b
ADC_H		= 0x8c
ADC_L		= 0x8d
ADC_M		= 0x8e
ADC_A		= 0x8f
SUB_B		= 0x90
SUB_C		= 0x91
SUB_D		= 0x92
SUB_E		= 0x93
SUB_H		= 0x94
SUB_L		= 0x95
SUB_M		= 0x96
SUB_A		= 0x97
SBB_B		= 0x98
SBB_C		= 0x99
SBB_D		= 0x9a
SBB_E		= 0x9b
SBB_H		= 0x9c
SBB_L		= 0x9d
SBB_M		= 0x9e
SBB_A		= 0x9f
ANA_B		= 0xa0
ANA_C		= 0xa1

JMP         = 0xc3
JZ          = 0xca
