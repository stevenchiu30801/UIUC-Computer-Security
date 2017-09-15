import sys
import urllib2
from collections import deque

def get_status(u): # returns 500 (padding error), 404 or 200 (OK)
	req = urllib2.Request(u)
	try:
		f = urllib2.urlopen(req)
		return f.code
	except urllib2.HTTPError, e:
		return e.code

ciphertext_file = sys.argv[1]
output_file = sys.argv[2]

with open(ciphertext_file) as f:
	ciphertext = f.read().strip()

blocks = map(''.join, zip(*[iter(ciphertext)] * 32)) # break into 16-byte blocks
pads = [hex(i)[2:].zfill(2) for i in range(16, 0, -1)] # put padding bytes into an array
plaintext = deque() # this will be final plaintext

print "Total number of blocks: " + str(len(blocks))

for i in range(1, len(blocks)): # go through all blocks starting from the last 2
	
	print "Starting decryption of block " + str(len(blocks) - i)

	c1 = map(''.join, zip(*[iter(blocks[-(i + 1)])] * 2)) # break each 16-byte block into individual bytes
	cp = map(''.join, zip(*[iter(blocks[-(i + 1)])] * 2)) # c1 that will be modified
	c2 = map(''.join, zip(*[iter(blocks[-i])] * 2)) # the block to be decrypted

	p = ['00'] * 16 # plaintext for c2

	for j in range(1, 17): # go through all bytes for the block, starting at the last one
		for g in range(0, 256): # g is the guess for the byte
			cp[-j] = hex(g ^ int(c1[-j], 16) ^ 16)[2:].zfill(2) # guess ^ original byte ^ 16
			url = "http://192.17.90.133:9998/mp1/yschiu2/?" + ''.join(cp) + ''.join(c2)

			if get_status(url) == 404: # if error != incorrect padding
				p[-j] = hex(g)[2:].zfill(2) # the guess is correct
				if j == 16: # the whole block has been decrypted
					print "Block " + str(len(blocks) - i) + " decrypted!"
					plaintext.appendleft(p)
					print "Plaintext so far: " + ''.join([chr(int(c, 16)) for sublist in plaintext for c in sublist])
				else:
					for k in range(1, j + 1): # adapt padding			
						cp[-k] = hex(int(pads[j - k + 1], 16)  ^ int(p[-k], 16) ^ int(c1[-k], 16))[2:].zfill(2) 
				break

plaintext = [chr(int(c, 16)) for sublist in plaintext for c in sublist]
print ''.join(plaintext)

with open(output_file, 'w') as f:
	f.write(''.join(plaintext))