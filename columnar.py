#!/usr/bin/env python
import optparse
import cryptutils
import sys

class Columnar(object):
    key = None

    #define an alphabetical key
    def __init__(self,key):
        key = cryptutils.convertInput(key,['upper','nospace','charonly'])
        #first, make sure that the key has no repeated letters
        if len(cryptutils.unique(key)) != len(key):
            raise ValueError,'Key must not have any repeated characters.'
        #next, figure out the sort order of the letters in the key
        keylist = list(key)
        keylist.sort()
        keyorder = []
        for ch in key:
            keyorder.append(keylist.index(ch))
        
        #make that list of key orders the key
        self.key = keyorder

    def decrypt(self,ciphertext):
        ciphertext = cryptutils.convertInput(ciphertext,['upper','nospace','charonly'])
        nrows = len(ciphertext)//len(self.key)
        rem = len(ciphertext) % len(self.key)
        block = []
        for row in range(0,nrows):
            rowlist = list('X'*len(self.key))
            block.append(rowlist)
        if rem:
            rowlist = list('X'*rem)
            block.append(rowlist)
        idx = 0
        for i in range(0,len(self.key)):
            col = self.key.index(i)
            for row in range(0,nrows):
                block[row][col] = ciphertext[idx]
                idx += 1
            if col <= rem-1:
                block[row+1][col] = ciphertext[idx]
                idx += 1
        plaintext = ''
        for chunk in block:
            plaintext = plaintext + ''.join(chunk)
        return plaintext

    def encrypt(self,message):
        message = cryptutils.convertInput(message,['upper','nospace','charonly'])
        if len(message) < len(self.key):
            raise ValueError,'Message must be longer than key'
        ncols = len(self.key)
        nrows = len(message)//ncols
        block = []
        nrem = len(message) % ncols
        for i in range(0,nrows):
            istart = i*ncols
            iend = istart+ncols
            block.append(message[istart:iend])
        
        block.append(message[iend:])
        #now read from the columns in the order specified by the key
        ciphertext = []
        for i in range(0,len(self.key)):
            col = self.key.index(i)
            for j in range(0,nrows):
                ciphertext.append(block[j][col])
            if col < nrem:
                ciphertext.append(block[j+1][col])

        return ''.join(ciphertext)
            
    
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
    c = Columnar(options.key)
    if options.doEncrypt:
        print c.encrypt(message)
    else:
        print c.decrypt(message)
