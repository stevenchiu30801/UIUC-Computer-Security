import sys

ciphertext_file = sys.argv[1]
key_file = sys.argv[2]
output_file = sys.argv[3]

with open(key_file) as f:
	key = f.read().strip()

with open(ciphertext_file) as f: 
	ciphertext = f.read().strip()

with open(output_file, 'w') as f:
	for c in ciphertext:
		if c == ' ':
			f.write(' ')
		elif c.isdigit():
			f.write(c)
		else:
			f.write(chr(ord('A') + key.index(c)))


