#!/usr/bin/env python
import optparse
import sys
import cryptutils

class RailFence(object):
    key = None
    def __init__(self,key):
        self.key = len(key)

    def getRows(self,nrails,nchars):
        lc = (nrails-1)*2
        nc = nchars//lc
        nrem = nchars % lc
        c1 = range(0,nrails)
        c2 = range(nrails-2,0,-1)
        rows = ((c1+c2)*nc)+c1[0:nrem]
        return(rows)

    def encrypt(self,message):
        message = cryptutils.convertInput(message,['upper','nospace','charonly'])
        nrails = self.key
        nposts = len(message)
        block = []
        for i in range(0,nrails):
            rail = list(' '*nposts)
            block.append(rail)
        
        rows = self.getRows(nrails,len(message))
       
        for i in range(0,len(message)):
            block[rows[i]][i] = message[i]
        
        ciphertext = ''
        for b in block:
            ciphertext = ciphertext + ''.join(b).replace(' ','')

        return ciphertext

    def decrypt(self,ciphertext):
        ciphertext = cryptutils.convertInput(ciphertext,['upper','nospace','charonly'])
        R = self.key
        N = len(ciphertext)
        d = (R-1)*2
        row = range(0,N,d)
        plaintext = list('0'*N)
        cidx = 0
        for idx in row:
            plaintext[idx] = ciphertext[cidx]
            cidx += 1

        for i in range(1,R-1):
            e = ((R-1)-i)*2
            p1 = range(i,N,d)
            p2 = range(i+e,N,d)
            dmax = max(len(p1),len(p2))
            for j in range(0,dmax):
                if j <= len(p1)-1:
                    idx = p1[j]
                    plaintext[idx] = ciphertext[cidx]
                    cidx += 1
                if j <= len(p2)-1:
                    idx = p2[j]
                    plaintext[idx] = ciphertext[cidx]
                    cidx += 1
        row = range(R-1,N,d)
        for idx in row:
            plaintext[idx] = ciphertext[cidx]
            cidx += 1

        return ''.join(plaintext)
                
            
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
    r = RailFence(options.key)
    if options.doEncrypt:
        print r.encrypt(message)
    else:
        print r.decrypt(message)    
