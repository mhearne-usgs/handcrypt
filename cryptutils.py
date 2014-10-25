#!/usr/bin/env python

import sys
import optparse
import re
from math import sqrt

UPPERSTART = 65
UPPEREND = 90
LOWERSTART = 97
LOWEREND = 122
NMOD = 26

def getPiDigits(n):
    a = 1
    b = 1/sqrt(2)
    t = 1/4
    p = 1
    for i in range(0,n):
        a1 = (a + b)/2
        b1 = sqrt(a*b)
        t1 = t - p*((a - a1)**2)
        p1 = 2 * p
        a = a1
        b = b1
        t = t1
        p = p1
    pi = ((a + b)**2)/(4 * t)
    return pi

def list2bin(piblock):
    pibitlist = [p % 2 for p in piblock]
    pibitstr = str(pibitlist)
    pibitstr = pibitstr.replace('[','')
    pibitstr = pibitstr.replace('L','')
    pibitstr = pibitstr.replace(']','')
    pibitstr = pibitstr.replace(',','')
    pibitstr = pibitstr.replace(' ','')
    return pibitstr

def dec2bin(n,p=None):
    '''convert denary integer n to binary string bStr'''
    bstr = ''
    if n < 0: raise ValueError, "must be a positive integer"
    if n == 0: return '0'
    while n > 0:
        bstr = str(n % 2) + bstr
        n = n >> 1
    if p is not None and len(bstr) < p:
        pad = '0'*(p-len(bstr))
        bstr = pad + bstr
    return bstr

def bin2dec(bitstr):
    return int(bitstr,2)

def convertInput(text,options):
    if 'upper' in options:
        text = text.upper()
    if 'nospaces' in options:
        text = text.replace(' ','')
    if 'charonly' in options:
        text = re.sub('[^a-zA-Z]','',text)
    return text

def unique(seq, keepstr=True):
    t = type(seq)
    if t in (str, unicode):
        t = (list, ''.join)[bool(keepstr)]
    seen = []
    return t(c for c in seq if not (c in seen or seen.append(c)))


def rotateChar(x,y,direction='forward'):
    isXUpper = False
    x = ord(x)
    y = ord(y)
    if x >= UPPERSTART and x <= UPPEREND:
        x = x - UPPERSTART
        isXUpper = True
    elif x >= LOWERSTART and x <= LOWEREND:
        x = x - LOWERSTART
    else:
        return chr(x)
    if y >= UPPERSTART and y <= UPPEREND:
        y = y - UPPERSTART
    elif y >= LOWERSTART and y <= LOWEREND:
        y = y - LOWERSTART
    if direction == 'forward':
        z = rotateNumForward(x,y) #number between 1-26
    else:
        z = rotateNumBackward(x,y)
    if isXUpper:
        return chr(z+UPPERSTART)
    else:
        return chr(z+LOWERSTART)
    
def rotateNumForward(x,y):
    return (x+y) % NMOD

def rotateNumBackward(x,y):
    return ((NMOD-y)+x) % NMOD

if __name__ == '__main__':
    for i in range(1,10):
        p = getPiDigits(1)
        print p

    
    
    
