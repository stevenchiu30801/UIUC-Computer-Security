import sys
import math

def main():

	if len(sys.argv) != 5:
		print "Incorrect number of arguments"
		print "usage: python %s <ciphertext_file> <key_file> <modulo_file> <output_file>"
		return

	''' open files '''
	with open(sys.argv[1]) as ciphertext_file:
		ciphertext = ciphertext_file.read().strip()
	with open(sys.argv[2]) as key_file:
		key = key_file.read().strip()
	with open(sys.argv[3]) as modulo_file:
		modulo = modulo_file.read().strip()

	output_file = open(sys.argv[4], 'w')

	c = int(ciphertext, 16)
	d = int(key, 16) 
	N = int(modulo, 16)

	# m = math.pow(c, d) % N
	m = pow(c, d) % N

	output_file.write("%x" % m)

if __name__ == "__main__":
	main()

