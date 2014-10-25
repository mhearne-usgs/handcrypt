#!/usr/bin/env python
KEYLENGTH = 16
class BitSpreader(object):
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

    def encrypt(self,message):
        ciphertext = ''
        for m in message:
            
