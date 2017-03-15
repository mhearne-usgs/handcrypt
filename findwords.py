#!/usr/bin/env python

import sys
import os.path

WORDFILE = 'englishwords.txt' #need a bigger file

if __name__ == '__main__':
    homedir = os.path.dirname(os.path.abspath(__file__)) #where is this script?
    wordfile = os.path.join(homedir,WORDFILE)
    inputword = sys.argv[1].lower()
    inputset = set(inputword)
    for line in open(wordfile,'rt').readlines():
        word = line.strip().lower()
        if len(word) < 4:
            continue
        wordset = set(word)
        intersection = inputset.intersection(wordset)
        if len(intersection) == len(word):
            print word
    
            
        
        
