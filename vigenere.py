#!/usr/bin/env python

import sys
import optparse
import cryptutils 

class Vigenere(object):
    key = None
    def __init__(self,key):
        self.key = key.upper()

    def decrypt(self,ciphertext):
        key = self.key
        ciphertext = cryptutils.convertInput(ciphertext,['upper','nospaces','charonly'])
        plaintext = []
        for i in range(0,len(ciphertext)):
            ch = ciphertext[i]
            r = i % len(key)
            plaintext.append(cryptutils.rotateChar(ch,key[r],direction='backward'))
        return ''.join(plaintext)

    def encrypt(self,message):
        key = self.key
        message = cryptutils.convertInput(message,['upper','nospaces','charonly'])
        outmessage = []

        for i in range(0,len(message)):
            ch = message[i]
            r = i % len(key)
            outmessage.append(cryptutils.rotateChar(ch,key[r]))
                
        return ''.join(outmessage)

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
    v = Vigenere(options.key)
    if options.doEncrypt:
        print v.encrypt(message)
    else:
        print v.decrypt(message)

    
