#!/usr/bin/env python

import sys
import re
import cryptutils
from string import ascii_uppercase
import optparse
import copy
from pi import PiGenerator
import math

class KeyOrder(object):
    KEYLENGTH = 20
    key = None
    extras = '., "&?' #extra characters we can use because we need to fill up 5 bits
    letters = ascii_uppercase+extras
    rdict = dict(zip(range(0,32),letters))
    fdict = dict(zip(letters,range(0,32)))
    def __init__(self,key):
        key = cryptutils.convertInput(key,['upper','nospace','charonly'])
        if len(key) < self.KEYLENGTH:
            raise ValueError,'Key Length must be %i characters or more.' % (self.KEYLENGTH)
        self.key = self.orderKey(key[0:self.KEYLENGTH])

    def orderKey(self,key):
        sk = sorted(key)
        ik = [-1 for x in range(0,len(key))]
        alreadyseen = '';
        for i in range(0,len(key)):
            ch = key[i]
            idx = sk.index(ch)
            ik[i] = idx
            sk[idx] = '0'
        return ik

    def getBitString(self,numbers):
        bitstring = ''
        for n in numbers:
            bitstring = bitstring + str(n % 2)
        return bitstring

    def scrambleKey(self,newmessage):
        nchars = len(newmessage)
        P = nchars * 5
        if P % 20:
            Q = P / 20.0
            P = int(math.ceil(Q)*20)
        pi = PiGenerator(P)
        scrambled = []
        for i in range(0,P/20):
            pstart = i*20
            pend = pstart + 20
            pd = pi.digits[pstart:pend]
            s = [(pd[i] + self.key[i])%10 for i in range(0,20)]
            scrambled = scrambled + s

            for i in range(0,10):
                scrambled = self.shuffle(scrambled)

        return self.shuffle(scrambled)

    def shuffle(self,scrambled):
        newscramble = [0 for i in scrambled]
        n = len(newscramble)
        nchunks = n/10
        key1 = []
        key2 = []
        for k in self.key:
            if k < 10:
                key1.append(k)
            else:
                key2.append(k-10)

        for i in range(0,nchunks/2):
            i1 = i*10
            i2 = i1+10
            block1 = scrambled[i1:i2]
            i3 = (nchunks-(i+1))*10
            i4 = i3+10
            block2 = scrambled[i3:i4]
            for j in range(0,10):
                k1 = key1[j]
                k2 = key2[j]
                newscramble[i1+j] = block2[k2]
                newscramble[i3+j] = block1[k1]

        return newscramble
    
    def encrypt(self,message):
        newmessage = ''
        ciphertext = ''
        bitstring = ''
        for m in message.upper():
            if m in self.letters:
                newmessage = newmessage + m
                
        scrambled = self.scrambleKey(newmessage)
        nchars = len(newmessage)
        
        nchunks = int(math.ceil(nchars/20.0))
        for ichunk in range(nchunks):
            #print 'Chunk %i' % ichunk
            istart = ichunk*20
            iend = istart + 20
            if iend > len(newmessage)-1:
                chunk = newmessage[istart:]
            else:
                chunk = newmessage[istart:istart+20]
            for i in range(0,len(chunk)):
                if len(chunk) < len(self.key):
                    kidx = i
                else:
                    kidx = self.key[i]
                ch = chunk[kidx]
                numch = self.fdict[ch]
                pstart = ichunk*20 + kidx*5
                pend = pstart + 5
                piblock = scrambled[pstart:pend]
                pibits = cryptutils.list2bin(piblock)
                pinum = cryptutils.bin2dec(pibits)
                bitstring = bitstring + self.rdict[pinum]
                numct = numch ^ pinum
                ciphertext = ciphertext + self.rdict[numct]
                #print '%2i %2i %2s %2i %4i %4i %-20s %2i %2i %s' % (i,kidx,ch,numch,pstart,pend,str(piblock),pinum,numct,ciphertext[-1])
            
                
        return (ciphertext,bitstring)

    def decrypt(self,ciphertext):
        newciphertext = ''
        plaintext = [0 for c in ciphertext]
        bitstring = ''
        for m in ciphertext.upper():
            if m in self.letters:
                newciphertext = newciphertext + m
                
        scrambled = self.scrambleKey(newciphertext)
        nchars = len(newciphertext)
        
        nchunks = int(math.ceil(nchars/20.0))
        for ichunk in range(nchunks):
            istart = ichunk*20
            chunk = newciphertext[istart:istart+20]
            for i in range(0,len(chunk)):
                if len(chunk) < len(self.key):
                    kidx = i
                else:
                    kidx = self.key[i]
                ch = chunk[i]
                numch = self.fdict[ch]
                pstart = ichunk*20 + kidx*5
                pend = pstart + 5
                piblock = scrambled[pstart:pend]
                pibits = cryptutils.list2bin(piblock)
                pinum = cryptutils.bin2dec(pibits)
                bitstring = bitstring + self.rdict[pinum]
                numct = numch ^ pinum
                plaintext[istart+kidx] = self.rdict[numct]

        plaintext = ''.join(plaintext)

        return (plaintext,bitstring)

if __name__ == '__main__':
    usage = 'usage: %prog [options] plain/ciphertext'
    parser = optparse.OptionParser(usage=usage)
    parser.add_option("-k", "--key", dest="key",
                  help="set key for encryption/decryption", metavar="KEY")
    parser.add_option("-e", "--encrypt", dest="doEncrypt",
                      action="store_true",default=False)
    parser.add_option("-d", "--decrypt", dest="doDecrypt",
                      action="store_true",default=False)
    parser.add_option("-b", "--genbits", dest="doGenBits",
                      action="store_true",default=False)
    
    (options, args) = parser.parse_args()
    if options.key is None or len(args) == 0:
        print 'Specify a key with -k and supply a message to encrypt/decrypt.'
        parser.print_help()
        sys.exit(1)

    if options.doEncrypt and options.doDecrypt:
        print 'You must select one of encryption or decryption.'
        parser.print_help()
        sys.exit(1)

    message = ' '.join(args)
    try:
        k = KeyOrder(options.key)
    except ValueError,msg:
        print msg
        parser.print_help()
        sys.exit(1)

    if options.doEncrypt:
        ct,bitstring = k.encrypt(message)
        print "'%s'" % ct
        if options.doGenBits:
            print "'%s'" % bitstring
    if options.doDecrypt:
        print k.decrypt(message)    

    if options.doGenBits:
        ct,bitstring = k.encrypt(message)
        print "'%s'" % bitstring
    
