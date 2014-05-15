__author__ = 'mandrake'

from namedstruct import NamedStruct
from arch import *

machine_descs = {
    0: "Undefined",
    1: "AT&T WE 32100",
    2: "SPARC",
    3: "Intel 386",
    4: "Motorola 68000",
    5: "Motorola 88000",
    6: "Intel 486 (deprecated)",
    7: "Intel 80860",
    8: "MIPS R3000",
    20: "PowerPC",
    21: "PowerPC64",
    40: "ARM",
    41: "DEC Alpha",
    43: "SPARC V9",
    62: "AMD64",
    47787: "Xilinx MicroBlaze"
}

class ElfHeader(NamedStruct):
    endianness = '<'
    definition = (
        ('e_ident', '16s'),     # The magic
        ('e_type', 'H'),
        ('e_machine', 'H'),
        ('e_version', 'I'),
        ('e_entry', 'I'),       # Address
        ('e_phoff', 'I'),       # Offset
        ('e_shoff', 'I'),       # Offset
        ('e_flags', 'I'),
        ('e_ehsize', 'H'),
        ('e_phentsize', 'H'),
        ('e_phnum', 'H'),
        ('e_shentsize', 'H'),
        ('e_shnum', 'H'),
        ('e_shstrndx', 'H')
    )

    def __init__(self, data):
        NamedStruct.__init__(self, data)
        self.e_ident = bytearray(self.e_ident)

    def e_machine_desc(self):
        return machine_descs[self.e_machine]

    def e_ident_desc(self):
        EI_CLASS = {
            0: 'ELFCLASSNONE (Invalid class)',
            1: 'ELFCLASS32 (32-bit objects)',
            2: 'ELFCLASS64 (64-bit objects)'
        }
        EI_DATA = {
            0: 'ELFDATANONE (Invalid data encoding)',
            1: 'ELFDATA2LSB (Little endian encoding)',
            2: 'ELFDATA2MSB (Big endian encoding)'
        }

        self.e_ident.extend([0] * (16 - len(self.e_ident)))
        ret  = 'Magic: %4s\n' % self.e_ident[0:4]
        ret += 'File class: %d - %s\n' % (self.e_ident[4], EI_CLASS[self.e_ident[4]])
        ret += 'Data encoding: %d - %s\n' % (self.e_ident[5], EI_DATA[self.e_ident[5]])
        ret += 'File version: %d\n' % self.e_ident[6]
        ret += 'OS/ABI identification: %d\n' % self.e_ident[7]
        ret += 'ABI version: %d\n' % self.e_ident[8]
        ret += 'Len: %d' % len(bytearray(self.e_ident))
        return ret

    def e_entry_desc(self):
        e_descs = {
            40: arm.header.e_entry_desc
        }

        try:
            tocall = e_descs[self.e_machine]
            ret = tocall(self.e_flags)
            return '\n'+'\n'.join(['\t' + q for q in ret.split('\n')])
        except KeyError:
            return self.e_flags

    def e_flags_desc(self):
        e_descs = {
            40: arm.header.e_flags_desc
        }

        try:
            tocall = e_descs[self.e_machine]
            ret = tocall(self.e_flags)
            return '\n'+'\n'.join(['\t' + q for q in ret.split('\n')])
        except KeyError:
            return self.e_flags