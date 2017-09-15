from Crypto.Util.number import inverse, GCD, getStrongPrime, isPrime
import sys
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.serialization import Encoding
import hashlib

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

b1 = int("54b20eff475aaea8b42edbe24ce88a1e54042659ac801709f939449a2682c7fbc7cb08f86e41f1c66be2de1cb1fb93790ef133d39ba59eca832de66d3cbfbb8d055484f8a38d5ea725e4e4b6a2404b7f3bc357b07cd971e74dc310bf9a5f68b7cfd528f497831d3e373c063b4154198ffa29e05cdf7ed3bcdccddaa810da7556", 16)
b2 = int("54b20eff475aaea8b42edbe24ce88a1e540426d9ac801709f939449a2682c7fbc7cb08f86e41f1c66be2de1cb17b94790ef133d39ba59eca832de6ed3cbfbb8d055484f8a38d5ea725e4e4b6a2404b7f3bc357307cd971e74dc310bf9a5f68b7cfd528f497831d3e373c063b41d4188ffa29e05cdf7ed3bcdccdda2810da7556", 16)
found = False
i = 0

while not found:
    print i
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
            print q1
            print q2
            found = True
            break
        k += 1
    #print "not found"
