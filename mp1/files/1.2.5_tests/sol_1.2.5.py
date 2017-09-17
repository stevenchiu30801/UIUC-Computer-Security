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
'''
p = getPrime(1024)
print 'p: ' + str(p)
q = getPrime(1024)
print 'q: ' + str(q)

privkey, pubkey = make_privkey(p, q)
cert = make_cert(netid, pubkey)

with open("cert1.cer", 'wb') as f:
    f.write(cert.public_bytes(Encoding.DER))

with open("cert1.cer", 'rb') as f:
    cert_bytes = f.read()
    cert = x509.load_der_x509_certificate(cert_bytes, default_backend())

print
print cert.tbs_certificate_bytes[:256].encode("hex")

with open("prefix", 'wb') as f:
    f.write(cert.tbs_certificate_bytes[:256])
'''

b1 = int("df89d48c5d344ff4184a6ed1689aa123757b8e09a06c61f012ce41aa0912af91d2e5aee7de0d42bb4f283f14c9a7905859546f2a2ca4550e64220654d36a7c9b0e50942cca09803dfabb178d36e62a99c7dd2c371ec9980b8605f0575f4c6dc1e815c1e9f2a69bdf16c5ebf84506640f002972216937aa910cff78d00e1366b1", 16)
b2 = int("df89d48c5d344ff4184a6ed1689aa123757b8e89a06c61f012ce41aa0912af91d2e5aee7de0d42bb4f283f14c927915859546f2a2ca4550e642206d4d36a7c9b0e50942cca09803dfabb178d36e62a99c7dd2cb71ec9980b8605f0575f4c6dc1e815c1e9f2a69bdf16c5ebf84586630f002972216937aa910cff78500e1366b1", 16)

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

certOne = make_cert("yschiu2", pubKeyOne)
certTwo = make_cert("yschiu2", pubKeyTwo)

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
