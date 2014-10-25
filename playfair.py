#!/usr/bin/env python

import sys
import re
import cryptutils
from string import ascii_uppercase
import optparse

class Playfair(object):
    key = None

    def __init__(self,key):
        key = cryptutils.unique(cryptutils.convertInput(key,['upper','nospace','charonly']))
        if len(key) > 25:
            raise ValueError,'Key Length must be 25 characters or less.'
        remchars = 25 - len(key)
        keylist = list(key)
        for ch in ascii_uppercase:
            if ch == 'J':
                continue
            if ch not in key:
                keylist.append(ch)
        key = ''.join(keylist)
        self.key = []
        self.key.append(key[0:5])
        self.key.append(key[5:10])
        self.key.append(key[10:15])
        self.key.append(key[15:20])
        self.key.append(key[20:25])
        

    def encrypt(self,message):
        message = cryptutils.convertInput(message,['upper','nospace','charonly'])
        digraphs = self.createDigraphs(message)
        #encode each digraph
        ciphergraphs = []
        for dg in digraphs:
            pair = self.transposeDigraph(dg)
            ciphergraphs.append(''.join(pair))
        return ''.join(ciphergraphs)

    def decrypt(self,ciphertext):
        ciphertext = cryptutils.convertInput(ciphertext,['upper','nospace','charonly'])
        #second, break the ciphertext up into digraphs
        digraphs = self.createDigraphs(ciphertext)
        #encode each digraph
        ciphergraphs = []
        for dg in digraphs:
            pair = self.transposeDigraph(dg,forward=False)
            ciphergraphs.append(''.join(pair))
            
        #remove any superfluous X characters
        plaintext = ''
        i = 0
        while i < len(ciphergraphs)-1:
            cg1 = ciphergraphs[i]
            cg2 = ciphergraphs[i+1]
            if cg1[1] == 'X' and cg1[0] == cg2[0]:
                plaintext = plaintext + cg1[0]
            else:
                plaintext = plaintext + cg1
            i += 1
        plaintext = plaintext + ciphergraphs[-1]
        if plaintext[-1] == 'X' and plaintext[-2] not in 'AEIOUY':
            plaintext = plaintext[0:-1]
        return plaintext

    def transposeDigraph(self,dg,forward=True):
        ch1 = dg[0]
        ch2 = dg[1]
        r1,c1 = self.getPosition(ch1)
        r2,c2 = self.getPosition(ch2)
        pair = ['X','X']
        #If ch1 and ch2 are on the same row, just slide each character over
        #by one to get the new digraph (rolling around at the end)
        if r1 == r2:
            if c1 == 4:
                if forward:
                    pair[0] = self.key[r1][0]
                else:
                    pair[0] = self.key[r1][3]
            else:
                if forward:
                    pair[0] = self.key[r1][c1+1]
                else:
                    pair[0] = self.key[r1][c1-1]
            if c2 == 4:
                if forward:
                    pair[1] = self.key[r2][0]
                else:
                    pair[1] = self.key[r2][3]
            else:
                if forward:
                    pair[1] = self.key[r2][c2+1]
                else:
                    pair[1] = self.key[r2][c2-1]
        #if ch1 and ch2 are in the same column, just slide each character
        #down one row to get new digraph (rolling back to top on last row)
        elif c1 == c2:
            if r1 == 4:
                if forward:
                    pair[0] = self.key[0][c1]
                else:
                    pair[0] = self.key[3][c1]
            else:
                if forward:
                    pair[0] = self.key[r1+1][c1]
                else:
                    pair[0] = self.key[r1-1][c1]
            if r2 == 4:
                if forward:
                    pair[1] = self.key[0][c2]
                else:
                    pair[1] = self.key[3][c2]
            else:
                if forward:
                    pair[1] = self.key[r2+1][c2]
                else:
                    pair[1] = self.key[r2-1][c2]
        #otherwise, then use the rectangle defined by the digraph
        else:
            pair[0] = self.key[r1][c2]
            pair[1] = self.key[r2][c1]
        
        return ''.join(pair)

    def getPosition(self,ch):
        for row in range(0,len(self.key)):
            col = self.key[row].find(ch)
            if col != -1:
                return row,col
            continue

    def createDigraphs(self,message):
        #Rules:
        #Convert J to I
        #If double letters in same digraph, space out with an X
        #If uneven number of overall letters, pad with an X
        message = message.replace('J','I')
        digraphs = []
        i = 0
        while True:
            if i >= len(message):
                break
            if i == len(message)-1:
                digraphs.append(message[i]+'X')
                break
            if message[i] == message[i+1]:
                digraphs.append(message[i]+'X')
                i += 1
                continue
            else:
                digraphs.append(message[i:i+2])
                i += 2
                continue
        
        return digraphs

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
    p = Playfair(options.key)
    if options.doEncrypt:
        print p.encrypt(message)
    else:
        print p.decrypt(message)    
