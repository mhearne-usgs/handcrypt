#!/usr/bin/env python
from string import ascii_uppercase

import caesar

LETTERS = ['etaoinshrdlcumwfgypbvkjxqz']
LETTERS = ['etaoinsh']
DIGRAPHS = ['ST','NG','TH','QU']


ciphertext = """LIVITCSWPIYVEWHEVSRIQMXLEYVEOIEWHRXEXIPFEMVEWHKVSTYLXZIXLIKIIXPIJVSZEYPERRGERIM
WQLMGLMXQERIWGPSRIHMXQEREKIETXMJTPRGEVEKEITREWHEXXLEXXMZITWAWSQWXSWEXTVEPMRXRSJ
GSTVRIEYVIEXCVMUIMWERGMIWXMJMGCSMWXSJOMIQXLIVIQIVIXQSVSTWHKPEGARCSXRWIEVSWIIBXV
IZMXFSJXLIKEGAEWHEPSWYSWIWIEVXLISXLIVXLIRGEPIRQIVIIBGIIHMWYPFLEVHEWHYPSRRFQMXLE
PPXLIECCIEVEWGISJKTVWMRLIHYSPHXLIQIMYLXSJXLIMWRIGXQEROIVFVIZEVAEKPIEWHXEAMWYEPP
XLMWYRMWXSGSWRMHIVEXMSWMGSTPHLEVHPFKPEZINTCMXIVJSVLMRSCMWMSWVIRCIGXMWYMX"""

keys = {}
for ch in ascii_uppercase:
    plaintext = caesar.decrypt(ciphertext,ch).upper()
    print
    print ch,plaintext
    print
    tscore = 0
    score = 4
    for dg in DIGRAPHS:
        tscore = plaintext.count(dg)*score
        score -= 1
    keys[ch] = tscore

# print keys
# smax = max(keys.values())
# for ch,tscore in keys.iteritems():
#     if tscore == smax:
#         print caesar.decrypt(ciphertext,ch)
#         break

    
