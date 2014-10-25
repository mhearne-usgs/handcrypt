#!/usr/bin/env python

import random
import string
import re
import optparse
import cryptutils

class Alberti(object):
    StableRing = string.ascii_uppercase
    MovingRing = string.ascii_lowercase
    key = None
    RandomGen = None
    UPPERA = 65
    NLETTERS = len(StableRing)
    def __init__(self,key):
        key = cryptutils.convertInput(key,['upper','nospace','charonly'])
        keyvalue = sum([self.getNumber(ch) for ch in key])
        r = random.Random()
        r.seed(keyvalue)
        values = []
        movring = ['x']*self.NLETTERS
        chidx = 0
        while len(values) < self.NLETTERS:
            ch = string.ascii_lowercase[chidx]
            idx = r.randint(0,self.NLETTERS-1)
            if idx in values:
                continue
            movring[idx] = ch
            values.append(idx)
            chidx += 1
            
        self.MovingRing = ''.join(movring)

        if not isinstance(key,str) and len(key) != 1:
            raise ValueError, 'Key must be a single character'
        self.key = key[0].lower()
        self.RandomGen = random.Random()
        self.RandomGen.seed()

    def getNumber(self,ch):
        return(ord(ch)-self.UPPERA)
    
    def getLetter(self,num):
        return(chr(num+self.UPPERA))
    
    def rotateMovingRing(self,ch):
        sidx = self.StableRing.find(ch)
        midx = self.MovingRing.find(self.key)
        idxdiff = midx - sidx
        if idxdiff > 0:
            idxdiff = self.NLETTERS-idxdiff
        else:
            idxdiff = abs(idxdiff)
        newring = list(self.MovingRing)
        for i in range(0,len(self.MovingRing)):
            ch = self.MovingRing[i]
            newidx = (i+idxdiff) % self.NLETTERS
            newring[newidx] = ch
        self.MovingRing = ''.join(newring)

    def encrypt(self,message):
        message = cryptutils.convertInput(message,['upper','nospace','charonly'])
        letters = []
        #Choose an initial configuration for the moving ring, and start the ciphertext with that character
        ciphertext = self.getLetter(self.RandomGen.randrange(0,self.NLETTERS))
        self.rotateMovingRing(ciphertext)
        for ch in message:
            if ch in letters:
                newch = self.getLetter(self.RandomGen.randrange(0,self.NLETTERS))
                self.rotateMovingRing(newch)
                ciphertext = ciphertext + newch
            else:
                letters.append(ch)
            idx = self.StableRing.find(ch)
            ciphertext = ciphertext + self.MovingRing[idx]
        
        return(ciphertext)

    def decrypt(self,ciphertext):
        ciphertext = cryptutils.convertInput(ciphertext,['upper','nospace','charonly'])
        plaintext = ''
        for ch in ciphertext:
            if ch.isupper(): #this is a key
                self.rotateMovingRing(ch)
                continue
            idx = self.MovingRing.find(ch)
            plaintext = plaintext + self.StableRing[idx]
        return(plaintext)

if __name__ == '__main__':
    usage = 'usage: %prog [options] plain/ciphertext'
    parser = optparse.OptionParser(usage=usage)
    parser.add_option("-k", "--key", dest="key",
                  help="set key for encryption/decryption", metavar="KEY")
    parser.add_option("-e", "--encrypt", dest="doEncrypt",
                      action="store_true",default=False)
    parser.add_option("-d", "--decrypt", dest="doDecrypt",
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
    c = Alberti(options.key)
    if options.doEncrypt:
        print c.encrypt(message)
    else:
        print c.decrypt(message)
