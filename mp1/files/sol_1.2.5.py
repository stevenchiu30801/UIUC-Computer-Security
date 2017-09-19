from Crypto.Util.number import inverse, GCD, getStrongPrime, isPrime, getPrime
import sys
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.serialization import Encoding
import hashlib
from mp1_certbuilder import make_privkey, make_cert

def CRT(b1, b2, p1, p2):
    N = p1 * p2
    invOne = inverse(p2, p1)
    invTwo = inverse(p1, p2)
    return -(b1 * invOne * p2 + b2 * invTwo * p1) % N

def getCoprimes(e = 65537):
    bitSize = 512
    p1, p2 = -1, -1
    while p1 == p2:
        p1 = getStrongPrime(bitSize, e)
        p2 = getStrongPrime(bitSize, e)
    assert(GCD(e, p1 - 1) == 1)
    assert(GCD(e, p2 - 1) == 1)
    return p1, p2
'''
netid = "yschiu2"
p = getPrime(1024)
q = getPrime(1024)

privkey, pubkey = make_privkey(p, q)
cert = make_cert(netid, pubkey)

with open("test.cer", 'wb') as f:
    f.write(cert.public_bytes(Encoding.DER))
print 'try the following command: openssl x509 -in test.cer -inform der -text -noout'

with open("prefix", 'wb') as f:
    f.write(cert.tbs_certificate_bytes[:256])
'''

b1 = int("47c8e8a566f31b9bdc340784812de348da554740450d30cd1b8a81edb3b31c48aab308e5cce8dffceb4bd9c1ccd3e65deaf4da2bd30116d72b5d25c6197d12d111f85a5302f54d42030b6b4ae46e61269dd4cfb58928ed3b1e29aa264b4c818ce52f77ff0536a1c62a8c09928954861cfa4cf62e77d92319712d44eb917bd724", 16)

b2 = int("47c8e8a566f31b9bdc340784812de348da5547c0450d30cd1b8a81edb3b31c48aab308e5cce8dffceb4bd9c1cc53e65deaf4da2bd30116d72b5d2546197d12d111f85a5302f54d42030b6b4ae46e61269dd4cf358928ed3b1e29aa264b4c818ce52f77ff0536a1c62a8c099289d4861cfa4cf62e77d92319712d446b917bd724", 16)

# find p1, p2, q1, q2
found = False
i = 0

while not found:
    print i
    p1, p2 = getCoprimes()
    b0 = CRT(b1 * 2**1024, b2 * 2**1024, p1, p2)

    k = 0
    b = 0
    e = 65537
    while b < 2 ** 1024:
        b = b0 + k * p1 * p2
        q1 = (b1 * 2 ** 1024 + b) / p1
        q2 = (b2 * 2 ** 1024 + b) / p2
        if isPrime(q1) and isPrime(q2) and GCD(e, q1 - 1) == 1 and GCD(e, q2 - 1) == 1:
            print "Found q1 and q2!"
            print "p1 = %d" % p1
            print "p2 = %d" % p2
            print "b0 = %d" % b0
            print "k = %d" % k
            print "b = %d" % b
            print "q1 = %d" % q1
            print "q2 = %d" % q2
            found = True
            break
        k += 1
    i += 1
	#print "not found"

ser = int("0e5184feb762ace00a7a98630423257479281443", 16)

with open("sol_1.2.5_factorsA.hex", 'w') as f:
	f.write("%x\n%x" % (p1, q1))

with open("sol_1.2.5_factorsB.hex", 'w') as f:
	f.write("%x\n%x" % (p2, q2))

privkeyA, pubkeyA = make_privkey(p1, q1)
privkeyB, pubkeyB = make_privkey(p2, q2)

certA = make_cert("yschiu2", pubkeyA, serial = ser)
certB = make_cert("yschiu2", pubkeyB, serial = ser)

with open("sol_1.2.5_certA.cer", 'wb') as f:
    f.write(certA.public_bytes(Encoding.DER))

with open("sol_1.2.5_certB.cer", 'wb') as f:
    f.write(certB.public_bytes(Encoding.DER))

# verify
print "md5 of certA: ", hashlib.md5(certA.tbs_certificate_bytes).hexdigest()
print "md5 of certB: ", hashlib.md5(certB.tbs_certificate_bytes).hexdigest()

