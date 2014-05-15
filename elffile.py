from namedstruct import NamedStruct
from header import *
from section import *
from segment import *


class ElfSymbolTableEntry(NamedStruct):
    endianness = '<'
    definition = (
        ('st_name', 'I'),
        ('st_value', 'I'),
        ('st_size', 'I'),
        ('st_info', 'B'),
        ('st_other', 'B'),
        ('st_shndx', 'H')
    )


class ElfRelocation(NamedStruct):
    endianness = '<'
    definition = (
        ('r_offset', 'I'),
        ('r_info', 'I')
    )


class ElfRelocationWithAddend(NamedStruct):
    endianness = '<'
    definition = (
        ('r_offset', 'I'),
        ('r_info', 'I'),
        ('r_addend', 'I')
    )

class ElfFile(object):
    def __init__(self, data):
        #print len(data)
        self.data = data
        self.header = ElfHeader(data)
        print(self.header)
        self.symbols = {}
        #self.commands = []

        strtable = ElfSection(self.data, self.header.e_shoff + self.header.e_shstrndx * self.header.e_shentsize, self.header)

        self.elfSections = {}
        self.sections = []
        self.segments = []
        self.vmem = {}

        for i in range(self.header.e_phnum):
            phentry = ElfSegment(
                self.data,
                self.header.e_phoff + i * self.header.e_phentsize,
                self.header
            )
            self.segments.append(phentry)
            #print(phentry)

        for i in range(self.header.e_shnum):
            shentry = ElfSection(
                self.data,
                self.header.e_shoff + i * self.header.e_shentsize,
                self.header,
                string_section=strtable
            )

            self.elfSections[shentry.name] = shentry
            # Saving only mapped segments
            if shentry.sh_addr != 0:
                self.vmem[shentry.sh_addr] = shentry

            #print(shentry)
            self.sections.append(shentry)

    @staticmethod
    def from_path(path):
        f = open(path, 'rb')
        ret = ElfFile(f.read())
        f.close()
        return ret

    @staticmethod
    def from_data(data):
        return ElfFile(data)

#q = ElfFile.from_path("test/file6.bin")
q = ElfFile.from_path("test/elf")
#print(q.segments[12])
#q.segments[12].dump_to_file('robbe')
print(q)