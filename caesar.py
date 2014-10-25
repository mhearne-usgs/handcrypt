#!/usr/bin/env python

import utils
from string import ascii_uppercase
import sys
from optparse import OptionParser
import cryptutils

class Caesar(object):
    def __init__(self,key):
        key = key[0].lower()
        self.key = key

    def decrypt(self,ciphertext):
        key = self.key
        ciphertext = cryptutils.convertInput(ciphertext,['upper','nospaces','charonly'])
        plaintext = []
        for i in range(0,len(ciphertext)):
            ch = ciphertext[i]
            plaintext.append(cryptutils.rotateChar(ch,key,direction='backward'))
        return ''.join(plaintext)

    def encrypt(self,message):
        key = self.key
        message = cryptutils.convertInput(message,['upper','nospaces','charonly'])
        outmessage = []
        for i in range(0,len(message)):
            ch = message[i]
            outmessage.append(cryptutils.rotateChar(ch,key))

        return ''.join(outmessage)

if __name__ == '__main__':
    usage = "usage: %prog [options] cipher or plaintext"
    parser = OptionParser(usage=usage)
    parser.add_option("-e", "--encrypt", dest="doEncrypt", action="store_true",
                      help="Encrypt plaintext", default=False)
    parser.add_option("-d", "--decrypt", dest="doDecrypt", action="store_true",
                      help="Decrypt ciphertext", default=False)
    parser.add_option("-k", "--key", dest="key",
                      help="Encryption/decryption key (shortened to one character)", metavar="KEY")

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    (options, args) = parser.parse_args()
    if options.key is None:
        print 'Single character key is required!'
        sys.exit(1)
    if not options.doEncrypt and not options.doDecrypt:
        print 'Must choose encryption or decryption!'
        sys.exit(1)
    if options.doEncrypt and options.doDecrypt:
        print 'Must choose encryption OR decryption!'
        sys.exit(1)
    text = ' '.join(args)
    c = Caesar(options.key)
    if options.doEncrypt:
        print c.encrypt(text)
    if options.doDecrypt:
        print c.decrypt(text)
