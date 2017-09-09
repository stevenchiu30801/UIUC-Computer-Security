import sys
import hashlib

file_1 = sys.argv[1]
file_2 = sys.argv[2]
output_file = sys.argv[3]

with open(file_1) as f:
	str1 = f.read().strip()

with open(file_2) as f:
	str2 = f.read().strip()

hash1 = bin(int(hashlib.sha256(str1).hexdigest(), 16))[2:].zfill(256)
hash2 = bin(int(hashlib.sha256(str2).hexdigest(), 16))[2:].zfill(256)

dist = 0

for i in range(0, 256):
	if (hash1[i] != hash2[i]):
		dist += 1

with open(output_file, 'w') as f:
	f.write(hex(dist)[2:])
