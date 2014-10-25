#!/usr/bin/env python

import re
import optparse
import cryptutils

class CheckerBoard(object):
    Block = ['ET AON RIS','BCDFGHJKLM','PQ/UVWXYZ.']
    Columns = [0,1,2,3,4,5,6,7,8,9]
    Rows = ['',2,6]
    Adds = [8,18]
    key = None
    UPPERA = 65
    def getNumber(self,ch):
        return(ord(ch)-self.UPPERA)

    def __init__(self,key,):
        self.key = sum([self.getNumber(ch.upper()) for ch in key])
        #self.key = '0452'

    def addKey(self,ct):
        ctstr = ''.join(ct)
        nch = len(ctstr)
        keystr = str(self.key)
        nblocks = nch//len(keystr) + 1
        keystr = keystr * nblocks
        keystr = keystr[0:nch]
        ct2 = []
        for i in range(0,nch):
            ch = int(ctstr[i])
            key = int(keystr[i])
            ct2.append(str((ch+key)%10))

        return ct2
        
    def subtractKey(self,pt):
        ptstr = ''.join(pt)
        nch = len(ptstr)
        keystr = str(self.key)
        nblocks = nch//len(keystr) + 1
        keystr = keystr * nblocks
        keystr = keystr[0:nch]
        ct2 = []
        for i in range(0,nch):
            ch = int(ptstr[i])
            key = int(keystr[i])
            ct2.append(str((ch-key)%10))
        
        return ct2

    def charToNum(self,message):
        ct = []
        for ch in message:
            for rowidx in range(0,3):
                if ch not in self.Block[rowidx]:
                    continue
                colidx = self.Block[rowidx].find(ch)
                if rowidx == 0:
                    ct.append(str(colidx))
                else:
                    row = self.Rows[rowidx]
                    ct.append(str(row)+str(colidx))
        return ct

    def numToChar(self,clist):
        ct2 = []
        while len(clist) > 1:
            if int(clist[0]) not in self.Rows[1:]:
                colidx = int(clist.pop(0))
                ct2.append(self.Block[0][colidx])
            else:
                rowidx = int(clist.pop(0))
                colidx = int(clist.pop(0))
                rowidx = self.Rows.index(rowidx)
                ct2.append(self.Block[rowidx][colidx])

        if len(clist):
            colidx = int(clist.pop(0))
            if colidx == self.Rows[1]:
                colidx = colidx+self.Adds[0]
            elif colidx == self.Rows[2]:
                colidx = colidx+self.Adds[1]
            ct2.append(self.Block[0][colidx])
            
        return(''.join(ct2))

    def encrypt(self,message):
        message = cryptutils.convertInput(message,['upper'])
        message = message.replace(' ','/')
        ct = self.charToNum(message)
        ct = self.addKey(ct)
        ct = self.numToChar(ct)
        return(ct)

    def decrypt(self,ciphertext):
        ciphertext = cryptutils.convertInput(ciphertext,['upper','nospace'])
        pt = self.charToNum(ciphertext)
        pt = self.subtractKey(pt)
        pt = self.numToChar(pt)
        pt = pt.replace('/',' ')
        return(pt)
        

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
    c = CheckerBoard(options.key)
    if options.doEncrypt:
        print c.encrypt(message)
    else:
        print c.decrypt(message)
