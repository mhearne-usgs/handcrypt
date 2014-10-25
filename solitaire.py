#!/usr/bin/env python

import string

def stringToDigits(mystr):
    digits = [string.ascii_lowercase.index(letter) for letter in re.sub('\s+','',mystr.lower())]
    return digits

def digitsToString(mydigits):
    alower = ord('a')
    mystr = [string.ascii_lowercase[digit] for digit in mydigits]
    return mystr

def getKeyStream(key):
    return stringToDigits(key)

if __name__ == '__main__':
    pass
