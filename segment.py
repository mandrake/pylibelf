__author__ = 'mandrake'

from namedstruct import NamedStruct

class ElfSegment(NamedStruct):
    endianness = '<'
    definition = (
        ('p_type', 'I'),
        ('p_offset', 'I'),
        ('p_vaddr', 'I'),
        ('p_paddr', 'I'),
        ('p_filesz', 'I'),
        ('p_memsz', 'I'),
        ('p_flags', 'I'),
        ('p_align', 'I')
    )

    def dump_to_file(self, filename):
        f = open(filename, 'wb')
        f.write(self.data[self.p_offset:self.p_offset+self.p_filesz])
        f.close()

    def dump(self):
        return self.data[self.p_offset:self.p_offset+self.p_filesz]

    def __init__(self, data, offset, hdr):
        NamedStruct.__init__(self, data, offset)
        self.offset = offset
        self.data = data
        self.header = hdr