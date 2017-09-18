from Crypto.Util.number import inverse, GCD, getStrongPrime, isPrime, getPrime
import sys
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.serialization import Encoding
import hashlib
from mp1certbuilder import make_cert, make_privkey

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
    #assert(GCD(e, p1 - 1) == 1)
    #assert(GCD(e, p2 - 1) == 1)
    return p1, p2

e = 65537
netid = "yschiu2"
ser = 1000
'''
p = getPrime(1024)
print 'p: ' + str(p)
q = getPrime(1024)
print 'q: ' + str(q)

privkey, pubkey = make_privkey(p, q)
cert = make_cert(netid, pubkey, serial = ser)

with open("cert1.cer", 'wb') as f:
    f.write(cert.public_bytes(Encoding.DER))

#with open("cert1.cer", 'rb') as f:
#    cert_bytes = f.read()
#    cert = x509.load_der_x509_certificate(cert_bytes, default_backend())

print
print cert.tbs_certificate_bytes[:256].encode("hex")

with open("prefix", 'wb') as f:
    f.write(cert.tbs_certificate_bytes[:256])
'''

b1 = int("8bfd6b3d3880692ac2054bd4e64c7aabe09cdad9f8150f75268e82a930b4add5dfc8a8ba6027b4e9ebc74f13eee19d5ac35325adb70d8e9f221f75873197fd4e98b512af8d1079432f2621c0d5376fa3b2a6e96321394062dd7bf6cc5c315da2878757fa398973b0694bb4cf88f1820ac898fa518c9eb3cd48a55d8c43131422", 16)
b2 = int("8bfd6b3d3880692ac2054bd4e64c7aabe09cda59f8150f75268e82a930b4add5dfc8a8ba6027b4e9ebc74f13ee619e5ac35325adb70d8e9f221f75073197fd4e98b512af8d1079432f2621c0d5376fa3b2a6e9e321394062dd7bf6cc5c315da2878757fa398973b0694bb4cf8871820ac898fa518c9eb3cd48a55d0c43131422", 16)

found = False
i = 0
while not found:
    if i % 1000 == 0:
        print i
    i += 1

    p1, p2 = getCoprimes()
    b0 = CRT(b1 * 2**1024, b2 * 2**1024, p1, p2)

    k = 0
    b = 0
    while b < 2 ** 1024:
        b = b0 + k * p1 * p2
        q1 = (b1 * 2 ** 1024 + b) / p1
        q2 = (b2 * 2 ** 1024 + b) / p2
        if isPrime(q1) and isPrime(q2) and GCD(e, q1 - 1) == 1 and GCD(e, q2 - 1) == 1:
            print "Found q1 and q2!"
            print "p1: " + str(p1)
            print "p2: " + str(p2)
            print "k: " + str(k)
            print "b: " + str(b)
            print "q1: " + str(q1)
            print "q2: " + str(q2)
            found = True
            break
        k += 1


privKeyOne, pubKeyOne = make_privkey(p1, q1)
privKeyTwo, pubKeyTwo = make_privkey(p2, q2)

certOne = make_cert("yschiu2", pubKeyOne, serial = ser)
certTwo = make_cert("yschiu2", pubKeyTwo, serial = ser)

print "Certificate 1"
print certOne.tbs_certificate_bytes.encode("hex")
print "Certificate 2"
print certTwo.tbs_certificate_bytes.encode("hex")

print hashlib.md5(certOne.tbs_certificate_bytes).hexdigest()
print hashlib.md5(certTwo.tbs_certificate_bytes).hexdigest()

with open("sol_1.2.5_certA.cer", 'wb') as f:
    f.write(certOne.public_bytes(Encoding.DER))
with open("sol_1.2.5_certB.cer", 'wb') as f:
    f.write(certTwo.public_bytes(Encoding.DER))
