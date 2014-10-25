#!/usr/bin/env python

import string
import sys

def stack(ciphertext,maxkey=10):
    #ciphertext is assumed to be a lowercase string with no spaces in it
    ic = {}
    for keylen in range(1,maxkey+1):
        ics = []
        for i in range(0,keylen):
            column = ciphertext[i:-1:keylen]
            ics.append(getIC(column))
        ic[keylen] = sum(ics)/len(ics)
    return ic


def getIC(column):
    N = len(column)
    nc = len(string.lowercase)
    freqs = dict(zip(string.lowercase,[0 for i in range(0,26)]))
    numer = 0
    for c in string.lowercase:
        freqs[c] = column.count(c)
        numer = column.count(c) * (column.count(c)-1)
        
    ic = float(numer)/(N*(N-1)/nc)
    return ic
        
def crack(ciphertext):
    ciphertext = ciphertext.lower()

    mic = getIC(ciphertext)
    n = len(ciphertext)

    mguess = (0.027*n)/((n-1)*mic-0.038*n+0.065)

    print 'Guessed key length is %.1f' % mguess
    
#     ic_exp = 1.73
#     N = len(ciphertext)
#     nc = len*string.lowercase

#     #count frequencies of each letter
#     freqs = dict(zip(string.lowercase,[0 for i in range(0,26)]))
#     numer = 0
#     for c in string.lowercase:
#         freqs[c] = ciphertext.count(c)
#         numer = ciphertext.count(c) * (ciphertext.count(c)-1)
        
#     ic = float(numer)/(N*(N-1)/nc)

#     keylen = (kp-kr)/(ko-kr)

    
        

     


if __name__ == '__main__':
    ciphertext = 'QPWKALVRXCQZIKGRBPFAEOMFLJMSDZVDHXCXJYEBIMTRQWNMEAIZRVKCVKVLXNEICFZPZCZZHKMLVZVZIZRRQWDKECHOSNYXXLSPMYKVQXJTDCIOMEEXDQVSRXLRLKZHOV'
    ciphertext = ciphertext.lower()
    icdict = stack(ciphertext)
    print icdict
    sys.exit(0)
    
    #ciphertext = 'HLKOSNTVPDJMWPUYPAGI'.lower()
    crack(ciphertext)
    
