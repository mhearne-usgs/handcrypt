#!/usr/bin/env python

import string
import os
import sys
import math
import struct
from random import SystemRandom
import time
import zlib
import base64

nums = ['%02i' % i for i in range(1,27)]
FDICT = dict(zip(string.uppercase,nums))
RDICT = dict(zip(nums,string.uppercase))

def findPrime(nbits):
    #First find the number of digits in a number with nbits bits
    ndigits = len(str(pow(2,nbits)))+1
    nchecks = 0
    while True:
        rbytes = os.urandom(ndigits+20) #guarantee that our number will have at least nbits
        dstr = '' #the number string we will be constructing
        i = 0
        while len(dstr) < ndigits:
            rbyte = rbytes[i]
            digit = str(ord(rbyte))[-1]
            if digit == '0' and not len(dstr):
                i += 1
                continue
            dstr = dstr + digit
            i += 1
        testnum = int(dstr)
        if (not testnum % 2) or (not testnum % 3) or (not testnum % 5):
            nchecks += 1
            continue

        isPrime = checkPrime(testnum)
        if isPrime:
            break
        nchecks += 1

    return (testnum,nchecks)

def checkPrime(n,k=10):
    isComposite = False
    for i in range(0,k):
        r1 = SystemRandom(time.time())
        a = r1.randint(1,n-1)
        isComposite = pow(a,n-1,n) != 1
        if isComposite:
            return False
    return True

def genKeys(nbits):
    p,nchecks = findPrime(nbits)
    r1 = SystemRandom(time.time())
    r2 = SystemRandom(time.time())
    a = r1.randint(1,p-2)
    k = r2.randint(1,p-2)
    pubkey = (p,a,pow(a,k,p))
    prikey = k
    return (pubkey,prikey)

def encrypt(message,pubkey):
    ordnums = [ord(ch) for ch in message]
    p,a,akp = pubkey
    r1 = SystemRandom(time.time())
    l = r1.randint(1,p-2)
    d = pow(a,l,p)
    encnums = [onum * pow(akp,l,p) for onum in ordnums]
    return (d,encnums)

def decrypt(e,d,pubkey,prikey):
    p,a,akp = pubkey
    k = prikey
    dp = pow(d,(p-1-k),p)
    plaintext = []
    for chnum in e:
        plaintext.append(chr((dp * chnum) % p))
    plaintext = ''.join(plaintext)
    return plaintext

def textify(encmessage):
    tmessage = ''
    tlist = [base64.b64encode(zlib.compress(str(e))) for e in encmessage]
    return ' '.join(tlist)

def untextify(textmessage):
    tlist = textmessage.split()
    encmessage = [int(zlib.decompress(base64.b64decode(t))) for t in tlist]
    return encmessage

if __name__ == '__main__':
    nbits = int(sys.argv[1])
    message = "I'm your father"
    print 'Input message is %s' % message
    t1 = time.time()
    pubkey,prikey = genKeys(nbits)
    t2 = time.time()
    d,ciphertext = encrypt(message,pubkey)
    t3 = time.time()
    print 'ciphertext is %s' % ciphertext

    enctext = textify(ciphertext)
    print 'Textified version of ciphertext is %s' % enctext

    ciphertext2 = untextify(enctext)
    
    
    plaintext = decrypt(ciphertext2,d,pubkey,prikey)
    t4 = time.time()
    print 'plaintext is %s' % plaintext
    print 'Key generation took %f seconds' % (t2-t1)
    print 'Encryption took %f seconds' % (t3-t2)
    print 'Decryption took %f seconds' % (t4-t3)

