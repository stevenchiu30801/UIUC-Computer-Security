#!/usr/bin/python
from pbp import *
from fractions import gcd
from Crypto.PublicKey import RSA

e = 65537 #	public exponent

# modular inverse
# reference from https://stackoverflow.com/questions/4798654/modular-multiplicative-inverse-function-in-python
def egcd(a, b):
	if a == 0:
		return (b, 0, 1)
	else:
		g, y, x = egcd(b % a, a)
		return (g, x - (b / a) * y, y)

def mulinv(a, m):
	g, x, y = egcd(a, m)
	if g != 1:
		raise Exception("modular inverse does not exist")
	else:
		return x % m

def main():
	with open("moduli.hex") as f:
		content = f.read().strip()
	N = content.split('\n')
	
	# Efficient way to compute all-pairs GCDs
	P = 1
	for i in range(0, len(N)):
		N[i] = int(N[i], 16)
		P = P * N[i]
	
	z = len(N) * [None]
	for i in range(0, len(N) - 1):
		x = P % (pow(N[i], 2) * pow(N[i + 1], 2))
		z[i] = x % pow(N[i], 2)
		z[i + 1] = x % pow(N[i + 1], 2)

	with open("1.2.4_ciphertext.enc.asc") as f:
		ciphertext = f.read()

#	# output into RSA_parameters.txt
	outfile = open("RSA_parameters.txt", 'w')

	for i in range(0, len(N)):
		g = gcd(N[i], z[i] / N[i])
		if g != 1:	# in moduli.hex, there is no modulus sharing both of it prime factors
			phi_n = (g - 1) * (N[i] / g - 1)
			d = mulinv(e, phi_n)

			outfile.write("%d %d %d %d %d\n" % (N[i], e, d, g, N[i] / g))
			rsakey = RSA.construct((N[i], long(e), long(d), long(g), long(N[i] / g)))

			# AES decrypt
			text = decrypt(rsakey, ciphertext)
			if text != "ValueError":
				print text

if __name__ == "__main__":
	main()
