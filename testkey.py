#!/usr/bin/env python

from keyorder import *
from crackutils import *
import sys
import numpy

k = KeyOrder('iwalkthewildwildwood')
# scrambled = numpy.random.randint(0,9,40)
# newscramble = k.shuffle(scrambled)
# print scrambled[0:10],scrambled[10:20],scrambled[20:30],scrambled[30:40]
# print newscramble[0:10],newscramble[10:20],newscramble[20:30],newscramble[30:40]
# sys.exit(0)
pt = 'my sister is the queen of all she surveys.  Her kids are geniuses, and good swimmers to boot.  Her brother is the emperor of the realms east of the kingdom known as California, and the prince of Whales.'
#pt = 'my sister is the que'
#pt = 'mole'
ct,bitstring = k.encrypt(pt)
pt2,bs = k.decrypt(ct)
s = k.scrambleKey(pt)

# scramblestr = ''
# for n in s:
#     scramblestr = scramblestr + str(n)

# f1 = freqCount(scramblestr)
# printFreq(f1,reverse=True)
print "'%s'" % pt
print "'%s'" % ct
print "'%s'" % pt2
#print "'%s'" % bitstring

f1 = freqCount(ct)
f2 = freqCount(bitstring)
# print 'Ciphertext frequency count in ascending order:'
# printFreq(f1)
# print 'Ciphertext frequency count in descending order:'
# printFreq(f1,reverse=True)
# print 'Ciphertext frequency count in alphabetical order:'
# printFreq(f1,alphabetical=True)

print
print 'Bitstring frequency count in ascending order:'
printFreq(f2)
print 'Bitstring frequency count in descending order:'
printFreq(f2,reverse=True)
# print 'Bitstring frequency count in alphabetical order:'
# printFreq(f2,alphabetical=True)


