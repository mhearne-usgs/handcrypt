#!/usr/bin/env python
import bfconstants

def u64(x):
    return x & 0xffffffffffffffff

class Blowfish(object):
    P = []
    S = []
    Key = []
    def __init__(self,key):
        self.Key = self.make64(key)
        self.initializeArrays()

    def make64(self,plaintext):
        rem = len(plaintext) % 4
        if rem:
            plaintext = plaintext + ''.join([chr(0) for x in range(0,4-rem)])
        ptlist = []
        for i in range(0,len(plaintext),4):
            p1 = ord(plaintext[i])
            p2 = ord(plaintext[i+1])
            p3 = ord(plaintext[i+2])
            p4 = ord(plaintext[i+3])
            output = 0L
            output = u64(output | p1)
            output = u64(output | p2 << 8)
            output = u64(output | p3 << 16)
            output = u64(output | p4 << 24)
            ptlist.append(output)
        return ptlist

    def initializeArrays(self):
        key32 = self.splitKey(self.Key)
        if len(key32) < 18:
            rem = 18 - len(key32)
            for i in range(0,rem):
                key32.append(key32[i])
        
        self.P = bfconstants.parray[0:]
        for i in range(0,len(self.P)):
            self.P[i] = self.P[i] ^ key32[i]
    
        allzerostr = ''.join([chr(0) for x in range(0,4)])
        allzero = self.make64(allzerostr)
        self.S = [bfconstants.sbox0[0:],bfconstants.sbox0[0:],bfconstants.sbox0[0:],bfconstants.sbox0[0:]]
        output = (self.blowfish(allzero,mode='encrypt'))[0]
        xL,xR = self.splitX(output)
        for i in range(0,len(self.P),2):
            self.P[i] = xL
            self.P[i+1] = xR
            output = self.blowfish(output,mode='encrypt')
            xL,xR = self.splitX(output)
    
        for i in range(0,len(self.S)):
            for j in range(0,len(self.S[i]),2):
                self.S[i][j] = xL
                self.S[i][j+1] = xR
                output = self.blowfish(output,mode='encrypt')
                xL,xR = self.splitX(output)
                    
    def blowfish(self,xlist,mode='encrypt'):
        if mode == 'encrypt':
            if isinstance(xlist,list):
                outlist = []
                for x in xlist:
                    newx = self.__blowfishforward(x)
                    outlist.append(newx)
                return outlist
            else:
                newx = self.__blowfishforward(xlist)
                return newx
        else:
            if isinstance(xlist,list):
                outlist = []
                for x in xlist:
                    newx = self.__blowfishbackward(x)
                    outlist.append(newx)
                return outlist
            else:
                newx = self.__blowfishbackward(xlist)
                return newx

    def __blowfishbackward(self,x):
        xL,xR = self.splitX(x)
        for i in range(17,1,-1):
            xL = xL ^ self.P[i]
            xR = self.F(xL) ^ xR
            tmp = xL
            xL = xR
            xR = tmp
        tmp = xL
        xL = xR
        xR = tmp
        xR = xR ^ self.P[1]
        xL = xL ^ self.P[0]
        newx = self.joinX(xL,xR)
        return newx

    def __blowfishforward(self,x):
        xL,xR = self.splitX(x)
        for i in range(0,16):
            xL = xL ^ self.P[i]
            xR = self.F(xL) ^ xR
            tmp = xL
            xL = xR
            xR = tmp
        tmp = xL
        xL = xR
        xR = tmp
        xR = xR ^ self.P[16]
        xL = xL ^ self.P[17]
        newx = self.joinX(xL,xR)
        return newx

    def F(self,x):
        d = x & 0x00FF
        x >>= 8
        c = x & 0x00FF
        x >>= 8
        b = x & 0x00FF
        x >>= 8
        a = x & 0x00FF
        y = self.S[0][a] + self.S[1][b]
        y = y ^ self.S[2][c]
        y = y + self.S[3][d]
        return y

    def encrypt(self,plaintext):
        plainlist = self.make64(plaintext)
        cipherlist = self.blowfish(plainlist,mode='encrypt')
        ciphertext = self.makeText(cipherlist)
        return ciphertext

    def decrypt(self,ciphertext):
        cipherlist = self.make64(ciphertext)
        plainlist = self.blowfish(cipherlist,mode='decrypt')
        plaintext = self.makeText(plainlist)
        return plaintext

    def makeText(self,list64):
        tout = ''
        for p in list64:
            d = p & 0x00FF
            p >>= 8
            c = p & 0x00FF
            p >>= 8
            b = p & 0x00FF
            p >>= 8
            a = p & 0x00FF
            tout = tout + chr(a) + chr(b) + chr(c) + chr(d)
        return tout
            
        
    def splitKey(self,key64):
        key32 = []
        for k in key64:
            xL,xR = self.splitX(k)
            key32.append(xL)
            key32.append(xR)
        return key32

    def splitX(self,x):
        xL = (x >> 32) << 32
        xR = x - xL
        return (xL,xR)

    def joinX(self,xL,xR):
        output = u64(0L)
        output = u64(output | xR)
        output = u64(output | xL << 8)
        return output


        
        
    
    
        
        
