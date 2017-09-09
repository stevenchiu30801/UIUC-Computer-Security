#!/usr/bin/python
import sys
from Crypto.Cipher import AES

def main():
	if len(sys.argv) != 5:
		print "Incorrect number of arguments"
		print "usage: python %s <ciphertext_file> <key_file> <iv_file> <output_file>" % sys.argv[0]
		return

	''' open files '''
	with open(sys.argv[1]) as ciphertext_file:
		ciphertext = ciphertext_file.read().strip()
	with open(sys.argv[2]) as key_file:
		key = key_file.read().strip()
	with open(sys.argv[3]) as iv_file:
		iv = iv_file.read().strip()

	output_file = open(sys.argv[4], 'w')

	''' convert data types '''
	binary_ciphertext = ciphertext.decode('hex')
	binary_key = key.decode('hex')
	binary_iv = iv.decode('hex')

	obj = AES.new(binary_key, AES.MODE_CBC, binary_iv)
	output_file.write(obj.decrypt(binary_ciphertext))

if __name__ == "__main__":
	main()
