__author__ = 'mandrake'

def e_flags_desc(e_flags_val):
    ret = 'ABI: %d\n' % ((e_flags_val & 0xff000000) >> 24)
    ret += 'BE8: %d\n' % ((e_flags_val & 0x00800000) >> 23)
    # ret += 'GCC (legacy)'
    if e_flags_val & 0x00000400:
        ret += 'Floating point: hardware'
    elif e_flags_val & 0x00000200:
        ret += 'Floating point: software'
    return ret

def e_entry_desc(e_entry_val):
    ret = ''
    if e_entry_val & 0x80000000:
        ret += 'Contains Thumb code\n'
    if not (e_entry_val & 0xc0000000):
        ret += 'Contains ARM code\n'
    return ret.strip()