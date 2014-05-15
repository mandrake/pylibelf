import struct


class NamedStruct(object):
    struct     = None
    endianness = ''
    definition = ()

    def __init__(self, data, offset=0):
        if self.struct is None:
            format = self.endianness + ''.join([formattype for name, formattype in self.definition])
            self.struct = struct.Struct(format)

        self.contents = self.struct.unpack_from(data, offset)

        for i, (name, typestring) in enumerate(self.definition):
            if 's' in typestring:
                self.contents = list(self.contents)
                self.contents[i] = self.contents[i].split(b'\0', 1)[0]

    def __getattr__(self, name: str):
        for i, (membername, formattype) in enumerate(self.definition):
            if name == membername:
                return self.contents[i]

    def __repr__(self):
        contents = ['%s: %s' % (name, self.contents[i]) for i, (name, x) in enumerate(self.definition)]
        return '%s - %s' % (self.__class__.__name__, ', '.join(contents))

    def __str__(self):
        # Checks if a description for a given parameter is available and substitutes it
        # to the plain value of the attribute
        attrs = [(name, self.contents[i], getattr(self, name + '_desc'))
                 for i, (name, _) in enumerate(self.definition)]
        attrs = [(a[0], a[1]) if (a[2] is None) else (a[0], a[2]()) for a in attrs]
        #print(attrs)
        conts = [('%s: %s\n' % x) for x in attrs]
        return '%s\n___________________\n%s___________________\n' % (self.__class__.__name__, ''.join(conts))



    def sizeOfStruct(self):
        return self.struct.size
