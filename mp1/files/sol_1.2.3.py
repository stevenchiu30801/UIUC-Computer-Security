import sys
import urllib2

def get_status(u):
	req = urllib2.Request(u)
	try:
		f = urllib2.urlopen(req)
		#print f.code
		#print f.read()
		return f.code
	except urllib2.HTTPError, e:
		#print e.read()
		#print e.code
		return e.code

def pad(msg):
	n = len(msg) % 16
	return msg + ''.join(chr(i) for i in range(16, n, -1))


ciphertext_file = sys.argv[1]

with open(ciphertext_file) as f:
	ciphertext = f.read().strip()

blocks = map(''.join, zip(*[iter(ciphertext)] * 32)) # break into 16-byte blocks

pads = [hex(i)[2:].zfill(2) for i in range(16, 0, -1)] # put pads into an array

#for i in range(7, -1, -1):
#	print i

c1 = map(''.join, zip(*[iter(blocks[-2])] * 2)) # break each 16-byte block into individual bytes
cp = map(''.join, zip(*[iter(blocks[-2])] * 2))
c2 = map(''.join, zip(*[iter(blocks[-1])] * 2))

p2 = ['00'] * 16 # plaintext block that we're decrypting
	
for g in range(0, 256):
	b = hex(g ^ int(c1[-1], 16) ^ 16)[2:].zfill(2) # guess ^ original byte ^ 16
	
	cp[-1] = b
	url = "http://192.17.90.133:9998/mp1/yschiu2/?" + ''.join(cp) + ''.join(c2)

	if get_status(url) == 404 and cp != c1:
		p2[-1] = hex(g)[2:].zfill(2) #hex(int(b, 16) ^ int(c1[-1], 16) ^ 16)[2:].zfill(2) # b ^ original byte ^ 16
		print p2
		cp[-1] = hex(15 ^ int(p2[-1], 16) ^ int(c1[-1], 16))[2:].zfill(2)
		break

'''
for g in range(0, 256):
	b = hex(g ^ int(c1[-2], 16) ^ 16)[2:].zfill(2)
	
	cp[-2] = b

	url = "http://192.17.90.133:9998/mp1/yschiu2/?" + ''.join(cp) + ''.join(c2)

	if get_status(url) == 404 and cp != c1:
		p2[-2] = hex(g)[2:].zfill(2) # hex(int(b, 16) ^ 16 ^ int(c1[-2], 16))[2:].zfill(2)
		print p2
		# cp[-1] = hex(14 ^ int(p2[-1], 16) ^ int(c1[-1], 16))[2:].zfill(2)
		# print cp
		break 		
'''