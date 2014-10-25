#!/usr/bin/python

from blowfish import *

b = Blowfish('I am the king of all I survey')
input = 'Help'
ct = b.encrypt(input)
pt = b.decrypt(ct)
print input
print ct
print pt
