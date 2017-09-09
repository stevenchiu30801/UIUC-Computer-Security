#!/usr/bin/python
import sys

def main():
	if len(sys.argv) != 3:
		print "Incorrect number of arguments"
		print "usage: python %s <file.txt> <output_file>" % sys.argv[0]

	''' open files'''
	with open(sys.argv[1]) as file:
		file_content = file.read().strip()

	output_file = open(sys.argv[2], 'w')

	''' WHA '''
	mask = 0x3FFFFFFF
	outHash = 0
	for ch in file_content:
		byte = ord(ch)
		intermediate = ((byte ^ 0xCC) << 24) | \
					   ((byte ^ 0x33) << 16) | \
					   ((byte ^ 0xAA) << 8) | \
					   (byte ^ 0x55)
		outHash = (outHash & mask) + (intermediate & mask)

	# print hex(outHash)[2:]
	# print bin(outHash)[2:]
	output_file.write(hex(outHash)[2:])

if __name__ == "__main__":
	main()
