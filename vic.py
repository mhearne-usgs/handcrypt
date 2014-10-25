#!/usr/bin/env python

from optparse import OptionParser
import sys
import re

# Take a ten or more letter word or phrase, strip out spaces and any non-letter characters.
# Return the order of the first ten letters alphabetically.
# Sum the numeric value of the first five letters, then return mod(sum,10) => sum1
# Sum the numeric value of the last five letters, then return mod(sum,10) => sum2

# Order the following group of characters in groups of 8, 10, and 10 using the sort order of the ten character key:
# ETAON RISHD LFCMU GYPWB VKJXQ Z./

# Use sum1 and sum2 to decide which columns in the first row should be blank.

# Create a block that looks roughly like this:
# 'ET AON RIS',
# 'BCDFGHJKLM',
# 'PQ/UVWXYZ.'

characters = ['ETAONRIS','HDLFCMUGYP','WBVKJXQZ./']
UPPERA = 65

def getNumber(ch):
    return(ord(ch)-UPPERA)

def createBlock(key):
    key = re.sub('[^a-zA-Z]','',key)
    key = key.upper()
    key = key[0:10]
    sum1 = sum([getNumber(ch) for ch in key[0:5]]) % 10
    sum2 = sum([getNumber(ch) for ch in key[5:10]]) % 10
    if sum1 == sum2:
        sum2 = sum([getNumber(ch) for ch in key[5:9]]) % 10
    #what if sum1 and sum2 are the same?
    numbers = [getNumber(ch) for ch in key]
    spairs = zip(numbers,list(key))
    spairs = sorted(spairs,key=lambda t:t[0])
    unzip = lambda l:tuple(zip(*l))
    a,skey = unzip(spairs)
    order = [] #the order in which the values from the block will be chosen
    lkey = list(key)
    for ch in skey:
        idx = lkey.index(ch)
        order.append(idx)
        lkey[idx] = '0'
    block = []
    row = ''
    for i in range(0,len(order)):
        idx = order[i]
        if idx  == sum1 or idx == sum2:
            row += ' '
        else:
            row += characters[0][idx]
    block.append(row)
    row = ''.join([characters[1][idx] for idx in order])
    block.append(row)
    row = ''.join([characters[2][idx] for idx in order])
    block.append(row)
    return block

if __name__ == '__main__':
    print createBlock("these are the times that try men's souls!0")
    
    
    
    
    
    
