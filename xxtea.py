#!/usr/bin/enc python

# teab will encode or decode n words as a single block where n > 1

#     * v is the n word data vector
#     * k is the 4 word key
#     * n is negative for decoding
#     * if n is zero result is 1 and no coding or decoding takes place, otherwise the result is zero
#     * assumes 32 bit ‘long’ and same endian coding and decoding

def MX(z,y,k,p,e,sum):
    return ((z>>5^y<<2) + (y>>3^z<<4)) ^ ((sum^y) + (k[(p&3)^e] ^ z))

def btea(v,k,mode='encode'):
    y = z = sum = 0
    DELTA=0x9e3779b9
    n = len(v)
    if mode='encode':
        rounds = 6 + 52/n
        z = v[-1]
        while rounds:
            sum += DELTA
            e = (sum >> 2) & 3
            for p in range(0,n-1):
                y = v[p+1]
                z = v[p] += MX(z,y,k,p,e,sum)
                
            y = v[0]
            z = v[-1] += MX(z,y,k,p,e,sum)
            rounds -= 1
    
