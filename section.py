__author__ = 'mandrake'

from namedstruct import NamedStruct

class ElfSection(NamedStruct):
    endianness = '<'
    definition = (
        ('sh_name', 'I'),
        ('sh_type', 'I'),
        ('sh_flags', 'I'),
        ('sh_addr', 'I'),
        ('sh_offset', 'I'),
        ('sh_size', 'I'),
        ('sh_link', 'I'),
        ('sh_info', 'I'),
        ('sh_addralign', 'I'),
        ('sh_entsize', 'I')
    )

    def __init__(self, data, offset, hdr, string_section=None):
        NamedStruct.__init__(self, data, offset)
        self.data = data
        self.offset = offset
        self.string_section = string_section
        self.header = hdr

    def dump_to_file(self, filename):
        f = open(filename, 'wb')
        f.write(self.data[self.sh_offset:self.sh_offset+self.sh_size])
        f.close()

    def dump(self):
        return self.data[self.sh_offset:self.sh_offset+self.sh_size]

    ### Description methods
    def sh_name_desc(self):
        if self.string_section is not None:
            a = self.string_section.sh_offset+self.sh_name
            b = self.data.find(b'\0', a)
            return str(self.data[a:b])
        return ""

    def __getattr__(self, item):
        if item == 'name':
            return self.sh_name_desc()
        else:
            return NamedStruct.__getattr__(self, item)

    def __str__(self):
        ret = NamedStruct.__str__(self)
        ret += "\nMy name is also "
        ret += self.name
        return ret