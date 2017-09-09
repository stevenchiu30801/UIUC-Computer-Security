from Crypto.Cipher import AES
import base64
import sys


with open('1.1.2.3_aes_weak_ciphertext.hex') as f:
	text = f.read().strip().decode('hex')

iv = 16 * '\x00'

for i in range(0, 32):
	key = hex(i)[2:].zfill(64)
	s = AES.new(key.decode('hex'), AES.MODE_CBC, iv).decrypt(text)
	print key + '\n' + s + '\n\n'
